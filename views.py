import os

import openai
from dotenv import load_dotenv
from flask import Blueprint, render_template
from openai import OpenAI

views = Blueprint(__name__, "views")

load_dotenv()
#client = OpenAI()
openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_gpt(prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


@views.route("/")
def home():
    return render_template("index.html", funFact = chat_gpt("Tell me a fun fact"))