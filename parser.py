import json
import copy
import yaml
from pint import UnitRegistry
ureg = UnitRegistry()
ureg.define('whole = 1 * dimensionless')
recipes = {}
with open('recipes.yaml','r') as f:
    recipes = yaml.load(f)
        
def recurseIngredients(recipe,directions):
    if 'ingredients' not in recipe:
        print(recipe)
        return recipe['quantity'] + ' of ' + recipe['name']
    else:
        directions += recipe['operation'] + ' '
        new_ingredients = []
        for i in range(len(recipe['ingredients'])):
            if recipe['ingredients'][i]['name'] in recipes.keys():  
                new_recipe = copy.deepcopy(recipes[recipe['ingredients'][i]['name']])
                new_ingredients.append(recurseIngredients(new_recipe,directions))
            else:
                new_ingredients.append(recurseIngredients(recipe['ingredients'][i],directions))
        directions += ' and '.join(new_ingredients) + '\n'
    return directions
        
def getPintString(pint):
    return '{!s}'.format(pint)
        
def makeYaml(recipe,servings):
    if 'makes' in recipe:
        recipe['makes'] = getPintString(ureg.parse_expression(recipe['makes']) * servings)
    if 'time' in recipe:
        recipe['time'] = getPintString(ureg.parse_expression(recipe['time']) * servings)
    for i in range(len(recipe['ingredients'])):
        ingredient = recipe['ingredients'][i]
        if 'name' in ingredient and ingredient['name'] in recipes.keys(): 
            multiplier = 1
            if 'quantity' in ingredient:
                multiplier = (ureg.parse_expression(ingredient['quantity'])/ureg.parse_expression(recipes[ingredient['name']]['makes'])).magnitude
            recipe['ingredients'][i] = makeYaml(recipes[ingredient['name']],servings*multiplier)
        if 'quantity' in ingredient:
            ingredient['quantity'] =getPintString(ureg.parse_expression(ingredient['quantity']) * servings)
        if 'ingredients' in ingredient:
            recipe['ingredients'][i] = makeYaml(recipe['ingredients'][i],servings)
    return recipe
            
print(json.dumps(makeYaml(recipes['rice'],1), sort_keys=True,indent=4))
print(json.dumps(makeYaml(recipes['bread'],2), sort_keys=True,indent=4))
