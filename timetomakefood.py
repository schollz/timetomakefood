import random 

from flask import Flask
from flask import render_template, request, redirect
app = Flask(__name__)

from lib.recipes import *

CURRENT_RECIPES = ['grilled cheese sandwich','cookies']

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello(path):
    if path == "":
        return redirect("/%s/" % random.choice(CURRENT_RECIPES).replace(' ','-'), code=302)
    if path[-1] != "/":
        return redirect(path + "/", code=302)
    ingredients = path.replace('-', ' ').split("/")
    main_ingredient = ingredients[0]
    other_ingredients = []
    if len(ingredients) > 2:
        other_ingredients = ingredients[1:-1]
    n = RecipeNetwork()
    other_recipes = CURRENT_RECIPES[:]
    other_recipes.remove(main_ingredient)
    return render_template('main2.html', recipe=n.generate_recipe(main_ingredient, other_ingredients), graphviz=n.generate_graphviz(ingredients), other_recipes=other_recipes)

if __name__ == "__main__":
    from waitress import serve
    serve(app, listen='*:8082')
