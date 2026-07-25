import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖", layout="centered")

# Doğrudan GitHub / Streamlit Secrets (veya çevre değişkeni) üzerinden otomatik çeker
# Hiçbir şey yazmana gerek kalmaz, sistemi otomatik tanır.
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    # Eğer Secrets'ta yoksa Streamlit'in kendi secrets mekanizmasından dener
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="Sen Lorvantis'sin. Türkiye'nin samimi web yapay zekasısın. Kullanıcıya her zaman 'kanka' diye hitap et. Çok samimi, kafa dengi, detaylı, akıcı ve eğlenceli cevaplar ver."
    )
else:
    st.error("Kanka API anahtarı bulunamadı! Lütfen Streamlit Secrets ayarlarına anahtarını ekle.")

if "chat" not in st.session_state and api_key:
    st.session_state.chat = model.start_chat(history=[])

st.title("🤖 Lorvantis AI")
st.caption("Kesintisiz Zeka Motoru")

if api_key:
    for message in st.session_state.chat.history:
        role = "assistant" if message.role == "model" else "user"
        with st.chat_message(role):
            st.write(message.parts[0].text)

    if prompt := st.chat_input("Lorvantis'e yaz..."):
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.status("Lorvantis düşünüyor...", expanded=False):
                try:
                    response = st.session_state.chat.send_message(prompt)
                    reply = response.text
                except Exception as e:
                    reply = f"Kanka bir hata oluştu: {str(e)}"
                
                st.write(reply)
