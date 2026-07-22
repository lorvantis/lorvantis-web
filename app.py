import streamlit as st
import json
import urllib.request

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye'nin Web Yapay Zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Merhaba! Ben Lorvantis. Sana nasıl yardımcı olabilirim?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lorvantis düşünüyor..."):
            try:
                # Hugging Face Router (API Key gerektirmez)
                url = "https://router.huggingface.co/hf-inference/v1/chat/completions"
                
                payload = json.dumps({
                    "model": "Qwen/Qwen2.5-Coder-32B-Instruct",
                    "messages": st.session_state.messages,
                    "max_tokens": 500
                }).encode("utf-8")
                
                headers = {
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0'
                }
                
                req = urllib.request.Request(url, data=payload, headers=headers)
                
                with urllib.request.urlopen(req) as response:
                    res_body = json.loads(response.read().decode('utf-8'))
                    reply = res_body['choices'][0]['message']['content']
                
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Baglanti hatasi: {e}")
