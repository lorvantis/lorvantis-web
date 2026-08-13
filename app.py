import streamlit as st
import urllib.request
import urllib.parse
import json
import html

st.set_page_config(page_title="Kailer AI", page_icon="🤖")

st.title("🤖 Kailer AI")
st.caption("64 Kişilik Ekip İçin Profesyonel Toparlayıcı Arama Motoru")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Kailer AI aktif. Neyi merak ediyorsan yaz kanka, web'i tarayıp tertemiz önüne getireyim?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def duzgun_web_aramasi(sorgu):
    s = sorgu.lower().strip()
    
    # Sohbetler
    if s in ["sa", "selam", "selamun aleykum", "selamın aleyküm", "merhaba", "hey"]:
        return "Aleykümselam kanka! 64 kişilik ekip için sistemler tam gaz ayakta, ne arıyoruz?"
    elif s in ["nasılsın", "naber", "ne var ne yok", "nasılsın?", "iyi misin"]:
        return "Bombaneyim kanka, arama motoru gibi fişek gibiyim! Sen nasılsın?"
    elif s in ["adın ne", "kimsin", "sen kimsin"]:
        return "Ben Kailer AI kanka! Ekibin için web'i anlık tarayan ve bilgiyi derleyen profesyonel yapay zeka sistemiyim."

    try:
        # DuckDuckGo üzerinden arama
        url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(sorgu)}&format=json&no_html=1&skip_disambig=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        
        parcalar = []
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if data.get("AbstractText"):
                parcalar.append(html.unescape(data["AbstractText"]))
                
            if data.get("RelatedTopics"):
                for topic in data["RelatedTopics"]:
                    if isinstance(topic, dict) and "Text" in topic and topic["Text"]:
                        parcalar.append(html.unescape(topic["Text"]))
                        
        if parcalar:
            temiz_ozet = "\n\n".join(parcalar[:2])
            return f"Kanka aradığın konu için web'den derlediğim net bilgiler:\n\n{temiz_ozet}"
            
        # Wikipedia Destekli Canlı Arama ve Derleme
        wiki_url = f"https://tr.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(sorgu)}&format=json"
        wiki_req = urllib.request.Request(wiki_url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(wiki_req, timeout=10) as w_resp:
            w_data = json.loads(w_resp.read().decode('utf-8'))
            search_results = w_data.get("query", {}).get("search", [])
            
            if search_results:
                ilk_sonuc = search_results[0]
                baslik = ilk_sonuc.get("title", "")
                snippet = html.unescape(ilk_sonuc.get("snippet", "").replace('<span class="searchmatch">', '').replace('</span>', ''))
                return f"Kanka ulaştığım güncel kaynak özeti ({baslik}):\n\n{snippet}..."

        return "Kanka web taraması tamamlandı ancak anlamlı bir metin bloğu yakalanamadı. Kelimeyi biraz daha net yazarak tekrar deneyebilirsin!"

    except Exception as e:
        return "Kanka arama sırasında anlık bir ağ dalgalanması oldu. Soruyu bir kez daha gönderirsen hemen veriyi çekeceğim!"

if prompt := st.chat_input("Kailer AI'da aratmak istediğin şeyi yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kailer AI verileri topluyor..."):
            reply = duzgun_web_aramasi(prompt)

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
