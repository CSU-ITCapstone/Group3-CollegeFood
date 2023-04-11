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
    # playing around with the html templates nyeisha worked on
    return render_template("index.html")

# when you go to this url everything in the function is run. 
# It may be better to to get the data setup outside of the function
# maybe we can have an html template that is just for displaying the data and render it on whichever page we need it.
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


    # calls the html file apiTesting.html, then tells the html file that the variable apidata
    # inside of the file is equal to the dectionary section "hints". Using hints allows us to see
    # all the foods related to what was searched
    return render_template("apiTesting.html", apidata = dict["hints"])
    


if __name__ == '__main__':
    app.run(debug = True)

