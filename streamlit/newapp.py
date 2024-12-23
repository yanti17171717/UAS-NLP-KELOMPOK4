import streamlit as st
from streamlit_chat import message
import joblib
import logging

# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Fungsi untuk memuat model chatbot
@st.cache_resource
def load_chatbot_model(model_path="./chatbot_model.pkl"):
    try:
        model = joblib.load(model_path)
        logging.info("Model berhasil dimuat.")
        return model
    except FileNotFoundError:
        logging.error(f"Model tidak ditemukan di path: {model_path}")
        return None
    except Exception as e:
        logging.error(f"Kesalahan saat memuat model: {e}")
        return None

# Fungsi untuk memvalidasi input pengguna
def validate_user_input(user_input):
    if not user_input.strip():
        return False, "Masukan tidak boleh kosong. Silakan masukkan pertanyaan Anda."
    return True, ""

# Fungsi untuk menghasilkan respons chatbot
def generate_response(model, user_input):
    if model is None:
        return "Model belum berhasil dimuat. Silakan periksa konfigurasi aplikasi."
    
    try:
        prediction = model.predict([user_input])
        if prediction and len(prediction) > 0:
            return prediction[0]
        else:
            return "Maaf, saya tidak memahami pertanyaan Anda. Bisakah Anda menjelaskannya lebih spesifik?"
    except Exception as e:
        logging.error(f"Kesalahan saat menghasilkan respons: {e}")
        return "Maaf, terjadi kesalahan saat memproses pertanyaan Anda. Silakan coba lagi."

# Fungsi utama untuk aplikasi
def main():
    # Konfigurasi halaman
    st.set_page_config(page_title="Chatbot Interaktif", page_icon="🤖", layout="wide")
    logging.info("Aplikasi berjalan di http://localhost:8501")

    # Judul halaman
    st.title("🤖 Chatbot Interaktif")

    # Muat model chatbot
    model = load_chatbot_model()

    # Inisialisasi sesi obrolan
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        st.session_state.messages.append(
            {"text": "Halo! Saya adalah chatbot. Bagaimana saya bisa membantu Anda hari ini?", "is_user": False}
        )

    # Fungsi untuk menangani input pengguna
    def handle_user_input():
        user_input = st.session_state["input_box"]
        is_valid, validation_message = validate_user_input(user_input)

        if not is_valid:
            # Jika input tidak valid, tambahkan pesan peringatan
            st.session_state.messages.append({"text": validation_message, "is_user": False})
        else:
            # Tambahkan input pengguna ke sesi
            st.session_state.messages.append({"text": user_input, "is_user": True})

            # Dapatkan respons dari model
            bot_response = generate_response(model, user_input)
            st.session_state.messages.append({"text": bot_response, "is_user": False})

        # Reset input box
        st.session_state["input_box"] = ""

    # Tampilan percakapan
    st.subheader("Percakapan")
    for idx, msg in enumerate(st.session_state.messages):
        message(msg["text"], is_user=msg["is_user"], key=f"message_{idx}")

    # Input pengguna
    st.text_input(
        "Ketik pesan Anda di sini:",
        key="input_box",
        on_change=handle_user_input  # Panggil callback saat input berubah
    )

if __name__ == "__main__":
    main()
