# Columbus State University Food Nutrition
# Godwin Jaja, Forest McDonald, Kristen Odum, Nyeisha Pace
# WebApp where users can find the nutrition values of food
# and find recipes based on their selected filters.

# Imports
from flask import Flask
from flask import render_template
import urllib.request, json

app = Flask(__name__)

@app.route("/")
def home():
    return "Columbus State Nutrition"

@app.route("/apiTesting")
def api_testing():

    # URL for connecting to Step 1 of the Api, includes app id and api key
    url = "https://api.edamam.com/api/food-database/v2/parser?app_id=d84791b8&app_key=498065e3b390e613e11cc5d5424eebce"

    # opens the URL
    response = urllib.request.urlopen(url)
    # reads the data
    data = response.read()
    # stores the data in a dictionary
    dict = json.loads(data)

    # calles the html file apiTesting.html not sure what is happening after that yet. UPDATE 
    # It doesn't give an error yet but it will load just with nothing on screen
    return render_template ("apiTesting.html", parsed = dict["parsed"])


if __name__ == '__main__':
    app.run(debug = True)

