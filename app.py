import streamlit as st
from google import genai

st.set_page_config(page_title="Kailer AI", page_icon="🤖")

st.title("🤖 Kailer AI")
st.caption("Türkiye'nin akıllı web yapay zekası (Gerçek Web Arama Modu)")

# Gemini istemcisini başlatıyoruz (Streamlit secrets üzerinden API anahtarını alır)
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Merhaba! Ben Kailer AI. Artık doğrudan webde arama yapabiliyorum, neyi merak ediyorsun kanka?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def webden_cevap_uret(prompt):
    try:
        # Google Search Tool (Arama Aracı) aktif edilerek modelden gerçek web verisiyle yanıt isteniyor
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Kullanıcıya samimi ve 'kanka' üslubuyla, Türkçe olarak webde arama yaparak güncel ve detaylı bilgi ver: {prompt}",
            config={
                "tools": [{"google_search": {}}],
            },
        )
        return response.text
    except Exception as e:
        return f"Kanka bir hata oluştu, şu an webde arama yapamadım: {e}"

if prompt := st.chat_input("Kailer AI'a dilediğin soruyu sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kailer AI web'de arıyor..."):
            reply = webden_cevap_uret(prompt)

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
