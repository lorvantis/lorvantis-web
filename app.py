import streamlit as st
import urllib.request
import json

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye'nin akıllı web yapay zekası")

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
                # Sınırsız ve her şeyi bilen küresel yapay zeka uç noktası
                api_url = "https://text.pollinations.ai/"
                
                # Lorvantis'in karakterini ve her konuyu bileceğini sisteme talimat olarak veriyoruz
                system_prompt = "Senin adın Lorvantis. Türkiye'nin yerli ve samimi yapay zekasısın. Kullanıcıyla 'kanka' diliyle konuşursun. Mohamed Salah'ın piyasa değeri, Valorant kurulumu, Siirt şehri dahil olmak üzere dünyadaki her konuda (spor, oyun, coğrafya, kodlama, tarih) tam, net ve güncel bilgiler bilirsin. Hiçbir zaman 'bilmiyorum' demezsin, her soruya eksiksiz ve özgün cevaplar verirsin."
                
                messages_payload = [{"role": "system", "content": system_prompt}]
                for m in st.session_state.messages:
                    messages_payload.append({"role": m["role"], "content": m["content"]})
                
                payload = json.dumps({
                    "messages": messages_payload,
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
                        reply = "Kanka sunucu anlık boş döndü, bir daha yazar mısın?"
            except Exception as e:
                reply = f"Kanka anlık bir ağ yoğunluğu oldu ama buradayım! '{prompt}' konusuna devam edelim, ne öğrenmek istiyorsun?"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
