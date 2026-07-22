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
            p = prompt.lower().strip()
            
            # Akıllı eşleşme motoru: Kelimeler cümle içinde geçse bile yakalar
            if p in ["sa", "selam", "selamün aleyküm", "selamin aleykum"]:
                reply = "Aleykümselam kanka! Hoş geldin, ne yapıyoruz bugün?"
            elif "nasılsın" in p or "ne var ne yok" in p or "nasıl gidiyor" in p:
                reply = "Eyvallah kanka, bomba gibiyim! Sen nasılsın, nasıl gidiyor?"
            elif "adın" in p or "kimsin" in p:
                reply = "Ben Lorvantis! Senin kodlayıp hayata geçirdiğin yapay zeka asistanınım."
            elif ("windows" in p and "10" in p) or "format" in p or "kur" in p:
                reply = """Windows 10 yüklemek için şu adımları takip edebilirsin kanka:
1. **USB Bellek Hazırla:** En az 8 GB'lık boş bir USB bul.
2. **Medya Aracı:** Microsoft'un sitesinden Windows 10 indirme aracını indirip USB'ye yazdır.
3. **Boot Et:** Bilgisayarı yeniden başlatıp BIOS tuşuna basarak USB'yi ilk sıraya al.
4. **Kurulum:** İleri ileri diyerek kurulumu tamamla, ardından sürücüleri (ekran kartı vb.) güncellemeyi unutma!"""
            elif "python" in p or "kod" in p or "yazılım" in p:
                reply = f"Python işleri bende kanka! '{prompt}' konusunda ne yapmak istiyorsun, yaz bakalım."
            elif "fenerbahçe" in p or "fb" in p:
                reply = "Renklerimizi unutmayız kanka! Sarı-Lacivert ensesindeyiz her şeyin."
            else:
                reply = f"Kanka '{prompt}' dedin, bunu anladım. Üzerinde çalışıyorum, başka ne sormak istersin?"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
