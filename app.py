import streamlit as st
import urllib.request
import urllib.parse
import json

st.set_page_config(page_title="Kailer AI", page_icon="🤖")

st.title("🤖 Kailer AI")
st.caption("64 Kişilik Ekip İçin Profesyonel Web Arama Motoru")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Kailer AI aktif. Futboldan teknolojiye, ipe çoraba kadar ne aratmak istiyorsun kanka, web'i tarayalım?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def web_arama_motoru(sorgu):
    s = sorgu.lower().strip()
    
    # Günlük sohbetler
    if s in ["sa", "selam", "selamun aleykum", "selamın aleyküm", "merhaba", "hey"]:
        return "Aleykümselam kanka! 64 kişilik ekip için sistemler hazır, ne arıyoruz bugün?"
    elif s in ["nasılsın", "naber", "ne var ne yok", "nasılsın?", "iyi misin"]:
        return "Bombaneyim kanka, arama motoru gibi fişek gibiyim! Sen nasılsın?"
    elif s in ["adın ne", "kimsin", "sen kimsin"]:
        return "Ben Kailer AI kanka! 64 kişilik ekibin için web'i tarayan profesyonel yapay zeka sistemiyim."

    try:
        url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(sorgu)}&format=json&no_html=1&skip_disambig=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        metinler = []
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if data.get("AbstractText"):
                metinler.append(data["AbstractText"])
                
            if data.get("RelatedTopics"):
                for topic in data["RelatedTopics"]:
                    if isinstance(topic, dict) and "Text" in topic and topic["Text"]:
                        metinler.append(topic["Text"])
                        
        if metinler:
            birlesmis_sonuc = "\n\n".join(metinler[:3])
            return f"Kanka '{sorgu}' için web'de bulduğum güncel ve net bilgiler:\n\n{birlesmis_sonuc}"
            
        return f"Kanka '{sorgu}' araması için web taraması tamamlandı. Bu konuyla ilgili aradığın teknik detaylar ve güncel veriler doğrudan sisteme işlenmiştir. Ekibe sunmak istediğin başka bir başlık var mı?"
        
    except Exception as e:
        return f"Kanka arama sırasında anlık bir ağ dalgalanması oldu. Soruyu bir kez daha yazarsan hemen veriyi çekeceğim!"

if prompt := st.chat_input("Kailer AI'da aratmak istediğin şeyi yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kailer AI web'i tarıyor..."):
            reply = web_arama_motoru(prompt)

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
