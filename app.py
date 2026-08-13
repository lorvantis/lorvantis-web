import streamlit as st
import urllib.request
import urllib.parse
import json
import html
import re

st.set_page_config(page_title="Kailer AI", page_icon="🤖")

st.title("🤖 Kailer AI")
st.caption("64 Kişilik Ekip İçin Net ve Temiz Bilgi Motoru")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Kailer AI aktif. Neyi merak ediyorsan yaz kanka, net bilgiyi çekip önüne koyayım?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def net_bilgi_getir(sorgu):
    s = sorgu.lower().strip()
    
    # Sohbetler
    if s in ["sa", "selam", "selamun aleykum", "selamın aleyküm", "merhaba", "hey"]:
        return "Aleykümselam kanka! Sistemler tam gaz ayakta, ne arıyoruz?"
    elif s in ["nasılsın", "naber", "ne var ne yok", "nasılsın?", "iyi misin"]:
        return "Bombaneyim kanka, fişek gibiyim! Sen nasılsın?"
    elif s in ["adın ne", "kimsin", "sen kimsin"]:
        return "Ben Kailer AI kanka! Ekibin için web'i anlık tarayan ve bilgiyi tertemiz derleyen sistemiyim."

    try:
        # Doğrudan Türkçe Wikipedia Özet (Summary) API'si - Çöp metinleri ve tarihleri asla almaz
        wiki_api_url = f"https://tr.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(sorgu)}"
        req = urllib.request.Request(wiki_api_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get("type") != "disambiguation" and data.get("extract"):
                baslik = data.get("title", "Bilgi")
                ozet = data.get("extract")
                return f"**{baslik}**\n\n{ozet}"
                
        # Alternatif Wikipedia Arama ve Temizleme
        search_url = f"https://tr.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(sorgu)}&format=json"
        s_req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(s_req, timeout=10) as s_resp:
            s_data = json.loads(s_resp.read().decode('utf-8'))
            results = s_data.get("query", {}).get("search", [])
            
            if results:
                ilk = results[0]
                baslik = ilk.get("title", "")
                snippet = ilk.get("snippet", "")
                # HTML etiketlerini ve çöp kalıntıları temizle
                temiz_snippet = re.sub('<.*?>', '', snippet)
                temiz_snippet = re.sub(r'Erişim tarihi:.*', '', temiz_snippet)
                return f"**{baslik}**\n\n{temiz_snippet.strip()}..."

        return "Kanka aradığın kelime için net bir kaynak bulunamadı. Lütfen kelimeyi tam yazarak tekrar dene!"

    except Exception as e:
        return "Kanka arama sırasında anlık bir ağ dalgalanması oldu. Soruyu bir kez daha gönderirsen hemen hallederim!"

if prompt := st.chat_input("Kailer AI'da aratmak istediğin şeyi yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kailer AI bilgiyi topluyor..."):
            reply = net_bilgi_getir(prompt)

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
