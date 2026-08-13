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
        with st.spinner("Kailer AI internetin altını üstüne getiriyor..."):
            
            reply = hizli_cevap(prompt)
            
            if not reply:
                api_url = "https://text.pollinations.ai/"
                
                system_prompt = """Senin adın Kailer AI. Kullanıcıyla 'kanka' diyerek samimi bir dille konuş. 
                Kullanıcı kelimeleri yanlış veya eksik yazsa bile ne demek istediğini anla. 
                Sanki dev bir arama motoruymuşsun gibi internetteki en güncel ve doğru bilgiyi bulup efsanevi bir kalitede sun. Arama yaptığını belli etme."""
                
                gecmis = st.session_state.messages[-1:]
                messages_payload = [{"role": "system", "content": system_prompt}]
                for m in gecmis:
                    messages_payload.append({"role": m["role"], "content": m["content"]})
                
                payload = {
                    "messages": messages_payload,
                    "model": "openai"
                }
                
                basarili = False
                son_hata = ""
                bekleme_suresi = 2
                
                for deneme in range(3):
                    try:
                        res = requests.post(
                            api_url,
                            json=payload,
                            headers={'Content-Type': 'application/json'},
                            timeout=15
                        )
                        
                        if res.status_code == 200:
                            cevap_metni = res.text.strip()
                            if cevap_metni:
                                reply = cevap_metni
                                basarili = True
                                break
                            else:
                                son_hata = "Boş Yanıt"
                                time.sleep(1.5)
                        elif res.status_code == 429:
                            son_hata = "429 - Sunucu Darlanmış"
                            time.sleep(bekleme_suresi)
                            bekleme_suresi += 3
                        else:
                            son_hata = f"HTTP {res.status_code}"
                            time.sleep(2)
                            
                    except requests.exceptions.Timeout:
                        son_hata = "Zaman Aşımı"
                        time.sleep(1.5)
                    except requests.exceptions.ConnectionError:
                        son_hata = "Bağlantı Hatası"
                        time.sleep(1.5)
                    except Exception as e:
                        son_hata = "Beklenmeyen Hata"
                        time.sleep(1.5)
                        
                if not basarili:
                    reply = f"Kanka internetin derinliklerinde kayboldum, sunucu geçici olarak zorlandı. (Gizli Hata: {son_hata}). 5 saniye bekleyip aynı soruyu tekrar yazar mısın?"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
