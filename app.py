import streamlit as st
import urllib.request
import urllib.parse
import time

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye’nin Web YapayZekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Selam kanka ne aramıştın?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Lorvantis'e bir şeyler yaz..."):
    cleaned_prompt = prompt.strip()
    lower_prompt = cleaned_prompt.lower()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.status("Lorvantis cevabı bulana kadar inatla arıyor...", expanded=True) as status:
            reply = ""
            handled_locally = False

            # 1. Temel selamlaşmalar
            if lower_prompt in ["sa", "selam", "slm"]:
                reply = "Aleykümselam kanka, nasılsın?"
                handled_locally = True
            elif lower_prompt in ["as", "aleykümselam"]:
                reply = "Aleykümselam kanka, ne var ne yok?"
                handled_locally = True
            elif any(w in lower_prompt for w in ["nasılsın", "naber", "ne var ne yok"]):
                reply = "İyiyim kanka, sen nasılsın, ne bakmıştın?"
                handled_locally = True
            elif any(w in lower_prompt for w in ["sağol", "sagol", "teşekkürler", "teşekkür ederim", "eyvallah"]):
                reply = "Bir şey değil kanka!"
                handled_locally = True

            # 2. Asla pes etmeyen ve o sinir bozucu hazır kalıba asla düşmeyen, gerçek anlamda bulana kadar arayan inatçı motor
            if not handled_locally:
                success = False
                # Sınırsız sabır: Cevap gelene kadar binlerce kez ve uzun timeout süreleriyle dener
                attempt = 0
                while not success:
                    attempt += 1
                    status.update(label=f"Lorvantis webde arıyor... (Deneme: {attempt})", state="running")
                    try:
                        system_prefix = (
                            "Sen Lorvantisin. Türkiye'nin web destekli en inatçı ve gelişmiş yapay zekasısın. "
                            "Kullanıcının sorduğu sorunun (Can Uzun kimdir, Can Uzun güncel takımı vb.) cevabını internetten tam, güncel ve eksiksiz bulmadan asla durma. "
                            "Dünya ve Türkiye üzerindeki tüm futbol/spor takımlarını, futbolcuları (Can Uzun vb.), kulüp tarihlerini, kadrolarını, "
                            "tüm şehirleri, ilçeleri, plakaları, binaları, tarihi yapıları ve coğrafi özellikleri eksiksiz bilirsin. "
                            "Valorant sorulduğunda kesinlikle Windows 10 kurulumu anlatmazsın; sadece Valorant oyununu anlatırsın. "
                            "Kurulum veya rehber istendiğinde uzun uzun adım adım açıklarsın. "
                            "Kullanıcıya her zaman samimi, kanka diliyle, net ve doyurucu cevaplar verirsin. Soru: "
                        )
                        
                        full_query = system_prefix + cleaned_prompt
                        encoded_query = urllib.parse.quote(full_query)
                        
                        cache_buster = int(time.time() * 1000) + attempt
                        api_url = f"https://text.pollinations.ai/{encoded_query}?search=true&t={cache_buster}"
                        
                        req = urllib.request.Request(
                            api_url, 
                            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'},
                            method='GET'
                        )
                        
                        # İstek süresini uzatarak sunucunun yanıt vermesini sabırla bekliyoruz
                        with urllib.request.urlopen(req, timeout=25) as response:
                            if response.getcode() == 200:
                                data = response.read().decode('utf-8').strip()
                                # Gelen veri geçerliyse, hata kodu içermiyorsa ve anlamlı uzunluktaysa kabul ediyoruz
                                if data and "402" not in data and len(data) > 15 and "üzgünüm" not in data.lower():
                                    reply = data
                                    success = True
                                    break
                    except Exception:
                        time.sleep(1.0) # Sunucuyu yormadan ama asla vazgeçmeden kısa bir nefes alıp tekrar deniyor
                        continue

            status.update(label="Lorvantis cevabı buldu!", state="complete", expanded=False)

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
