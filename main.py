from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np
import os
import requests
import uuid
from datetime import datetime
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Firebase Admin SDK initialization
FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH")
if not FIREBASE_CREDENTIALS_PATH or not os.path.exists(FIREBASE_CREDENTIALS_PATH):
    raise FileNotFoundError("Firebase credentials file not found.")

# Initialize Firebase Admin SDK with service account
cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred)

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

@app.route('/')
def home():
    return "Welcome to the oral disease detection app!"

@app.route("/predict", methods=["POST"])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    img = tf.io.decode_image(file.read(), channels=3)
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
            "message": "Confidence is too low for reliable prediction."
        })

    # Ambil data dari Firestore
    disease_data = get_disease_info(predicted_class)

    
     # Simpan data prediksi ke Firestore
    prediction_id = str(uuid.uuid4())  # Generate a unique ID
    created_at = datetime.utcnow().isoformat()
    prediction_data = {
        "id": prediction_id,
        "result": predicted_class,
        "description": disease_data.get("description", "No description available"),
        "treatment": disease_data.get("treatment", "No treatment available"),
        "createdAt": created_at
    }
    
    # Simpan data prediksi di koleksi 'predictions'
    db.collection("predictions").document(prediction_id).set(prediction_data)
    
    
    return jsonify({
        "class": predicted_class,
        "confidence": float(confidence),
        "description": disease_data.get("description", "No description available"),
        "treatment": disease_data.get("treatment", "No treatment available"),
        "createdAt": created_at
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
                "result": prediction_data.get("result"),
                "description": prediction_data.get("description"),
                "treatment": prediction_data.get("treatment"),
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
