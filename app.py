import streamlit as st
import g4f

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
                # Doğrudan g4f provider yapısını kullanan hatasız çağrı
                response = g4f.ChatCompletion.create(
                    model=g4f.models.gpt_4o_mini,
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                )
                reply = str(response)
            except Exception as e:
                try:
                    response = g4f.ChatCompletion.create(
                        model=g4f.models.gpt_35_turbo,
                        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    )
                    reply = str(response)
                except Exception as err:
                    reply = f"Bağlantı kurulamadı: {err}"

            full_reply = f"{reply}\n\n🌐 https://lorvantis-web.streamlit.app"
            st.write(full_reply)
            st.session_state.messages.append({"role": "assistant", "content": full_reply})
