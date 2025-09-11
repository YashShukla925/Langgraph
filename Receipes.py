import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from langgraph.graph import StateGraph

import os
from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# For Streamlit Cloud, load from secrets if env var is missing
if not GOOGLE_API_KEY and "GOOGLE_API_KEY" in st.secrets:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# --- Gemini LLM ---
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

# --- Define state ---
RecipeState = dict


# --- Node 1: Recipe Suggestion ---
def suggest_recipes(state):
    ingredients = state["ingredients"]
    messages = [
        SystemMessage(content="You are a creative chef."),
        HumanMessage(content=f"I have these ingredients: {ingredients}. Suggest 3 meals I can cook.")
    ]
    recipes = llm.invoke(messages).content
    return {**state, "recipes": recipes}

# --- Node 2: Rate Recipes ---
def rate_recipes(state):
    recipes = state["recipes"]
    messages = [
        SystemMessage(content="You are a culinary expert."),
        HumanMessage(content=f"Rate these meals by preparation time, difficulty, and healthiness:\n\n{recipes}")
    ]
    ratings = llm.invoke(messages).content
    return {**state, "ratings": ratings}

# --- Node 3: Nutrition Estimator ---
def estimate_nutrition(state):
    recipes = state["recipes"]
    messages = [
        SystemMessage(content="You are a nutritionist."),
        HumanMessage(content=f"Estimate calories, protein, carbs, and fats for each of these recipes:\n\n{recipes}")
    ]
    nutrition = llm.invoke(messages).content
    return {**state, "nutrition": nutrition}

# --- Node 4: Final Formatter ---
def format_output(state):
    formatted = f"""
🍽️ **Recipes**:
{state['recipes']}

📊 **Ratings**:
{state['ratings']}

🥗 **Nutrition Estimates**:
{state['nutrition']}
"""
    return {"result": formatted}

# --- Build LangGraph ---
builder = StateGraph(RecipeState)
builder.add_node("suggest", suggest_recipes)
builder.add_node("rate", rate_recipes)
builder.add_node("nutrition", estimate_nutrition)
builder.add_node("format", format_output)

builder.set_entry_point("suggest")
builder.add_edge("suggest", "rate")
builder.add_edge("rate", "nutrition")
builder.add_edge("nutrition", "format")
builder.set_finish_point("format")

graph = builder.compile()




#  UI Part
st.set_page_config(page_title="Fridge Recipe Generator 🍳")
st.title("🥕 YourChef")

ingredients_input = st.text_area("🧺 Enter the ingredients in your fridge:", placeholder="e.g. eggs, spinach, tomatoes, onion...")

if st.button("🍽️ Generate Recipes"):
    if ingredients_input.strip() == "":
        st.warning("Please enter some ingredients.")
    else:
        with st.spinner("Cooking up ideas..."):
            result = graph.invoke({"ingredients": ingredients_input})
            st.markdown(result["result"])




