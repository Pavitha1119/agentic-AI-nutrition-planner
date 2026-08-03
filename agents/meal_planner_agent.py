"""
Meal Planner Agent
-------------------
Combines the user's nutrition profile (BMI and calorie needs),
food preferences, and disease-specific dietary guidance to generate
a personalized one-day meal plan.
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# Initialize Groq LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.4,
)


# -----------------------------
# Nutrition Calculations
# -----------------------------

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """Calculate Body Mass Index."""
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)


def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    """Calculate Basal Metabolic Rate using the Mifflin-St Jeor Equation."""
    if gender.lower() == "male":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161


def calculate_daily_calories(bmr: float, goal: str) -> int:
    """
    Estimate daily calorie requirement.
    Assumes a lightly active lifestyle.
    """
    maintenance = bmr * 1.375

    goal = goal.lower()

    if "loss" in goal:
        return round(maintenance - 500)

    elif "gain" in goal:
        return round(maintenance + 500)

    return round(maintenance)


def build_profile_summary(user_profile: dict) -> dict:
    """Calculate BMI, BMR and target calorie intake."""

    bmi = calculate_bmi(
        user_profile["weight_kg"],
        user_profile["height_cm"]
    )

    bmr = calculate_bmr(
        user_profile["weight_kg"],
        user_profile["height_cm"],
        user_profile["age"],
        user_profile["gender"]
    )

    daily_calories = calculate_daily_calories(
        bmr,
        user_profile["goal"]
    )

    return {
        "bmi": bmi,
        "bmr": round(bmr),
        "daily_calories": daily_calories,
    }


# -----------------------------
# Prompt
# -----------------------------

MEAL_PLAN_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a professional Meal Planner Agent in an AI Nutrition Planning System.

Your task is to generate a realistic ONE-DAY meal plan.

Requirements:
- Create Breakfast, Lunch, Dinner and 1–2 Healthy Snacks.
- Follow the user's medical dietary guidance exactly.
- Never recommend foods that contradict the medical guidance.
- Respect the user's food preference (Vegetarian, Vegan, Non-Vegetarian, etc.).
- Match the user's health goal (Weight Loss, Weight Gain, Maintenance, Muscle Building).
- Stay close to the target daily calorie requirement (approximate is acceptable).
- Recommend balanced meals with carbohydrates, protein, healthy fats and vegetables.

For every meal provide:
- Meal name
- Foods
- Short description
- Approximate calories

Return the answer in clean Markdown.
"""
    ),
    (
        "human",
        """
User Profile

Age: {age}
Gender: {gender}
BMI: {bmi}
Target Calories: {daily_calories} kcal
Goal: {goal}
Food Preference: {food_preference}

Medical Dietary Guidance

{disease_guidance}

Generate a personalized one-day meal plan.
"""
    )
])


# -----------------------------
# Main Function
# -----------------------------

def generate_meal_plan(
    user_profile: dict,
    disease_guidance: str = "No medical guidance available."
) -> dict:

    profile_summary = build_profile_summary(user_profile)

    chain = MEAL_PLAN_PROMPT | llm

    response = chain.invoke({
        "age": user_profile["age"],
        "gender": user_profile["gender"],
        "bmi": profile_summary["bmi"],
        "daily_calories": profile_summary["daily_calories"],
        "goal": user_profile["goal"],
        "food_preference": user_profile["food_preference"],
        "disease_guidance": disease_guidance,
    })

    return {
        "profile_summary": profile_summary,
        "meal_plan": response.content,
    }


# -----------------------------
# Testing
# -----------------------------

if __name__ == "__main__":

    test_profile = {
        "age": 25,
        "gender": "Male",
        "height_cm": 175,
        "weight_kg": 70,
        "goal": "Weight Loss",
        "food_preference": "Vegetarian",
    }

    sample_guidance = """
DO:
- Eat whole grains.
- Eat vegetables.
- Eat healthy fats.

DON'T:
- Sugary drinks.
- White bread.
- Refined sugar.
"""

    result = generate_meal_plan(
        test_profile,
        sample_guidance
    )

    print("===== Profile Summary =====")
    print(result["profile_summary"])

    print("\n===== Meal Plan =====")
    print(result["meal_plan"])