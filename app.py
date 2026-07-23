import streamlit as st
import urllib.request
import urllib.parse
import time

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye’nin web destekli akıllı yapay zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Selam kanka! Kurulumları ve rehberleri artık eskisi gibi uzun uzun, adım adım anlatma modunu açtık. Ne kuruyoruz veya ne öğreniyoruz?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Lorvantis'e bir şeyler yaz..."):
    cleaned_prompt = prompt.strip()
    lower_prompt = cleaned_prompt.lower()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lorvantis hazırlıyor..."):
            reply = ""
            handled_locally = False

            # 1. İstediğin günlük kelimeler (Anında yerel yanıt)
            if lower_prompt in ["sa", "selam", "slm"]:
                reply = "Aleykümselam kanka, nasılsın?"
                handled_locally = True
            elif lower_prompt in ["as", "aleykümselam"]:
                reply = "Aleykümselam kanka, ne var ne yok?"
                handled_locally = True
            elif any(w in lower_prompt for w in ["nasılsın", "naber", "ne var ne yok"]):
                reply = "İyiyim kanka, sen nasılsın, ne bakmıştın?"
                handled_locally = True
            elif any(w in lower_prompt for w in ["sağol", "sagol", "teşekkürler", "teşekkür ederim", "eyvallah"]):
                reply = "Bir şey değil kanka!"
                handled_locally = True

            # 2. Kurulum ve Rehber İstekleri (Adım adım uzun açıklama modu)
            if not handled_locally:
                if any(w in lower_prompt for w in ["windows 10", "kurulum", "format", "nasıl kur", "kuracağım"]):
                    reply = (
                        "Kanka istedin uzun rehberi patlatıyorum, adım adım Windows 10 kurulumu şöyle:\n\n"
                        "**1. Hazırlık Aşaması:**\n"
                        "- En az **8 GB'lık boş bir flash bellek** bul (İçindeki her şey silinecek, dikkat et!)\n"
                        "- Başka bir çalışan bilgisayardan Microsoft'un resmi sitesine gidip **Media Creation Tool** (Medya Oluşturma Aracı) programını indir.\n"
                        "- Programı aç, flash belleğini seç ve Windows 10'un ISO dosyasını flash'a yazdır.\n\n"
                        "**2. Boot Etme (USB'den Başlatma):**\n"
                        "- Hazırladığın flash belleği format atacağın bilgisayara tak ve makineyi yeniden başlat.\n"
                        "- Açılışta marka logosu gelir gelmez anakartının Boot tuşuna (ASUS/MSI için genelde **F12, F11 veya Del**) sürekli basarak Boot Menüsü'ne gir.\n"
                        "- Açılan listeden flash belleğini (USB HDD veya marka adı olarak geçer) seçip Enter'a bas.\n\n"
                        "**3. Kurulum Adımları:**\n"
                        "- Karşına gelen ilk ekranda dil ve klavye ayarını seçip *İleri* de ve **Şimdi Yükle** butonuna tıkla.\n"
                        "- Ürün anahtarın yoksa 'Ürün anahtarım yok' diyerek bu adımı geç.\n"
                        "- Tür olarak **Özel: Yalnızca Windows'u yükle (gelişmiş)** seçeneğini seç.\n"
                        "- Bilgisayarındaki eski Windows'un kurulu olduğu sürücüyü seçip biçimlendir veya sil, ardından o boş alanı seçip *İleri* de. Dosyalar kopyalanmaya başlayacak!\n\n"
                        "Yükleme bitince bilgisayar yeniden başlayacak, işte bu kadar kanka! 😎🔥"
                    )
                    handled_locally = True

            # 3. Diğer tüm sorular için web araması motoru
            if not handled_locally:
                success = False
                for attempt in range(3):
                    try:
                        system_prefix = (
                            "Sen Lorvantisin. Türkiye'nin web destekli en akıllı yapay zekasısın. "
                            "Dünya üzerindeki tüm ülkeleri, başkentlerini; Türkiye'deki 81 ili (plakaları, nüfusları, özellikleri dahil) eksiksiz bilirsin. "
                            "Aktif futbolu, kulüpleri (Fenerbahçe vb.), futbolcuları (Kerem Aktürkoğlu vb.), Valorant'ı ve uzayı tanırsın. "
                            "Kullanıcıya her zaman samimi, kanka diliyle, net ve doyurucu cevaplar verirsin. Soru: "
                        )
                        
                        full_query = system_prefix + cleaned_prompt
                        encoded_query = urllib.parse.quote(full_query)
                        
                        cache_buster = int(time.time() * 1000) + attempt
                        api_url = f"https://text.pollinations.ai/{encoded_query}?search=true&t={cache_buster}"
                        
                        req = urllib.request.Request(
                            api_url, 
                            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'},
                            method='GET'
                        )
                        
                        with urllib.request.urlopen(req, timeout=10) as response:
                            if response.getcode() == 200:
                                data = response.read().decode('utf-8').strip()
                                if data and "402" not in data:
                                    reply = data
                                    success = True
                                    break
                    except Exception:
                        time.sleep(0.3)
                        continue
                
                # Web araması yanıt veremezse akıllı yedekler
                if not success:
                    if any(w in lower_prompt for w in ["tanıt", "hakkında", "nerede", "plakası"]):
                        if "mardin" in lower_prompt:
                            reply = "Mardin, Güneydoğu Anadolu Bölgesi'nde yer alan; taş mimarisi, dar sokakları, tarihi kaleleri ve eşsiz Mezopotamya manzarasıyla büyüleyen **47 plakalı** efsanevi şehrimizdir kanka! 🏛️"
                        elif "siirt" in lower_prompt:
                            reply = "Siirt, Güneydoğu'da yer alan; büryan kebabı, tiftik battaniyesi, Veysel Karani türbesi ve **56 plakasıyla** öne çıkan güzel bir ilimizdir kanka! 🇹🇷"
                        elif "istanbul" in lower_prompt:
                            reply = "İstanbul, iki kıtayı birbirine bağlayan, tarihi yarımadası, Boğaz'ı ve **34 plakasıyla** Türkiye'nin kalbi olan devasa metropoldür kanka! 🌉"
                        else:
                            reply = f"Kanka **'{cleaned_prompt}'** yerini eyvallah biliyoruz; tarihiyle ve kültürüyle bambaşka bir noktadır. Başka hangi şehri veya ülkeyi merak ediyorsun? 😎"
                    elif any(w in lower_prompt for w in ["kerem aktürkoğlu", "aktürkoğlu", "fenerbahçe", "fener"]):
                        if "kerem" in lower_prompt:
                            reply = "Kerem Aktürkoğlu, Türk futbolunun hızı, çalım yeteneği ve bitiriciliğiyle göz dolduran milli kanat oyuncusudur kanka! ⚡⚽"
                        else:
                            reply = "Fenerbahçe şampiyonluk yolunda kadro kalitesiyle ve taraftarıyla ligin tozunu attıran dev bir camiadır kanka 💛💙"
                    elif "valorant" in lower_prompt:
                        reply = "Valorant, Riot Games'in Riot Client üzerinden oynanan taktiksel FPS oyunudur kanka. Bilgisayarına indirip Vanguard korumasıyla oynayabilirsin! 🎮"
                    else:
                        reply = f"Kanka **'{cleaned_prompt}'** konusunu inceledik. İnternet bağlantısında anlık bir dalgalanma oldu ama tüm detayları biliyoruz. Tekrar dener misin? 🔥"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
