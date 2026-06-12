# SkinGuard AI

SkinGuard AI adalah prototype aplikasi web berbasis AI untuk skrining awal lesi kulit dari citra dermatoskopi. Sistem ini menampilkan hasil prediksi 7 kelas lesi kulit, confidence score, risk level, distribusi probabilitas, GradCAM, AI Chat Assistant, dan rekomendasi rumah sakit.

> SkinGuard AI bukan alat diagnosis final. Hasil prediksi hanya digunakan sebagai skrining awal dan edukasi. Keputusan medis tetap harus melalui pemeriksaan dokter.

---

## Identitas Project

Project ini dibuat untuk memenuhi tugas mata kuliah Pengantar Proyek Sains Data.

- Nama Project: SkinGuard AI
- Kelompok: 06
- Anggota:
  - Kasih Kristanti N. - 5052231033
  - Putri Amalia F. - 5052231037
  - Zanna Quinsa H.D - 5052231039

---

## Model

Model final menggunakan:

```text
EfficientNetB0 + Balanced Training Set + Test-Time Augmentation (TTA)
```

Hasil evaluasi model:

| Metrik | Nilai |
|---|---:|
| Test Accuracy | 80,72% |
| Weighted F1-score | 80,78% |
| Macro F1-score | 66,77% |

Model mengklasifikasikan gambar ke dalam 7 kelas:

| Kode | Kelas |
|---|---|
| AKIEC | Actinic Keratoses / Intraepithelial Carcinoma |
| BCC | Basal Cell Carcinoma |
| BKL | Benign Keratosis-like Lesions |
| DF | Dermatofibroma |
| MEL | Melanoma |
| NV | Melanocytic Nevi |
| VASC | Vascular Lesions |

Catatan: model belum memiliki kelas khusus untuk kulit normal. Jika gambar kulit normal diunggah, sistem tetap akan memilih kelas yang paling mirip dari 7 kelas yang tersedia.

---

## Struktur Project

```bash
skinguard-reproducible/
├── Dockerfile
├── README.md
├── .gitignore
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── model_loader.py
│   ├── image_processing.py
│   ├── gemini_service.py
│   ├── hospital_data.py
│   ├── gradcam.py
│   ├── requirements.txt
│   ├── env.example
│   └── models/
│       └── skinguard_model.keras
└── frontend/
    ├── index.html
    ├── script.js
    └── style.css
```

File `backend/.env`, dataset, hasil eksperimen, virtual environment, dan cache tidak disertakan agar project lebih ringan dan aman untuk dijalankan ulang.

---

## Cara Menjalankan Project

### 1. Buat file environment

```bash
cp backend/env.example backend/.env
```

Isi file `backend/.env`:

```env
MODEL_PATH=models/skinguard_model.keras
GEMINI_API_KEY=isi_api_key_google_ai_studio
GEMINI_MODEL=gemini-2.0-flash
```

Jika `GEMINI_API_KEY` kosong, aplikasi tetap dapat berjalan, tetapi AI Chat akan menggunakan fallback response.

### 2. Jalankan backend

Pastikan Docker Desktop sudah aktif.

```bash
docker build -t skinguard-backend .
```

```bash
docker run --rm -p 8000:8000 \
  --env-file backend/.env \
  -v "$(pwd)/backend:/app" \
  skinguard-backend
```

Cek backend:

```text
http://localhost:8000/health
```

Output yang diharapkan:

```json
{
  "status": "healthy",
  "model_loaded": true,
  "gemini_available": true,
  "version": "1.0.0"
}
```

### 3. Jalankan frontend

Buka terminal baru:

```bash
cd frontend
npx vite --host 0.0.0.0 --port 5173
```

Buka aplikasi di browser:

```text
http://localhost:5173
```

---

## Endpoint Backend

| Endpoint | Method | Fungsi |
|---|---|---|
| `/health` | GET | Cek status backend, model, dan Gemini |
| `/predict` | POST | Prediksi lesi kulit dari gambar |
| `/gradcam` | POST | Visualisasi GradCAM |
| `/chat` | POST | AI Chat Assistant |
| `/hospitals` | GET | Daftar rumah sakit |
| `/hospitals/cities` | GET | Daftar kota rumah sakit |

---

## Reproducibility Checklist

File yang disertakan:

- source code backend
- source code frontend
- model final `skinguard_model.keras`
- Dockerfile
- `requirements.txt`
- `env.example`
- README

File yang tidak disertakan:

- `.env`
- `backend/.env`
- dataset mentah
- hasil eksperimen training
- virtual environment
- cache Python/Vite
- `.DS_Store`

---

## Troubleshooting

### Port 8000 sudah dipakai

```bash
docker ps
docker stop nama_container
```

Atau stop semua container aktif:

```bash
docker stop $(docker ps -q)
```

### File `.env` belum ada

```bash
cp backend/env.example backend/.env
```

### Model tidak terbaca

Pastikan file ini ada:

```text
backend/models/skinguard_model.keras
```

### Frontend gagal karena tidak ada package.json

Gunakan:

```bash
npx vite --host 0.0.0.0 --port 5173
```

Bukan `npm install`.

---

## Teknologi

- Python
- TensorFlow / Keras
- EfficientNetB0
- FastAPI
- Docker
- Gemini AI
- Vite
- HTML, CSS, JavaScript

---

## Disclaimer

SkinGuard AI hanya digunakan untuk skrining awal dan edukasi. Hasil prediksi tidak menggantikan diagnosis dokter. Untuk kondisi kulit yang mencurigakan, berubah cepat, berdarah, nyeri, atau berisiko tinggi, pengguna disarankan berkonsultasi dengan dokter spesialis kulit.
