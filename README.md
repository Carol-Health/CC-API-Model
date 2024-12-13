# Carol Health API

API ini dirancang untuk mendukung aplikasi **Carol Health**. Aplikasi ini membantu pengguna mendeteksi penyakit mulut melalui foto dan memberikan riwayat hasil prediksi secara otomatis.

## Requirements

- Python 3.8+
- Firebase Admin SDK
- Google Cloud Storage
- TensorFlow
- Flask
- flask==3.1.0
- tensorflow==2.17.1
- gunicorn==21.2.0
- python-dotenv==1.0.1
- firebase-admin
- google-cloud-storage
- pytz
  
**Versi**: 1.0.0

---

## Daftar Endpoint API

| Endpoint           | HTTP Method | Deskripsi                                                              |
|--------------------|-------------|------------------------------------------------------------------------|
| **/predict**       | POST        | Mengirimkan foto mulut untuk prediksi penyakit.                        |
| **/history/<uid>** | GET         | Mengambil riwayat prediksi berdasarkan ID pengguna (user ID).          |

---

## Contoh Penggunaan API

### 1. **/predict**
- **URL**: `/predict`
- **Method**: `POST`
- **Deskripsi**: Endpoint ini digunakan untuk mengirimkan foto mulut, dan API akan memberikan hasil prediksi penyakit berdasarkan model Machine Learning.
- **Request Body**:
  ```json
  {
    "image": "base64_encoded_image_string"
  }
