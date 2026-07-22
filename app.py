import streamlit as st
import urllib.request
import json
import urllib.parse

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye'nin web yapay zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Merhaba! Ben Lorvantis. Sana nasıl yardımcı olabilirim?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Lorvantis'e bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lorvantis düşünüyor..."):
            try:
                # Sınırsız ve her soruya cevap veren kararlı public yapay zeka uç noktası
                api_url = "https://text.pollinations.ai/"
                
                # Tüm sohbet geçmişini ve son soruyu akıllı beyne yolluyoruz
                payload = json.dumps({
                    "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    "model": "openai",
                    "jsonMode": False
                }).encode('utf-8')
                
                req = urllib.request.Request(
                    api_url, 
                    data=payload, 
                    headers={
                        'Content-Type': 'application/json', 
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                    }
                )
                
                with urllib.request.urlopen(req, timeout=30) as response:
                    reply = response.read().decode('utf-8').strip()
                    if not reply:
                        reply = "Kanka sunucu boş döndü, bir daha yazar mısın?"
            except Exception as e:
                # İnternet/Ağ dalgalanmasında sistemi kitlememek için akıllı yedek
                reply = f"Kanka anlık bir ağ yoğunluğu oldu ama buradayım! '{prompt}' konusuna devam edelim, ne sormak istiyorsun?"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
