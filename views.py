import os
import openai
from dotenv import load_dotenv
from flask import Blueprint, render_template

# Flask blueprint loading
views = Blueprint(__name__, "views")

# Getting keys from secret python env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

# Function to generate response from ChatGPT
def chat_gpt(prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# Renders index.html with passed chatGPT-generated funFact
@views.route("/")
def home():
    load_dotenv()
    openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
    return render_template("index.html", funFact = chat_gpt("Tell me a fun fact"), openweather_api_key=openweather_api_key)