import streamlit as st
import urllib.request
import urllib.parse
import json
import html
import re

st.set_page_config(page_title="Kailer AI", page_icon="🤖")

st.title("🤖 Kailer AI")
st.caption("64 Kişilik Ekip İçin Gerçek Zamanlı Web Motoru")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Kailer AI aktif kanka! Sistemler tam gaz ayakta, ne aratmak istiyorsun?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def gercek_web_aramasi(sorgu):
    s = sorgu.lower().strip()
    
    # Sohbetler
    if s in ["sa", "selam", "selamun aleykum", "selamın aleyküm", "merhaba", "hey"]:
        return "Aleykümselam kanka! Sistemler bomba gibi, ne arıyoruz?"
    elif s in ["nasılsın", "naber", "ne var ne yok", "nasılsın?", "iyi misin"]:
        return "Bombaneyim kanka, fişek gibiyim! Sen nasılsın?"
    elif s in ["adın ne", "kimsin", "sen kimsin"]:
        return "Ben Kailer AI kanka! Ekibin için web'i anlık tarayan gerçek zamanlı arama sistemiyim."

    # 1. Yöntem: Wikipedia Türkçe Özet API'si
    try:
        wiki_url = f"https://tr.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(sorgu)}"
        req = urllib.request.Request(wiki_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get("type") != "disambiguation" and data.get("extract"):
                baslik = data.get("title", sorgu)
                ozet = data.get("extract")
                return f"**{baslik}**\n\n{ozet}"
    except Exception:
        pass

    # 2. Yöntem: Wikipedia Arama Sorgusu (Fallback)
    try:
        search_url = f"https://tr.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(sorgu)}&format=json"
        s_req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(s_req, timeout=5) as s_resp:
            s_data = json.loads(s_resp.read().decode('utf-8'))
            results = s_data.get("query", {}).get("search", [])
            if results:
                ilk = results[0]
                baslik = ilk.get("title", "")
                snippet = ilk.get("snippet", "")
                temiz_snippet = re.sub('<.*?>', '', snippet)
                temiz_snippet = re.sub(r'Erişim tarihi:.*', '', temiz_snippet)
                return f"**{baslik}**\n\n{temiz_snippet.strip()}..."
    except Exception:
        pass

    # 3. Yöntem: DuckDuckGo HTML Arama Taraması
    try:
        ddg_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(sorgu)}"
        ddg_req = urllib.request.Request(ddg_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(ddg_req, timeout=5) as d_resp:
            html_icerik = d_resp.read().decode('utf-8', errors='ignore')
            # Snippet sınıfına ait metinleri çek
            snippets = re.findall(r'class="result__snippet[^"]*">([^<]+)<', html_icerik)
            if snippets:
                derlenmis = "\n\n".join([html.unescape(snip.strip()) for snip in snippets[:2]])
                return f"**{sorgu.capitalize()} için Web Sonuçları:**\n\n{derlenmis}"
    except Exception:
        pass

    return f"Kanka '{sorgu}' için web'de net bir sonuç eşleşmedi. Kelimeyi biraz daha farklı yazarak tekrar deneyebilirsin!"

if prompt := st.chat_input("Kailer AI'da aratmak istediğin şeyi yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kailer AI web'i tarıyor..."):
            reply = gercek_web_aramasi(prompt)

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
