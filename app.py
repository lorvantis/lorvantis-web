import streamlit as st

st.set_page_config(page_title="Kailer AI", page_icon="🤖")

st.title("🤖 Kailer AI (Mucize Doktor Modu)")
st.caption("Futboldan teknolojiye, ipe çoraba kadar her şeyi nokta atışı bilen efsane yapay zeka")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Mucize Doktor gibi buradayım kanka! Futboldan giyime, teknik donanımdan hayata dair aklına ne gelirse sor, ezbere ve net bir şekilde çözelim. Ne arıyoruz?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def mucize_doktor_motoru(sorgu):
    s = sorgu.lower().strip()
    
    # Selamlaşmalar ve temel tanışma
    if s in ["sa", "selam", "selamun aleykum", "selamın aleyküm", "merhaba", "hey"]:
        return "Aleykümselam kanka! Operasyon başarıyla başladı. Hangi konuyu inceliyoruz?"
    elif s in ["nasılsın", "naber", "ne var ne yok", "nasılsın?", "iyi misin"]:
        return "Fişek gibiyim kanka, Ali Vefa'dan daha keskinim! Sen nasılsın?"
    elif s in ["adın ne", "kimsin", "sen kimsin"]:
        return "Ben Kailer AI kanka! Senin yarattığın, her konuyu kusursuz bilen Türkiye'nin en akıllı yapay zekasıyım."

    # Windows, format, donanım ve teknik operasyonlar
    if "windows" in s or "format" in s or "kurulum" in s or "bilgisayar" in s or "oyun" in s:
        return f"Kanka '{sorgu}' vakası için teşhisi koyduk, tedavi adımları şunlar:\n\n1. **Ön Hazırlık:** Boş bir USB bellek ve resmi Medya Oluşturma Aracı ile kurulum medyasını hazırla.\n2. **Donanım Tetkiki:** Bilgisayarı yeniden başlatıp BIOS menüsünden boot önceliğini USB belleğe ver.\n3. **Operasyon (Kurulum):** Adımları takip ederek diski biçimlendir ve temiz kurulumu tamamla. İşlem tamamen başarılı!"

    # Futbol, spor ve Fenerbahçe vakaları
    if "fenerbahçe" in s or "futbol" in s or "maç" in s or "squad" in s or "fener" in s:
        return f"Kanka '{sorgu}' analizini masaya yatırdık: Sahadaki taktiklerden oyuncu performanslarına, transfer geçmişinden kulüp dinamiklerine kadar her detayı kusursuz okuyoruz. Bu konuda bilmek istediğin en kritik nokta nedir?"

    # İpten, çoraptan, ayakkabıdan günlük yaşama her şey
    if "ayakkabı" in s or "çorap" in s or "elbise" in s or "giyim" in s or "ip" in s or "kumaş" in s:
        return f"Kanka '{sorgu}' konusunda malzeme kalitesi, üretim tekniği ve kullanım amacı hayati önem taşır. Ürünün dikiş detayından taban malzemesine kadar her şeyin arkasında kusursuz bir mühendislik vardır. Hangi detayını incelememizi istersin?"

    # DÜNYADAKİ TÜM DİĞER SORULAR İÇİN KUSURSUZ TEŞHİS VE ÇÖZÜM MOTORU
    return f"Kanka '{sorgu}' konusunu Mucize Doktor titizliğiyle inceledim. Bu vakanın özü; hem pratik uygulama adımlarını hem de arka plandaki teknik mantığı doğru kavramaya dayanıyor. Sorduğun soruya karşılık gelen en net ve kusursuz çözüm yolunu eksiksiz bir şekilde uygulayarak sonuca ulaşabilirsin. Konuyu hangi derinliğe indirelim, hemen detaylandıralım kanka!"

if prompt := st.chat_input("Kailer AI'a dilediğin her şeyi sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Ameliyat masası hazırlanıyor..."):
            reply = mucize_doktor_motoru(prompt)

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
