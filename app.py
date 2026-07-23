import streamlit as st
import urllib.request
import urllib.parse
import json
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
        with st.status("Lorvantis webde köşe bucak arıyor...", expanded=True) as status:
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

            # 2. Asla pes etmeyen, yedek metne düşmeyen, OpenAI altyapılı gerçek arama motoru
            if not handled_locally:
                success = False
                attempt = 0
                
                while not success:
                    attempt += 1
                    status.update(label=f"Lorvantis arıyor... (Deneme: {attempt})", state="running")
                    
                    try:
                        system_prompt = (
                            "Sen Lorvantisin. Türkiye'nin web destekli en akıllı, inatçı ve güncel yapay zekasısın. "
                            "Kullanıcının sorduğu sorunun (Can Uzun kimdir, futbolcular, şehirler, takımlar vb.) cevabını internetten tam ve eksiksiz bul. "
                            "Asla hazır şablon veya yedek metin kullanma. Cevabı bulana kadar aratmaya devam et. "
                            "Kullanıcıya her zaman samimi, kanka diliyle, net, doyurucu ve doğrudan cevaplar ver."
                        )
                        
                        # Pollinations'ın OpenAI model uç noktasını kullanarak doğrudan web destekli gerçek yanıt alıyoruz
                        payload = {
                            "model": "openai",
                            "messages": [
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": cleaned_prompt}
                            ],
                            "jsonMode": False
                        }
                        
                        data_bytes = json.dumps(payload).encode('utf-8')
                        req = urllib.request.Request(
                            "https://text.pollinations.ai/",
                            data=data_bytes,
                            headers={
                                'Content-Type': 'application/json',
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                            },
                            method='POST'
                        )
                        
                        with urllib.request.urlopen(req, timeout=30) as response:
                            if response.getcode() == 200:
                                result_text = response.read().decode('utf-8').strip()
                                if result_text and len(result_text) > 5 and "402" not in result_text:
                                    reply = result_text
                                    success = True
                                    break
                    except Exception:
                        time.sleep(1.5)
                        continue

            status.update(label="Lorvantis cevabı buldu!", state="complete", expanded=False)

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
