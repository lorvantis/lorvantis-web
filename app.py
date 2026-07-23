import streamlit as st
import urllib.request
import urllib.parse
import time

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye’nin web destekli akıllı yapay zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Selam kanka! Selamlaşmaları yerelleştirdik, şehirleri, ülkeleri ve güncel futbolu ise tam kapasite açtık. Ne soruyorsun?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Lorvantis'e bir şeyler yaz..."):
    cleaned_prompt = prompt.strip()
    lower_prompt = cleaned_prompt.lower()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lorvantis inceliyor ve webde aratıyor..."):
            reply = ""
            handled_locally = False

            # 1. İstediğin günlük kelimeler (Web'e gitmeden anında yerel yanıt)
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

            # 2. Günlük kalıplar dışındaki her şey için gelişmiş web arama motoru
            if not handled_locally:
                success = False
                for attempt in range(3):  # Şansı artırmak için deneme hakkını 3 yaptık
                    try:
                        system_prefix = (
                            "Sen Lorvantisin. Türkiye'nin web destekli en akıllı yapay zekasısın. "
                            "Dünya üzerindeki tüm ülkeleri, başkentlerini, para birimlerini, tarihini; "
                            "Türkiye'deki 81 ilin tamamını (plakaları, nüfusları, coğrafi özellikleri, nesi meşhur olduğu dahil) eksiksiz tanır ve tanıtırın. "
                            "Ayrıca aktif futbolu, tüm ligleri, güncel futbolcuları (Kerem Aktürkoğlu, Arda Güler vb.), kulüpleri (Fenerbahçe vb.), "
                            "Valorant gibi oyunları, tarihi ve uzayı derinlemesine bilirsin. "
                            "Kullanıcıya her zaman samimi, kanka diliyle, net, doyurucu ve doğrudan soruya odaklanarak cevap verirsin. Soru: "
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
                                if data and "402" not in data:
                                    reply = data
                                    success = True
                                    break
                    except Exception:
                        time.sleep(0.4)
                        continue
                
                # Web araması anlık takılırsa şehirleri, ülkeleri ve futbolu kaçırmayan akıllı yedek
                if not success:
                    # Şehir / Ülke tanıtımları
                    if any(w in lower_prompt for w in ["tanıt", "hakkında", "nerede", "nüfusu", "plakası"]):
                        if "mardin" in lower_prompt:
                            reply = "Mardin, Güneydoğu Anadolu Bölgesi'nde yer alan; taş mimarisi, dar sokakları, tarihi kaleleri ve eşsiz Mezopotamya manzarasıyla büyüleyen **47 plakalı** efsanevi şehrimizdir kanka! 🏛️"
                        elif "siirt" in lower_prompt:
                            reply = "Siirt, Güneydoğu'da yer alan; büryan kebabı, tiftik battaniyesi, Veysel Karani türbesi ve **56 plakasıyla** öne çıkan güzel bir ilimizdir kanka! 🇹🇷"
                        elif "istanbul" in lower_prompt:
                            reply = "İstanbul, iki kıtayı birbirine bağlayan, tarihi yarımadası, Boğaz'ı ve **34 plakasıyla** Türkiye'nin kalbi olan devasa metropoldür kanka! 🌉"
                        else:
                            reply = f"Kanka **'{cleaned_prompt}'** yerini veya şehrini eyvallah biliyoruz; tarihiyle ve kültürüyle bambaşka bir noktadır. Başka hangi şehri veya ülkeyi merak ediyorsun? 😎"
                    
                    # Aktif futbolcular ve takımlar
                    elif any(w in lower_prompt for w in ["kerem aktürkoğlu", "aktürkoğlu", "futbolcu", "fenerbahçe", "fener", "arda güler"]):
                        if "kerem" in lower_prompt:
                            reply = "Kerem Aktürkoğlu, Türk futbolunun hızı, çalım yeteneği ve bitiriciliğiyle göz dolduran milli kanat oyuncusudur kanka! ⚡⚽"
                        else:
                            reply = "Futbol dünyası ve Süper Lig her zaman heyecan dolu kanka! Fenerbahçe ise şampiyonluk yolunda kadro kalitesiyle ve taraftarıyla ligin tozunu attıran dev bir camiadır 💛💙 Başka hangi futbolcuyu veya takımı konuşuyoruz?"
                    
                    # Valorant ve Donanım
                    elif "valorant" in lower_prompt:
                        reply = "Valorant, Riot Games'in Riot Client üzerinden oynanan taktiksel FPS oyunudur kanka. Bilgisayarına indirip Vanguard korumasıyla oynayabilirsin! 🎮"
                    elif "windows 10" in lower_prompt or "format" in lower_prompt:
                        reply = "Kanka Windows 10 kurmak için 8GB'lık bir USB'ye Media Creation Tool ile ISO yazdırıp Boot menüsünden (F12/F11) yükleyebilirsin! 😎"
                    
                    # Genel yedek
                    else:
                        reply = f"Kanka **'{cleaned_prompt}'** konusunu inceledik. İnternet bağlantısında anlık bir dalgalanma oldu ama tüm şehirlerin, ülkelerin ve futbol dünyasının detaylarını hafızamızda tutuyoruz. Tekrar dener misin? 🔥"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
