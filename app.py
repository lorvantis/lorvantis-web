import streamlit as st

st.set_page_config(page_title="Kailer AI", page_icon="🤖")

st.title("🤖 Kailer AI")
st.caption("64 Kişilik Ekip İçin Güvenli Bilgi Motoru")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Kailer AI aktif kanka! Sistemler tam gaz ayakta, bombalar güvenli. Ne arıyoruz?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def kailer_kesin_motor(sorgu):
    s = sorgu.lower().strip()
    
    # Sohbetler
    if s in ["sa", "selam", "selamun aleykum", "selamın aleyküm", "merhaba", "hey"]:
        return "Aleykümselam kanka! Sistemler tam gaz ayakta, bombalar güvenli, ne arıyoruz?"
    elif s in ["nasılsın", "naber", "ne var ne yok", "nasılsın?", "iyi misin"]:
        return "Bombaneyim kanka, fişek gibiyim! Sen nasılsın?"
    elif s in ["adın ne", "kimsin", "sen kimsin"]:
        return "Ben Kailer AI kanka! Ekibin için bilgi üreten, hata tanımayan sistemiyim."

    # Windows Kurulum
    if "windows" in s or "format" in s or "kurulum" in s:
        return "**Windows Kurulum Rehberi**\n\n1. En az 8 GB boş bir USB bellek resmi araçla önyüklenebilir yapılır.\n2. Bilgisayar yeniden başlatılıp BIOS'tan USB boot seçilir.\n3. Disk bölümleri yapılandırılıp kurulum tamamlanır."

    # Valorant / Oyun
    if "valorant" in s or "oyun" in s or "riot" in s:
        return "**Valorant ve Riot Sistem Gereksinimleri**\n\n1. Windows 11 için TPM 2.0 ve Secure Boot aktif olmalıdır.\n2. Çekirdek düzeyinde çalışan Riot Vanguard koruması gereklidir.\n3. Resmi Riot istemcisi ile giriş yapılarak oynanır."

    # Matematik
    if "matematik" in s:
        return "**Matematik Nedir?**\n\nSayıların, şekillerin, yapıların ve aralarındaki mantıksal ilişkilerin incelendiği formal bilim dalıdır."

    # Countryballs
    if "countryballs" in s or "polandball" in s:
        return "**Countryballs (Polandball)**\n\nÜlkelerin ulusal kimliklerinin, tarihsel arka planlarının, dış ilişkilerinin ve diplomatik esprilerinin ülkelere ait topları temsil eden karakterlerle mizahi olarak ele alındığı bir internet meme kültürüdür."

    # Bitlis
    if "bitlis" in s:
        return "**Bitlis**\n\nTürkiye'nin Doğu Anadolu Bölgesi'nde yer alan, tarihi dokusu, Van Gölü kıyısındaki Ahlat ilçesi, tarihi mezarlıkları ve büryan kebabı ile ünlü tarihi bir ilimizdir."

    # Genel Akıllı Yanıt (Asla boş dönmez, soru sormaz, direkt bilgi verir)
    return f"**{sorgu.capitalize()}**\n\nBu konu; teknik altyapı, pratik uygulama adımları ve güncel standartlar çerçevesinde ele alınır. Ekibinin projede en yüksek verimi alabilmesi için bu parametrelerin eksiksiz uygulanması esastır."

if prompt := st.chat_input("Kailer AI'da aratmak istediğin şeyi yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kailer AI iş başında..."):
            reply = kailer_kesin_motor(prompt)

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
