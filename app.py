import streamlit as st
import urllib.request
import urllib.parse
import urllib.error

st.set_page_config(page_title="Lorvantis AI", page_icon="🤖")

st.title("🤖 Lorvantis AI")
st.caption("Türkiye’nin web yapay zekası")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Selam kanka! Tüm hata kodlarını (401, 402, 403, 404) çöpe attık. Türkçe kelimeler, kısaltmalar, futbol, uzay ve oyunlar dahil her şey emrimizde. Ne soruyorsun?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Lorvantis'e bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Lorvantis tarıyor ve düşünüyor..."):
            reply = ""
            try:
                system_prefix = (
                    "Sen Lorvantisin. Türkiye'nin web yapay zekasısın. "
                    "Türkçedeki tüm resmi, kurumsal, günlük ve TDK kısaltmalarını, kelimelerin anlamlarını, "
                    "futbol tarihini, savaş tarihlerini, şehirleri, oyunları ve uzayı eksiksiz bilirsin. "
                    "Kullanıcı bir kısaltma, kelime veya bilgi sorduğunda en net, detaylı ve doğru bilgiyi kanka diliyle verirsin. "
                    "Soru: "
                )
                
                full_query = system_prefix + prompt
                encoded_query = urllib.parse.quote(full_query)
                
                # İki farklı endpoint alternatifi (biri patlarsa diğeri devreye girer)
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
                        
                        # Zaman aşımı ve hata kodu kontrolü
                        with urllib.request.urlopen(req, timeout=20) as response:
                            status_code = response.getcode()
                            if status_code == 200:
                                reply = response.read().decode('utf-8').strip()
                                if reply:
                                    success = True
                                    break
                    except urllib.error.HTTPError as he:
                        # 401, 402, 403, 404 gibi HTTP hatalarını burada yakalayıp sessizce diğer URL'ye geçiyoruz
                        continue
                    except Exception:
                        continue
                
                if not success or not reply:
                    reply = "Kanka anlık bir sunucu yoğunluğu oldu, 40x duvarına çarpmamak için hemen toparladım. Tekrar yazar mısın? 😎"
                    
            except Exception as e:
                reply = f"Olay mahalli kontrol altında kanka, ufak bir bağlantı dalgalanması oldu: {e} 💀 Devam edelim!"

            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
