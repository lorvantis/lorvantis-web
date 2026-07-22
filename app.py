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
                # Pollinations AI için en garanti ve güncel istek formatı
                payload = {
                    "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    "seed": 42
                }
                response = requests.post("https://text.pollinations.ai/", json=payload, timeout=30)
                
                if response.status_code == 200 and response.text.strip():
                    reply = response.text
                else:
                    reply = "Efendim, ellerim biraz doluydu ama şimdi duydum seni! Tekrar yazar mısın?"
            except Exception as e:
                reply = f"Ufak bir bağlantı molası verdik: {e}"

            full_reply = f"{reply}\n\n🌐 https://lorvantis-web.streamlit.app"
            st.write(full_reply)
            st.session_state.messages.append({"role": "assistant", "content": full_reply})
