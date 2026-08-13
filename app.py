import streamlit as st
import urllib.request
import urllib.parse
import time

st.set_page_config(page_title="Kailer AI", page_icon="🤖")

st.title("🤖 Kailer AI")
st.caption("Türkiye'nin akıllı web yapay zekası (Arama Motoru Modu)")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Merhaba! Ben Kailer AI. Neyi aramamı istersin kanka?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 1. BASİT SOHBETLERİ WEBDE ARAMASIN (Anında yerel cevap)
def hizli_cevap(prompt):
    p = prompt.lower().strip()
    if p in ["sa", "selam", "selamun aleykum", "selamın aleyküm", "merhaba", "hey"]:
        return "Aleykümselam kanka! Hoş geldin, ne arıyoruz bugün?"
    elif p in ["nasılsın", "naber", "ne var ne yok", "nasılsın?", "iyi misin"]:
        return "Bombaneyim kanka, arama motoru gibi fişek gibiyim! Sen nasılsın?"
    elif p in ["adın ne", "kimsin", "sen kimsin"]:
        return "Ben Kailer AI kanka! Senin yarattığın, Türkiye'nin en sağlam yapay zekasıyım."
    return None

if prompt := st.chat_input("Kailer AI'a bir şeyler yaz veya arat..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kailer AI internetin altını üstüne getiriyor..."):
            
            # Önce hızlı cevaplara baksın
            reply = hizli_cevap(prompt)
            
            if not reply:
                # 2. ARAMA MOTORU MANTIĞI VE İNATÇI DÖNGÜ
                # Soruyu en hızlı şekilde aramak için URL formatına çeviriyoruz
                talimat = f"Sen Kailer AI'sın. Kullanıcıya 'kanka' diye hitap et. Arama yaptığını veya sunucuya bağlandığını asla söyleme, sadece cevabı net ve doğru bir şekilde ver. Soru şu: {prompt}"
                safe_prompt = urllib.parse.quote(talimat)
                api_url = f"https://text.pollinations.ai/{safe_prompt}"
                
                basarili = False
                # 10 kez deneyecek, cevabı alana kadar bırakmayacak (Kullanıcıya hata göstermez)
                for deneme in range(10):
                    try:
                        req = urllib.request.Request(
                            api_url, 
                            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                        )
                        # Timeout 15 saniye - beklemeye toleranslı
                        with urllib.request.urlopen(req, timeout=15) as response:
                            cevap_metni = response.read().decode('utf-8').strip()
                            if cevap_metni:
                                reply = cevap_metni
                                basarili = True
                                break # Cevabı bulduğu an döngüden çıkar ve cevabı verir!
                    except Exception:
                        time.sleep(2) # Koparsa 2 saniye nefes alıp tekrar saldırır
                        continue
                        
                # 10 denemede bile sunucu tamamen çökmüşse (çok nadir)
                if not basarili:
                    reply = "Kanka internetin derinliklerinde kayboldum, tam buluyordum ki koptu. Aynı soruyu bir daha yapıştırsana!"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
