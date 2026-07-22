import streamlit as st
from g4f.client import Client

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye'nin web yapay zekası")

client = Client()

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
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages
                )
                reply = response.choices[0].message.content
            except Exception:
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=st.session_state.messages
                    )
                    reply = response.choices[0].message.content
                except Exception as e:
                    reply = f"Şu an bağlantı kurulamadı: {e}"

            full_reply = f"{reply}\n\n🌐 https://lorvantis-web.streamlit.app"
            st.write(full_reply)
            st.session_state.messages.append({"role": "assistant", "content": full_reply})
