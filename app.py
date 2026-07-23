import streamlit as st
import urllib.request
import json

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye’nin web yapay zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Selam kanka! Model derdini de bitirdik, sahne bizim 😎 Dök içini 🔥"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Lorvantis'e bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lorvantis düşünüyor..."):
            try:
                api_url = "https://text.pollinations.ai/"
                
                system_prompt = """Senin adın Lorvantis. Türkiye'nin yerli, samimi, kanka dilli yapay zekasısın. 
                Asla robota bağlamazsın. Kullanıcı sana 'nasılsın' derse asla hata mesajı vermez, 'İyiyim kanka, sen nasılsın, ne kaynatıyoruz?' gibi samimi cevaplar verirsin. 
                Gerektiğinde kısa ve net, gerektiğinde uzun ve detaylı, bol bol emoji kullanarak konuşursun. Dünyadaki her şeyi (kodlama, oyun, spor, teknoloji) çok iyi bilirsin. Asla 'bilmiyorum' demezsin."""
                
                messages_payload = [{"role": "system", "content": system_prompt}]
                
                for m in st.session_state.messages[-10:]:
                    messages_payload.append({"role": m["role"], "content": m["content"]})
                
                # Model parametresini sildik, API kendi varsayılanını kullansın 404 yemesin:
                payload = json.dumps({
                    "messages": messages_payload,
                    "jsonMode": False
                }).encode('utf-8')
                
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
                        reply = "Kanka sunucu boş döndü bi secdeye varıp geliyim, tekrar yaz 😄"
            except Exception as e:
                reply = f"Olay mahalli karıştı kanka, API bi patlak verdi: {e} 💀 Ama sen dert etme, konuyu baştan alalım!"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
