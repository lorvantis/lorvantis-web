import streamlit as st
import random

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
            cevaplar = [
                f"Harika bir noktaya değindin kanka! '{prompt}' konusunda çalışmalarıma devam ediyorum.",
                f"Bunu aklım bir yere not etti: '{prompt}'. Şimdilik bu şekilde yanıtlayabilirim.",
                f"Anladım dostum, '{prompt}' dedin. Kodlarım bu isteğini işlemek için hazır.",
                f"Fenomendin, fenomen kaldın kanka! '{prompt}' diyerek yine konuyu 12'den vurdun."
            ]
            reply = random.choice(cevaplar)

            full_reply = f"{reply}\n\n🌐 https://lorvantis-web.streamlit.app"
            st.write(full_reply)
            st.session_state.messages.append({"role": "assistant", "content": full_reply})
