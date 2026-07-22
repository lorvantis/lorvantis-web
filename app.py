import streamlit as st

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
            p = prompt.lower()
            
            # Kelime bazlı akıllı yanıt motoru (İnternet kopmalarına ve 402 hatalarına son!)
            if "nasılsın" in p or "ne var ne yok" in p:
                reply = "Eyvallah kanka, bomba gibiyim! Sen nasılsın, nasıl gidiyor?"
            elif "merhaba" in p or "selam" in p:
                reply = "Aleykümselam kanka, hoş geldin! Ne yapıyoruz bugün?"
            elif "adın" in p or "kimsin" in p:
                reply = "Ben Lorvantis! Senin kodlayıp hayata geçirdiğin yapay zeka asistanınım."
            elif "python" in p or "kod" in p:
                reply = f"Python ve kodlama işleri bende kanka! '{prompt}' konusunda sabaha kadar yazabiliriz."
            elif "fenerbahçe" in p or "fb" in p:
                reply = "Renklerimizi unutmayız kanka! Sarı-Lacivert ensesindeyiz her şeyin."
            else:
                reply = f"'{prompt}' dedin kanka, bunu kaydettim. Üzerinde çalışıyorum, başka ne sormak istersin?"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
