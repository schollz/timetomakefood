"""Parser for the recursive recipes
"""

import json
import copy
import yaml
from pint import UnitRegistry

__author__ = "Zack Scholl"
__copyright__ = "Copyright 2015"
__credits__ = ["Zack Scholl", "Travis Scholl"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Zack Scholl"
__email__ = "zack@hypercubeplatforms.com"
__status__ = "Development"

ureg = UnitRegistry()
ureg.define('whole = 1 * dimensionless')


recipes = {}
with open('recipes.yaml', 'r') as f:
    recipes = yaml.load(f)


def getPintString(pint):
    """Stringifying for the units
    """
    return '{!s}'.format(pint)


def makeYaml(recipe, servings=1):
    """Recursively generates a new JSON

    This JSON contains all the key recipes it can find in the original recipe

    Input:

        recipe = root node of the recipe of interest
        servings = number of servings

    """
    if 'makes' in recipe:
        recipe['makes'] = getPintString(
            ureg.parse_expression(recipe['makes']) * servings)
    if 'time' in recipe:
        recipe['time'] = getPintString(
            ureg.parse_expression(recipe['time']) * servings)
    for i in range(len(recipe['ingredients'])):
        ingredient = recipe['ingredients'][i]
        if 'name' in ingredient and ingredient['name'] in recipes.keys():
            multiplier = 1
            if 'quantity' in ingredient:
                multiplier = (ureg.parse_expression(ingredient['quantity']) / ureg.parse_expression(
                    recipes[ingredient['name']]['makes'])).magnitude
            recipe['ingredients'][i] = makeYaml(
                recipes[ingredient['name']],
                servings * multiplier)
        if 'quantity' in ingredient:
            ingredient['quantity'] = getPintString(
                ureg.parse_expression(ingredient['quantity']) * servings)
        if 'ingredients' in ingredient:
            recipe['ingredients'][i] = makeYaml(
                recipe['ingredients'][i], servings)
    return recipe

print(json.dumps(makeYaml(recipes['rice'], 1), sort_keys=True, indent=4))
print(json.dumps(makeYaml(recipes['bread'], 2), sort_keys=True, indent=4))
