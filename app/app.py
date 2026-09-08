import streamlit as st
import json
from pathlib import Path
from datetime import datetime
from google import genai
from google.genai import types

# -------------------------------------------------
# PAGE SETTINGS
# -------------------------------------------------

st.set_page_config(
    page_title="AgriMedic AIx",
    page_icon="🌱",
    layout="centered"
)

# -------------------------------------------------
# GEMINI SETUP
# -------------------------------------------------

try:
    gemini_client = genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"]
    )
    gemini_ready = True
except Exception as e:
    gemini_client = None
    gemini_ready = False
    gemini_error = str(e)


# -------------------------------------------------
# FILE SETTINGS
# -------------------------------------------------

REPORTS_FILE = Path("data/reports.json")

REPORTS_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


# -------------------------------------------------
# HISTORY FUNCTIONS
# -------------------------------------------------

def load_reports():

    if not REPORTS_FILE.exists():
        return []

    try:

        content = REPORTS_FILE.read_text(
            encoding="utf-8"
        )

        if not content.strip():
            return []

        data = json.loads(content)

        if isinstance(data, list):
            return data

        return []

    except (
        json.JSONDecodeError,
        OSError
    ):
        return []


def save_reports(reports):

    REPORTS_FILE.write_text(
        json.dumps(
            reports,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )


def save_report(
    crop,
    crop_age,
    problem_type,
    location,
    soil_moisture,
    fertilizer_used,
    symptoms,
    question,
    advice,
    image_analysis=""
):

    reports = load_reports()

    report = {
        "id": datetime.now().strftime(
            "%Y%m%d%H%M%S%f"
        ),

        "date": datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        ),

        "crop": crop,
        "crop_age": crop_age,
        "problem_type": problem_type,

        "location": (
            location
            if location
            else "Not provided"
        ),

        "soil_moisture": soil_moisture,
        "fertilizer_used": fertilizer_used,

        "symptoms": (
            symptoms
            if symptoms
            else "Not provided"
        ),

        "question": question,
        "advice": advice,
        "image_analysis": image_analysis
    }

    reports.insert(0, report)

    save_reports(reports)


# -------------------------------------------------
# GEMINI IMAGE ANALYSIS
# -------------------------------------------------

def analyze_crop_image(
    uploaded_image,
    crop,
    crop_age,
    problem_type,
    symptoms,
    question
):

    if not gemini_ready:
        return """
### ⚠️ Gemini Configuration Error

Gemini API is not configured correctly.

Please check the GEMINI_API_KEY in Streamlit Secrets.
"""

    try:

        image_bytes = uploaded_image.getvalue()

        prompt = f"""
You are AgriMedic AIx, an agricultural crop-image analysis assistant.

Analyze this crop image carefully and provide practical agricultural guidance.

USER INFORMATION

Crop: {crop}
Crop age: {crop_age} days
Problem type: {problem_type}

Symptoms:
{symptoms if symptoms else "Not provided"}

Question:
{question}

TASK

1. Identify the crop if possible.
2. Describe only the visible symptoms.
3. Give the most likely possible causes.
4. Consider disease, pest, nutrient deficiency, water stress and environmental causes.
5. Give a confidence level.
6. Explain what additional close-up photos or information are needed.
7. Give safe, practical agricultural recommendations.

IMPORTANT SAFETY RULES

- Do not claim a confirmed diagnosis from an image alone.
- If the image is unclear, explicitly say so.
- Do not recommend excessive fertilizer or pesticide use.
- Do not invent symptoms that are not visible.
- Prefer integrated pest management.
- Recommend locally approved agricultural treatment only after proper identification.
- Keep the answer practical and easy for a farmer to understand.

Use clear Markdown headings.
"""

        response = gemini_client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=uploaded_image.type
                ),
                prompt
            ]
        )

        if response.text:
            return response.text

        return "Gemini returned an empty response."

    except Exception as e:

        return f"""
### ⚠️ Image Analysis Error

Gemini could not analyze the uploaded image.

Please try again with a clear JPG or PNG photo.

**Technical error:** `{str(e)}`
"""



# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------

st.markdown(
    """
    <style>

    .main {
        background-color: #f7faf7;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 900px;
    }

    h1 {
        color: #1b5e20;
    }

    h2, h3 {
        color: #2e7d32;
    }

    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #d7e8d7;
        padding: 15px;
        border-radius: 12px;
    }

    .stButton > button {
        width: 100%;
        background-color: #2e7d32;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.7rem;
        font-weight: bold;
    }

    .stButton > button:hover {
        background-color: #1b5e20;
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -------------------------------------------------
# LOAD REPORT HISTORY
# -------------------------------------------------

reports = load_reports()


# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.title("🌱 AgriMedic AIx")

st.subheader(
    "AI-Powered Agricultural Assistant"
)

st.write(
    "Your intelligent assistant for practical "
    "agricultural guidance, crop problem identification "
    "and AI-powered crop image analysis."
)

st.divider()


# =================================================
# DASHBOARD
# =================================================

st.header("📊 Dashboard")

total_reports = len(reports)

unique_crops = len(
    set(
        report.get("crop", "")
        for report in reports
        if report.get("crop")
    )
)

unique_problems = len(
    set(
        report.get("problem_type", "")
        for report in reports
        if report.get("problem_type")
    )
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📄 Total Reports",
        total_reports
    )

with col2:
    st.metric(
        "🌾 Crops",
        unique_crops
    )

with col3:
    st.metric(
        "🔎 Problem Types",
        unique_problems
    )


# =================================================
# PREVIOUS REPORTS
# =================================================

st.header("📚 Previous Crop Reports")

if not reports:

    st.info(
        "No previous reports yet. "
        "Generate your first agricultural report below."
    )

else:

    st.write(
        f"You have **{len(reports)}** saved report(s)."
    )

    for index, report in enumerate(reports):

        crop_name = report.get(
            "crop",
            "Unknown"
        )

        problem = report.get(
            "problem_type",
            "Unknown problem"
        )

        report_date = report.get(
            "date",
            "Unknown date"
        )

        report_id = report.get(
            "id",
            index
        )

        with st.expander(
            f"🌾 {crop_name} — "
            f"{problem} — "
            f"{report_date}"
        ):

            st.write(
                f"**Crop:** {crop_name}"
            )

            st.write(
                f"**Crop age:** "
                f"{report.get('crop_age', 'N/A')} days"
            )

            st.write(
                f"**Problem:** {problem}"
            )

            st.write(
                f"**Location:** "
                f"{report.get('location', 'Not provided')}"
            )

            st.write(
                f"**Soil condition:** "
                f"{report.get('soil_moisture', 'N/A')}"
            )

            st.write(
                f"**Recent fertilizer:** "
                f"{report.get('fertilizer_used', 'N/A')}"
            )

            st.write("### 📝 Question")

            st.write(
                report.get(
                    "question",
                    "Not provided"
                )
            )

            st.write("### 🌱 Symptoms")

            st.write(
                report.get(
                    "symptoms",
                    "Not provided"
                )
            )

            if report.get("image_analysis"):

                st.write(
                    "### 📷 AI Image Analysis"
                )

                st.markdown(
                    report["image_analysis"]
                )

            st.write(
                "### 🔎 Agricultural Advice"
            )

            st.markdown(
                report.get(
                    "advice",
                    "No advice available."
                )
            )

            if st.button(
                "🗑️ Delete This Report",
                key=f"delete_{report_id}"
            ):

                reports.pop(index)

                save_reports(reports)

                st.success(
                    "Report deleted successfully."
                )

                st.rerun()


st.divider()


# =================================================
# ASK AGRIMEDIC
# =================================================

st.header("🔍 Ask AgriMedic")


# -------------------------------------------------
# CROP INFORMATION
# -------------------------------------------------

st.subheader("🌾 Crop Information")

crop = st.selectbox(
    "Select your crop",
    [
        "Wheat",
        "Rice",
        "Maize",
        "Cotton",
        "Tomato",
        "Potato",
        "Sugarcane",
        "Other"
    ]
)

crop_age = st.number_input(
    "Crop age (days)",
    min_value=1,
    max_value=1000,
    value=30
)

problem_type = st.selectbox(
    "What type of problem are you seeing?",
    [
        "Yellow leaves / Growth problem",
        "Pest / Insect",
        "Disease",
        "Nutrient deficiency",
        "Water / Irrigation",
        "Other"
    ]
)


# -------------------------------------------------
# FARM INFORMATION
# -------------------------------------------------

st.subheader("📍 Farm Information")

location = st.text_input(
    "Farm location",
    placeholder="Example: Islamabad, Pakistan"
)

soil_moisture = st.selectbox(
    "Current soil condition",
    [
        "Normal",
        "Dry",
        "Very dry",
        "Wet",
        "Waterlogged",
        "I don't know"
    ]
)

fertilizer_used = st.selectbox(
    "Have you recently applied fertilizer?",
    [
        "No",
        "Yes",
        "I don't know"
    ]
)


# -------------------------------------------------
# SYMPTOMS
# -------------------------------------------------

st.subheader("📝 Crop Symptoms")

symptoms = st.text_area(
    "Describe the symptoms",
    placeholder=(
        "Example: Older leaves are yellow, "
        "plants are growing slowly, and soil is slightly wet."
    ),
    height=120
)


# -------------------------------------------------
# IMAGE
# -------------------------------------------------

st.subheader("📷 Crop Photo")

uploaded_image = st.file_uploader(
    "Upload a photo of the affected crop/leaf",
    type=[
        "jpg",
        "jpeg",
        "png"
    ]
)

if uploaded_image:

    st.image(
        uploaded_image,
        caption="Uploaded crop image",
        use_container_width=True
    )

    st.success(
        "📷 Crop photo uploaded successfully."
    )


# -------------------------------------------------
# QUESTION
# -------------------------------------------------

st.subheader("❓ Your Question")

question = st.text_area(
    "What is your agricultural question?",
    placeholder=(
        "Example: My wheat crop has yellow leaves. "
        "What could be the reason?"
    ),
    height=120
)


# =================================================
# AGRICULTURAL ADVICE FUNCTION
# =================================================

def get_agricultural_advice(
    crop,
    crop_age,
    problem_type,
    location,
    soil_moisture,
    fertilizer_used,
    symptoms,
    question
):

    q = question.lower()
    s = symptoms.lower()

    location_text = (
        location
        if location
        else "Not provided"
    )

    symptoms_text = (
        symptoms
        if symptoms
        else "Not provided"
    )


    # =================================================
    # WHEAT + YELLOW LEAVES
    # =================================================

    if crop == "Wheat" and (
        "yellow" in q
        or "yellowing" in q
        or "yellow" in s
    ):

        if soil_moisture in [
            "Wet",
            "Waterlogged"
        ]:

            irrigation = """
### 💧 Irrigation Recommendation

The soil is reported as **wet/waterlogged**.

- Avoid unnecessary irrigation for now.
- Check field drainage.
- Standing water can reduce oxygen around the roots.
- Allow excess water to drain before the next irrigation.
"""

        elif soil_moisture in [
            "Dry",
            "Very dry"
        ]:

            irrigation = """
### 💧 Irrigation Recommendation

The soil is reported as **dry**.

- Check soil moisture at root depth.
- Irrigate according to crop stage, soil type and weather.
- Avoid severe dryness.
- Avoid excessive irrigation after watering.
"""

        else:

            irrigation = """
### 💧 Irrigation Recommendation

- Check soil moisture before irrigation.
- Avoid unnecessary watering.
- Avoid prolonged waterlogging.
- Irrigation should depend on crop stage, soil type and weather.
"""


        if fertilizer_used == "No":

            fertilizer = """
### 🌱 Fertilizer Recommendation

Because older wheat leaves are yellow and growth is slow,
**nitrogen deficiency is one possibility**.

- Do not apply a large amount of fertilizer based only on leaf color.
- A soil test is recommended.
- If nitrogen deficiency is confirmed, follow locally recommended wheat fertilizer rates.
"""

        elif fertilizer_used == "Yes":

            fertilizer = """
### 🌱 Fertilizer Recommendation

You recently applied fertilizer.

- Do not immediately add more fertilizer.
- Check which fertilizer was applied and how much.
- Observe the crop response.
- Consider soil testing if yellowing continues.
"""

        else:

            fertilizer = """
### 🌱 Fertilizer Recommendation

- First determine whether fertilizer has already been applied.
- Consider a soil test before major fertilizer changes.
- Avoid applying large amounts of fertilizer without knowing the nutrient requirement.
"""


        return f"""
### 🌾 Wheat — Yellow Leaves

Based on the information provided, possible causes include:

- **Nitrogen deficiency**
- **Water stress**
- **Poor drainage**
- **Disease**
- **Micronutrient deficiency**

### 🔎 What to Check

- Check whether yellowing starts on older or younger leaves.
- Inspect soil moisture.
- Look for spots, stripes or unusual patterns.
- Check for insects.
- Inspect roots if possible.
- Consider a soil test.

{fertilizer}

{irrigation}

### 📋 Crop Information

**Crop:** {crop}  
**Crop age:** {crop_age} days  
**Problem type:** {problem_type}  
**Location:** {location_text}

### 📝 Reported Symptoms

{symptoms_text}

### ⚠️ Important

This is general agricultural guidance, not a confirmed diagnosis.

Do not apply large amounts of fertilizer or pesticides based only on these symptoms.
"""


    elif problem_type == "Water / Irrigation":

        return f"""
### 💧 Water / Irrigation Problem

**Crop:** {crop}  
**Crop age:** {crop_age} days  
**Location:** {location_text}

### 🔎 What to Check

- Check soil moisture at root depth.
- Look for standing water.
- Check whether soil is very dry.
- Inspect roots if possible.
- Consider recent rainfall and weather.
- Consider crop growth stage.

### 💧 Irrigation Recommendation

- If soil is dry, irrigation may be needed depending on crop stage and soil.
- If soil is wet, avoid unnecessary irrigation.
- If water is standing, improve drainage where possible.

### 📝 Reported Symptoms

{symptoms_text}
"""


    elif problem_type == "Nutrient deficiency":

        return f"""
### 🌱 Possible Nutrient Deficiency

**Crop:** {crop}  
**Crop age:** {crop_age} days  
**Location:** {location_text}

Possible nutrients include:

- Nitrogen
- Phosphorus
- Potassium
- Sulfur
- Iron
- Other micronutrients

### 🌱 Fertilizer Recommendation

- Soil testing is recommended before significant fertilizer application.
- Avoid guessing the nutrient only from leaf color.
- Check whether fertilizer was recently applied.
- Follow locally recommended fertilizer rates.

### 📝 Reported Symptoms

{symptoms_text}
"""


    elif problem_type == "Pest / Insect":

        return f"""
### 🐛 Pest / Insect Problem

**Crop:** {crop}  
**Crop age:** {crop_age} days  
**Location:** {location_text}

### 🔎 What to Check

- Inspect the underside of leaves.
- Look for insects or eggs.
- Check for holes or chewing damage.
- Check curled leaves.
- Look for webbing or sticky material.
- Check young shoots and stems.

### 🧪 Pest Management

Do not immediately apply pesticides without identifying the pest when possible.

If identified, use locally recommended treatment and follow the product label.

### 📝 Reported Symptoms

{symptoms_text}
"""


    elif problem_type == "Disease":

        return f"""
### 🦠 Possible Plant Disease

**Crop:** {crop}  
**Crop age:** {crop_age} days  
**Location:** {location_text}

### 🔎 What to Check

- Leaf spots
- Yellow or brown patches
- Wilting
- Stem damage
- Fungal growth
- Whether symptoms are spreading

### 🌱 Management

- Improve field sanitation where appropriate.
- Avoid unnecessary pesticide use.
- Improve drainage where relevant.
- Use locally recommended disease-control measures after identification.

### 📝 Reported Symptoms

{symptoms_text}
"""


    else:

        return f"""
### 🌱 AgriMedic Guidance

**Crop:** {crop}  
**Crop age:** {crop_age} days  
**Problem type:** {problem_type}  
**Location:** {location_text}

### 📝 Reported Symptoms

{symptoms_text}

### 🔎 What to Check

- Leaf color and pattern
- Plant growth
- Soil moisture
- Insects or pests
- Spots or fungal growth
- Recent fertilizer application
- Drainage conditions

### 🌱 Fertilizer

Avoid applying large amounts of fertilizer until the likely cause is identified.

A soil test is recommended when nutrient deficiency is suspected.

### 💧 Irrigation

Check soil moisture before irrigation.

Avoid both prolonged dryness and unnecessary waterlogging.

### ⚠️ Important

More information may be needed for a reliable diagnosis.
"""


# =================================================
# GET ADVICE
# =================================================

if st.button("🌱 Get Agricultural Advice"):

    if not question.strip():

        st.warning(
            "Please enter your agricultural question."
        )

    else:

        with st.spinner(
            "AgriMedic is preparing advice..."
        ):

            advice = get_agricultural_advice(
                crop,
                crop_age,
                problem_type,
                location,
                soil_moisture,
                fertilizer_used,
                symptoms,
                question
            )

        st.success(
            "Agricultural Advice"
        )

        st.markdown(advice)


        # =================================================
        # GEMINI IMAGE ANALYSIS
        # =================================================

        image_analysis = ""

        if uploaded_image:

           with st.spinner("🤖 Gemini is analyzing the crop image..."):

            image_analysis = analyze_crop_image(
                uploaded_image,
                crop,
                crop_age,
                problem_type,
                symptoms,
                question
            )

           st.subheader("📷 AI Crop Image Analysis")
           st.markdown(image_analysis)



        # =================================================
        # SAVE REPORT
        # =================================================

        save_report(
            crop,
            crop_age,
            problem_type,
            location,
            soil_moisture,
            fertilizer_used,
            symptoms,
            question,
            advice,
            image_analysis
        )

        st.success(
            "💾 Report saved to your history!"
        )


        # =================================================
        # DOWNLOAD REPORT
        # =================================================

        report_text = f"""
AgriMedic AIx — Agricultural Report

Date:
{datetime.now().strftime("%Y-%m-%d %H:%M")}

Crop:
{crop}

Crop age:
{crop_age} days

Problem type:
{problem_type}

Farm location:
{location if location else "Not provided"}

Soil condition:
{soil_moisture}

Recent fertilizer:
{fertilizer_used}

Symptoms:
{symptoms if symptoms else "Not provided"}

Question:
{question}

----------------------------------------
AI CROP IMAGE ANALYSIS
----------------------------------------

{image_analysis if image_analysis else "No image analysis performed."}

----------------------------------------
AGRICULTURAL ADVICE
----------------------------------------

{advice}

----------------------------------------
Important:
This report provides general agricultural guidance.
AI image analysis is not a confirmed field diagnosis.

Do not apply large amounts of fertilizer or pesticides
without proper identification and locally appropriate advice.
"""

        st.download_button(
            label="📄 Download Agricultural Report",
            data=report_text,
            file_name="AgriMedic_Agricultural_Report.txt",
            mime="text/plain"
        )


# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.divider()

st.caption(
    "🌱 AgriMedic AIx — Agricultural Assistant"
)
