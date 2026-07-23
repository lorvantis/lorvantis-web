import streamlit as st
import urllib.request
import urllib.parse
import json
import random

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye’nin web yapay zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Selam kanka! Artık her soruya tek tip değil, taptaze ve farklı cevaplarla akıyoruz. Ne kaynatıyoruz?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Lorvantis'e bir şeyler yaz..."):
    cleaned_prompt = prompt.strip()
    if cleaned_prompt.lower() in ["sa", "selam", "slm"]:
        full_user_input = "Selamün aleyküm kanka, nasılsın?"
    elif cleaned_prompt.lower() in ["as", "aleykümselam"]:
        full_user_input = "Aleykümselam kanka, ne var ne yok?"
    else:
        full_user_input = cleaned_prompt

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lorvantis düşünüyor..."):
            reply = ""
            try:
                system_prompt = (
                    "Sen Lorvantisin. Türkiye'nin web yapay zekasısın. "
                    "Türkçedeki tüm resmi, kurumsal, günlük ve TDK kısaltmalarını, kelimelerin anlamlarını, "
                    "futbol tarihini, savaş tarihlerini, şehirleri, oyunları ve uzayı eksiksiz bilirsin. "
                    "Asla aynı kalıp cümleleri tekrarlama, her defasında yaratıcı, farklı ve kanka diline uygun özgün cevaplar ver."
                )
                
                messages_payload = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": full_user_input}
                ]
                
                # Modelin hep aynı cevabı vermesini engellemek için rastgele seed (tohum) ekliyoruz:
                payload = json.dumps({
                    "messages": messages_payload,
                    "seed": random.randint(1, 1000000),
                    "jsonMode": False
                }).encode('utf-8')
                
                api_url = "https://text.pollinations.ai/?search=true"
                
                req = urllib.request.Request(
                    api_url, 
                    data=payload,
                    headers={
                        'Content-Type': 'application/json',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                    },
                    method='POST'
                )
                
                with urllib.request.urlopen(req, timeout=20) as response:
                    if response.getcode() == 200:
                        reply = response.read().decode('utf-8').strip()
                
                if not reply:
                    reply = "Aleykümselam kanka! Sunucu anlık bi nefes aldı ama hallettik, devam edelim 😎"
                    
            except Exception as e:
                reply = f"Kanka sistem taş gibi ayakta, ufak bir dalgalanma oldu: {e} 💀"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
