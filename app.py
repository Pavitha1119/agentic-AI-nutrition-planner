import streamlit as st
from PIL import Image
import base64
import os
import mimetypes
from agents.disease_agent import get_disease_guidance
from agents.meal_planner_agent import generate_meal_plan

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
logo_path = "assets/logo.png"
logo = Image.open(logo_path) if os.path.exists(logo_path) else None

st.set_page_config(
    page_title="NutriGenie AI",
    page_icon=logo if logo else "🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Helper: encode local image to base64 (for CSS background / img tag)
# ---------------------------------------------------------
def get_base64(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

hero_img_base64 = get_base64("assets/ai_nutrition_agent.jpg")
st.write(os.path.exists("assets/ai_nutrition_agent.jpg"))  # or .webp

# ---------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Hide default Streamlit padding at top */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Hero section container */
    .hero-container {
        background: linear-gradient(135deg, #1E90FF 0%, #0F6FDE 100%);
        border-radius: 24px;
        padding: 60px 50px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        box-shadow: 0 20px 40px rgba(15, 111, 222, 0.25);
        margin-bottom: 40px;
    }

    .hero-text {
        flex: 1;
        min-width: 320px;
        color: white;
        padding-right: 30px;
    }

    .hero-text h1 {
        font-size: 44px;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 20px;
        color: white;
    }

    .hero-text h1 span {
        color: #1a1a2e;
        background: white;
        padding: 2px 12px;
        border-radius: 8px;
    }

    .hero-text p {
        font-size: 17px;
        color: #e6f0ff;
        margin-bottom: 30px;
        line-height: 1.6;
    }

    .hero-img {
        flex: 1;
        min-width: 280px;
        display: flex;
        justify-content: center;
    }

    .hero-img img {
        max-width: 100%;
        border-radius: 16px;
    }

    /* Feature cards */
    .feature-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        border: 1px solid #eef1f6;
        height: 100%;
        transition: transform 0.2s ease;
    }

    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 24px rgba(15, 111, 222, 0.12);
    }

    .feature-icon {
        font-size: 28px;
        margin-bottom: 12px;
    }

    .feature-title {
        font-weight: 700;
        font-size: 16px;
        color: #1a1a2e;
        margin-bottom: 6px;
    }

    .feature-desc {
        font-size: 13.5px;
        color: #6b7280;
        line-height: 1.5;
    }

    /* Section heading */
    .section-heading {
        text-align: center;
        font-size: 26px;
        font-weight: 800;
        color: #1a1a2e;
        margin: 40px 0 30px 0;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Top nav-style header (logo + title)
# ---------------------------------------------------------
col1, col2 = st.columns([1, 6])
with col1:
    if logo:
        st.image(logo, width=70)
with col2:
    st.markdown("### NutriGenie AI")

# ---------------------------------------------------------
# Hero Section
# ---------------------------------------------------------

if hero_img_base64:
    img_tag = f'<img src="data:image/jpg;base64,{hero_img_base64}" alt="AI Nutrition Agent">'
else:
    img_tag = """
    <div style="
        width:350px;
        height:350px;
        background:#ffffff;
        border-radius:20px;
        display:flex;
        align-items:center;
        justify-content:center;
        color:#1E90FF;
        font-size:22px;
        font-weight:bold;
        box-shadow:0 10px 25px rgba(0,0,0,0.15);
    ">
        Image Not Found
    </div>
    """

st.markdown(f"""
<div class="hero-container">
    <div class="hero-text">
        <h1>Personalized Nutrition,<br>Powered by <span>Agentic AI</span></h1>
        <p>
            NutriGenie AI uses a team of intelligent agents working together to understand
            your health goals, dietary needs, and food preferences, then generate a
            personalized nutrition plan just for you.
        </p>
    </div>


</div>
""", unsafe_allow_html=True)
# ---------------------------------------------------------
# Feature Cards
# ---------------------------------------------------------
st.markdown('<div class="section-heading">🚀 What NutriGenie AI Does</div>', unsafe_allow_html=True)

features = [
    ("📊", "BMI & Calorie Tracking", "Calculates BMI and daily calorie requirements based on your profile."),
    ("🩺", "Health-Aware Planning", "Considers medical conditions like Diabetes and Hypertension automatically."),
    ("🥗", "Personalized Meal Plans", "Generates meal plans tailored to your preferences and lifestyle."),
    ("🤖", "Multi-Agent Architecture", "Router, Nutrition, Disease, Preference & Profile agents work together."),
]

cols = st.columns(4)
for col, (icon, title, desc) in zip(cols, features):
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <div class="feature-title">{title}</div>
            <div class="feature-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Nutrition Profile Form
# ---------------------------------------------------------
st.markdown('<div class="section-heading">📝 Tell Us About Yourself</div>', unsafe_allow_html=True)

with st.form("nutrition_profile_form"):
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, step=1)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, step=0.5)
        weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, step=0.5)

    with col2:
        disease = st.multiselect(
            "Medical Conditions (if any)",
            ["None", "Diabetes", "Hypertension", "Cholesterol", "Thyroid", "PCOS", "Other"],
            default=["None"]
        )
        goal = st.selectbox(
            "Your Goal",
            ["Weight Loss", "Weight Gain", "Maintain Weight", "Muscle Building", "General Health"]
        )
        food_preference = st.selectbox(
            "Food Preference",
            ["Vegetarian", "Non-Vegetarian", "Vegan", "Eggetarian"]
        )

    submitted = st.form_submit_button(" Generate My Nutrition Plan")

if submitted:
        st.session_state["user_profile"] = {
            "age": age,
            "gender": gender,
            "height_cm": height,
            "weight_kg": weight,
            "diseases": disease,
            "goal": goal,
            "food_preference": food_preference,
        }
        st.success(" Profile saved! Passing your details to the AI agents...")
        st.json(st.session_state["user_profile"])
# ---------------------------------------------
# Agent 1 - Disease Guideline Agent
# ---------------------------------------------

        with st.spinner("Disease Guideline Agent is analyzing your medical conditions..."):

            disease_result = get_disease_guidance(
                st.session_state["user_profile"]["diseases"]
    )
            st.divider()

            st.subheader(" Disease Guideline Agent")

            st.markdown(disease_result["guidance"])

        with st.expander("View Sources"):

            for src in disease_result["sources"]:
                st.write(f"- {src}")

# ---------------------------------------------
# Agent 2 - Meal Planner Agent
# ---------------------------------------------

        with st.spinner("Meal Planner Agent is creating your personalized meal plan..."):

            meal_result = generate_meal_plan(
                st.session_state["user_profile"],
                disease_result["guidance"]
    )
        st.divider()

        st.subheader(" Personalized Meal Plan")

        profile = meal_result["profile_summary"]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("BMI", profile["bmi"])

        with col2:
            st.metric("BMR", f'{profile["bmr"]} kcal')

        with col3:
            st.metric("Daily Calories", f'{profile["daily_calories"]} kcal')


        st.markdown(meal_result["meal_plan"])