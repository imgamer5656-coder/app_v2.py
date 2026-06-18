import streamlit as st
from groq import Groq

# ==========================================
# PAGE CONFIG & PREMIUM DARK THEME
# ==========================================
st.set_page_config(
    page_title="Peak AI Pro",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced Audio Theme Tuning
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0d1117;
        font-family: 'Inter', sans-serif;
        color: #c9d1d9;
    }
    
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .module-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    
    .module-title {
        color: #58a6ff;
        font-size: 1.15rem;
        font-weight: 600;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .main-title {
        text-align: center;
        font-weight: 700;
        color: #f0f6fc;
        margin-top: -40px;
        margin-bottom: 5px;
        font-size: 2.2rem;
    }
    .main-subtitle {
        text-align: center;
        color: #8b949e;
        font-size: 0.95rem;
        margin-bottom: 30px;
    }
    
    /* Neon Status Indicator for Voice */
    .voice-badge {
        background-color: #1f293d;
        border: 1px solid #388bfd;
        color: #58a6ff;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 10px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# JAVASCRIPT NATIVE TTS ENGINE INJECTION
# ==========================================
def trigger_voice_engine(text_to_speak, lang_code, voice_gender, rate=1.0):
    # Escape single/double quotes safely for JS execution
    safe_text = text_to_speak.replace("'", "\\'").replace('"', '\\"').replace("\n", " ")
    
    js_script = f"""
    <script>
        var msg = new SpeechSynthesisUtterance();
        msg.text = "{safe_text}";
        msg.lang = "{lang_code}";
        msg.rate = {rate};
        
        // Fetch all available system voices
        var voices = window.speechSynthesis.getVoices();
        
        // Logic to filter best premium matches for Male/Female in Urdu/English
        for(var i = 0; i < voices.length; i++) {{
            if(voices[i].lang.includes("{lang_code}")) {{
                if("{voice_gender}" === "Female" && (voices[i].name.includes("Zira") || voices[i].name.includes("Female") || voices[i].name.includes("Google") || voices[i].name.includes("Natural"))) {{
                    msg.voice = voices[i];
                    break;
                }} else if("{voice_gender}" === "Male" && (voices[i].name.includes("David") || voices[i].name.includes("Male") || voices[i].name.includes("Ravi"))) {{
                    msg.voice = voices[i];
                    break;
                }}
            }}
        }}
        window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_script, height=0, width=0)

# ==========================================
# GROQ API SETUP
# ==========================================
try:
    client = Groq(api_key=st.secrets["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"])
except Exception:
    # ⚠️ LOCAL TESTING: Paste your real gsk_... key here
    client = Groq(api_key="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") 

# ==========================================
# SESSION STATE & SIDEBAR ROOMS
# ==========================================
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {"Chat 1": [{"role": "system", "content": "You are Peak AI Pro, a modern multi-lingual business assistant. Keep answers comprehensive but punchy."}]}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

if "last_processed_response" not in st.session_state:
    st.session_state.last_processed_response = ""

with st.sidebar:
    st.markdown("<h2 style='color:#f0f6fc; font-size:1.4rem; font-weight:600;'>💼 Enterprise Hub</h2>", unsafe_allow_html=True)
    st.write(" ")
    
    if st.button("➕ New Conversation", use_container_width=True):
        new_chat_id = f"Chat {len(st.session_state.all_chats) + 1}"
        st.session_state.all_chats[new_chat_id] = [{"role": "system", "content": "You are Peak AI Pro, a modern multi-lingual business assistant. Keep answers comprehensive but punchy."}]
        st.session_state.current_chat = new_chat_id
        st.rerun()
    
    st.write("---")
    st.markdown("<p style='color:#8b949e; font-size:0.85rem; font-weight:500;'>ACTIVE SESSIONS:</p>", unsafe_allow_html=True)
    
    chat_options = list(st.session_state.all_chats.keys())
    selected_chat = st.radio("Select Session", chat_options, label_visibility="collapsed", index=chat_options.index(st.session_state.current_chat))
    
    if selected_chat != st.session_state.current_chat:
        st.session_state.current_chat = selected_chat
        st.rerun()

messages = st.session_state.all_chats[st.session_state.current_chat]

# ==========================================
# MAIN APP HUB
# ==========================================
st.markdown("<h1 class='main-title'>Peak AI Pro</h1>", unsafe_allow_html=True)
st.markdown("<p class='main-subtitle'>Advanced Discussion Stream • Multi-Lingual Speech Engine</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.3], gap="large")

# ------------------------------------------
# COLUMN 1: INTERACTIVE VOICE ENGINE PANEL (NEW)
# ------------------------------------------
with col1:
    st.markdown('<div class="module-box">', unsafe_allow_html=True)
    st.markdown('<div class="module-title">🎙️ Speech Engine Control</div>', unsafe_allow_html=True)
    
    auto_speak = st.toggle("🔊 Auto-Speak AI Responses", value=True, help="When enabled, AI will read out answers instantly.")
    
    st.write(" ")
    # Language Matrix Mapping
    language_choice = st.selectbox("Speech Language Platform:", ["Urdu (Pakistan)", "English (United States)", "English (United Kingdom)"])
    lang_map = {
        "Urdu (Pakistan)": "ur-PK",
        "English (United States)": "en-US",
        "English (United Kingdom)": "en-GB"
    }
    target_lang_code = lang_map[language_choice]
    
    # Voice Gender Profile Selectors
    voice_gender = st.radio("Voice Profile Gender:", ["Female", "Male"], horizontal=True)
    
    # Speed Controller Slider
    speech_rate = st.slider("Speech Rate Speed:", min_value=0.7, max_value=1.5, value=1.0, step=0.1)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Dedicated Manual Reply Player Block
    if st.session_state.last_processed_response:
        st.markdown('<div class="module-box">', unsafe_allow_html=True)
        st.markdown('<div class="voice-badge">Engine Status: Ready</div>', unsafe_allow_html=True)
        st.write("Replay the latest assistant generation stream cleanly:")
        if st.button("▶️ Replay Latest Audio", use_container_width=True):
            trigger_voice_engine(st.session_state.last_processed_response, target_lang_code, voice_gender, speech_rate)
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# COLUMN 2: PROFESSIONAL DISCUSSION INTERFACE
# ------------------------------------------
with col2:
    st.markdown("<p style='font-weight:600; font-size:1.1rem; color:#58a6ff; margin-bottom:10px;'>💬 Interactive Stream</p>", unsafe_allow_html=True)
    
    chat_container = st.container(height=520, border=True)
    
    with chat_container:
        for message in messages[1:]:
            avatar = "👤" if message["role"] == "user" else "🤖"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    prompt = st.chat_input("Ask Peak AI Pro something...")

    if prompt:
        with chat_container:
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)

        messages.append({"role": "user", "content": prompt})

        # Process Streaming Response via Groq Text Platform
        with chat_container:
            with st.chat_message("assistant", avatar="🤖"):
                message_placeholder = st.empty()
                full_response = ""
                
                stream = client.chat.completions.create(
                    model="llama-3.1-8b-instant", # Ultra fast response model for real-time speech matching
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1024,
                    stream=True
                )
                for chunk in stream:
                    content = chunk.choices[0].delta.content
                    if content:
                        full_response += content
                        message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)

        messages.append({"role": "assistant", "content": full_response})
        st.session_state.last_processed_response = full_response
        
        # If Auto-Speak is enabled, immediately run Javascript Injection
        if auto_speak:
            trigger_voice_engine(full_response, target_lang_code, voice_gender, speech_rate)
            
        st.rerun()