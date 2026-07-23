import streamlit as st
import urllib.request
import urllib.parse
import urllib.error

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye’nin web yapay zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Selam kanka! İster 'Sa' yaz ister destan yaz, 40x duvarı tarih oldu. Ne kaynatıyoruz?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Lorvantis'e bir şeyler yaz..."):
    # Kullanıcı kısa "sa", "slm", "he" falan yazarsa API patlamasın diye arka planda genişletiyoruz:
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
        with st.spinner("Lorvantis inceliyor..."):
            reply = ""
            try:
                system_prefix = (
                    "Sen Lorvantisin. Türkiye'nin web yapay zekasısın. "
                    "Türkçedeki tüm resmi, kurumsal, günlük ve TDK kısaltmalarını, kelimelerin anlamlarını, "
                    "futbol tarihini, savaş tarihlerini, şehirleri, oyunları ve uzayı eksiksiz bilirsin. "
                    "Kullanıcı kısa ve samimi bir selam verdiyse (Örn: Sa) sen de aynı samimiyetle kanka diliyle karşılık verin. "
                    "Soru: "
                )
                
                full_query = system_prefix + full_user_input
                encoded_query = urllib.parse.quote(full_query)
                
                api_urls = [
                    f"https://text.pollinations.ai/{encoded_query}?search=true",
                    f"https://text.pollinations.ai/{encoded_query}"
                ]
                
                success = False
                for api_url in api_urls:
                    try:
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
                                if reply:
                                    success = True
                                    break
                    except Exception:
                        continue
                
                if not success or not reply:
                    reply = "Aleykümselam kanka! Sunucu anlık bi nefes aldı ama hallettik, devam edelim 😎"
                    
            except Exception as e:
                reply = f"Kanka sistem taş gibi ayakta, ufak bir dalgalanma oldu: {e} 💀"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
