# AgriN-BRICS-AI
# 🌾 AgriN: Regenerative AI & Crop Diagnostic Hub
> **Track 4: AgriN & Regenerative AI** | BRICS Agricultural Cooperation Platform

AgriN is an AI-driven, dynamic multilingual crop diagnostic and seasonal advisory platform. Built specifically for regional farmers across BRICS nations, AgriN bridges language barriers and provides instant, localized agricultural insights—from leaf disease diagnosis to climate-aware seasonal crop planning.

---

## ✨ Key Features

* **📷 Multilingual Disease Diagnosis & Image Analytics**: Upload leaf photos to receive instant diagnostic confidence scores, affected area estimations, yield risk evaluations, and organic treatment plans powered by **Gemini 2.5 Flash**.
* **📊 Seasonal Crop & Timing Advisor**: Real-time advice tailored to soil conditions, water availability, and current local temperatures.
* **🌐 Dynamic Localization**: Live UI and advisory translations across 15 global and regional languages (Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali, Marathi, Gujarati, Punjabi, Spanish, French, Chinese, Russian, Portuguese, and English) using `deep-translator`.
* **🔊 Voice Advisory Output**: Converts diagnostic reports into clear regional spoken audio via Google Text-to-Speech (`gTTS`) to assist low-literacy farmers.
* **🌤️ Real-Time Weather Integration**: Dynamic local weather data fetching powered by Open-Meteo.

---

## 🛠️ Tech Stack

* **Frontend / Framework**: Python, Streamlit
* **AI Model**: Google Gemini GenAI API (`gemini-2.5-flash`)
* **Localization & Translation**: `deep-translator`
* **Text-to-Speech**: `gTTS` (Google Text-to-Speech)
* **Weather API**: Open-Meteo API
* **Deployment**: Streamlit Community Cloud

---

## 🚀 Quickstart & Local Setup

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/Jeswanthsurya-debug/AgriN-BRICS-AI.git](https://github.com/Jeswanthsurya-debug/AgriN-BRICS-AI.git)
   cd AgriN-BRICS-AI
