import random 

from flask import Flask
from flask import render_template, request, redirect
app = Flask(__name__)

from lib.recipes import *

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.DEBUG)
logger = logging.getLogger('timetomakefood')

CURRENT_RECIPES = ['grilled cheese sandwich','cookies', 'noodles', 'tortilla']

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
    logger.info(path)
    n = RecipeNetwork()
    return render_template('main2.html', recipe=n.generate_recipe(main_ingredient, other_ingredients), graphviz=n.generate_graphviz(ingredients), other_recipes=CURRENT_RECIPES)

if __name__ == "__main__":
    from waitress import serve
    serve(app, listen='*:8082')
