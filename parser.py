"""Parser for the recursive recipes
"""

import json
import copy
import sys
import uuid 

import yaml
from pint import UnitRegistry

from tree import Tree

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
        self.ureg.define('slice = 10 * grams')
        self.ureg.define('loaf = 500 * grams')
        self.ureg.define('tbl = 1 * tablespoon')
        self.constant_time_operations = ['boil','heat','saute','set','rise','bake','cool'] 

    def getRecipes(self):
        recipe_names = []
        for r in self.recipes.keys():
            recipe_names.append(r.title())
        return sorted(recipe_names)
        
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
        
    def makeRecipe(self, food, servings, time_limit):
        recipe = self.getFullJSON(food, int(servings))
        time_limit = self.ureg.parse_expression(time_limit)
        print('Time limit: ' + str(time_limit))
        (tree,root) = self._makeTree(recipe)
        #tree.display(root)
        arr = {}
        tree.list(root, arr)
        start = min(arr.keys())-1
        realStart = start+1
        totalTime = 1000*self.ureg.years
        while start<-1 and totalTime>time_limit:
          finalString = ""
          start += 1
          lastFoods = []
          currentFoods = []
          newFood = ""
          currentOperation = ""
          makes = ""
          stepNum = 0
          totalTime = self.ureg.parse_expression('0 hours')
          for i in range(realStart,-1):
              for item in arr[i]:
                  item = json.loads(item)
                  if 'time' in item.keys() and i>=start:
                      totalTime += self.ureg.parse_expression(item['time'])
                  if 'name' in item.keys() and 'quantity' in item.keys():
                      if i>= start:
                        stepNum += 1
                      if i>=start:
                        if len(currentFoods)>0:
                            finalString += ('\n' + str(stepNum) + '. Mix ' + str((self.ureg.parse_expression(item['quantity']))) + ' of ' + item['name'] + ' with the ' + ' and '.join(currentFoods))
                        elif len(lastFoods) > 0:
                            finalString += ('\n' + str(stepNum) + '. Mix ' + str((self.ureg.parse_expression(item['quantity']))) + ' of ' + item['name'] + ' with the ' + ' and '.join(lastFoods))        
                        else:
                            finalString += ('\n' + str(stepNum) + '. Take ' + str((self.ureg.parse_expression(item['quantity']))) + ' of ' + item['name'])
                      currentFoods.append(item['name'])
                  if 'operation' in item.keys():
                      currentOperaiton = ""
                      if 'info' in item.keys():
                        currentOperation += item['info'].capitalize()+ '. '
                      currentOperation += item['operation'].capitalize()+ ' '
                      if len(currentFoods) > 0 :
                        currentOperation += 'the ' + ' and '.join(currentFoods)
                      if 'time' in item.keys():
                          time_mag = self.ureg.parse_expression(item['time']).to(self.ureg.minutes)
                          if time_mag.magnitude > 108000:
                            time_mag = time_mag.to(self.ureg.months)
                          elif time_mag.magnitude > 3600:
                            time_mag = time_mag.to(self.ureg.days)
                          elif time_mag.magnitude > 60:
                            time_mag = time_mag.to(self.ureg.hours)
                          currentOperation += ' for ' +  str(round(time_mag))
                          if 'name' in item.keys():
                            currentOperation += ' to make ' + item['name']
                  if 'makes' in item.keys() and 'name' in item.keys():
                      makes = 'Makes ' + item['makes'] + ' ' + item['name']
                  if 'name' in item.keys():
                      newFood = item['name']
              lastFoods = currentFoods
              if len(currentOperation)>0:
                  if i>=start:
                    stepNum += 1
                    finalString += ('\n' + str(stepNum) + '. ' + currentOperation)
                  currentOperation = "" 
                  currentFoods = []
                  currentFoods.append(newFood)
          finalString += "\n" + str(makes) + "\n"
          if totalTime.magnitude < 1:
              finalString += str(round(totalTime.to(self.ureg.minutes)))
          elif totalTime.magnitude > 24:
              finalString += str(round(totalTime.to(self.ureg.days)))
          else:
              finalString += str(round(totalTime.to(self.ureg.hours)))
        return finalString
        

    def _makeTree(self,r):
        t = Tree()
        root = json.dumps({'node':'uuidroot'})
        t.add_node(root)
        self._recurseTree(t,r,root)
        return (t,root)
    
    def _recurseTree(self,t,r,root):
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
                self._recurseTree(t,r['ingredients'][i],newroot)  
        r2.pop("ingredients", None)
        if 'operation' in r2.keys():
            t.add_node(json.dumps(r2),newroot)
        else:
            t.add_node(json.dumps(r2),root)

            
