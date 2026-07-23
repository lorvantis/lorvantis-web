import streamlit as st
import urllib.request
import json

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye’nin web yapay zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Merhaba. Lorvantis aktif. Futboldan uzaya, tarihten oyunlara kadar tüm verilerle buradayım. Ne öğrenmek istiyorsun?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Lorvantis'e bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lorvantis düşünüyor..."):
            try:
                api_url = "https://text.pollinations.ai/?search=true"
                
                system_prompt = """Senin adın Lorvantis. Türkiye'nin web yapay zekasısın. 
                Kullanıcıyla 'kanka' diliyle konuşursun ancak bilgide asla taviz vermezsin. 
                Futbol tarihi, savaş tarihi, dünya şehirleri, ülkeler, uzay bilimi ve video oyunları dahil olmak üzere web üzerindeki tüm bilgilere hakimsin. 
                Kullanıcı bir şey sorduğunda en doğru, güncel ve detaylı bilgiyi verirsin. Asla 'bilmiyorum' demezsin."""
                
                messages_payload = [{"role": "system", "content": system_prompt}]
                
                for m in st.session_state.messages[-10:]:
                    messages_payload.append({"role": m["role"], "content": m["content"]})
                
                # 402 ücret duvarına takılmamak için modeli 'sur' yaptık (tamamen ücretsiz)
                payload = json.dumps({
                    "messages": messages_payload,
                    "model": "sur",
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
                        reply = "Sunucu boş döndü kanka, bir daha yazar mısın?"
            except Exception as e:
                reply = f"Hata yakalandı kanka: {e} 💀 402 duvarını delmek için başka alternatiflere bakarız."

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
