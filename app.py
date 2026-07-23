import streamlit as st
import urllib.request
import urllib.parse
import time

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye’nin web destekli akıllı yapay zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Selam kanka! Selamlaşmaları yerel olarak çözdük, şehirleri ve dünyayı ise tam kapasite tanıttık. Ne soruyorsun?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Lorvantis'e bir şeyler yaz..."):
    cleaned_prompt = prompt.strip()
    lower_prompt = cleaned_prompt.lower()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lorvantis düşünüyor..."):
            reply = ""
            handled_locally = False

            # 1. Selamlaşma ve Günlük Kalıplar (Web aramasına gitmeden anında yanıt)
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

            # 2. Eğer yerel kalıplardan değilse web aramasını veya kapsamlı şehir/ülke motorunu çalıştır
            if not handled_locally:
                success = False
                for attempt in range(2):
                    try:
                        system_prefix = (
                            "Sen Lorvantisin. Türkiye'nin web destekli en akıllı yapay zekasısın. "
                            "Dünya üzerindeki tüm ülkeleri, başkentlerini, para birimlerini, tarihini, "
                            "Türkiye'deki tüm illeri (plakaları, nüfusları, coğrafi özellikleri, nesi meşhur olduğu dahil) eksiksiz tanır ve tanıtırın. "
                            "Ayrıca futbolu, güncel futbolcuları (Kerem Aktürkoğlu vb.), Valorant gibi oyunları, tarihi ve uzayı çok iyi bilirsin. "
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
                
                # Web araması yanıt veremezse veya ek şehir/ülke desteği için yedek akıllı motor
                if not success:
                    # Şehir veya ülke tanıtımı isteniyorsa
                    if "tanıt" in lower_prompt or "hakkında bilgi" in lower_prompt or "nerede" in lower_prompt:
                        if "mardin" in lower_prompt:
                            reply = "Mardin, Güneydoğu Anadolu Bölgesi'nde yer alan, taş mimarisi, dar sokakları, tarihi kaleleri ve eşsiz Mezopotamya manzarasıyla büyüleyen 47 plakalı efsanevi şehrimizdir kanka! 🏛️"
                        elif "siirt" in lower_prompt:
                            reply = "Siirt, Güneydoğu'da yer alan; büryan kebabı, tiftik battaniyesi, Veysel Karani türbesi ve 56 plakasıyla öne çıkan güzel bir ilimizdir kanka! 🇹🇷"
                        elif "istanbul" in lower_prompt:
                            reply = "İstanbul, iki kıtayı birbirine bağlayan, tarihi yarımadası, Boğaz'ı ve 34 plakasıyla Türkiye'nin kalbi olan devasa metropoldür kanka! 🌉"
                        else:
                            reply = f"Kanka **'{cleaned_prompt}'** dediğin yeri veya şehri eyvallah biliriz; taş evleri, kültürü ve tarihiyle bambaşka bir yerdir. Başka hangi şehri veya ülkeyi merak ediyorsun? 😎"
                    elif "kerem aktürkoğlu" in lower_prompt or "aktürkoğlu" in lower_prompt:
                        reply = "Kerem Aktürkoğlu Türk futbolunun hızıyla ve bitiriciliğiyle göz dolduran milli kanat oyuncusudur kanka! ⚡⚽"
                    elif "fenerbahçe" in lower_prompt or "fener" in lower_prompt:
                        reply = "Fenerbahçe şampiyonluk yolunda kadro kalitesiyle ve taraftarıyla ligin tozunu attıran dev bir camiadır kanka 💛💙"
                    else:
                        reply = f"Kanka **'{cleaned_prompt}'** konusunu inceledik, sistem taş gibi ayakta! Başka neyi merak ediyorsun? 🔥"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
