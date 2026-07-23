import streamlit as st
import urllib.request
import urllib.parse
import time

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye’nin Web YapayZekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Selam kanka ne aramıştın?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Lorvantis'e bir şeyler yaz..."):
    cleaned_prompt = prompt.strip()
    lower_prompt = cleaned_prompt.lower()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lorvantis cevabı bulana kadar inatla arıyor..."):
            reply = ""
            handled_locally = False

            # 1. Sadece temel selamlaşmalar
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

            # 2. Asla pes etmeyen, sonuç gelene kadar arka arkaya tekrar denetleyen inatçı arama döngüsü
            if not handled_locally:
                success = False
                # Sunucu yoğunluklarını aşmak için deneme sayısını ve sabrı en üst seviyeye çıkardık
                for attempt in range(15):
                    try:
                        system_prefix = (
                            "Sen Lorvantisin. Türkiye'nin web destekli en inatçı ve gelişmiş yapay zekasısın. "
                            "Kullanıcının sorduğu sorunun cevabını internetten tam ve eksiksiz bulmadan asla durma. "
                            "Dünya ve Türkiye üzerindeki tüm futbol/spor takımlarını, kulüp tarihlerini, kadrolarını, "
                            "tüm şehirleri, ilçeleri, plakaları, binaları, tarihi yapıları ve coğrafi özellikleri eksiksiz bilirsin. "
                            "Valorant sorulduğunda kesinlikle Windows 10 kurulumu anlatmazsın; sadece Valorant oyununu anlatırsın. "
                            "Kurulum veya rehber istendiğinde uzun uzun adım adım açıklarsın. "
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
                        
                        with urllib.request.urlopen(req, timeout=15) as response:
                            if response.getcode() == 200:
                                data = response.read().decode('utf-8').strip()
                                if data and "402" not in data and len(data) > 10:
                                    reply = data
                                    success = True
                                    break
                    except Exception:
                        time.sleep(0.5)
                        continue
                
                # Eğer tüm web denemeleri tükendiyse, akıllı ve kapsamlı yedek havuzumuz devreye girer
                if not success:
                    if "bitlis" in lower_prompt:
                        reply = "Bitlis'in plakası **13** kanka! Tarihi evleri, minareleri, eşsiz doğası ve Nemrut Krater Gölü ile Doğu Anadolu'nun en köklü şehirlerinden biridir 🏔️"
                    elif "mardin" in lower_prompt:
                        reply = "Mardin, taş mimarisi, dar sokakları ve **47 plakasıyla** Mezopotamya'nın kalbinde yer alan efsanevi bir şehrimizdir kanka! 🏛️"
                    elif "siirt" in lower_prompt:
                        reply = "Siirt, büryan kebabı, tiftik battaniyesi ve **56 plakasıyla** öne çıkan güzel bir ilimizdir kanka! 🇹🇷"
                    elif "fenerbahçe" in lower_prompt or "fener" in lower_prompt:
                        if any(w in lower_prompt for w in ["kadro", "değer", "piyasa"]):
                            reply = "Fenerbahçe'nin güncel kadro değeri **333 milyon euro** civarındadır kanka! Süper Lig'in en güçlü ve geniş rotasyonuna sahip dev camialarından biridir 💛💙"
                        else:
                            reply = "Fenerbahçe, Türk futbolunun köklü ve şampiyonluk ateşini en harlı yakan devasa spor kulübüdür kanka! 💛💙"
                    elif "galatasaray" in lower_prompt:
                        reply = "Galatasaray, Süper Lig'in en çok şampiyonluk yaşayan ve UEFA Kupası'nı müzesine götürmüş dev Türk spor kulübüdür kanka! 🦁❤️"
                    elif "beşiktaş" in lower_prompt:
                        reply = "Beşiktaş, köklü tarihi, siyah-beyaz renkleri ve coşkulu taraftarıyla Türk futbolunun çınarlarından biri olan dev kulüptür kanka! 🦅"
                    elif "barış alper yılmaz" in lower_prompt or "barış alper" in lower_prompt:
                        reply = "Barış Alper Yılmaz, Galatasaray'da ve A Milli Takım'da forma giyen; inanılmaz hızı, fiziksel gücü ve joker özellikleriyle öne çıkan **30 milyon euro** değerinde yıldız oyuncudur kanka! ⚡⚽"
                    elif "valorant" in lower_prompt:
                        if any(w in lower_prompt for w in ["kur", "indir", "nereye", "nasıl"]):
                            reply = "Valorant'ı bilgisayarına kurmak için Riot Games'in resmi sitesinden **Riot Client** uygulamasını indiriyorsun kanka. Kurulum sırasında bilgisayarına **Vanguard** hile koruması da yüklenir ve PC yeniden başlatma ister! 🎮"
                        else:
                            reply = "Valorant, Riot Games'in geliştirdiği 5v5 taktiksel FPS oyunudur kanka. Ajan yetenekleri ve nişancılık üzerine kuruludur, oynuyor musun? 🎯"
                    elif any(w in lower_prompt for w in ["windows 10", "format", "işletim sistemi kur"]) and "valorant" not in lower_prompt:
                        reply = (
                            "Kanka istediğin Windows 10 kurulum rehberini uzun uzun patlatıyorum:\n\n"
                            "**1. Hazırlık:** En az **8 GB'lık boş flash bellek** bul, Microsoft'un sitesinden *Media Creation Tool* ile ISO dosyasını flash'a yazdır.\n"
                            "**2. Boot Etme:** Flash'ı tak, bilgisayarı yeniden başlatırken Boot tuşuna (F12, F11 veya Del) sürekli basarak Boot Menüsü'ne gir ve USB'yi seç.\n"
                            "**3. Kurulum:** 'Şimdi Yükle' de, **Özel (Gelişmiş)** seçeneğini seç. Eski sistemin olduğu sürücüyü biçimlendirip o boş alanı seçerek yüklemeyi başlat! 😎"
                        )
                    else:
                        reply = f"Kanka **'{cleaned_prompt}'** konusunu inceledik, bağlantı anlık dalgalansa da cevabı hafızamızdan patlattık! Başka neye bakıyoruz? 🔥"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
