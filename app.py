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
        # SENİN SEVDİĞİN YÜKLEME YAZISI (Dokunmadık!)
        with st.spinner("Kailer AI internetin altını üstüne getiriyor..."):
            
            reply = hizli_cevap(prompt)
            
            if not reply:
                # 2. ARAMA MOTORU MANTIĞI (CEVAPLARI ŞAHLANDIRDIK)
                # Artık cevapların çok daha kaliteli, doyurucu ve efsane olması için talimatı güçlendirdik!
                talimat = f"Senin adın Kailer AI. Kullanıcıyla 'kanka' diyerek samimi bir dille konuş. Verdiğin cevaplar asla kısa, basit veya sıkıcı olmasın; çok detaylı, zekice, nokta atışı ve efsanevi kalitede olsun. Kullanıcının sorusuna en doyurucu bilgiyi sun. Arama yaptığını belli etme. Soru şu: {prompt}"
                
                safe_prompt = urllib.parse.quote(talimat)
                api_url = f"https://text.pollinations.ai/{safe_prompt}"
                
                basarili = False
                for deneme in range(10):
                    try:
                        req = urllib.request.Request(
                            api_url, 
                            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                        )
                        with urllib.request.urlopen(req, timeout=15) as response:
                            cevap_metni = response.read().decode('utf-8').strip()
                            if cevap_metni:
                                reply = cevap_metni
                                basarili = True
                                break 
                    except Exception:
                        time.sleep(2) 
                        continue
                        
                if not basarili:
                    # SENİN SEVDİĞİN HATA YAZISI (Dokunmadık!)
                    reply = "Kanka internetin derinliklerinde kayboldum, tam buluyordum ki koptu. Aynı soruyu bir daha yapıştırsana!"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
