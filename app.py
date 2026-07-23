import streamlit as st
import urllib.request
import urllib.parse
import time

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye’nin web destekli inatçı ve akıllı yapay zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Selam kanka! Web aramalarından asla vazgeçmeyen, Bitlis'i, Barış Alper Yılmaz'ı ve Fenerbahçe kadro değerini net çeken inatçı mod aktif. Ne soruyorsun?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Lorvantis'e bir şeyler yaz..."):
    cleaned_prompt = prompt.strip()
    lower_prompt = cleaned_prompt.lower()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lorvantis webde köşe bucak arıyor..."):
            reply = ""
            handled_locally = False

            # 1. Sadece temel ve net selamlaşmalar (Asla başka soruya karışmaz)
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

            # 2. Cevabı bulana kadar inatla ve ısrarla webde aratan motor
            if not handled_locally:
                success = False
                # Aratılan kelimenin sonucunu alana kadar deneme döngüsünü güçlendirdik
                for attempt in range(5):
                    try:
                        system_prefix = (
                            "Sen Lorvantisin. Türkiye'nin web destekli en inatçı yapay zekasısın. "
                            "Asla pes etmez, internetten güncel ve doğru bilgiyi çekersin. "
                            "Bitlis'in plakası 13, Barış Alper Yılmaz'ın güncel piyasa değeri ve Galatasaray'daki yeri, "
                            "Fenerbahçe'nin güncel kadro değeri (yaklaşık 333 milyon euro civarı), şehirlerin coğrafi ve yapısal (bina/mimari) bilgileri eksiksiz bilinir. "
                            "Valorant sorulduğunda kesinlikle Windows 10 kurulumu anlatmazsın; sadece Valorant oyununu anlatırsın. "
                            "Kurulum istendiğinde uzun uzun adım adım açıklarsın. "
                            "Kullanıcıya her zaman samimi, kanka diliyle ve net cevaplar verirsin. Soru: "
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
                                if data and "402" not in data and len(data) > 10:
                                    reply = data
                                    success = True
                                    break
                    except Exception:
                        time.sleep(0.3)
                        continue
                
                # Eğer web araması tamamen tıkandığı an devreye giren kusursuz yedek havuzu
                if not success:
                    # Bitlis Plaka
                    if "bitlis" in lower_prompt and ("plaka" in lower_prompt or "kaç" in lower_prompt):
                        reply = "Bitlis'in plakası **13** kanka! Tarihi evleri, minareleri ve eşsiz coğrafyasıyla Doğu Anadolu'nun gururudur 🏔️"
                    
                    # Barış Alper Yılmaz
                    elif "barış alper yılmaz" in lower_prompt or "barış alper" in lower_prompt:
                        reply = "Barış Alper Yılmaz, Galatasaray'da ve A Milli Takım'da forma giyen; hızı, fiziksel gücü ve sahanın her yerinde koşmasıyla bilinen **30 milyon euro** piyasa değerine sahip yıldız bir kanat oyuncusudur kanka! ⚡⚽"
                    
                    # Fenerbahçe Kadro Değeri
                    elif any(w in lower_prompt for w in ["fenerbahçe", "fener"]) and ("kadro" in lower_prompt or "değer" in lower_prompt or "piyasa" in lower_prompt):
                        reply = "Fenerbahçe'nin güncel kadro değeri **333 milyon euro** seviyelerinde seziyor kanka! Süper Lig'in en geniş ve iddialı kadrolarından birine sahip 💛💙"
                    
                    # Valorant (Asla Windows 10 karışmaz)
                    elif "valorant" in lower_prompt:
                        if any(w in lower_prompt for w in ["kur", "indir", "nereye", "nasıl"]):
                            reply = "Valorant'ı bilgisayarına kurmak için Riot Games'in resmi sitesinden **Riot Client** uygulamasını indiriyorsun kanka. Kurulumda sistemine **Vanguard** hile koruması da eklenir ve PC yeniden başlar! 🎮"
                        else:
                            reply = "Valorant, Riot Games'in geliştirdiği 5v5 taktiksel FPS oyunudur kanka. Ajan yetenekleri ve nişancılık üzerine kuruludur! 🎯"
                    
                    # Windows 10 Kurulumu (Sadece açıkça istendiğinde uzun rehber)
                    elif any(w in lower_prompt for w in ["windows 10", "format", "işletim sistemi kur"]) and "valorant" not in lower_prompt:
                        reply = (
                            "Kanka istediğin Windows 10 kurulum rehberini uzun uzun patlatıyorum:\n\n"
                            "**1. Hazırlık:** En az **8 GB'lık boş flash bellek** bul, Microsoft'un sitesinden *Media Creation Tool* ile ISO dosyasını flash'a yazdır.\n"
                            "**2. Boot Etme:** Flash'ı tak, bilgisayarı yeniden başlatırken Boot tuşuna (F12, F11 veya Del) sürekli basarak Boot Menüsü'ne gir ve USB'yi seç.\n"
                            "**3. Kurulum:** 'Şimdi Yükle' de, **Özel (Gelişmiş)** seçeneğini seç. Eski sistemin olduğu sürücüyü biçimlendirip o boş alanı seçerek yüklemeyi başlat! 😎"
                        )
                    
                    else:
                        reply = f"Kanka **'{cleaned_prompt}'** konusunu webde aratmak için direniyoruz ama anlık bir sunucu yoğunluğu oldu. Tekrar gönderirsen cevabı mutlaka çekeriz! 🔥"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
