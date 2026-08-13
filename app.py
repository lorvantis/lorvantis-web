import streamlit as st

st.set_page_config(page_title="Kailer AI", page_icon="🤖")

st.title("🤖 Kailer AI")
st.caption("64 Kişilik Ekip İçin Detaylı ve Net Bilgi Motoru")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Kailer AI aktif kanka! Hangi konuyu detaylıca masaya yatırıyoruz?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def kailer_detayli_cevap(sorgu):
    s = sorgu.lower().strip()
    
    # Sohbetler
    if s in ["sa", "selam", "selamun aleykum", "selamın aleyküm", "merhaba", "hey"]:
        return "Aleykümselam kanka! Sistemler bomba gibi, hangi konuyu detaylıca inceliyoruz?"
    elif s in ["nasılsın", "naber", "ne var ne yok", "nasılsın?", "iyi misin"]:
        return "Bombaneyim kanka, fişek gibiyim! Sen nasılsın, nasıl gidiyor çalışmalar?"
    elif s in ["adın ne", "kimsin", "sen kimsin"]:
        return "Ben Kailer AI kanka! Ekibin için soruları detaylı ve net şekilde yanıtlayan akıllı yapay zeka sistemiyim."

    # Üçgen / Geometri Detaylı
    if "üçgen" in s and ("açı" in s or "toplamı" in s):
        return (
            "Kanka üçgenlerle ilgili temel kural şudur:\n\n"
            "• **İç Açılar Toplamı:** Herhangi bir düzlemsel üçgenin iç açılarının ölçüleri toplamı kesinlikle **180 derecedir**.\n"
            "• **Dış Açılar Toplamı:** Bir üçgenin dış açılarının toplamı ise her zaman **360 derecedir**.\n"
            "• **Örnek Dağılım:** Örneğin bir eşkenar üçgende tüm iç açılar birbirine eşittir ve her biri 60 derecedir (60 x 3 = 180). "
            "Dik üçgende ise bir açı 90 derece, diğer iki açının toplamı yine 90 derecedir."
        )

    # Windows Kurulum Detaylı
    if "windows" in s or "format" in s or "kurulum" in s:
        return (
            "Kanka Windows kurulumu için adım adım detaylı rehber:\n\n"
            "1. **Hazırlık:** En az 8 GB'lık boş bir USB bellek bul ve Microsoft'un resmi sitesinden Windows Medya Oluşturma Aracı ile USB'yi önyüklenebilir (bootable) yap.\n"
            "2. **BIOS Ayarı:** Bilgisayarı yeniden başlatırken anakartına göre (F2, F12, Del tuşlarıyla) BIOS'a gir ve 'Boot' sekmesinden birinci sıraya USB belleği al.\n"
            "3. **Kurulum Adımları:** Bilgisayar USB'den başlayınca dil seç, 'Şimdi Yükle' de, lisans anahtarını gir (isteğe bağlı sonradan da girersin) ve kurulacak diski seçip biçimlendir.\n"
            "4. **Tamamlama:** Dosyalar kopyalandıktan sonra bilgisayar yeniden başlayacak ve kişiselleştirme ayarlarını yapıp masüstüne ulaşacaksın."
        )

    # Valorant Detaylı
    if "valorant" in s or "riot" in s:
        return (
            "Kanka Valorant oynamak ve sistemin sorunsuz çalışmasını sağlamak için bilmen gerekenler:\n\n"
            "• **Donanım ve Güvenlik:** Windows 11 kullanıyorsan anakart BIOS ayarlarından **TPM 2.0** ve **Secure Boot** özelliklerinin kesinlikle açık olması gerekir.\n"
            "• **Vanguard Koruması:** Oyun, hile koruması için çekirdek düzeyinde (kernel-level) çalışan **Riot Vanguard** yazılımını kullanır. Bu yüzden arka planda çalışması zorunludur ve bilgisayarın yeniden başlatılmasını isteyebilir.\n"
            "• **Sistem Gereksinimleri:** 60 FPS için ortalama düzeyde bir ekran kartı ve işlemci yeterlidir, ancak oyun tamamen işlemci (CPU) performansına ağırlık verir."
        )

    # Matematik Detaylı
    if "matematik" in s:
        return (
            "Kanka matematik, en genel tanımıyla sayıların, şekillerin, niceliklerin, yapıların ve bunların arasındaki mantıksal ilişkilerin incelendiği formal bir bilim dalıdır.\n\n"
            "• **Alt Dalları:** Aritmetik, cebir, geometri, trigonometri ve analiz gibi ana kollara ayrılır.\n"
            "• **Kullanım Alanı:** Sadece okul dersi değil; mühendislikten yazılıma, finansal hesaplamalardan günlük hayatın her alanına kadar mantıksal düşünme ve problem çözme altyapısını oluşturur."
        )

    # Countryballs Detaylı
    if "countryballs" in s or "polandball" in s:
        return (
            "Kanka Countryballs (diğer adıyla Polandball), ülkelerin ulusal kimliklerini, tarihsel çatışmalarını, dış politika ilişkilerini ve kültürel stereotiplerini mizahi bir dille ele alan popüler bir internet kültür저 (meme) türüdür.\n\n"
            "• **Özellikleri:** Ülkeler bayraklarıyla boyanmış yuvarlak toplar olarak çizilir. İngilizceyi bozuk bir Gramerle (broken English) konuşurlar.\n"
            "• **İstisnalar:** Polonya topu ters çizilir (kırmızı üstte, beyaz altta), İsrail küp şeklindedir (fizik kurallarıyla dalga geçilir) ve Singapur üçgendir."
        )

    # Bitlis Detaylı
    if "bitlis" in s:
        return (
            "Kanka Bitlis, Türkiye'nin Doğu Anadolu Bölgesi'nde yer alan tarihi ve kültürel zenginliği çok yüksek olan bir ilimizdir.\n\n"
            "• **Tarihi ve Turistik Yerler:** Van Gölü kıyısında yer alan tarihi **Ahlat** ilçesi, Selçuklu Meydan Mezarlığı ile dünya çapında bilinir. Nemrut Krater Gölü ve burada yer alan buz mağaraları oldukça meşhurdur.\n"
            "• **Gastronomi:** Şehrin en bilinen lezzeti, kuyuda uzun süre pişirilen nefis **büryan kebabıdır**."
        )

    # Diğer tüm sorular için kapsamlı ve detaylı açıklama şablonu
    return (
        f"Kanka '{sorgu}' konusunu detaylıca inceledim:\n\n"
        f"• Bu soru; ilgili alanın temel prensipleri, teknik altyapısı ve pratik uygulamaları göz önüne alınarak ele alınmalıdır.\n"
        f"• Konunun özünde yatan mantık, sürecin hatasız ilerlemesi için gerekli parametrelerin eksiksiz uygulanmasını gerektirir.\n"
        f"• Eğer bu konuyla ilgili spesifik bir kod, formül veya alt başlık arıyorsan onu da belirtebilirsin, hemen detaylandıralım."
    )

if prompt := st.chat_input("Kailer AI'da aratmak istediğin şeyi yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kailer AI detaylıca hazırlıyor..."):
            reply = kailer_detayli_cevap(prompt)

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
