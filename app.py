import streamlit as st
import urllib.request
import json
import time

st.set_page_config(page_title="Kailer AI", page_icon="🤖")

st.title("🤖 Kailer AI")
st.caption("Türkiye'nin akıllı web yapay zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Merhaba! Ben Kailer AI. Sana nasıl yardımcı olabilirim?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 1. BASİT SOHBETLERİ WEBDE ARAMASIN (Anında yerel cevap)
def hizli_cevap(prompt):
    p = prompt.lower().strip()
    if p in ["sa", "selam", "selamun aleykum", "selamın aleyküm", "merhaba", "hey"]:
        return "Aleykümselam kanka! Hoş geldin, ne yapıyoruz bugün?"
    elif p in ["nasılsın", "naber", "ne var ne yok", "nasılsın?", "iyi misin"]:
        return "Bombaneyim kanka, sistemler canavar gibi! Sen nasılsın?"
    elif p in ["adın ne", "kimsin", "sen kimsin"]:
        return "Ben Kailer AI kanka! Senin yarattığın, Türkiye'nin en sağlam yapay zekasıyım."
    return None

if prompt := st.chat_input("Kailer AI'a bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kailer AI düşünüyor..."):
            
            # Önce hızlı cevaplara baksın (API'ye gitmeden anında çözer)
            reply = hizli_cevap(prompt)
            
            # Eğer basit bir sohbet değilse, dışarıdaki zeki beyne sorsun
            if not reply:
                api_url = "https://text.pollinations.ai/"
                system_prompt = """Senin adın Kailer AI. Türkiye'nin yerli, en zeki ve samimi yapay zekasısın. Kullanıcıyla hep 'kanka' diliyle konuşursun.
                KURALLAR:
                1. Sorulan sorulara (oyun, spor, coğrafya, tarih, teknik vb.) en doğru, güncel ve net cevabı anında ver.
                2. Asla 'şunu araştırdım', 'internette arıyorum', 'konudan devam edelim' gibi gevezelikler yapma. Direkt cevabı patlat."""
                
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
                
                # 2. BAĞLANTI KOPARSA TEKRAR DENEME SİSTEMİ (3 Kez Dener)
                max_deneme = 3
                for deneme in range(max_deneme):
                    try:
                        # Timeout süresini kısalttık ki donup kalmasın, koparsa hemen tekrar denesin
                        with urllib.request.urlopen(req, timeout=10) as response:
                            cevap_metni = response.read().decode('utf-8').strip()
                            if cevap_metni:
                                reply = cevap_metni
                                break # Cevabı bulduğu an döngüden çıkar
                    except Exception as e:
                        if deneme < max_deneme - 1:
                            time.sleep(1) # 1 saniye bekleyip sunucuya tekrar saldırır
                            continue
                        else:
                            reply = "Kanka sunucu bağlantısı koptu, 3 kez zorladım ama bağlanamadım. Birkaç saniye sonra tekrar yazar mısın?"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
