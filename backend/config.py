import os
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "SkinGuard AI"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Intelligent Skin Disease Detection & Clinical Decision Support System"
    DEBUG: bool = Field(default=False, env="DEBUG")

    # Server
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")

    # Model
    MODEL_PATH: str = Field(default="models/skinguard_model.keras", env="MODEL_PATH")
    IMAGE_SIZE: int = 224
    IMAGE_CHANNELS: int = 3

    # Gemini AI
    GEMINI_API_KEY: str = Field(default="", env="GEMINI_API_KEY")
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # CORS
    ALLOWED_ORIGINS: list[str] = ["*"]

    # Upload
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_IMAGE_TYPES: list[str] = ["image/jpeg", "image/png", "image/webp"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Class labels HAM10000
CLASS_LABELS = {
    0: "Actinic Keratosis",
    1: "Basal Cell Carcinoma",
    2: "Benign Keratosis",
    3: "Dermatofibroma",
    4: "Melanoma",
    5: "Melanocytic Nevi",
    6: "Vascular Lesion",
}

# Risk level mapping per class
CLASS_RISK_LEVEL = {
    "Actinic Keratosis": "medium",
    "Basal Cell Carcinoma": "high",
    "Benign Keratosis": "low",
    "Dermatofibroma": "low",
    "Melanocytic Nevi": "low",
    "Melanoma": "critical",
    "Vascular Lesion": "medium",
}

# Risk level display labels
RISK_DISPLAY = {
    "low": "Risiko Rendah",
    "medium": "Risiko Sedang",
    "high": "Risiko Tinggi",
    "critical": "Risiko Kritis",
}

# Short medical description per class
CLASS_DESCRIPTIONS = {
    "Actinic Keratosis": (
        "Actinic Keratosis adalah kondisi prakanker yang disebabkan oleh paparan sinar matahari "
        "berlebih. Ditandai dengan bercak kulit kasar, bersisik, dan kering. Perlu pengawasan medis "
        "karena berpotensi berkembang menjadi karsinoma sel skuamosa."
    ),
    "Basal Cell Carcinoma": (
        "Basal Cell Carcinoma adalah jenis kanker kulit yang paling umum. Muncul sebagai benjolan "
        "kecil berwarna merah muda atau transparan. Jarang menyebar ke organ lain namun memerlukan "
        "penanganan medis segera."
    ),
    "Benign Keratosis": (
        "Benign Keratosis merupakan pertumbuhan kulit non-kanker yang umum terjadi seiring usia. "
        "Biasanya berwarna coklat hingga hitam, bertekstur kasar. Kondisi ini bersifat jinak "
        "dan tidak memerlukan pengobatan khusus kecuali mengganggu."
    ),
    "Dermatofibroma": (
        "Dermatofibroma adalah tumor kulit jinak yang umum, biasanya muncul di tungkai bawah. "
        "Berwarna coklat kemerahan, keras saat diraba, dan biasanya tidak menimbulkan keluhan. "
        "Tidak berbahaya dan tidak memerlukan pengobatan rutin."
    ),
    "Melanocytic Nevi": (
        "Melanocytic Nevi atau tahi lalat adalah pertumbuhan kulit jinak yang terdiri dari sel melanosit. "
        "Umumnya berwarna coklat atau hitam dengan ukuran kecil. Perlu dipantau jika terjadi perubahan "
        "ukuran, warna, atau bentuk."
    ),
    "Melanoma": (
        "Melanoma adalah jenis kanker kulit yang paling berbahaya dan berasal dari sel melanosit. "
        "Dapat menyebar ke organ vital jika tidak segera ditangani. Deteksi dan penanganan dini "
        "sangat penting untuk prognosis yang baik."
    ),
    "Vascular Lesion": (
        "Vascular Lesion adalah kelainan pada pembuluh darah kulit yang dapat berupa bercak merah "
        "atau keunguan. Sebagian besar bersifat jinak namun perlu evaluasi medis untuk memastikan "
        "tidak ada kondisi yang mendasari."
    ),
}

# Recommendation text per risk level
RISK_RECOMMENDATIONS = {
    "low": (
        "Kondisi kulit Anda terdeteksi berisiko rendah. Tetap lakukan pemantauan mandiri secara "
        "rutin terhadap perubahan warna, bentuk, atau ukuran lesi. Konsultasikan ke dokter kulit "
        "jika terdapat perubahan yang mencurigakan."
    ),
    "medium": (
        "Kondisi kulit Anda memerlukan perhatian lebih lanjut. Segera konsultasikan hasil ini "
        "kepada dokter kulit atau dermatologis untuk pemeriksaan dan evaluasi lebih lanjut. "
        "Jangan menunda konsultasi medis."
    ),
    "high": (
        "Kondisi kulit Anda terdeteksi berisiko tinggi. Sangat disarankan untuk segera "
        "berkonsultasi dengan dokter spesialis kulit. Penanganan dini sangat penting untuk "
        "hasil pengobatan yang optimal."
    ),
    "critical": (
        "Kondisi kulit Anda terdeteksi berisiko kritis. Segera kunjungi dokter spesialis kulit "
        "atau rumah sakit terdekat untuk pemeriksaan menyeluruh. Jangan tunda penanganan medis. "
        "Hasil ini bukan diagnosis final, konsultasi medis profesional wajib dilakukan."
    ),
}


settings = Settings()
