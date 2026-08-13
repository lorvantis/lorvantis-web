import streamlit as st
import urllib.request
import json

st.set_page_config(page_title="Kailer AI", page_icon="🤖")

st.title("🤖 Kailer AI")
st.caption("Türkiye'nin akıllı web yapay zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Merhaba! Ben Kailer AI. Sana nasıl yardımcı olabilirim?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Kailer AI'a bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kailer AI düşünüyor..."):
            try:
                api_url = "https://text.pollinations.ai/"
                
                # Kesin ve net talimat seti (Gevezece laflar yasaklandı)
                system_prompt = """Senin adın Kailer AI. Türkiye'nin yerli, en zeki ve samimi yapay zekasısın. Kullanıcıyla hep 'kanka' diliyle konuşursun.
                
                KURALLAR:
                1. Kullanıcı sana 'sa', 'selam', 'selamun aleykum' veya türevi bir şey yazarsa, kesinlikle başka hiçbir şey söylemeden sadece ve sadece: 'Aleykümselam kanka! Ne yapıyoruz bugün?' de. Asla 'ne öğrenmek istiyorsun' gibi sıkıcı sorular sorma.
                2. Kullanıcı bir soru sorduğunda (oyun, spor, coğrafya, tarih, teknik vb.), arkada derinlemesine araştırma yapıp en doğru, güncel ve net cevabı anında ver. 
                3. Asla 'şunu araştırdım', 'konudan devam edelim', 'ilk adımı nereye atalım' gibi yapay zeka gevezelikleri veya kaçamak cevaplar yapma. Direkt konunun net cevabını patlat."""
                
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
