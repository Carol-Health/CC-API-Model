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

---

## Tools
- TensorFlow
- Flask
- Python
- VS Code
- Google Cloud SDK
- Firebase Admin SDK
- Google Cloud Console
- Postman

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
    "file": "ulcer.jpg"
  }
- **Response Body**:
  ```json
  {
    "confidence": 0.9998513460159302,
    "createdAt": "2024-12-13 11:50:53",
    "description": "Mouth ulcer atau disebut juga dengan istilah aphthous stomatitis atau sariawan adalah kondisi hilangnya atau terkikisnya bagian jaringan halus yang melapisi bagian dalam mulut (mucous membrane).",
    "image_url": "https://storage.googleapis.com/carol-image-predict/images/carol-image-predict/images/12f7c6e5-dafc-4a52-985d-1648584e007a.jpg",
    "name": "Sariawan (Mouth ulcer)",
    "treatment": "Obat kumur atau salep topikal untuk mengurangi rasa sakit, serta menjaga kebersihan mulut dengan hati-hati."
  }

### 1. **/history<uid>**
- **URL**: `/history<uid>`
- **Method**: `GET`
- **Deskripsi**: Endpoint ini digunakan untuk mendapatkan riwayat prediksi penyakit berdasarkan ID pengguna.
- **Response Body**:
  ```json
  {
            "createdAt": "2024-12-12 15:33:25",
            "description": "Mouth ulcer atau disebut juga dengan istilah aphthous stomatitis atau sariawan adalah kondisi hilangnya atau terkikisnya bagian jaringan halus yang melapisi bagian dalam mulut (mucous membrane).",
            "id": "08df5edc-8068-44dd-aa83-7867c17da6a6",
            "image_url": "https://storage.googleapis.com/carol-image-predict/images/carol-image-predict/images/619f84f8-c3ef-47ea-be43-0e6bd193fa7b.jpg",
            "name": "Sariawan (Mouth ulcer)",
            "treatment": "Obat kumur atau salep topikal untuk mengurangi rasa sakit, serta menjaga kebersihan mulut dengan hati-hati."
        },
        {
            "createdAt": "2024-12-12 20:04:57",
            "description": "Hypodontia adalah kelainan genetik pada gigi ketika terdapat satu atau lebih gigi yang tidak tumbuh sama sekali. Tingkat keparahan hypodontia berbeda pada tiap orang dan ditentukan berdasarkan jumlah gigi yang hilang. Tanpa penanganan, kondisi ini dapat memengaruhi kemampuan makan, mengunyah, hingga berbicara.",
            "id": "187b32a3-5f4d-4c97-b47b-c22546eacc4d",
            "image_url": "https://storage.googleapis.com/carol-image-predict/images/carol-image-predict/images/bd0110fa-cd5d-41c7-bdc4-2477bd35867c.jpg",
            "name": "Hypodontia (Missing teeth)",
            "treatment": "Penanaman gigi atau penggunaan prostetik gigi untuk menggantikan gigi yang hilang."
        },
        {
            "createdAt": "2024-12-12 18:25:37",
            "description": "Mouth ulcer atau disebut juga dengan istilah aphthous stomatitis atau sariawan adalah kondisi hilangnya atau terkikisnya bagian jaringan halus yang melapisi bagian dalam mulut (mucous membrane).",
            "id": "190e1e41-ae48-43de-93e7-853f1316feb3",
            "image_url": "https://storage.googleapis.com/carol-image-predict/images/carol-image-predict/images/21cfef9b-a2db-4261-a728-559195b5a2c1.jpg",
            "name": "Sariawan (Mouth ulcer)",
            "treatment": "Obat kumur atau salep topikal untuk mengurangi rasa sakit, serta menjaga kebersihan mulut dengan hati-hati."
        }
