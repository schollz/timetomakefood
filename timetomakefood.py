import random
import time
from os import mkdir
from os.path import isfile, join
import json
import textwrap

import sqlite3
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

CURRENT_RECIPES = ['tortilla', 'refried beans', 'grilled cheese sandwich','cookies', 'noodles', 'white sauce','loaf of bread','eggs benedict','english muffin', 'pancakes', 'mustard', 'mayonnaise']
n = RecipeNetwork()

try:
    mkdir("cache")
except:
    pass
first_time_users = {}

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello(path):

    start = time.time()
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
    cache_file = join("cache",md5(json.dumps(list(sorted(ingredients)))) + ".json")
    # n = RecipeNetwork()
    if isfile(cache_file) and True:
        logger.debug("Using cache {}".format(cache_file))
        recipe = json.load(open(cache_file))
    else:
        recipe = n.generate_recipe(main_ingredient, other_ingredients)
        with open(cache_file,'w') as f:
            f.write(json.dumps(recipe))
    logger.debug("{} {} {:2.0f} ms".format(request.remote_addr,path,1000*(time.time()-start)))
    first_time_user = True
    if request.remote_addr not in first_time_users:
        first_time_users[request.remote_addr] = time.time()
    else:
        if first_time_users[request.remote_addr] - time.time() > 60 * 60 * 72:
            first_time_users[request.remote_addr] = time.time()
        else:
            first_time_user = False
    return render_template('main2.html', recipe=recipe, graphviz=n.generate_graphviz(ingredients), other_recipes=CURRENT_RECIPES,first_time_user=first_time_user,url=path)



def parse_search_string(s):
    """
    Given a string like 
        +peanut butter -chocolate
    Returns
        - list to include
        - list to exclude
    """

    ings = (' '+s).replace(' +','zZz').replace(' -','zZz').split('zZz')
    include = []
    exclude = []
    for ing in ings:
        if len(ing) == 0:
            continue
        if '+'+ing in s:
            include.append(ing)
        if '-'+ing in s:
            exclude.append(ing)
    return include,exclude


def get_recipes(search_string, include_words=[], exclude_words=[]):
    conn = sqlite3.connect('recipes.sqlite3.db')
    c = conn.cursor()

    if include_words == [] and exclude_words == []:
        if len(search_string) < 5:
            conn.close()
            return [], []
        include_words, exclude_words = parse_search_string(search_string)
    sql_statements = []


    recipes = []
    if len(include_words)+len(exclude_words) == 0:
        conn.close()
        return [],[]

    sources_to_include = set()
    t = time.time()
    for row in c.execute("SELECT source FROM recipesearch WHERE ingredients MATCH '*%s*'" % "*".join(include_words)):
        sources_to_include.add(row[0])
    sources_to_include = list(sources_to_include)
    logger.debug("inclusive " + str(time.time()-t))

    sources_to_exclude = set()
    for word in exclude_words:
        sql_statement = '(instr(ingredients,"{w}") == 0 AND instr(name,"{w}") == 0)'.format(w=word)
        sql_statements.append(sql_statement)

    if len(sources_to_include) > 100:
        sources_to_include = sources_to_include[:100]
        random.shuffle(sources_to_include)
    sql_statement = "SELECT * FROM (SELECT * FROM recipes WHERE source=='{}') WHERE ".format("' OR source=='".join(sources_to_include)) + " AND ".join(sql_statements)
    recipes = []
    recipe_datas = []
    t = time.time()
    rows = c.execute(sql_statement)
    logger.debug("exclusive " + str(time.time()-t))
    t3 = time.time()
    for row in rows:
        t2 = time.time()
        source, name, ingredients, num_ingredients, instructions, ratingValue, ratingCount = row
        ingredients = json.loads(ingredients)
        instructions = json.loads(instructions)
        recipe_data = {}
        recipe_data['name'] = name.title()
        recipe_data['ingredients'] = ingredients
        recipe_data['instructions'] = instructions
        recipe_text = ""
        recipe_text += "-"*70 + "\n"
        recipe_text += name.title().center(70) + "\n\n"
        for i,ingredient in enumerate(ingredients):
            ingredient = "  \n   ".join(textwrap.wrap(ingredient.strip(),65))
            recipe_text += "   - {}\n".format(ingredient) 
        recipe_text += "\n"
        for i,instruction in enumerate(instructions):
            instruction = "  \n   ".join(textwrap.wrap(instruction.strip(),65))
            recipe_text += "  {}. {}\n".format(i+1,instruction)
        recipe_text += "\n"
        recipes.append(recipe_text)
        recipe_datas.append(recipe_data)
        logger.debug(time.time()-t2)
    logger.debug("parsed rows " + str(time.time()-t3))
    t = time.time()
    conn.close()
    logger.debug("closed " + str(time.time()-t))
    return recipes, recipe_datas

# import time
t2 = time.time()
get_recipes("",include_words=["cocoa","oat","milk","sugar"],exclude_words=["flour","egg","bread"])
print(time.time()-t2)

@app.route('/find')
def recipelist():
    message = ""
    exclude_words = []
    include_words = []
    for word in request.args.get('exclude',default='').split(','):
        word = word.lower().strip()
        if len(word) > 2:
            exclude_words.append(word)
    for word in request.args.get('include',default='').split(','):
        word = word.lower().strip()
        if len(word) > 2:
            include_words.append(word)
    logger.info(exclude_words)
    logger.info(include_words)
    logger.info(len(exclude_words) + len(include_words))
    if len(exclude_words) + len(include_words) > 2:
        recipes, recipes_data = get_recipes("", exclude_words=exclude_words, include_words=include_words)
    else:
        if len(exclude_words) + len(include_words) > 0:
            message = "Must include at least three ingredients"
        recipes, recipes_data = [],[]

    return render_template('recipes2.html', recipes=recipes_data, found_recipes=len(recipes_data)>0,include_words=", ".join(include_words),exclude_words=", ".join(exclude_words), message=message)

if __name__ == "__main__":
    from waitress import serve
    serve(app, listen='*:8082')
