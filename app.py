import streamlit as st
import urllib.request
import urllib.parse
import time

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye’nin web destekli akıllı yapay zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Selam kanka! Web aramalarından asla vazgeçmeme modunu, Bitlis'ten Barış Alper Yılmaz'a ve Fenerbahçe kadro değerine kadar tüm özel bilgileri güncelledik. Ne soruyorsun?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Lorvantis'e bir şeyler yaz..."):
    cleaned_prompt = prompt.strip()
    lower_prompt = cleaned_prompt.lower()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lorvantis webde köşe bucak aratıyor..."):
            reply = ""
            handled_locally = False

            # 1. Sadece temel selamlaşmalar (Asla yanlışlıkla başka bir soruya cevap vermez)
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

            # 2. Asla pes etmeyen, cevabı bulana kadar webde inatla aratan motor
            if not handled_locally:
                success = False
                # Deneme sayısını ve arama kararlılığını artırdık
                for attempt in range(4):
                    try:
                        system_prefix = (
                            "Sen Lorvantisin. Türkiye'nin web destekli en akıllı ve inatçı yapay zekasısın. "
                            "Asla pes etmez, sorulan sorunun cevabını internetten bulup getirirsin. "
                            "Bitlis'in plakası 13, Barış Alper Yılmaz'ın Galatasaray'ın milli futbolcusu olduğunu, "
                            "Fenerbahçe'nin güncel kadro değerini, Türkiye'deki tüm il, ilçe ve coğrafi bilgileri eksiksiz bilirsin. "
                            "Valorant sorulduğunda asla Windows 10 kurulumu anlatmaz, tamamen Valorant'ı (oyun mekanikleri, Riot Client, Vanguard) anlatırsın. "
                            "Kurulum veya rehber istendiğinde uzun uzun adım adım açıklarsın. "
                            "Kullanıcıya her zaman samimi, kanka diliyle, net ve doğrudan soruya odaklanarak cevap verirsin. Soru: "
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
                        
                        with urllib.request.urlopen(req, timeout=12) as response:
                            if response.getcode() == 200:
                                data = response.read().decode('utf-8').strip()
                                # Gelen cevabın boş veya hatalı olmadığını doğruluyoruz
                                if data and "402" not in data and len(data) > 10:
                                    reply = data
                                    success = True
                                    break
                    except Exception:
                        time.sleep(0.4)
                        continue
                
                # Eğer web araması gerçekten sonuna kadar zorlanıp yanıt alamazsa, bağlamı asla karıştırmayan nokta atışı akıllı yedekler
                if not success:
                    # Bitlis Plaka
                    if "bitlis" in lower_prompt and ("plaka" in lower_prompt or "kaç" in lower_prompt):
                        reply = "Bitlis'in plakası **13** kanka! Minareleri, milattan kaleme kaleleri ve eşsiz doğasıyla Doğu Anadolu'nun inci şehirlerinden biridir. 🏔️"
                    
                    # Barış Alper Yılmaz
                    elif "barış alper yılmaz" in lower_prompt or "barış alper" in lower_prompt:
                        reply = "Barış Alper Yılmaz, Galatasaray'da ve A Milli Futbol Takımı'mızda forma giyen; inanılmaz hızı, gücü ve çok yönlülüğüyle (kanat, bek, forvet oynayabilen) sahnenin tozunu attıran efsane bir oyuncudur kanka! ⚡⚽"
                    
                    # Fenerbahçe Kadro Değeri
                    elif any(w in lower_prompt for w in ["fenerbahçe", "fener"]) and ("kadro" in lower_prompt or "değer" in lower_prompt or "piyasa" in lower_prompt):
                        reply = "Fenerbahçe'nin kadro ve piyasa değeri transfer dönemlerine göre güncelleniyor kanka! Süper Lig'in en yüksek piyasa değerine ve en geniş rotasyonuna sahip, şampiyonluk ateşini yakan dev kadrolardan biridir 💛💙"
                    
                    # Valorant (Asla Windows 10 karışmayacak)
                    elif "valorant" in lower_prompt:
                        if any(w in lower_prompt for w in ["kur", "indir", "nereye", "nasıl"]):
                            reply = "Valorant'ı bilgisayarına kurmak için Riot Games'in resmi sitesinden **Riot Client** uygulamasını indiriyorsun kanka. Kurulum sırasında bilgisayarına otomatik olarak **Vanguard** hile koruması da yüklenir ve yeniden başlatma ister. İşlem bu kadar! 🎮"
                        else:
                            reply = "Valorant, Riot Games'in geliştirdiği 5v5 taktiksel bir FPS oyunudur kanka. Ajan yetenekleri ve keskin nişancılık üzerine kuruludur, oynuyor musun? 🎯"
                    
                    # Windows 10 Kurulumu (Sadece açıkça istendiğinde)
                    elif any(w in lower_prompt for w in ["windows 10", "format", "işletim sistemi kur"]) and "valorant" not in lower_prompt:
                        reply = (
                            "Kanka sorduğun Windows 10 kurulum rehberi adım adım şöyle:\n\n"
                            "**1. Hazırlık:** En az **8 GB'lık boş flash bellek** bul, Microsoft'un sitesinden *Media Creation Tool* ile ISO'yu flash'a yazdır.\n"
                            "**2. Boot:** Flash'ı tak, PC'yi yeniden başlatırken Boot tuşuna (F12, F11 veya Del) basıp USB'yi seç.\n"
                            "**3. Kurulum:** 'Şimdi Yükle', ardından **Özel (Gelişmiş)** seçeneğini seç. Eski sürücüyü biçimlendirip boş alana yüklemeyi başlat! 😎"
                        )
                    
                    # Şehirler genel tanıtım
                    elif any(w in lower_prompt for w in ["tanıt", "hakkında", "nerede"]):
                        if "mardin" in lower_prompt:
                            reply = "Mardin, taş mimarisi ve 47 plakasıyla Mezopotamya'nın incisidir kanka! 🏛️"
                        elif "siirt" in lower_prompt:
                            reply = "Siirt, büryan kebabı ve 56 plakasıyla Doğu'nun güzel şehridir kanka! 🇹🇷"
                        else:
                            reply = f"Kanka **'{cleaned_prompt}'** konusunu webde inatla arattık ama anlık sunucu takıldı. Tekrar yazarsan cevabı mutlaka çekeriz! 🔥"
                    
                    else:
                        reply = f"Kanka **'{cleaned_prompt}'** konusunu webde aratmak için direniyoruz ama anlık bir kopukluk oldu. Tekrar gönderirsen şak diye ekrandasın! 🚀"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
