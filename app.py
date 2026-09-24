import streamlit as st
from google import genai
import requests
from PIL import Image
import pandas as pd
from gtts import gTTS
import io

# Page Configuration
st.set_page_config(page_title="AgriN - AI Crop Assistant", layout="wide")

# Multilingual UI Dictionary
TRANSLATIONS = {
    "English": {
        "title": "🌾 AgriN: Regenerative AI & Crop Diagnostic Hub",
        "subtitle": "BRICS Agricultural Cooperation & Localized Advisory Platform",
        "settings": "⚙️ Settings & Localization",
        "api_key": "Enter Gemini API Key",
        "choose_lang": "🌐 Choose Output Language",
        "lat": "Latitude",
        "lon": "Longitude",
        "temp": "Temperature (°C)",
        "wind": "Wind Speed (km/h)",
        "tab1": "🌱 Disease Diagnosis & Image Analytics",
        "tab2": "📊 Seasonal Crop & Timing Advisor",
        "upload_title": "📷 Upload Crop/Leaf Photo for Diagnosis & Statistics",
        "upload_label": "Choose an image...",
        "btn_diagnose": "Run Diagnostic & Generate Statistics",
        "img_analytics": "📈 Image Analytics & Metrics",
        "audio_title": "🔊 Audio Advisory",
        "season_title": "📅 Seasonal Crop Selection & Exact Timing Guide",
        "soil_type": "Soil Type",
        "current_season": "Current Season",
        "water_avail": "Water Availability",
        "btn_schedule": "Get Season & Timing Schedule",
        "err_key": "Please enter your Gemini API Key in the sidebar."
    },
    "Hindi (हिंदी)": {
        "title": "🌾 एग्री-एन: पुनर्योजी एआई और फसल निदान केंद्र",
        "subtitle": "ब्रिक्स कृषि सहयोग और स्थानीयकृत परामर्श मंच",
        "settings": "⚙️ सेटिंग्स और स्थानीयकरण",
        "api_key": "Gemini API कुंजी दर्ज करें",
        "choose_lang": "🌐 भाषा चुनें",
        "lat": "अक्षांश (Latitude)",
        "lon": "रेखांश (Longitude)",
        "temp": "तापमान (°C)",
        "wind": "हवा की गति (km/h)",
        "tab1": "🌱 रोग निदान और छवि विश्लेषण",
        "tab2": "📊 मौसमी फसल और समय सलाहकार",
        "upload_title": "📷 निदान और आंकड़ों के लिए फसल/पत्ती का फोटो अपलोड करें",
        "upload_label": "एक छवि चुनें...",
        "btn_diagnose": "निदान चलाएं और आंकड़े तैयार करें",
        "img_analytics": "📈 छवि विश्लेषण और मेट्रिक्स",
        "audio_title": "🔊 ऑडियो सलाह",
        "season_title": "📅 मौसमी फसल चयन और सटीक समय गाइड",
        "soil_type": "मिट्टी का प्रकार",
        "current_season": "वर्तमान मौसम",
        "water_avail": "पानी की उपलब्धता",
        "btn_schedule": "मौसम और समय सारणी प्राप्त करें",
        "err_key": "कृपया साइडबार में अपनी Gemini API कुंजी दर्ज करें।"
    },
    "Tamil (தமிழ்)": {
        "title": "🌾 அக்ரி-என்: AI பயிர் நோய் கண்டறிதல் மையம்",
        "subtitle": "பிரிக்ஸ் விவசாய ஒத்துழைப்பு மற்றும் உள்ளூர் ஆலோசனை தளம்",
        "settings": "⚙️ அமைப்புகள் & மொழியாக்கம்",
        "api_key": "Gemini API சாவியை உள்ளிடவும்",
        "choose_lang": "🌐 மொழியைத் தேர்ந்தெடுக்கவும்",
        "lat": "அட்சரேகை (Latitude)",
        "lon": "தீர்க்கரேகை (Longitude)",
        "temp": "வெப்பநிலை (°C)",
        "wind": "காற்றின் வேகம் (km/h)",
        "tab1": "🌱 நோய் கண்டறிதல் & புகைப்பட பகுப்பாய்வு",
        "tab2": "📊 பருவகால பயிர் & நேர ஆலோசனை",
        "upload_title": "📷 பயிர்/இலை புகைப்படத்தைப் பதிவேற்றவும்",
        "upload_label": "ஒரு படத்தைத் தேர்ந்தெடுக்கவும்...",
        "btn_diagnose": "பகுப்பாய்வு செய்து புள்ளிவிவரங்களைப் பெறு",
        "img_analytics": "📈 புகைப்பட பகுப்பாய்வு & அளவீடுகள்",
        "audio_title": "🔊 குரல் வழிகாட்டி",
        "season_title": "📅 பருவகால பயிர் தேர்வு & துல்லியமான கால அட்டவணை",
        "soil_type": "மண் வகை",
        "current_season": "தற்போதைய பருவம்",
        "water_avail": "நீர் வசதி",
        "btn_schedule": "பயிர் கால அட்டவணையைப் பெறுங்கள்",
        "err_key": "தயவுசெய்து Gemini API சாவியை உள்ளிடவும்."
    },
    "Telugu (తెలుగు)": {
        "title": "🌾 అగ్రి-ఎన్: పునరుత్పత్తి AI & పంట రోగనిర్ధారణ కేంద్రం",
        "subtitle": "బ్రిక్స్ వ్యవసాయ సహకారం & స్థానిక సలహా వేదిక",
        "settings": "⚙️ సెట్టింగ్‌లు & స్థానీకరణ",
        "api_key": "Gemini API కీని నమోదు చేయండి",
        "choose_lang": "🌐 భాషను ఎంచుకోండి",
        "lat": "అక్షాంశం (Latitude)",
        "lon": "రేఖాంశం (Longitude)",
        "temp": "ఉష్ణోగ్రత (°C)",
        "wind": "గాలి వేగం (km/h)",
        "tab1": "🌱 రోగ నిర్ధారణ & ఇమేజ్ విశ్లేషణ",
        "tab2": "📊 రుతుపవన పంట & సమయ సలహాదారు",
        "upload_title": "📷 నిర్ధారణ & గణాంకాల కోసం పంట/ఆకు ఫోటోను అప్‌లోడ్ చేయండి",
        "upload_label": "చిత్రాన్ని ఎంచుకోండి...",
        "btn_diagnose": "విశ్లేషణ ప్రారంభించు & గణాంకాలను పొందు",
        "img_analytics": "📈 ఇమేజ్ విశ్లేషణ & కొలమానాలు",
        "audio_title": "🔊 ఆడియో సలహా",
        "season_title": "📅 రుతుపవన పంట ఎంపిక & ఖచ్చితమైన సమయ గైడ్",
        "soil_type": "నేల రకం",
        "current_season": "ప్రస్తుత కాలం",
        "water_avail": "నీటి లభ్యత",
        "btn_schedule": "పంటల సమయ షెడ్యూల్‌ను పొందండి",
        "err_key": "దయచేసి సైడ్‌బార్‌లో మీ Gemini API కీని నమోదు చేయండి."
    }
}

