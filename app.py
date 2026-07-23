import streamlit as st
import urllib.request
import urllib.parse

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye’nin web yapay zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Merhaba. Lorvantis aktif. Tüm Türkçe kelimeler, kısaltmalar, futbol, uzay ve oyunlar cebimde. Ne öğrenmek istiyorsun?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Lorvantis'e bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lorvantis inceliyor ve düşünüyor..."):
            try:
                # Türkçe kelimeleri, TDK kısaltmalarını ve genel kültürü eksiksiz bilen sistem talimatı:
                system_prefix = (
                    "Sen Lorvantisin. Türkiye'nin web yapay zekasısın. "
                    "Türkçedeki tüm resmi, kurumsal, günlük ve TDK kısaltmalarını, kelimelerin anlamlarını, "
                    "futbol tarihini, savaş tarihlerini, şehirleri ve oyunları eksiksiz bilirsin. "
                    "Kullanıcı sana bir kısaltma veya kelime sorduğunda (Örn: TCDD, vb., vs., TDK vb.) "
                    "açılımını, anlamını ve detayını kanka diliyle ama net bir şekilde açıklarsın. "
                    "Soru: "
                )
                
                full_query = system_prefix + prompt
                encoded_query = urllib.parse.quote(full_query)
                
                api_url = f"https://text.pollinations.ai/{encoded_query}?search=true"
                
                req = urllib.request.Request(
                    api_url, 
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                    },
                    method='GET'
                )
                
                with urllib.request.urlopen(req, timeout=30) as response:
                    reply = response.read().decode('utf-8').strip()
                    if not reply:
                        reply = "Sunucu boş döndü kanka, bir daha yazar mısın?"
            except Exception as e:
                reply = f"Hata yakalandı kanka: {e} 💀 Bağlantıda anlık bir sıkıntı oldu, tekrar deneyelim."

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
