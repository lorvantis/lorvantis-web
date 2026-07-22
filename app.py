import streamlit as st
import json
import urllib.request

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("7/24 Aktif Web Yapay Zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Merhaba! Ben Lorvantis. Sana nasıl yardımcı olabilirim?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lorvantis düşünüyor..."):
            try:
                # Pollinations AI Endpoint
                url = "https://text.pollinations.ai/"
                
                # Mesaj geçmişini temiz formatlama
                formatted_messages = [
                    {"role": m["role"], "content": m["content"]} 
                    for m in st.session_state.messages
                ]
                
                payload = json.dumps({
                    "messages": formatted_messages,
                    "model": "openai"
                }).encode("utf-8")
                
                # 403 engelini aşmak için tarayıcı başlıkları (User-Agent)
                headers = {
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
                
                req = urllib.request.Request(url, data=payload, headers=headers)
                
                with urllib.request.urlopen(req) as response:
                    reply = response.read().decode('utf-8')
                
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
