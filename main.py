from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np
import os
import requests
import uuid
import pytz
from datetime import datetime
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import firestore
from google.cloud import storage

app = Flask(__name__)

# Load environment variables
load_dotenv()

firebase_admin.initialize_app()

# Initialize Firestore client
db = firestore.client()

# Load model
LATEST_MODEL_URL = os.getenv("LATEST_MODEL_URL")
DESTINATION_MODEL_PATH = os.getenv("DESTINATION_MODEL_PATH")

# Download the model from the specified URL
response = requests.get(LATEST_MODEL_URL)
with open(DESTINATION_MODEL_PATH, 'wb') as f:
    f.write(response.content)

# Load the model
model = load_model(DESTINATION_MODEL_PATH)

class_names = ['calculus', 'caries', 'gingivitis', 'hypodontia', 'tooth_discoloration', 'ulcer']

# Fungsi upload foto mulut dari user ke Storage
def upload_to_storage(source_file, destination_name) :
    try:
        bucket_name = os.getenv("CLOUD_STORAGE_BUCKET")
        base_url = os.getenv("CLOUD_STORAGE_URL")

        # Menghubungkan ke Cloud Storage
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_name)

        # Upload file ke Cloud Storage
        blob.upload_from_string(source_file, content_type="image/jpeg")

        # Bangun URL publik
        public_url = f"{base_url}{bucket_name}/{destination_name}"

        return public_url
    except Exception as e:
        raise RuntimeError(f"Gagal upload ke bucket: {str(e)}")


@app.route('/')
def home():
    return "Welcome to the oral disease detection app!"

@app.route("/predict", methods=["POST"])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    file_data = file.read()
    
    try:
        unique_filename = f"images/{uuid.uuid4()}.jpg"  
        public_url = upload_to_storage(file_data, unique_filename)
    except Exception as e:
        return jsonify({"error": f"Failed to upload image: {str(e)}"}), 500
    
    img = tf.io.decode_image(file_data, channels=3)
    img = tf.image.resize(img, (224, 224))  # Resize sesuai model input
    img = img / 255.0  # Normalisasi
    img = np.expand_dims(img, axis=0)

    # Predict
    predictions = model.predict(img)
    predicted_class = class_names[np.argmax(predictions)]
    confidence = np.max(predictions)

    # Jika confidence rendah
    if confidence < 0.9:
        return jsonify({
            "class": "Not detected",
            "confidence": float(confidence),
            "message": "Confidence is too low for reliable prediction.",
            "image_url": public_url
        })

    # Ambil data dari Firestore
    disease_data = get_disease_info(predicted_class)
    
    # Simpan data prediksi ke Firestore
    prediction_id = str(uuid.uuid4())  # Generate a unique ID
    # Dapatkan waktu UTC saat ini
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)

    # Tentukan zona waktu WIB (UTC+7)
    wib = pytz.timezone('Asia/Jakarta')

    # Konversi waktu UTC ke WIB
    wib_now = utc_now.astimezone(wib)

    # Format waktu sesuai kebutuhan
    formatted_time = wib_now.strftime('%Y-%m-%d %H:%M:%S')
    
    
    prediction_data = {
        "id": prediction_id,
        "name": disease_data.get("name", "No name available"),
        "description": disease_data.get("description", "No description available"),
        "treatment": disease_data.get("treatment", "No treatment available"),
        "image_url": public_url,
        "createdAt": formatted_time
    }
    
    # Simpan data prediksi di koleksi 'predictions'
    db.collection("predictions").document(prediction_id).set(prediction_data)
    
    
    return jsonify({
        "name": disease_data.get("name", "No name available"),
        "confidence": float(confidence),
        "description": disease_data.get("description", "No description available"),
        "treatment": disease_data.get("treatment", "No treatment available"),
        "image_url": public_url,
        "createdAt": formatted_time
    })

@app.route("/history", methods=["GET"])
def get_history():
    try:
        predictions_ref = db.collection("predictions")
        predictions = predictions_ref.stream()

        history = []
        for prediction in predictions:
            prediction_data = prediction.to_dict()
            history.append({
                "id": prediction.id,
                "name": prediction_data.get("name"),
                "description": prediction_data.get("description"),
                "treatment": prediction_data.get("treatment"),
                "image_url": prediction_data.get("image_url"),
                "createdAt": prediction_data.get("createdAt")
            })

        return jsonify({"status": "success", "data": history})

    except Exception as e:
        return jsonify({"error": f"Error retrieving history: {str(e)}"}), 500


def get_disease_info(diseases_class):
    """
    Mengambil deskripsi dan treatment dari Firestore berdasarkan kelas penyakit.
    """
    try:
        doc_ref = db.collection("diseases").document(diseases_class)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return {"description": "No description found", "treatment": "No treatment found"}
    except Exception as e:
        return {"description": f"Error retrieving data: {str(e)}", "treatment": ""}

# Run server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))