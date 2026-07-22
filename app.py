import streamlit as st
import requests

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye'nin web yapay zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Merhaba! Ben Lorvantis. Sana nasıl yardımcı olabilirim?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Lorvantis'e bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lorvantis düşünüyor..."):
            try:
                # Kesin çalışan alternatif public uç nokta (OpenAI uyumlu format)
                payload = {
                    "model": "openai",
                    "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                }
                response = requests.post("https://text.pollinations.ai/", json=payload, timeout=30)
                
                # Yanıtın durumunu ve içeriğini kontrol edelim
                if response.status_code == 200:
                    reply = response.text
                else:
                    reply = f"Sunucu hata kodu döndürdü: {response.status_code} - {response.text}"
            except Exception as e:
                reply = f"Kritik hata yakalandı: {e}"

            full_reply = f"{reply}\n\n🌐 https://lorvantis-web.streamlit.app"
            st.write(full_reply)
            st.session_state.messages.append({"role": "assistant", "content": full_reply})
