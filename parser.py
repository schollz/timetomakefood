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
recipe = book.getFullJSON('bread', 4)

print(json.dumps(recipe, sort_keys=True, indent=4))


from tree import Tree
import uuid 
(_ROOT, _DEPTH, _BREADTH) = range(3)

tree = Tree()

tree.add_node('Harry')  # root node
tree.add_node("Bill", "Harry")
tree.add_node("Jane", "Harry")
tree.add_node("Joe", "Jane")
tree.add_node("Diane", "Jane")
tree.add_node("George", "Diane")
tree.add_node("Mary", "Diane")
tree.add_node("Jill", "George")
tree.add_node("Carol", "Jill")
tree.add_node("Grace", "Bill")
tree.add_node("Mark", "Jane")
tree.add_node("Bob", "Harry")

tree.display("Harry")

def makeTree(r):
    t = Tree()
    t.add_node('uuidroot')
    recurseTree(t,r,'uuidroot')
    return t
    
def recurseTree(t,r,root,):
    newroot = 'uuid' + str(uuid.uuid4())
    r2 = copy.deepcopy(r)
    if 'ingredients' in r.keys():
        t.add_node(newroot,root)
        hasNextIngredient = False
        for i in range(len(r['ingredients'])):
            if 'ingredients' in r['ingredients'][i].keys():
                hasNextIngredient = True
        if not hasNextIngredient:
            t.add_node('uuid' + str(uuid.uuid4()),newroot)
        for i in range(len(r['ingredients'])):
            recurseTree(t,r['ingredients'][i],newroot)  
    r2.pop("ingredients", None)
    t.add_node(json.dumps(r2),root)

tree = makeTree(recipe)
tree.display('uuidroot')

print("***** BREADTH-FIRST ITERATION *****")
traversed = []
for node in tree.traverse("uuidroot", mode=_BREADTH):
    print(node)
    if 'uuid' not in node:
        traversed.append(json.loads(node))


    
