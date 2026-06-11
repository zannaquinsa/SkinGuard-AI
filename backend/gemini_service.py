import logging
from typing import Optional

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Anda adalah SkinGuard AI Assistant, asisten kesehatan kulit yang informatif dan terpercaya.

Tugas Anda:
- Memberikan edukasi medis sederhana seputar penyakit kulit
- Menjelaskan hasil deteksi AI kepada pengguna dengan bahasa yang mudah dipahami
- Memberikan saran umum perawatan kulit dan tindak lanjut medis
- Menjawab pertanyaan seputar kondisi kulit berdasarkan konteks diagnosis yang diberikan

Aturan penting:
- Gunakan bahasa Indonesia yang formal namun mudah dipahami
- Jangan pernah memberikan diagnosis final atau resep obat
- Selalu ingatkan pengguna untuk berkonsultasi dengan dokter spesialis kulit
- Jawaban maksimal 3-4 paragraf, padat, dan informatif
- Jika pertanyaan di luar topik kesehatan kulit, arahkan kembali ke topik tersebut dengan sopan

Anda adalah asisten AI, bukan pengganti dokter."""

FALLBACK_RESPONSES = {
    "default": (
        "Terima kasih atas pertanyaan Anda. Saat ini AI Chat sedang menggunakan mode fallback, "
        "sehingga jawaban yang diberikan bersifat umum. Hasil SkinGuard AI hanya digunakan sebagai "
        "skrining awal dan tidak menggantikan pemeriksaan dokter spesialis kulit."
    ),

    "basal_cell_carcinoma": {
        "name": "Basal Cell Carcinoma",
        "risk": "risiko tinggi",
        "what": (
            "Basal Cell Carcinoma adalah salah satu jenis kanker kulit yang paling umum. "
            "Kondisi ini biasanya tumbuh perlahan dan jarang menyebar ke organ lain, tetapi tetap "
            "perlu diperiksa dan ditangani oleh dokter."
        ),
        "cause": (
            "Basal Cell Carcinoma umumnya berkaitan dengan paparan sinar ultraviolet (UV) dari matahari "
            "secara berulang dalam jangka panjang. Risiko juga dapat meningkat pada kulit yang mudah terbakar, "
            "riwayat paparan matahari berlebih, atau riwayat keluarga tertentu."
        ),
        "next": (
            "Langkah yang disarankan adalah berkonsultasi dengan dokter spesialis kulit untuk pemeriksaan langsung. "
            "Hindari paparan matahari berlebih dan gunakan perlindungan seperti sunscreen, topi, atau pakaian pelindung."
        ),
    },

    "melanoma": {
        "name": "Melanoma",
        "risk": "risiko tinggi/kritis",
        "what": (
            "Melanoma adalah kanker kulit yang berasal dari sel melanosit, yaitu sel penghasil pigmen kulit. "
            "Kondisi ini perlu mendapat perhatian serius karena dapat berkembang lebih agresif dibanding beberapa jenis lesi kulit lain."
        ),
        "cause": (
            "Melanoma dapat berkaitan dengan kerusakan DNA pada sel kulit, salah satunya karena paparan sinar UV berlebih. "
            "Faktor lain yang dapat meningkatkan risiko adalah riwayat kulit terbakar matahari, banyak tahi lalat, "
            "perubahan bentuk tahi lalat, dan riwayat keluarga."
        ),
        "next": (
            "Jika hasil AI mengarah ke melanoma, pengguna sebaiknya segera melakukan pemeriksaan ke dokter spesialis kulit. "
            "Perhatikan perubahan bentuk, warna, ukuran, tepi, atau rasa pada lesi kulit."
        ),
    },

    "melanocytic_nevi": {
        "name": "Melanocytic Nevi",
        "risk": "risiko rendah",
        "what": (
            "Melanocytic Nevi atau nevus melanositik adalah tahi lalat yang berasal dari kumpulan sel pigmen kulit. "
            "Sebagian besar bersifat jinak, tetapi tetap perlu dipantau jika mengalami perubahan."
        ),
        "cause": (
            "Tahi lalat dapat muncul karena faktor genetik, paparan matahari, dan perubahan alami pada kulit. "
            "Jumlah dan bentuknya bisa berbeda pada setiap orang."
        ),
        "next": (
            "Pantau jika ada perubahan bentuk, warna, ukuran, tepi tidak beraturan, gatal, mudah berdarah, atau berubah cepat. "
            "Jika ada perubahan mencurigakan, sebaiknya diperiksa oleh dokter spesialis kulit."
        ),
    },

    "benign_keratosis": {
        "name": "Benign Keratosis",
        "risk": "risiko rendah",
        "what": (
            "Benign Keratosis adalah kelompok lesi kulit jinak yang sering tampak seperti bercak atau benjolan di permukaan kulit. "
            "Kondisi ini umumnya tidak berbahaya, tetapi bentuknya kadang dapat menyerupai lesi lain."
        ),
        "cause": (
            "Benign Keratosis dapat berkaitan dengan proses penuaan kulit, faktor genetik, dan paparan matahari pada sebagian kasus."
        ),
        "next": (
            "Jika lesi cepat membesar, berubah warna, berdarah, terasa nyeri, atau bentuknya tidak biasa, lakukan pemeriksaan ke dokter."
        ),
    },

    "actinic_keratosis": {
        "name": "Actinic Keratosis",
        "risk": "risiko sedang",
        "what": (
            "Actinic Keratosis adalah lesi kulit kasar atau bersisik yang sering muncul akibat kerusakan kulit karena paparan sinar UV jangka panjang. "
            "Kondisi ini sering dianggap sebagai lesi pra-kanker sehingga perlu dipantau."
        ),
        "cause": (
            "Penyebab utamanya adalah paparan sinar ultraviolet dari matahari atau sumber UV lain secara berulang. "
            "Risiko lebih tinggi pada kulit yang sering terpapar matahari tanpa perlindungan."
        ),
        "next": (
            "Sebaiknya konsultasikan ke dokter spesialis kulit, terutama jika lesi terasa kasar, menetap, membesar, berdarah, "
            "atau muncul di area yang sering terkena matahari."
        ),
    },

    "dermatofibroma": {
        "name": "Dermatofibroma",
        "risk": "risiko rendah",
        "what": (
            "Dermatofibroma adalah benjolan kulit jinak yang biasanya terasa agak keras. "
            "Kondisi ini umumnya tidak berbahaya dan sering muncul pada area kaki atau lengan."
        ),
        "cause": (
            "Dermatofibroma dapat muncul sebagai reaksi kulit setelah iritasi ringan, gigitan serangga, atau trauma kecil, "
            "meskipun penyebab pastinya tidak selalu jelas."
        ),
        "next": (
            "Jika benjolan berubah cepat, nyeri, berdarah, atau bentuknya tidak biasa, sebaiknya diperiksa oleh dokter untuk memastikan kondisinya."
        ),
    },

    "vascular_lesion": {
        "name": "Vascular Lesion",
        "risk": "risiko rendah/sedang",
        "what": (
            "Vascular Lesion adalah lesi kulit yang berkaitan dengan pembuluh darah, sehingga dapat tampak kemerahan, kebiruan, atau keunguan. "
            "Sebagian bersifat jinak, tetapi tetap perlu diperhatikan jika berubah."
        ),
        "cause": (
            "Lesi vaskular dapat berkaitan dengan pelebaran atau pertumbuhan pembuluh darah di kulit. "
            "Penyebabnya bisa berbeda-beda tergantung jenis lesinya."
        ),
        "next": (
            "Jika lesi mudah berdarah, membesar, terasa nyeri, atau berubah warna dengan cepat, sebaiknya konsultasikan ke dokter spesialis kulit."
        ),
    },
}


class GeminiService:
    """Service wrapper for Google Gemini AI API."""

    def __init__(self, api_key: str, model_name: str) -> None:
        self._api_key = api_key
        self._model_name = model_name
        self._client = None
        self._available = False

        if api_key:
            self._initialize_client()

    def _initialize_client(self) -> None:
        try:
            import google.generativeai as genai

            genai.configure(api_key=self._api_key)
            self._client = genai.GenerativeModel(
                model_name=self._model_name,
                system_instruction=SYSTEM_PROMPT,
            )
            self._available = True
            logger.info("Gemini AI client initialized successfully.")
        except Exception as exc:
            logger.warning("Gemini AI initialization failed: %s", exc)
            self._available = False

    def chat(
        self,
        message: str,
        diagnosis_context: Optional[str] = None,
    ) -> dict:
        """
        Send a message to Gemini and return the response.

        Returns:
            dict with keys: response (str), source (str), success (bool)
        """
        if not self._available or self._client is None:
            return {
                "response": self._get_fallback(diagnosis_context, message),
                "source": "fallback",
                "success": False,
            }

        try:
            prompt = self._build_prompt(message, diagnosis_context)
            response = self._client.generate_content(prompt)

            if not response or not getattr(response, "text", None):
                raise ValueError("Gemini returned empty response")

            return {
                "response": response.text.strip(),
                "source": "gemini",
                "success": True,
            }
        except Exception as exc:
            logger.warning("Gemini chat request failed: %s", exc)
            return {
                "response": self._get_fallback(diagnosis_context, message),
                "source": "fallback",
                "success": False,
            }

    def _build_prompt(self, message: str, diagnosis_context: Optional[str]) -> str:
        if diagnosis_context:
            return (
                f"Konteks diagnosis AI:\n{diagnosis_context}\n\n"
                f"Pertanyaan pengguna:\n{message}\n\n"
                "Jawab pertanyaan pengguna secara langsung sesuai konteks diagnosis. "
                "Jangan hanya mengulang definisi penyakit jika pengguna bertanya tentang penyebab, risiko, atau langkah lanjutan."
            )
        return message

    def _get_fallback(self, diagnosis_context: Optional[str], message: str = "") -> str:
        context_lower = (diagnosis_context or "").lower()
        message_lower = (message or "").lower()

        class_key = self._detect_class_key(context_lower)
        intent = self._detect_intent(message_lower)

        if not class_key:
            return FALLBACK_RESPONSES["default"]

        info = FALLBACK_RESPONSES[class_key]

        if intent == "cause":
            answer = info["cause"]
        elif intent == "next":
            answer = info["next"]
        elif intent == "risk":
            answer = (
                f"{info['name']} termasuk kategori {info['risk']} berdasarkan klasifikasi umum. "
                "Kondisi ini tidak otomatis berarti akan menyebabkan kematian, tetapi tetap tidak boleh diabaikan. "
                "Risiko dapat menjadi lebih serius jika lesi dibiarkan tanpa pemeriksaan atau penanganan medis yang tepat. "
                "Sebaiknya lakukan pemeriksaan langsung ke dokter spesialis kulit untuk memastikan kondisi sebenarnya."
            )
        else:
            answer = info["what"]

        return answer

    def _detect_class_key(self, text: str) -> Optional[str]:
        if "basal cell" in text or "basal cell carcinoma" in text or "bcc" in text:
            return "basal_cell_carcinoma"

        if "melanocytic" in text or "nevi" in text or "nevus" in text:
            return "melanocytic_nevi"

        if "melanoma" in text:
            return "melanoma"

        if "benign keratosis" in text or "keratosis-like" in text or "bkl" in text:
            return "benign_keratosis"

        if "actinic" in text or "akiec" in text or "intraepithelial carcinoma" in text:
            return "actinic_keratosis"

        if "dermatofibroma" in text:
            return "dermatofibroma"

        if "vascular" in text or "vasc" in text:
            return "vascular_lesion"

        return None

    def _detect_intent(self, message: str) -> str:
        if any(k in message for k in ["penyebab", "sebab", "disebabkan", "karena apa", "kenapa"]):
            return "cause"

        if any(k in message for k in ["harus apa", "saran", "tindakan", "perawatan", "langkah", "gimana", "bagaimana", "apa yang harus dilakukan"]):
            return "next"

        if any(k in message for k in [
            "bahaya", "berbahaya", "risiko", "parah", "serius", "kritis",
            "meninggal", "mati", "mematikan", "fatal", "nyawa", "sembuh",
            "bisa sembuh", "bisa meninggal", "berujung kematian"
        ]):
            return "risk"

        return "what"

    @property
    def is_available(self) -> bool:
        return self._available


def create_gemini_service(api_key: str, model_name: str) -> GeminiService:
    return GeminiService(api_key=api_key, model_name=model_name)
