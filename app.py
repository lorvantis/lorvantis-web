import streamlit as st
import requests

# Sayfa ayarları
st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")
st.title("🤖 Lorvantis AI Assistant")

# ngrok tünel adresimiz ve modelimiz
NGROK_URL = "https://footer-shimmer-drinking.ngrok-free.dev"
MODEL_NAME = "llama3" # Bilgisayarındaki model adı farklıysa burayı değiştir (örn: mistral, qwen)

# Sohbet geçmişini saklama
if "messages" not in st.session_state:
    st.session_state.messages = []

# Geçmiş mesajları ekrana yazırma
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan mesaj alma
if prompt := st.chat_input("Lorvantis'e bir şeyler yaz..."):
    # Kullanıcı mesajını göster ve kaydet
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Yanıt üretiliyor göstergesi
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking... 💭")
        
        try:
            # Ngrok tüneli üzerinden bilgisayarındaki Ollama'ya bağlanma
            response = requests.post(
                f"{NGROK_URL}/api/generate",
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                answer = response.json().get("response", "Yanıt alınamadı.")
                message_placeholder.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                message_placeholder.error(f"Hata oluştu! Kod: {response.status_code}")
                
        except Exception as e:
            message_placeholder.error("Model kapalı veya bağlantı kurulamadı. Lütfen bilgisayarında Ollama ve ngrok'un açık olduğundan emin ol!")
