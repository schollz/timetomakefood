import random
import time
from os import mkdir
from os.path import isfile, join
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


try:
    mkdir("cache")
except:
    pass
first_time_users = {}
n = RecipeNetwork()

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
    if isfile(cache_file):
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
    return render_template('main2.html', recipe=recipe, graphviz=n.generate_graphviz(ingredients), other_recipes=CURRENT_RECIPES,first_time_user=first_time_user)

if __name__ == "__main__":
    from waitress import serve
    serve(app, listen='*:8082')
