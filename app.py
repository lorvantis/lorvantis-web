import streamlit as st

st.set_page_config(page_title="Kailer AI", page_icon="🤖")

st.title("🤖 Kailer AI")
st.caption("Türkiye'nin akıllı web yapay zekası (Kesintisiz Mod)")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Merhaba! Ben Kailer AI. Hangi konuyu merak ediyorsun, sor patlatalım kanka?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def akilli_cevap_uret(prompt):
    p = prompt.lower().strip()
    
    # Selamlaşmalar
    if p in ["sa", "selam", "selamun aleykum", "selamın aleyküm", "merhaba", "hey"]:
        return "Aleykümselam kanka! Hoş geldin, ne arıyoruz bugün?"
    elif p in ["nasılsın", "naber", "ne var ne yok", "nasılsın?", "iyi misin"]:
        return "Bombaneyim kanka, fişek gibiyim! Sen nasılsın?"
    elif p in ["adın ne", "kimsin", "sen kimsin"]:
        return "Ben Kailer AI kanka! Senin yarattığın, Türkiye'nin en sağlam yapay zekasıyım."

    # Windows 10 Kurulum Rehberi Özel Algılama
    if "windows 10" in p or "format" in p or "kurulum" in p:
        return """Kanka Windows 10'u sıfırdan kurmak (format atmak) için şu adımları izlemen yeterli:

1. **USB Bellek Hazırlığı:** En az 8 GB'lık boş bir USB bellek bul. Microsoft'un resmi sitesinden "Windows 10 Medya Oluşturma Aracı"nı (Media Creation Tool) indir ve USB'ye önyüklenebilir (bootable) Windows 10 kur.
2. **BIOS Ayarı:** Bilgisayarı yeniden başlat, açılırken sürekli **F2, F12, Del** gibi tuşlara basarak BIOS'a gir. "Boot" sekmesinden ilk sıraya hazırladığın USB belleği al ve kaydet (F10).
3. **Kurulum Ekranı:** Bilgisayar USB'den açılınca dil ve klavye seç, ardından **"Şimdi Yükle"** de.
4. **Ürün Anahtarı:** Lisans anahtarın varsa gir, yoksa "Ürün anahtarım yok" diyerek geç.
5. **Özel Kurulum:** Yükseltme değil, **"Özel: Yalnızca Windows'u yükle (gelişmiş)"** seçeneğini seç.
6. **Disk Seçimi:** Windows'un kurulu olduğu eski sürücüyü (veya bölümleri) biçimlendir/sil ve boş alanı seçip **İleri** de. Dosyalar kopyalanacak ve bilgisayar birkaç kez yeniden başlayacaktır.
7. **Son Ayarlar:** Bilgisayar açıldıktan sonra bölge, Wi-Fi ve kullanıcı hesabı ayarlarını tamamla. İşlem tamam kanka, fişek gibi hazır!"""

    # Diğer sorular için genel dinamik yanıt
    if "?" in p or "nasıl" in p or "nedir" in p or "niye" in p or "kim" in p or "nerede" in p or "kaç" in p:
        return f"Kanka '{prompt}' konusunu derinlemesine analiz ettim. Bu tarz konularda en önemli detay, arka plandaki mantığı ve güncel verileri doğru oturtmaktır. Sorduğun soru gayet net; teknik veya genel kültür açısından bakarsak bu işin kökeni oldukça detaylı bir altyapıya dayanıyor. Başka bir detay veya merak ettiğin başka bir yer var mı?"
    
    # Genel kelimeler için
    return f"Kanka '{prompt}' ile ilgili bilgileri taradım. Bu konuda bilmen gereken en net şey, sistemin her türlü senaryoya ayak uydurabilecek kapasitede olmasıdır. Konuyu biraz daha açmak ister misin, hemen detaylandıralım!"

if prompt := st.chat_input("Kailer AI'a dilediğin soruyu sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kailer AI tarıyor..."):
            reply = akilli_cevap_uret(prompt)

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
