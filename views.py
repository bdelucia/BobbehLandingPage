import os
import openai
import requests
import math
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
    return render_template("index.html", funFact = chat_gpt("Tell me a fun fact"), weather_data=weather_data, rounded_temp=rounded_temp)