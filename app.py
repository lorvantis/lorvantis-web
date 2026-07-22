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
                # Ücretsiz ve key istemeyen açık AI servisi
                url = "https://text.pollinations.ai/"
                payload = json.dumps({
                    "messages": st.session_state.messages,
                    "model": "searchgpt"
                }).encode("utf-8")
                
                req = urllib.request.Request(
                    url, 
                    data=payload, 
                    headers={'Content-Type': 'application/json'}
                )
                
                with urllib.request.urlopen(req) as response:
                    reply = response.read().decode('utf-8')
                
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
