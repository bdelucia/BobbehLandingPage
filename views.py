import os
import openai
import httpx
import math
import random
from dotenv import load_dotenv
from flask import Blueprint, render_template
import asyncio

# Flask blueprint loading
views = Blueprint(__name__, "views")

# Getting keys from secret python env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key
openweather_api_key = os.getenv("OPENWEATHER_API_KEY")

# Function to generate weather data
async def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweather_api_key}&units=imperial"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    # Check for errors
    if response.status_code != 200:
        print("Error response from OpenWeather API:", response.json())
        response.raise_for_status()

    # Check if 'main' key is in the response
    if 'main' not in response.json():
        print("KeyError: 'main' not found in weather data response")
        print("Full response:", response.json())
        raise KeyError("'main' key not found in weather data response")

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
async def chat_gpt(prompt):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.8,
        "top_p": 0.8
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)

    # Check for errors
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"].strip()

# Renders index.html with passed arguments
@views.route("/")
async def home():
    # Run tasks concurrently
    weather_data, fun_fact = await asyncio.gather(
        get_weather_data("85308"),
        chat_gpt(get_random_fun_fact_prompt())
    )
    rounded_temp = math.ceil(weather_data["main"]["temp"])  # Rounds temperature up to whole number for better presentation
    return render_template("index.html", funFact=fun_fact, weather_data=weather_data, rounded_temp=rounded_temp)
