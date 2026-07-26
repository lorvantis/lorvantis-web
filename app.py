import streamlit as st
import requests
import json

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖", layout="centered")

# Gizli anahtarı Streamlit secrets'tan alır
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = ""

st.title("🤖 Lorvantis AI")
st.caption("Türkiye'nin Web YapayZekası")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Lorvantis'e yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Lorvantis düşünüyor...")
        
        try:
            # Doğrudan Gemini API HTTP isteği (Ekstra paket derdi yok)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            contents = []
            for m in st.session_state.messages:
                role = "user" if m["role"] == "user" else "model"
                contents.append({"role": role, "parts": [{"text": m["content"]}]})
                
            payload = {
                "contents": contents,
                "system_instruction": {"parts": [{"text": "Sen Lorvantis'sin. Türkiye'nin samimi web yapay zekasısın. Kullanıcıya her zaman 'kanka' diye hitap et. Çok samimi, kafa dengi, detaylı, akıcı ve eğlenceli cevaplar ver."}]}
            }
            
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            
            if response.status_code == 200:
                res_json = response.json()
                reply = res_json['candidates'][0]['content']['parts'][0]['text']
            else:
                reply = f"Kanka hata oluştu: {response.text}"
                
        except Exception as e:
            reply = f"Kanka bir aksilik çıktı: {str(e)}"
            
        message_placeholder.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
