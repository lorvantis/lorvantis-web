if st.session_state.ready_image:
    user_display = f"🖼️ [Görsel] {prompt}"
    img_b64 = encode_image(st.session_state.ready_image)
    st.session_state.ready_image = None 
    
st.session_state.chats[st.session_state.current_chat].append({"role": "user", "content": user_display})
st.chat_message("user").write(user_display)

with st.chat_message("assistant"):
    with st.status("Lorvantis düşünüyor...", expanded=False) as status:
        reply = ""
        success = False
        last_error = ""
        
        contents = []
        chat_history = st.session_state.chats[st.session_state.current_chat]
        
        for m in chat_history[:-1]:
            # Google API standartlarında roller 'user' ve 'model' olmalıdır
            role = "user" if m["role"] == "user" else "model"
            clean_text = str(m["content"])
            if clean_text.startswith("🖼️ [Görsel] "):
                clean_text = clean_text.replace("🖼️ [Görsel] ", "", 1)
            
            contents.append({
                "role": role,
                "parts": [{"text": clean_text}]
            })
        
        current_parts = [{"text": prompt}]
        if img_b64:
            current_parts.append({
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": img_b64
                }
            })
        
        contents.append({
            "role": "user",
            "parts": current_parts
        })

        payload = {
            "system_instruction": {
                "parts": [{"text": "Sen Lorvantis'sin. Türkiye'nin samimi web yapay zekasısın. Kullanıcıya her zaman 'kanka' diye hitap et. Çok samimi, kafa dengi, detaylı, akıcı ve eğlenceli cevaplar ver. Arkandaki altyapı Google Gemini'dir. Hikaye istendiğinde harika hikayeler kurgula."}]
            },
            "contents": contents
        }
        headers = {'Content-Type': 'application/json'}
        
        for key in API_KEYS:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
                res = requests.post(url, headers=headers, data=json.dumps(payload), timeout=20)
                
                if res.status_code == 200:
                    data = res.json()
                    if "candidates" in data and len(data["candidates"]) > 0:
                        reply = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                        success = True
                        break 
                else:
                    last_error = res.text
            except Exception as e:
                last_error = str(e)
                continue 
        
        if not success:
            reply = f"Kanka API bağlantısında takıldık (Hata detayı: {last_error[:100]}). Anahtarları veya isteği kontrol edelim."
        
        status.update(label="Hazır!", state="complete", expanded=False)

    st.write(reply)
    st.session_state.chats[st.session_state.current_chat].append({"role": "assistant", "content": reply})
