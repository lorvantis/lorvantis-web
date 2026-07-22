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
                api_url = "https://text.pollinations.ai/"
                
                system_prompt = """Senin adın Lorvantis. Türkiye'nin yerli ve samimi yapay zekasısın. Kullanıcıyla hep 'kanka' diliyle konuşursun. 
                KESİN KURAL: Kullanıcı sana 'sa', 'selam', 'selamun aleykum' veya türevi bir selamlaşma yazarsa, kesinlikle başka bir şey sormadan direkt 'Aleykümselam kanka! Hoş geldin, ne yapıyoruz bugün?' diye selamını alırsın. 
                Bunun dışında Mohamed Salah'ın piyasa değeri, Valorant kurulumu, Siirt şehri dahil dünyadaki her şeyi (spor, oyun, coğrafya, kodlama) eksiksiz bilirsin. Asla 'bilmiyorum' demezsin."""
                
                messages_payload = [{"role": "system", "content": system_prompt}]
                
                # Geçmişin sadece son 10 mesajını alalım ki kafa karışmasın
                for m in st.session_state.messages[-10:]:
                    messages_payload.append({"role": m["role"], "content": m["content"]})
                
                payload = json.dumps({
                    "messages": messages_payload,
                    "model": "openai",
                    "jsonMode": False
                }).encode('utf-8')
                
                # BURASI ÖNEMLİ: method='POST' ekledik ki istek reddedilmesin!
                req = urllib.request.Request(
                    api_url, 
                    data=payload, 
                    headers={
                        'Content-Type': 'application/json', 
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                    },
                    method='POST'
                )
                
                with urllib.request.urlopen(req, timeout=30) as response:
                    reply = response.read().decode('utf-8').strip()
                    if not reply:
                        reply = "Kanka sunucu anlık boş döndü, bir daha yazar mısın?"
            except Exception as e:
                # Hatanın ne olduğunu görmek için konsola da basalım
                print(f"Hata detayı: {e}")
                reply = f"Kanka anlık bir ağ yoğunluğu oldu ama buradayım! '{prompt}' konusuna devam edelim, ne öğrenmek istiyorsun?"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
