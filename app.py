import streamlit as st
import requests
import time

st.set_page_config(page_title="Kailer AI", page_icon="🤖")

st.title("🤖 Kailer AI")
st.caption("Türkiye'nin akıllı web yapay zekası (Arama Motoru Modu)")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Merhaba! Ben Kailer AI. Neyi aramamı istersin kanka?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def hizli_cevap(prompt):
    p = prompt.lower().strip()
    if p in ["sa", "selam", "selamun aleykum", "selamın aleyküm", "merhaba", "hey"]:
        return "Aleykümselam kanka! Hoş geldin, ne arıyoruz bugün?"
    elif p in ["nasılsın", "naber", "ne var ne yok", "nasılsın?", "iyi misin"]:
        return "Bombaneyim kanka, arama motoru gibi fişek gibiyim! Sen nasılsın?"
    elif p in ["adın ne", "kimsin", "sen kimsin"]:
        return "Ben Kailer AI kanka! Senin yarattığın, Türkiye'nin en sağlam yapay zekasıyım."
    return None

if prompt := st.chat_input("Kailer AI'a bir şeyler yaz veya arat..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        # SENİN SEVDİĞİN YÜKLEME YAZISI (Aynen duruyor)
        with st.spinner("Kailer AI internetin altını üstüne getiriyor..."):
            
            reply = hizli_cevap(prompt)
            
            if not reply:
                api_url = "https://text.pollinations.ai/"
                
                # YENİ BEYİN TALİMATI: Yazım hatalarını anla, webde ara!
                system_prompt = """Senin adın Kailer AI. Kullanıcıyla 'kanka' diyerek samimi bir dille konuş. 
                Kullanıcı kelimeleri yanlış veya eksik yazsa bile (yazım hatası yapsa bile) ne demek istediğini anla. 
                Sanki dev bir arama motoruymuşsun gibi internetteki en güncel, doğru ve detaylı bilgiyi bulup efsanevi bir kalitede sun. Arama yaptığını belli etme."""
                
                gecmis = st.session_state.messages[-3:]
                messages_payload = [{"role": "system", "content": system_prompt}]
                for m in gecmis:
                    messages_payload.append({"role": m["role"], "content": m["content"]})
                
                basarili = False
                son_hata = ""
                
                # YENİ GÜÇLÜ MOTOR (requests) - 5 Kez Dener, Asla Pes Etmez
                for deneme in range(5):
                    try:
                        res = requests.post(
                            api_url,
                            json={"messages": messages_payload, "model": "openai"},
                            headers={'Content-Type': 'application/json'},
                            timeout=15
                        )
                        
                        if res.status_code == 200 and res.text:
                            reply = res.text.strip()
                            basarili = True
                            break 
                        else:
                            son_hata = f"Sunucu Hatası: {res.status_code}"
                            time.sleep(1.5)
                    except Exception as e:
                        son_hata = "Bağlantı Kesintisi"
                        time.sleep(1.5)
                        
                if not basarili:
                    # SENİN SEVDİĞİN HATA YAZISI (Gizli Hata Kodu ile)
                    reply = f"Kanka internetin derinliklerinde kayboldum, tam buluyordum ki koptu. (Gizli Hata: {son_hata})"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
