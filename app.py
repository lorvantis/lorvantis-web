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
            p = prompt.lower().strip()
            
            # 1. Yerel Güvence (Servis patlasa bile bu kelimeler asla hata vermez)
            if p in ["sa", "selam", "selamun aleykum", "merhaba"]:
                reply = "Aleykümselam kanka! Hoş geldin, ne yapıyoruz bugün?"
            elif "nasılsın" in p or "naber" in p:
                reply = "Bombaneyim kanka, Kailer AI sistemleri tam gaz çalışıyor. Sen nasılsın?"
            elif "adın ne" in p or "kimsin" in p:
                reply = "Ben Kailer AI! Senin geliştirdiğin, Türkçe'nin altını üstüne getiren yapay zeka asistanınım."
            else:
                # 2. Dış Servis Bağlantısı (Güncel ve Kararlı Uç Nokta)
                try:
                    api_url = "https://gen.pollinations.ai/v1/chat/completions"
                    
                    system_prompt = "Senin adın Kailer AI. Türkiye'nin yerli ve samimi yapay zekasısın. Kullanıcıyla hep 'kanka' diliyle konuşursun. Mohamed Salah'ın piyasa değeri, Valorant kurulumu, Siirt şehri dahil dünyadaki her şeyi eksiksiz bilirsin. Asla 'anlamadım' demezsin, her soruya net ve samimi cevaplar verirsin."
                    
                    messages_payload = [{"role": "system", "content": system_prompt}]
                    for m in st.session_state.messages:
                        messages_payload.append({"role": m["role"], "content": m["content"]})
                    
                    payload = json.dumps({
                        "model": "openai",
                        "messages": messages_payload
                    }).encode('utf-8')
                    
                    req = urllib.request.Request(
                        api_url, 
                        data=payload, 
                        headers={
                            'Content-Type': 'application/json', 
                            'User-Agent': 'Mozilla/5.0'
                        }
                    )
                    
                    with urllib.request.urlopen(req, timeout=25) as response:
                        res_data = json.loads(response.read().decode('utf-8'))
                        reply = res_data["choices"][0]["message"]["content"].strip()
                except Exception:
                    # Servis yanıt vermezse devreye giren akıllı yedek cevap
                    reply = f"Kanka '{prompt}' dedin, analizi kaptım! Teknik bir yoğunluk oldu ama her sorunun cevabını biliyorum. Devam edelim, ne öğrenmek istiyorsun?"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