# Sidebar Settings
st.sidebar.header("⚙️ Settings & Localization")
api_key = st.sidebar.text_input("Gemini API Key", type="password")

selected_lang_name = st.sidebar.selectbox("🌐 Choose Output Language", list(TRANSLATIONS.keys()))
t = TRANSLATIONS[selected_lang_name]

lang_codes = {
    "English": "en",
    "Hindi (हिंदी)": "hi",
    "Tamil (தமிழ்)": "ta",
    "Telugu (తెలుగు)": "te"
}
target_lang_code = lang_codes[selected_lang_name]

lat = st.sidebar.number_input(t["lat"], value=13.0827, format="%.4f")
lon = st.sidebar.number_input(t["lon"], value=80.2707, format="%.4f")

# Header Section
st.title(t["title"])
st.subheader(t["subtitle"])

# Audio Helper Function
def play_audio(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except Exception:
        return None

# Fetch Weather Data
def get_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        res = requests.get(url).json()
        return res.get("current_weather", {})
    except Exception:
        return {}

weather = get_weather(lat, lon)
if weather:
    col1, col2 = st.columns(2)
    col1.metric(t["temp"], weather.get("temperature", "N/A"))
    col2.metric(t["wind"], weather.get("windspeed", "N/A"))

st.divider()

# Navigation Tabs
tab1, tab2 = st.tabs([t["tab1"], t["tab2"]])

# TAB 1: Disease Diagnosis
with tab1:
    st.header(t["upload_title"])
    uploaded_file = st.file_uploader(t["upload_label"], type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        col_img, col_stat = st.columns([1, 1])
        with col_img:
            st.image(image, caption="Uploaded Image", use_column_width=True)
        
        if st.button(t["btn_diagnose"]):
            if not api_key:
                st.error(t["err_key"])
            else:
                try:
                    client = genai.Client(api_key=api_key)
                    prompt = (
                        f"Analyze this plant leaf image and respond strictly in {selected_lang_name}.\n"
                        "SECTION 1 - STATISTICAL SUMMARY:\n"
                        "- Diagnostic Confidence Score: [0-100%]\n"
                        "- Healthy Leaf Area: [0-100%]\n"
                        "- Affected Area: [0-100%]\n"
                        "- Estimated Yield Impact Risk: [Low/Medium/High]\n\n"
                        "SECTION 2 - DETAILED ANALYSIS:\n"
                        "1. Identified Disease/Issue Name\n"
                        "2. Severity Level\n"
                        "3. Organic/Regenerative Treatment Steps"
                    )
                    
                    with st.spinner("Analyzing..."):
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=[image, prompt]
                        )
                    
                    with col_stat:
                        st.subheader(t["img_analytics"])
                        st.write(response.text)
                        
                        st.subheader(t["audio_title"])
                        audio_fp = play_audio(response.text, target_lang_code)
                        if audio_fp:
                            st.audio(audio_fp, format="audio/mp3")
                        
                except Exception as e:
                    st.error(f"Error: {e}")

# TAB 2: Seasonal Crop Advisor
with tab2:
    st.header(t["season_title"])
    
    col_a, col_b = st.columns(2)
    with col_a:
        soil_type = st.selectbox(t["soil_type"], ["Clay", "Sandy", "Loam", "Black Soil", "Red Soil"])
        season = st.selectbox(t["current_season"], ["Kharif / Rainy", "Rabi / Winter", "Zaid / Summer"])
    with col_b:
        water_availability = st.selectbox(t["water_avail"], ["High / Irrigated", "Moderate", "Low / Rainfed"])

    if st.button(t["btn_schedule"]):
        if not api_key:
            st.error(t["err_key"])
        else:
            try:
                client = genai.Client(api_key=api_key)
                prompt = (
                    f"Acts as an expert agricultural advisor. Respond entirely in {selected_lang_name}.\n"
                    f"Parameters: Soil: {soil_type}, Season: {season}, Temp: {weather.get('temperature', '28')}°C, Water: {water_availability}\n"
                    f"Provide: 1. Best 3 crops suitable right now. 2. Exact Sowing to Harvest Timeline. 3. Regenerative farming techniques."
                )
                
                with st.spinner("Calculating..."):
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt
                    )
                st.write(response.text)
                
                st.subheader(t["audio_title"])
                audio_fp = play_audio(response.text, target_lang_code)
                if audio_fp:
                    st.audio(audio_fp, format="audio/mp3")

            except Exception as e:
                st.error(f"Error: {e}")