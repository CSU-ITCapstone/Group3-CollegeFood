# Columbus State University Food Nutrition
# Godwin Jaja, Forest McDonald, Kristen Odum, Nyeisha Pace
# WebApp where users can find the nutrition values of food
# and find recipes based on their selected filters.

# Imports
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "Columbus State Nutrition"



