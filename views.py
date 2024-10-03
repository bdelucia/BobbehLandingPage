import os
import openai
import requests
import math
import random
from dotenv import load_dotenv
from flask import Blueprint, render_template

# Flask blueprint loading
views = Blueprint(__name__, "views")

# Getting keys from secret python env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key
openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
# Function to generate weather data
def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweather_api_key}&units=imperial"
    response = requests.get(url)
    return response.json()

def get_random_fun_fact_prompt():
    prompts = [
        "Tell me a unique fun fact about space.",
        "What's an unusual fun fact about the solar system that isn't commonly known?",
        "Give me three unique fun facts about animals.",
        "What are some surprising discoveries in science that changed our understanding of the world?",
        "Tell me about an interesting event in history that most people don’t know about.",
        "What’s a little-known fact about a famous person?",
        "Tell me an unusual fact about a sports event or athlete that might surprise fans.",
        "What is a fun fact about a popular dish that originated from a specific region?",
        "What’s a fun fact about an invention that had unexpected consequences?"
    ]
    
    return random.choice(prompts)

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
    weather_data = get_weather_data("85308")
    rounded_temp = math.ceil(weather_data["main"]["temp"])
    prompt = get_random_fun_fact_prompt()
    return render_template("index.html", funFact = chat_gpt(prompt), weather_data=weather_data, rounded_temp=rounded_temp)