# Columbus State University Food Nutrition
# Godwin Jaja, Forest McDonald, Kristen Odum, Nyeisha Pace
# WebApp where users can find the nutrition values of food
# and find recipes based on their selected filters.

# Imports
from flask import Flask, render_template, request
import urllib.request, json
# for taking the data from the api
from requests import Session #request,

app = Flask(__name__)

@app.route("/")
def home():
    # playing around with the html templates nyeisha worked on
    return render_template("index.html")


@app.route("/searchFood", methods = ['POST', 'GET'])
def search_food():
    #retriving the user input from the html file
    if request.method == "GET":
        # the input is stored as food = searchedFood
        

        return render_template("form.html")

# when you go to this url everything in the function is run. 
# It may be better to to get the data setup outside of the function
# maybe we can have an html template that is just for displaying the data and render it on whichever page we need it.
@app.route("/apiTesting", methods = ['POST', 'GET'])
def api_testing():

    if request.method == "POST":

        # Take the user input from the html form and store it
        searched_food = request.form.get("searchedFood")

        # The API URL for connecting to Step 1, no api key or app id
        parser_url = "https://api.edamam.com/api/food-database/v2/parser?"

        # These are the paramaters the API takes. ingr is the food the the API searches
        paramaters = {
            'app_id' : 'd84791b8',
            'app_key' : '498065e3b390e613e11cc5d5424eebce',
            'ingr' : searched_food,
            'nutrition-type' : 'cooking'
        }
        headers = {
            'Accepts' : 'application/json',
            'content-type' : 'application/json'
        }

        session = Session()
        session.headers.update(headers)
        parser_Response = session.get(parser_url, headers = headers, params = paramaters)
        text = parser_Response.text
        global parser_data
        parser_data = json.loads(text)

        # Take the food id
        food_id = parser_data['hints'][0]['food']['foodId']

        # take the uri 
        measures = parser_data['hints'][0]['measures'][0]['uri']


        # this is a paramater that is passed to the api as json. 
        nutrition_ingredients = {
                      "ingredients": [
                        {
                          "quantity": 1, # quantity of one because we are giving the nutrients of one serving of food
                          "measureURI": measures,
                          "qualifiers": [
                            ""
                          ],
                          "foodId": food_id
                        }
                      ]
                    }

        # Setup for the second part of the api call, nutrients
        nutrients_url = "https://api.edamam.com/api/food-database/v2/nutrients"

        # The params for the second step are just the id and key
        nutrition_paramaters = {
            'app_id' : 'd84791b8',
            'app_key' : '498065e3b390e613e11cc5d5424eebce'
        }
        
        # here we POST our json data, nutrition_ingredients, to the API. it returns with more json data.
        nutrition_response = session.post(nutrients_url, headers = headers, params = nutrition_paramaters, json = nutrition_ingredients)
        nutrition_data = nutrition_response.json()

        # Here is the data stored in varibles for easy access
        measure_label = parser_data['hints'][0]['measures'] # Loop through this in html using 
        food_image = parser_data['hints'][0]['food']['image']
        calories = nutrition_data['calories']
        weight = nutrition_data['totalWeight']
        diet_labels = nutrition_data['dietLabels']
        health_labels = nutrition_data['healthLabels']
        cautions = nutrition_data['cautions']
        total_nutrients = nutrition_data['totalNutrients']


        # calls the html file apiTesting.html, then tells the html file that the variable apidata
        # inside of the file is equal to the dectionary section "hints". Using hints allows us to see
        # all the foods related to what was searched. These are all for testing
        return render_template("apiTesting.html",
                               measure_data = measure_label,
                               apidata = parser_data["hints"],
                               nutrition_data = nutrition_data,
                               calories = calories,
                               weight = weight,
                               searched_food = searched_food,
                               food_image = food_image)


if __name__ == '__main__':
    app.run(debug = True)
