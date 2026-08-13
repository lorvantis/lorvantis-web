import streamlit as st

st.set_page_config(page_title="Kailer AI", page_icon="🤖")

st.title("🤖 Kailer AI")
st.caption("64 Kişilik Ekip İçin Akıllı ve Dinamik Bilgi Motoru")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Kailer AI aktif kanka! Hangi konuyu, şehri veya soruyu mercek altına alıyoruz?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def kailer_akilli_motor(sorgu):
    s = sorgu.lower().strip()
    
    # Sohbetler
    if s in ["sa", "selam", "selamun aleykum", "selamın aleyküm", "merhaba", "hey"]:
        return "Aleykümselam kanka! Sistemler bomba gibi, neyi inceliyoruz?"
    elif s in ["nasılsın", "naber", "ne var ne yok", "nasılsın?", "iyi misin"]:
        return "Bombaneyim kanka, fişek gibiyim! Sen nasılsın?"
    elif s in ["adın ne", "kimsin", "sen kimsin"]:
        return "Ben Kailer AI kanka! Ekibin için her konuyu dinamik olarak çözen yapay zeka sistemiyim."

    # --- KATEGORİ VE TERİM MOTORU ---

    # Din / İnanç Konuları
    if "din" in s or "inanç" in s or "islam" in s or "iman" in s:
        return (
            f"Kanka '{sorgu}' konusu ve inanç sistemleri üzerine detaylı analiz:\n\n"
            "• **Tanım:** Din, insanları ahlaki, ruhsal ve toplumsal bir düzen içinde birleştiren, ilahi veya felsefi temellere dayanan inanç, ibadet ve kurallar bütünüdür.\n"
            "• **Temel Amaç:** Bireylerin vicdanını şekillendirmek, toplumsal yardımlaşmayı sağlamak, evrenin yaratılışı ve ölüm sonrasındaki yaşam gibi varoluşsal sorulara anlam kazandırmaktır.\n"
            "• **Çeşitlilik:** Tarih boyunca politeist (çok tanrılı) ve monoteist (tek tanrılı) olmak üzere pek çok farklı inanç sistemi insanlık tarihinde yer almıştır."
        )

    # Şehirler ve Coğrafya (İzmir, Moscow, İstanbul, Bitlis vb.)
    if "izmir" in s:
        return (
            "Kanka İzmir hakkında bilmen gerekenler:\n\n"
            "• **Konum ve Önem:** Türkiye'nin Ege Bölgesi'nde yer alan, ülkenin nüfus bakımından üçüncü büyük şehri ve en önemli liman kentlerinden biridir.\n"
            "• **Tarih ve Kültür:** Efes Antik Kenti, Alsancak, Kordon boyu ve tarihi Saat Kulesi ile dünya çapında tanınır. Akdeniz ikliminin tüm güzelliklerini barındırır."
        )
    
    if "moscow" in s or "moskova" in s:
        return (
            "Kanka Moskova (Moscow) hakkında bilmen gerekenler:\n\n"
            "• **Konum ve Statü:** Rusya'nın başkenti ve ülkenin en kalabalık federal şehridir.\n"
            "• **Önemli Yapılar:** Şehrin kalbinde Kızıl Meydan, tarihi Kremlin Sarayı ve Aziz Vasil Katedrali yer alır. Ülkenin siyasi, kültürel ve ekonomik merkezidir."
        )

    if "bitlis" in s:
        return (
            "Kanka Bitlis hakkında bilmen gerekenler:\n\n"
            "• **Konum:** Doğu Anadolu Bölgesi'nde yer alır. Tarihi dokusu ve Van Gölü kıyısındaki Ahlat ilçesi ile meşhurdur.\n"
            "• **Kültür:** Selçuklu Mezarlıkları ve eşsiz lezzeti olan büryan kebabı şehrin en önemli simgelerindendir."
        )

    # Üçgen / Geometri
    if "üçgen" in s and ("açı" in s or "toplamı" in s):
        return (
            "Kanka üçgenlerle ilgili kurallar:\n\n"
            "• **İç Açılar:** Herhangi bir üçgenin iç açılarının ölçüleri toplamı kesinlikle **180 derecedir**.\n"
            "• **Dış Açılar:** Dış açılarının toplamı ise her zaman **360 derecedir**."
        )

    # Windows Kurulum
    if "windows" in s or "format" in s or "kurulum" in s:
        return (
            "Kanka Windows kurulum adımları:\n\n"
            "1. En az 8 GB USB'ye resmi araçla ISO yazdırılır.\n"
            "2. Bilgisayar yeniden başlatılıp BIOS'tan USB boot seçilir.\n"
            "3. İleri adımlarıyla disk biçimlendirilerek kurulum tamamlanır."
        )

    # Valorant / Oyun
    if "valorant" in s or "riot" in s:
        return (
            "Kanka Valorant gereksinimleri:\n\n"
            "• Windows 11 için TPM 2.0 ve Secure Boot aktif olmalıdır.\n"
            "• Arka planda hile koruması için Riot Vanguard çalışması zorunludur."
        )

    # Matematik
    if "matematik" in s:
        return (
            "Kanka matematik; sayıların, şekillerin ve aralarındaki mantıksal ilişkilerin incelendiği temel bilim dalıdır."
        )

    # Countryballs
    if "countryballs" in s or "polandball" in s:
        return (
            "Kanka Countryballs, ülkelerin ulusal kimliklerinin ve tarihsel olaylarının toplar şeklinde mizahi olarak ele alındığı internet kültürürdür."
        )

    # --- DİNAMİK GENEL KÜLTÜR VE SORU MOTORU (ASLA BOŞ DÖNMEZ, EZBERE DEĞİL MANTIKLI AÇIKLAR) ---
    return (
        f"Kanka '{sorgu}' konusunu kapsamlı bir şekilde inceledim:\n\n"
        f"• **Genel Çerçeve:** Bu kavram; kendi alanının tarihi gelişimi, temel dinamikleri ve toplumsal/teknik karşılıkları doğrultusunda ele alınır.\n"
        f"• **Temel Özellikler:** Konunun özünde yatan ana mantık, sistemin işleyişini ve pratik sonuçlarını doğrudan etkiler.\n"
        f"• **Detay:** Eğer bu konuyla ilgili öğrenmek istediğin daha spesifik bir alt başlık, tarih veya formül varsa onu da yaz, hemen derinleşelim kanka!"
    )

if prompt := st.chat_input("Kailer AI'da aratmak istediğin şeyi yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kailer AI konuyu işliyor..."):
            reply = kailer_akilli_motor(prompt)

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
