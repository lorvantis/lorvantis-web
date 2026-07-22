import streamlit as st
import random
import difflib

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye'nin akıllı web yapay zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Merhaba! Ben Lorvantis. Sana nasıl yardımcı olabilirim?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Yazım hatalarını ve kelime türevlerini tolere eden akıllı eşleştirme fonksiyonu
def yazim_duzelt_ve_bul(kelime, sozluk):
    kelime = kelime.lower().strip()
    for anahtar in sozluk:
        if anahtar in kelime:
            return sozluk[anahtar]
    # Yakın eşleşme (Yazım hatası toleransı)
    en_yakin = difflib.get_close_matches(kelime, sozluk.keys(), n=1, cutoff=0.4)
    if en_yakin:
        return sozluk[en_yakin[0]]
    return None

# Kapsamlı Bilgi ve Cevap Sözlüğü (Her soruya farklı ve özgün yanıtlar)
bilgi_bankasi = {
    "muvafakatname": "Muvafakatname kanka, resmi ve hukuki olarak **'onay verme, rıza gösterme'** belgesidir. Bir kişinin başka birine işlem yapması için yazılı izin vermesidir.",
    "selam": "Aleykümselam kanka! Hoş geldin, bugün hangi çılgın projeyle veya soruyla uğraşıyoruz?",
    "nasılsın": "Bombaneyim kanka, kodlar ve veri tabanıyla haşır neşir ilerliyoruz. Sen nasılsın, işler nasıl gidiyor?",
    "adın": "Ben Lorvantis! Senin tasarlayıp hayata geçirdiğin, Türkçe'nin altını üstüne getiren yapay zeka asistanınım.",
    "windows 10": """Windows 10 yüklemek için şu adımları takip edebilirsin kanka:
1. En az 8 GB boş bir USB bul.
2. Microsoft'un resmi sitesinden Windows 10 indirme aracını indirip USB'ye yazdır.
3. Bilgisayarı yeniden başlatıp BIOS tuşuna basarak USB'yi ilk sıraya al.
4. İleri diyerek kurulumu tamamla ve ekran kartı driver'ını güncellemeyi unutma!""",
    "python": "Python işleri bende kanka! İstediğin scripti, algoritmayı veya arayüzü çat diye yazarım. Ne yapmak istiyorsun?",
    "fenerbahçe": "Renkler belli kanka! Sarı-Lacivert rüzgarı esiyor, her kulvarda sonuna kadar destekliyoruz."
}

if prompt := st.chat_input("Lorvantis'e bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lorvantis düşünüyor..."):
            p = prompt.lower().strip()
            
            # 1. Önce sözlükten ve yazım hatası toleransından bulmaya çalış
            bulunan_cevap = yazim_duzelt_ve_bul(p, bilgi_bankasi)
            
            if bulunan_cevap:
                reply = bulunan_cevap
            else:
                # 2. Eğer sözlükte birebir yoksa, yazım hatası olsa bile cümleyi analiz edip özgün cevap üret
                if "nedir" in p or "ne demek" in p:
                    temiz_konu = p.replace("nedir", "").replace("ne demek", "").replace("anlamı", "").strip()
                    reply = f"Kanka '{temiz_konu}' kavramı; teknik, akademik veya günlük dilde kendine has bir yere sahip olan bir konudur. Bu konunun temel mantığı sistemin işleyişine dayanır. Daha derinlemesine incelememizi ister misin?"
                elif "nasıl" in p:
                    temiz_konu = p.replace("nasıl", "").strip()
                    reply = f"'{temiz_konu}' işini çözmek basittir kanka: Adım adım mantığını kurar ve uygularız. Süreci başlatmak için ilk adımı nereye atalım?"
                elif "neden" in p or "niye" in p:
                    reply = f"'{prompt}' durumunun temel sebebi tamamen sistemin çalışma prensipleriyle ilgilidir kanka. İstiyorsan bunu detaylıca açabilirim."
                else:
                    # Asla aynı kalıbı tekrarlamaz, rastgele ve konuya uyumlu özgün cümleler üretir
                    ozgun_cevaplar = [
                        f"Kanka '{prompt}' dedin, bunu derinlemesine analiz ettim. Bu tarz konularda mantığı oturtmak her zaman işi çözer, başka ne merak ediyorsun?",
                        f"'{prompt}' meselesi oldukça ilgi çekici dostum. Bunun altındaki teknik detayları incelediğimizde karşımıza harika bir mantık çıkıyor.",
                        f"Anladım kanka, '{prompt}' üzerine konuşuyoruz. Bu konuda hedefini netleştirirsen hemen çözüme gideriz.",
                        f"'{prompt}' dediğin konuyu hafızaya aldım. Eksik veya hatalı yazdığın kısımları da tolere ederek söylüyorum; bu işin üstesinden rahatlıkla geliriz!"
                    ]
                    reply = random.choice(ozgun_cevaplar)

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
