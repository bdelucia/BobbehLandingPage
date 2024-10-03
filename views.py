import os
import openai
import math
import random
from dotenv import load_dotenv
from flask import Blueprint, render_template
import requests

# Flask blueprint loading
views = Blueprint(__name__, "views")

# Getting keys from secret python env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key
openweather_api_key = os.getenv("OPENWEATHER_API_KEY")

def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweather_api_key}&units=imperial"
    response = requests.get(url)
    return response.json()


def get_random_fun_fact_prompt():
    prompts = [
        "Tell me a unique fun fact about space in 50 words or less.",
        "What's an unusual fun fact about the solar system that isn't commonly known in 50 words or less",
        "Give me three unique fun facts about animals in 50 words or less.",
        "What are some surprising discoveries in science that changed our understanding of the world in 50 words or less?",
        "Tell me about an interesting event in history that most people don’t know about in 50 words or less.",
        "What’s a little-known fact about a famous person in 50 words or less?",
        "Tell me an unusual fact about a sports event or athlete that might surprise fans in 50 words or less.",
        "What is a fun fact about a popular dish that originated from a specific region in 50 words or less?",
        "What’s a fun fact about an invention that had unexpected consequences in 50 words or less?"
    ]
    return random.choice(prompts)

# Function to generate response from ChatGPT
def chat_gpt(prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        top_p=0.8
    )
    return response.choices[0].message.content.strip()

# Renders index.html with passed arguments
@views.route("/")
def home():
    weather_data = get_weather_data("85308")
    rounded_temp = math.ceil(weather_data["main"]["temp"]) # Rounds temperature up to whole number for better presentation
    prompt = get_random_fun_fact_prompt()
    return render_template("index.html", funFact = chat_gpt(prompt), weather_data=weather_data, rounded_temp=rounded_temp)
