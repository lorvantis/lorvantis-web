import streamlit as st
import urllib.request
import urllib.parse
import time

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye’nin web yapay zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Selam kanka! Fener'in piyasa değerinden tut uzaya kadar her şeyi webden çekmeye hazırım. Ne soruyorsun?"}]

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
        with st.spinner("Lorvantis webde aratıyor..."):
            reply = ""
            try:
                system_prefix = (
                    "Sen Lorvantisin. Türkiye'宁 web yapay zekasısın. "
                    "Türkçedeki tüm resmi, kurumsal, günlük ve TDK kısaltmalarını, kelimelerin anlamlarını, "
                    "futbol tarihini, kulüplerin güncel piyasa değerlerini, kadrolarını, savaş tarihlerini, şehirleri, oyunları ve uzayı eksiksiz bilirsin. "
                    "Kullanıcı bir şey sorduğunda web araması yaparak güncel ve net bilgiyi kanka diliyle verirsin. "
                    "Soru: "
                )
                
                full_query = system_prefix + full_user_input
                encoded_query = urllib.parse.quote(full_query)
                
                cache_buster = int(time.time() * 1000)
                api_url = f"https://text.pollinations.ai/{encoded_query}?search=true&t={cache_buster}"
                
                req = urllib.request.Request(
                    api_url, 
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                    },
                    method='GET'
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
