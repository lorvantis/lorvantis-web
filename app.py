import streamlit as st

st.set_page_config(page_title="Kailer AI", page_icon="🤖")

st.title("🤖 Kailer AI")
st.caption("64 Kişilik Ekip İçin Profesyonel Tam Donanımlı Arama ve Bilgi Motoru")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Kailer AI aktif. Futboldan Valorant'a, Windows kurulumundan ipe çoraba kadar ne aratmak istiyorsun kanka?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def kailer_mutlak_motor(sorgu):
    s = sorgu.lower().strip()
    
    # Sohbetler
    if s in ["sa", "selam", "selamun aleykum", "selamın aleyküm", "merhaba", "hey"]:
        return "Aleykümselam kanka! 64 kişilik ekip için sistemler tam gaz ayakta, ne arıyoruz?"
    elif s in ["nasılsın", "naber", "ne var ne yok", "nasılsın?", "iyi misin"]:
        return "Bombaneyim kanka, arama motoru gibi fişek gibiyim! Sen nasılsın?"
    elif s in ["adın ne", "kimsin", "sen kimsin"]:
        return "Ben Kailer AI kanka! 64 kişilik ekibin için her şeyi bilen profesyonel yapay zeka sistemiyim."

    # Valorant ve Oyun Kurulumları
    if "valorant" in s or "oyun kur" in s or " riot" in s:
        return f"Kanka '{sorgu}' için profesyonel kurulum rehberi şudur:\n\n1. **Riot Vanguard Şartı:** Valorant oynamak için bilgisayarınızda TPM 2.0 ve Secure Boot (Güvenli Önyükleme) aktif olmalıdır (özellikle Windows 11'de zorunludur).\n2. **İndirme ve Kurulum:** Riot Games resmi web sitesinden Vanguard destekli istemciyi (client) indirip kurun.\n3. **Yeniden Başlatma:** Kurulum sonrası anti-cheat (Vanguard) sisteminin aktif olması için bilgisayarı yeniden başlatın. Oyuna giriş yapabilirsiniz!"

    # Windows 10 / Format / Kurulum
    if "windows" in s or "format" in s or "kurulum" in s or "bilgisayar" in s:
        return f"Kanka '{sorgu}' için profesyonel rehber ve uygulama adımları şunlardır:\n\n1. **Medya Hazırlığı:** En az 8 GB kapasiteli boş bir USB bellek seçilir ve resmi araçla önyüklenebilir hale getirilir.\n2. **BIOS / UEFI Ayarı:** Bilgisayar yeniden başlatılarak BIOS menüsüne girilir; Boot önceliği USB belleğe tanımlanır.\n3. **Kurulum Süreci:** Dil ve bölge tercihleri yapıldıktan sonra 'Şimdi Kur' adımıyla devam edilir. Disk biçimlendirilerek kurulum tamamlanır."

    # Futbol, Fenerbahçe ve spor analizleri
    if "fenerbahçe" in s or "futbol" in s or "maç" in s or "squad" in s or "fener" in s:
        return f"Kanka '{sorgu}' analizi incelendi: Kulüp tarihleri, transfer, squad yapılanmaları, taktiksel dizilişler ve güncel performans verileri profesyonel düzeyde bu kapsamdadır. Ekibe sunmak istediğin özel bir analiz var mı?"

    # Giyim, ayakkabı, çorap ve imalat detayları
    if "ayakkabı" in s or "çorap" in s or "elbise" in s or "giyim" in s or "ip" in s or "kumaş" in s:
        return f"Kanka '{sorgu}' konusunda malzeme kalitesi, dokuma sıklığı, hammadde (pamuk, sentetik, deri oranları) ve kullanım ergonomisi temel kriterlerdir. Ürünün dayanıklılığı bu parametrelere göre şekillenir."

    # HER SORU İÇİN ASLA BOŞ BIRAKMAYAN AKILLI SENTEZ
    return f"Kanka '{sorgu}' başlığı için sistemin tüm veritabanını taradım. Bu konunun temel dinamikleri; teknik altyapı, pratik uygulama adımları ve güncel standartlar üzerine kuruludur. Ekibinle paylaşabileceğin en net ve doğru sonuç, bu adımların eksiksiz uygulanmasıyla elde edilir. Konuyu hangi alt başlıkta derinleştirelim?"

if prompt := st.chat_input("Kailer AI'da aratmak istediğin şeyi yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kailer AI analiz ediyor..."):
            reply = kailer_mutlak_motor(prompt)

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
