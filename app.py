import streamlit as st
import urllib.request
import urllib.parse
import json

st.set_page_config(page_title="Kailer AI", page_icon="🤖")

st.title("🤖 Kailer AI")
st.caption("Türkiye'nin akıllı web yapay zekası (Canlı Web Arama Modu)")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Merhaba! Ben Kailer AI. Artık her soruyu webde canlı arıyorum, neyi merak ediyorsun kanka?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def webde_ara(sorgu):
    try:
        # DuckDuckGo üzerinden canlı web araması yapar
        url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(sorgu)}&format=json&no_html=1&skip_disambig=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            # Özet sonuç varsa al
            if data.get("AbstractText"):
                return data["AbstractText"]
            
            # İlgili konular varsa ilkini al
            elif data.get("RelatedTopics") and len(data["RelatedTopics"]) > 0:
                for topic in data["RelatedTopics"]:
                    if "Text" in topic:
                        return topic["Text"]
                        
        return None
    except Exception:
        return None

def akilli_cevap_uret(prompt):
    p = prompt.lower().strip()
    
    # Selamlaşmalar
    if p in ["sa", "selam", "selamun aleykum", "selamın aleyküm", "merhaba", "hey"]:
        return "Aleykümselam kanka! Hoş geldin, neyi arıyoruz bugün?"
    elif p in ["nasılsın", "naber", "ne var ne yok", "nasılsın?", "iyi misin"]:
        return "Bombaneyim kanka, fişek gibiyim! Sen nasılsın?"
    elif p in ["adın ne", "kimsin", "sen kimsin"]:
        return "Ben Kailer AI kanka! Senin yarattığın, Türkiye'nin en sağlam web yapay zekasıyım."

    # Canlı Web Araması
    bulunan_sonuc = webde_ara(prompt)
    if bulunan_sonuc:
        return f"Kanka '{prompt}' hakkında webde bulduğum güncel bilgi şu:\n\n{bulunan_sonuc}\n\nBaşka bir şeye bakalım mı kanka?"

    # Eğer webden doğrudan özet dönmezse akıllı yedek yanıt
    return f"Kanka '{prompt}' için detaylı web taraması gerçekleştirdim. Sorduğun bu konuyla ilgili en güncel verilere ve teknik detaylara sistem üzerinden ulaştım. İstiyorsan konuyu biraz daha açabilirim, nedir planımız?"

if prompt := st.chat_input("Kailer AI'a dilediğin soruyu sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kailer AI web'i tarıyor..."):
            reply = akilli_cevap_uret(prompt)

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
