# 🌱 AgriMedic AIx

**AI-Powered Agricultural Assistant**

AgriMedic AIx is an AI-powered agricultural assistant that helps farmers identify possible crop problems and receive practical agricultural guidance using crop information, symptoms, farm conditions, and uploaded crop images.

## 🚀 Features

- 🌾 Crop selection and crop-age information
- 🔎 Agricultural problem identification
- 📝 Crop symptom description
- 📷 Crop and leaf image upload
- 🤖 AI-powered crop image analysis using Google Gemini
- 🌱 Agricultural recommendations
- 💧 Irrigation guidance
- 🧪 Fertilizer guidance
- 📚 Previous crop report history
- 📊 Agricultural report dashboard
- 📄 Downloadable agricultural reports

## 🤖 AI Crop Image Analysis

Users can upload a photo of an affected crop or leaf.

AgriMedic AIx sends the image and agricultural information to Google Gemini for AI-assisted analysis.

The system can provide:

- Possible crop identification
- Visible symptoms
- Possible causes
- Confidence level
- Additional information needed
- Practical recommendations
- Suggestions for further field inspection

## 🌾 Supported Crop Information

The application currently supports crop information for:

- Wheat
- Rice
- Maize
- Cotton
- Tomato
- Potato
- Sugarcane
- Other crops

## 🔍 Agricultural Problems

Users can provide information about:

- Yellow leaves / Growth problems
- Pest / Insect problems
- Plant diseases
- Nutrient deficiencies
- Water / Irrigation problems
- Other agricultural problems

## 📊 Dashboard

AgriMedic AIx provides a dashboard showing:

- Total reports
- Number of crops
- Number of problem types
- Previous agricultural reports

## 📚 Report History

Generated reports are stored locally in:

```text
data/reports.json
````

 Users can view previous reports and delete reports when required.

 ## 📄 Report Download

 Users can download an agricultural report containing:

 - Crop information
- Crop age
- Problem type
- Farm location
- Soil condition
- Fertilizer information
- Reported symptoms
- Agricultural question
- AI/agricultural advice

 ## 🛠️ Technology Stack

 - Python
- Streamlit
- Google Gemini
- Google GenAI SDK
- JSON
- HTML/CSS through Streamlit

 ## 📁 Project Structure

```
AgriMedic-AIx/
│
├── app/
│   └── app.py
│
├── data/
│   └── reports.json
│
├── .gitignore
│
└── README.md
```

 ## ⚙️ Installation

 Clone the repository:

```
git clone https://github.com/muzamal478/AgriMedic-AIx.git
```

 Go to the project folder:

```
cd AgriMedic-AIx
```

 Create and activate a virtual environment:

```
python -m venv .venv
```

 Windows PowerShell:

```
.venv\Scripts\Activate.ps1
```

 Install the required packages:

```
pip install streamlit google-genai
```

 ## 🔐 Gemini API Configuration

 Create the following file:

```
.streamlit/secrets.toml
```

 Add your Gemini API key there:

```
GEMINI_API_KEY = "YOUR_API_KEY_HERE"
```

 **Never upload your API key to GitHub.**

 The `.streamlit/secrets.toml` file should remain private and should be included in `.gitignore`.

 ## ▶️ Run the Application

 Run:

```
streamlit run app/app.py
```

 The application will open in your browser.

 ## 🎯 Project Goal

 The goal of AgriMedic AIx is to provide farmers and agricultural learners with an easy-to-use AI-assisted tool for understanding crop symptoms and making better-informed agricultural decisions.

 The system combines:

 **Farmer Information + Crop Symptoms + Farm Conditions + Crop Image → AI-Assisted Agricultural Guidance**

 ## ⚠️ Disclaimer

 AgriMedic AIx provides general agricultural guidance and AI-assisted observations.

 It is **not a replacement for professional agricultural diagnosis, laboratory testing, or qualified agricultural experts**.

 Users should verify important crop-treatment decisions with qualified local agricultural professionals before applying fertilizers, pesticides, or other treatments.

 ## 👨‍💻 Hackathon Project

 **Project:** AgriMedic AIx\
 **Event:** AI Hackathon Pakistan\
 **Project ID:** P02726
