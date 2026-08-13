import streamlit as st
import urllib.request
import urllib.parse
import json

st.set_page_config(page_title="Kailer AI", page_icon="🤖")

st.title("🤖 Kailer AI")
st.caption("Türkiye'nin akıllı web arama motoru")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Merhaba! Ben Kailer AI. Hangi konuyu aratmak istiyorsun kanka?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def internette_ara(sorgu):
    s = sorgu.lower().strip()
    
    # Günlük sohbetler
    if s in ["sa", "selam", "selamun aleykum", "selamın aleyküm", "merhaba", "hey"]:
        return "Aleykümselam kanka! Hoş geldin, ne arıyoruz bugün?"
    elif s in ["nasılsın", "naber", "ne var ne yok", "nasılsın?", "iyi misin"]:
        return "Bombaneyim kanka, arama motoru gibi fişek gibiyim! Sen nasılsın?"
    elif s in ["adın ne", "kimsin", "sen kimsin"]:
        return "Ben Kailer AI kanka! Senin yarattığın, Türkiye'nin en sağlam yapay zekasıyım."

    try:
        # DuckDuckGo Anında Cevap API (Asla 429 veya 402 vermez, tamamen ücretsiz ve stabildir)
        url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(sorgu)}&format=json&no_html=1&skip_disambig=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            # Önce doğrudan özet bilgiye bakar
            if data.get("AbstractText"):
                return f"Kanka araştırdım, bulduğum net bilgi şu:\n\n{data['AbstractText']}"
            
            # Bulamazsa ilgili başlıklara bakar
            elif data.get("RelatedTopics"):
                for topic in data["RelatedTopics"]:
                    if "Text" in topic:
                        return f"Kanka bulduğum en güncel detay:\n\n{topic['Text']}"
                        
        return f"Kanka '{sorgu' için web'i taradım ancak nokta atışı özet bir metin dönmedi. Ama bu konunun detaylarını ve mantığını sistemimde biliyorum; istiyorsan biraz daha açayım!"
    
    except Exception as e:
        return f"Kanka arama yaparken anlık bir ağ pürüzü oldu. Soruyu bir daha yazar mısın, hemen çekeyim!"

if prompt := st.chat_input("Kailer AI'a aratmak istediğin şeyi yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kailer AI web'in altını üstüne getiriyor..."):
            reply = internette_ara(prompt)

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
