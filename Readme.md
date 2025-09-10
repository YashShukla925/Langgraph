#  Fridge Recipe Generator   

A **LangGraph + Streamlit** powered app that generates creative recipes from leftover ingredients in your fridge. It also provides **ratings** (based on time, difficulty, and healthiness) and **nutrition estimates** for each recipe.  

---

##  Features  
- **Recipe Generation** – Get 3 meal ideas based on the ingredients you have.  
- **Comparison Table** – Rate recipes by **preparation time, difficulty, and healthiness**.  
- **Nutrition Insights** – Estimate **calories, protein, carbs, and fats** for each recipe.  
- **Interactive UI** – Built with **Streamlit** for a smooth and simple user experience.  
- **Powered by AI** – Uses **Google Gemini (via LangChain + LangGraph)** for reasoning and response formatting.  

---

##  Tech Stack  
- [Streamlit](https://streamlit.io/) – Interactive web UI.  
- [LangGraph](https://github.com/langchain-ai/langgraph) – Orchestrating multi-step AI workflows.  
- [LangChain](https://www.langchain.com/) – LLM wrapper for prompt management.  
- [Google Gemini API](https://ai.google.dev/) – Generative AI model (`gemini-1.5-flash`).  
- [Python-dotenv](https://pypi.org/project/python-dotenv/) – Load API keys securely.