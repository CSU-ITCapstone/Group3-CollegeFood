# Columbus State University Food Nutrition
# Godwin Jaja, Forest McDonald, Kristen Odum, Nyeisha Pace
# WebApp where users can find the nutrition values of food
# and find recipes based on their selected filters.

# Imports
from flask import Flask, render_template, request
import json
from flatten_json import flatten
# for taking the data from the api
from requests import Session #request,
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    # playing around with the html templates nyeisha worked on
    return render_template("index.html")

@app.route("/searchFood", methods = ['POST', 'GET'])
def search_food():
    #retriving the user input from the html file
    if request.method == "GET":
        return render_template("form.html")

def get_parser_data():

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
        parser_data = json.loads(text)

        # Flatten the parser data
        parser_data = flatten(parser_data)

        return parser_data

# args: data, use parser_data
def create_label_array(data):

        # Store all the food labels in an array, we can eaisly display this data 
        #global food_label_array
        food_label_array = []
        food_label_array.clear()
        for key, label in data.items():
            if "hints" in key and "food_label" in key:
                food_label_array.append(label)
        
        return food_label_array

# this function takes food_label_array and parser_data as args and returns an array of the measures for the selected food
# this will let us list the measures for the user to select
# args: label_array, use food_label_array | data, use parser_data | food, use the clicked_food from the url
def create_measures_array(label_array, data):
    
    if request.method == "GET":
        
        global clicked_food
        clicked_food = request.args.get("clickedFood")

        food_label_index = label_array.index(clicked_food)
        measures_string = "hints_{}_measures".format(food_label_index)

        # when user clicks a food label we return that label and search the array for the 
        # index of selected food 

        #global food_measures_array
        food_measures_array = []
        food_measures_array.clear()
        for key, value in data.items():
            if measures_string in key and "label" in key and "qualified" not in key:
                food_measures_array.append(value)
      
        return food_measures_array
    
# Will get the uri by taking the measure arry and label arry to get the index of both
# to format the search string properly
# args: measures_array, give food_measures_array | label_array, give food_label_array | data, give parser_data
def get_measures_uri(measures_array, label_array, data):

    clicked_measure = request.args.get("clickedMeasure")

    food_label_index = label_array.index(clicked_food)
    food_measure_index = measures_array.index(clicked_measure)

    food_uri = data["hints_{}_measures_{}_uri".format(food_label_index, food_measure_index)]

    return food_uri
    
# this function takes the parser_data and food_label_array and gets the foodId based on what the user clicked
# args: data, use parser_data | label_array, use food_label_array
def get_foodId(label_array, data):

    food_label_index = label_array.index(clicked_food)
    food_Id = data["hints_{}_food_foodId".format(food_label_index)]
    return food_Id
    
# this sunction takes parser_data and food_label_array and gets the image link for the selected food
# args: data, use parser_data | label_array, use food_label_array
def get_food_image(label_array, data):

    clicked_food = request.args.get("clickedFood")
    food_label_index = label_array.index(clicked_food)

    food_image = data["hints_{}_food_image".format(food_label_index)]

    return food_image

# will get the nutrition information for the selected measure of food
# args: uri, get_food_uri | food_Id, get_foodId
def get_nutrition_data(uri, food_Id):

    # this is a paramater that is passed to the api as json. 
    nutrition_ingredients = {
          "ingredients": [
            {
              "quantity": 1, # quantity of one because we are giving the nutrients of one serving of food
              "measureURI": uri,
              "qualifiers": [
                ""
              ],
              "foodId": food_Id
            }
          ]
        }
    headers = {
            'Accepts' : 'application/json',
            'content-type' : 'application/json'
        }
    nutrition_paramaters = {
        'app_id' : 'd84791b8',
        'app_key' : '498065e3b390e613e11cc5d5424eebce'
    }

    # Setup for the second part of the api call, nutrients
    nutrients_url = "https://api.edamam.com/api/food-database/v2/nutrients"

    # here we POST our json data, nutrition_ingredients, to the API. it returns with more json data.
    session = Session()
    nutrition_response = session.post(nutrients_url, headers = headers, params = nutrition_paramaters, json = nutrition_ingredients)
    nutrition_data = nutrition_response.json()

    # Flatten the json data
    nutrition_data = flatten(nutrition_data)

    return nutrition_data


@app.route("/searchFood/returnedFood", methods = ['POST', 'GET'])
def returnedFood_main():
    global parser_data
    parser_data = get_parser_data()
    global food_label_array
    food_label_array = create_label_array(parser_data)
    
    return render_template("apiTesting.html", 
                        parser_data = parser_data,
                        food_label_array = food_label_array                            
                        )

@app.route("/searchFood/returnedFood/foodMeasures", methods = ['POST', 'GET'])
def foodMeasures_main():
    global food_measures_array
    food_measures_array = create_measures_array(food_label_array, parser_data)
    
    return render_template("foodMeasures.html", food_measures_array = food_measures_array)

@app.route("/searchFood/returnedFood/foodMeasures/foodNutrition", methods = ['POST', 'GET'])
def foodNutrition_main():

    measure_uri = get_measures_uri(food_measures_array, food_label_array, parser_data)
    food_Id = get_foodId(food_label_array, parser_data)

    nutrition_data = get_nutrition_data(measure_uri, food_Id)

    return render_template("foodNutrition.html", nutrition_data = nutrition_data)

if __name__ == '__main__':
    app.run(debug = True)
