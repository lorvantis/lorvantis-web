import streamlit as st
import json
import urllib.request

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("7/24 Aktif Web Yapay Zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Merhaba! Ben Lorvantis. Sana nasıl yardımcı olabilirim?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lorvantis düşünüyor..."):
            try:
                # Kesintisiz ve tamamen ücretsiz açık AI hattı
                url = "https://text.pollinations.ai/openai"
                
                payload = json.dumps({
                    "messages": st.session_state.messages,
                    "model": "mistral"
                }).encode("utf-8")
                
                headers = {
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0'
                }
                
                req = urllib.request.Request(url, data=payload, headers=headers)
                
                with urllib.request.urlopen(req) as response:
                    reply = response.read().decode('utf-8')
                
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                # Yedek Ücretsiz Servis (DuckDuckGo / DDG AI)
                try:
                    import urllib.parse
                    encoded_prompt = urllib.parse.quote(prompt)
                    backup_url = f"https://text.pollinations.ai/{encoded_prompt}"
                    req = urllib.request.Request(backup_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req) as response:
                        reply = response.read().decode('utf-8')
                    st.write(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                except Exception as ex:
                    st.error(f"Sistem meşgul, lütfen tekrar dene. Detay: {ex}")
