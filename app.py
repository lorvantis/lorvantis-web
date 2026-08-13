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

    # 1. Valorant İndirme ve Kurulum
    if "valorant" in p and ("indir" in p or "kur" in p or "yükle" in p):
        return """Kanka Valorant'ı bilgisayarına indirmek ve kurmak için şu adımları takip et:
1. **Resmi Siteye Git:** playvalorant.com adresine gir ve oyunu indir butonuna tıkla.
2. **Vanguard'ı Unutma:** Valorant ile birlikte arka planda çalışan anti-cheat sistemi **Vanguard** da kurulacaktır, bu zorunludur.
3. **Riot Games Hesabı:** Kurulum bittikten sonra Riot hesabınla giriş yap (yoksa hızlıca yeni bir tane oluştur).
4. **Güncellemeler:** Oyun açıldığında küçük bir güncelleme yapabilir, bittikten sonra mermileri sızdırmaya başlayabilirsin kanka!"""

    # 2. Valorant Nick / İsim Önerileri
    if "valorant" in p and ("nick" in p or "isim" in p or "ad" in p):
        return """Kanka sana lobinin altını üstüne getirecek en kral Valorant nick önerileri:
* **Vortex #187**
* **Gölge Adam #0001**
* **Kain #3169**
* **Lorvantis #AI**
* **Fenerli #1907**
Hangisini beğeniyorsan yapıştır geç kanka!"""

    # 3. Windows 10 Kurulumu (Format)
    if "windows 10" in p or "format" in p or ("kurulum" in p and "windows" in p):
        return """Kanka Windows 10'u sıfırdan kurmak (format atmak) için şu adımları izlemen yeterli:
1. **USB Bellek Hazırlığı:** En az 8 GB'lık boş bir USB bellek bul. Microsoft'un sitesinden Media Creation Tool ile USB'ye Windows 10 kur.
2. **BIOS Ayarı:** Bilgisayarı yeniden başlat, açılırken **F2, F12 veya Del** ile BIOS'a girip ilk sıraya USB'yi al.
3. **Yükleme:** Bilgisayar açılınca "Şimdi Yükle" de, anahtarın yoksa "Ürün anahtarım yok" diyerek geç.
4. **Özel Kurulum:** **"Özel: Yalnızca Windows'u yükle"** seçeneğini seç, eski diski biçimlendirip devam et. İşlem tamamdır kanka!"""

    # 4. Fenerbahçe
    if "fenerbahçe" in p or "fener" in p:
        return "Kanka Fenerbahçe bu ülkenin en büyük tutkusudur! Kadıköy'de defteri kapatır masayı kurarız, sarı lacivert devama devam!"

    # Diğer her türlü genel soru için
    if "?" in p or "nasıl" in p or "nedir" in p or "niye" in p or "kim" in p or "nerede" in p or "kaç" in p:
        return f"Kanka '{prompt}' konusunu inceledim. Bu tarz konularda en önemli detay mantığı kavramaktır; süreç tamamen teknik altyapıya ve doğru adımları izlemene dayanıyor. Başka bir takıldığın yer var mı kanka?"
    
    return f"Kanka '{prompt}' ile ilgili sistemi taradım. Konuyu biraz daha açarsan hemen detaylandıralım, nedir planımız?"

if prompt := st.chat_input("Kailer AI'a dilediğin soruyu sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kailer AI tarıyor..."):
            reply = akilli_cevap_uret(prompt)

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
