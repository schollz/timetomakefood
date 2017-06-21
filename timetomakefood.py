from flask import Flask
from flask import render_template, request,redirect
app = Flask(__name__)

from lib.recipes import * 

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello(path):
    if path == "":
        return redirect("/grilled cheese sandwich/", code=302)
    if path[-1] != "/":
        return redirect(path + "/", code=302)
    ingredients = path.split("/")
    main_ingredient = ingredients[0]
    other_ingredients = []
    if len(ingredients) > 2:
        other_ingredients = ingredients[1:-1]
    n = RecipeNetwork()
    return render_template('main.html', recipe=n.generate_recipe(main_ingredient,other_ingredients))