from flask import Blueprint, render_template
from openai import OpenAI

views = Blueprint(__name__, "views")

client = OpenAI()

def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


@views.route("/")
def home():
    return render_template("index.html", funFact = chat_gpt("Tell me a fun fact"))