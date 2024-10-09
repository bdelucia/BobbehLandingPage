import os
import openai
import math
import random
from dotenv import load_dotenv
from flask import Blueprint, render_template, request, redirect, url_for
import requests

# Flask blueprint loading
views = Blueprint(__name__, "views")

# Getting keys from secret python env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key
openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")
fact_api_key = os.getenv("API_NINJAS_KEY")

def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweather_api_key}&units=imperial"
    response = requests.get(url)
    return response.json()

def get_news():
    url = (
        'https://newsapi.org/v2/top-headlines?'
        'country=us&'
        'category=science&'
        f'apiKey={news_api_key}'
    )
    response = requests.get(url)
    news_data = response.json()

    # Get the top 5 articles
    articles = [article for article in news_data['articles'] if '[Removed]' not in article['title']]
    return articles[:5] if articles else []

def get_fun_fact():
    url = 'https://api.api-ninjas.com/v1/facts?'
    response = requests.get(url, headers={'X-Api-Key': fact_api_key})
    fact = response.json()
    return fact[0]['fact']

def get_api_responses():
    # API responses
    weather_data = get_weather_data("85308")
    rounded_temp = math.ceil(weather_data["main"]["temp"]) # Rounds temperature up to whole number for better presentation
    funFact = get_fun_fact()
    news_articles = get_news()
    return weather_data, rounded_temp, funFact, news_articles

@views.route('/process_prompt', methods=['POST'])
def process_prompt():
    prompt = request.form.get('prompt')

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens = 100
    )

    response = response.choices[0].message.content.strip()
    return redirect(url_for('views.home', response=response))

# Renders index.html with passed arguments
@views.route("/")
def home():
    weather_data, rounded_temp, funFact, news_articles = get_api_responses()
    response = request.args.get('response', None)
    return render_template("index.html", funFact = funFact, weather_data=weather_data, rounded_temp=rounded_temp, news_articles=news_articles, response=response)
