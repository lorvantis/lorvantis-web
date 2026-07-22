import streamlit as st
import requests

# --- SAYFA AYARLARI (Mobil Uyumlu) ---
st.set_page_config(
    page_title="Lorvantis",
    page_icon="🤖",
    layout="centered"
)

# Koyu Tema Şıklığı
st.markdown("""
    <style>
    .main { background-color: #000000; }
    stTextInput > div > div > input { background-color: #121212; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("LORVANTIS 🤖")
st.caption("Kanka Tarzı Yapay Zeka Arayüzü")

# Sohbet Geçmişi Hafızası
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski Mesajları Ekrana Bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan Mesaj Alımı
if prompt := st.chat_input("Bir şeyler yaz kanka..."):
    # Kullanıcı Mesajı
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yapay Zeka Cevabı
    with st.chat_message("assistant"):
        with st.spinner("Düşünüyorum kanka..."):
            try:
                full_prompt = (
                    "Senin adın Lorvantis. Samimi, kanka tarzında ve akıllı bir Türkçe yapay zekasın. "
                    "Cevap uzunluğunu kullanıcının sorusuna göre ayarla. Teknik anlatımda detay ver, "
                    "basit sorularda kısa kes.\n\n"
                    f"Kullanıcı: {prompt}\nLorvantis:"
                )
                
                payload = {
                    "model": "llama3.2",
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {"temperature": 0.3, "num_predict": 500}
                }
                
                # Bilgisayarındaki Ollama'ya Bağlanır
                res = requests.post("http://localhost:11434/api/generate", json=payload)
                
                if res.status_code == 200:
                    answer = res.json().get("response", "Cevap yok kanka.")
                else:
                    answer = "Ollama ile bağlantı kurulamadı kanka."
            except Exception as e:
                answer = "Hata oluştu kanka, model açık mı kontrol et!"

            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})