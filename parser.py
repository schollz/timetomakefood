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

class Recipes:
    
    def __init__(self):
        self.recipes = {}
        with open('recipes.yaml', 'r') as f:
            self.recipes = yaml.load(f)
        for key in self.recipes.keys():
          self.recipes[key]['name'] = key
        self.ureg = UnitRegistry()
        self.ureg.define('whole = 1 * dimensionless')
        self.constant_time_operations = ['boil','heat','saute','set','rise','bake','cool'] 

    def _getPintString(self, pint):
        """Stringifying for the units
        """
        return '{!s}'.format(pint)

    def getFullJSON(self,name,servings):
        r = self._makeYaml(self.recipes[name],servings)
        r['name'] = name
        return r
        
    def _makeYaml(self, recipe, servings=1):
        """Recursively generates a new JSON

        This JSON contains all the key recipes it can find in the original recipe

        Input:

            recipe = root node of the recipe of interest
            servings = number of servings

        """
        if 'makes' in recipe:
            recipe['makes'] = self._getPintString(
                self.ureg.parse_expression(recipe['makes']) * servings)
        if 'time' in recipe:
            if 'operation' in recipe and recipe['operation'] in self.constant_time_operations:
                pass
            else:
                recipe['time'] = self._getPintString(
                    self.ureg.parse_expression(recipe['time']) * servings)
        for i in range(len(recipe['ingredients'])):
            ingredient = recipe['ingredients'][i]
            if 'name' in ingredient and ingredient['name'] in self.recipes.keys():
                multiplier = 1
                if 'quantity' in ingredient:
                    multiplier = (self.ureg.parse_expression(ingredient['quantity']) / self.ureg.parse_expression(
                        self.recipes[ingredient['name']]['makes'])).magnitude
                recipe['ingredients'][i] = self._makeYaml(
                    self.recipes[ingredient['name']],
                    servings * multiplier)
            if 'quantity' in ingredient:
                ingredient['quantity'] = self._getPintString(
                    self.ureg.parse_expression(ingredient['quantity']) * servings)
            if 'ingredients' in ingredient:
                recipe['ingredients'][i] = self._makeYaml(
                    recipe['ingredients'][i], servings)
        return recipe

    
book = Recipes()
recipe = book.getFullJSON('bread', 1)

print(json.dumps(recipe, sort_keys=True, indent=4))


from tree import Tree
import uuid 
(_ROOT, _DEPTH, _BREADTH) = range(3)

tree = Tree()

def makeTree(r):
    t = Tree()
    root = json.dumps({'node':'uuidroot'})
    t.add_node(root)
    recurseTree(t,r,root)
    return t
    
def recurseTree(t,r,root,):
    newroot = json.dumps({'node':'uuid' + str(uuid.uuid4())})
    r2 = copy.deepcopy(r)
    hasNextIngredient = False
    if 'ingredients' in r.keys():
        t.add_node(newroot,root)
        for i in range(len(r['ingredients'])):
            if 'ingredients' in r['ingredients'][i].keys():
                hasNextIngredient = True
        if not hasNextIngredient:
            newroot2 = json.dumps({'node':'uuid' + str(uuid.uuid4())})
            t.add_node(newroot2,newroot)
        for i in range(len(r['ingredients'])):
            recurseTree(t,r['ingredients'][i],newroot)  
    r2.pop("ingredients", None)
    if 'operation' in r2.keys():
        t.add_node(json.dumps(r2),newroot)
    else:
        t.add_node(json.dumps(r2),root)

tree = makeTree(recipe)
root = json.dumps({'node':'uuidroot'})
tree.display(root)

arr = {}
tree.list(root, arr)
start = min(arr.keys())
lastFoods = []
currentFoods = []
newFood = ""
currentOperation = ""
makes = ""
stepNum = 0
for i in range(start,-1):
    for item in arr[i]:
        item = json.loads(item)
        if 'name' in item.keys() and 'quantity' in item.keys():
            stepNum += 1
            if len(currentFoods)>0:
                print(str(stepNum) + '. Mix ' + item['quantity'] + ' of ' + item['name'] + ' with the ' + ' and '.join(currentFoods))
            elif len(lastFoods) > 0:
                print(str(stepNum) + '. Mix ' + item['quantity'] + ' of ' + item['name'] + ' with the ' + ' and '.join(lastFoods))        
            else:
                print(str(stepNum) + '. Take ' + item['quantity'] + ' of ' + item['name'])
            currentFoods.append(item['name'])
        if 'operation' in item.keys():
            currentOperaiton = ""
            if 'info' in item.keys():
              currentOperation = item['info'].title() + '. '
            currentOperation += item['operation'].title()
            if 'time' in item.keys():
                currentOperation += ' for ' + item['time']
                if 'name' in item.keys():
                  currentOperation += ' to make ' + item['name']
        if 'makes' in item.keys() and 'name' in item.keys():
            makes = 'Makes ' + item['makes'] + ' ' + item['name']
            newFood = item['name']
    lastFoods = currentFoods
    if len(currentOperation)>0:
        stepNum += 1
        print(str(stepNum) + '. ' + currentOperation)
        currentOperation = "" 
        currentFoods = []
        currentFoods.append(newFood)
print(makes)