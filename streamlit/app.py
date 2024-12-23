import streamlit as st
from streamlit_chat import message
import joblib
import logging
import streamlit as st
from streamlit_chat import message


# Fungsi untuk memuat model chatbot
@st.cache_resource
def load_chatbot_model():
    return joblib.load('./chatbot_model.pkl')


# Fungsi untuk menghasilkan respons
def generate_response(model, user_input):
    try:
        prediction = model.predict([user_input])
        return prediction[0]
    except Exception:
        return "Maaf, saya tidak mengerti pertanyaan itu."

def main():
    # Konfigurasi halaman
    st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="wide")
    logging.info("Aplikasi berjalan di: http://localhost:8501")

    # Judul halaman
    st.title("🤖 Chatbot Interaktif")

import streamlit as st
from streamlit_chat import message
import joblib
import logging

# Fungsi untuk memuat model chatbot
@st.cache_resource
def load_chatbot_model():
    return joblib.load('./chatbot_model.pkl')

# Fungsi untuk menghasilkan respons
def generate_response(model, user_input):
    try:
        prediction = model.predict([user_input])
        return prediction[0]
    except Exception:
        return "Maaf, saya tidak mengerti pertanyaan itu."

def main():
    # Konfigurasi halaman
    st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="wide")
    logging.info("Aplikasi berjalan di: http://localhost:8501")

    # Judul halaman
    st.title("🤖 Chatbot Interaktif")

    # Muat model chatbot
    model = load_chatbot_model()

    # Inisialisasi sesi obrolan
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        st.session_state.messages.append({"text": "Halo! Saya adalah chatbot. Bagaimana saya bisa membantu Anda hari ini?", "is_user": False})

    # Tampilan percakapan
    st.subheader("Percakapan")
    for idx, msg in enumerate(st.session_state.messages):
        message(msg["text"], is_user=msg["is_user"], key=f"message_{idx}")

    # Input pengguna
    user_input = st.text_input(
        "Ketik pesan Anda di sini:",
        key="input_box",
        on_change=None
    )

    if st.button("Kirim"):
        if user_input.strip():
            st.session_state.messages.append({"text": user_input, "is_user": True})
            bot_response = generate_response(model, user_input)
            st.session_state.messages.append({"text": bot_response, "is_user": False})

if __name__ == "__main__":
    main()
    

    # Muat model chatbot
    model = load_chatbot_model()

    # Inisialisasi sesi obrolan
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        st.session_state.messages.append({"text": "Halo! Saya adalah chatbot. Bagaimana saya bisa membantu Anda hari ini?", "is_user": False})
    def generate_response(user_input):
        return f"Ini adalah respons untuk: {user_input}"
    def handle_input_change():
        st.session_state["input_box"] = ""
    # Tampilan percakapan
    st.subheader("Percakapan")
    for idx, msg in enumerate(st.session_state.messages):
        message(msg["text"], is_user=msg["is_user"], key=f"message_{idx}")

    # Input pengguna
    user_input = st.text_input(
        "Ketik pesan Anda di sini:",
        key="input_box",
        on_change=handle_input_change
    )

    if user_input.strip():
        st.session_state.messages.append({"text": user_input, "is_user": True})
        bot_response = generate_response(user_input)
        st.session_state.messages.append({"text": bot_response, "is_user": False})

    
        # Tambahkan input pengguna ke sesi
        st.session_state.messages.append({"text": user_input, "is_user": True})

        # Dapatkan respons dari model
        bot_response = generate_response(model, user_input)
        st.session_state.messages.append({"text": bot_response, "is_user": False})

        # Reset input box
        st.session_state["input_box"] = ""

if __name__ == "__main__":
    main()
