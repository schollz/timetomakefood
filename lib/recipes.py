import json
from operator import itemgetter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import toml
from networkx import Graph, all_simple_paths, shortest_path
import pint 
from unidecode import unidecode
ureg = pint.UnitRegistry()

import lib.duration as duration

class RecipeNetwork(object):
    """A network of recipes

    Attributes:
      ?
    """

    def __init__(self):
        """Return a RecipeNetwork object""" 
        self.load_recipes()
        self.generate_graph()

    def load_recipes(self):
      self.all_recipes = toml.load(open('datav2/data.toml','r'))['recipe']
      self.recipe_has_data = {}
      for recipe in self.all_recipes:
        for product in recipe['product']:
          self.recipe_has_data[product['name']] = True
      for recipe in self.all_recipes:
        for ingredient in recipe['ingredient']:
          if ingredient['name'] not in self.recipe_has_data:
            self.recipe_has_data[ingredient['name']] = False

    def generate_graph(self):
      """Generate a network of recipes with edges weighted by the time to create the recipe"""
      self.G = Graph()
      # Add nodes
      for recipe in self.all_recipes:
        for product in recipe['product']:
          if product['name'] not in self.G.nodes():
            self.G.add_node(product['name'])
        for ingredient in recipe['ingredient']:
          if ingredient['name'] not in self.G.nodes():
            self.G.add_node(ingredient['name'])
      
      # Determine times to make each ingredient
      self.time_to_make = {}
      for recipe in self.all_recipes:
        how_long = duration.from_str(recipe['time']).total_seconds()
        for product in recipe['product']:
          if product['name'] not in self.time_to_make:
            self.time_to_make[product['name']] = duration.from_str(recipe['time']).total_seconds()

      # Add edges
      for recipe in self.all_recipes:
        how_long = duration.from_str(recipe['time']).total_seconds()
        for product in recipe['product']:
          for ingredient in recipe['ingredient']:
            if ingredient['name'] in self.time_to_make: 
              how_long += self.time_to_make[ingredient['name']]
            self.G.add_edge(product['name'],ingredient['name'],weight=how_long)

    def determine_ordering(self, recipes,final_recipe):
      """
      Input:
        recipes = ["salt","cheese sandwich"]
        final_recipe = "grilled cheese sandwich"
      Output:
        ["salt","cheese sandwich","grilled cheese sandwich"]
      """

      path_lengths = {}
      for starting_recipe in recipes:
        path = shortest_path(self.G, source=starting_recipe, target=final_recipe)
        path_length = 0
        for i, node in enumerate(path):
          if i == 0: 
            continue
          path_length += self.G[path[i-1]][node]['weight']
        path_lengths[starting_recipe] = path_length + self.time_to_make[starting_recipe]

      recipe_ordering = []
      recipe_ordering.append(final_recipe)
      for recipe,path_length in sorted(path_lengths.items(), key=itemgetter(1), reverse=False):
        recipe_ordering.append(recipe)
      return recipe_ordering

    def combine_recipes(self,recipes):
      new_recipe = {'ingredients':{},'instructions':[],'seconds':0}
      for recipe_to_add in recipes:
        for recipe in self.all_recipes:
          found_it = False
          for product in recipe['product']:
            if product['name'] == recipe_to_add:
              found_it = True
              break 
          if not found_it:
            continue             
          for ingredient in recipe['ingredient']:
            print(recipe_to_add,ingredient)
            try:
              amount = ingredient['number'] * ureg.parse_expression(ingredient['measure'])
            except:
              print(ingredient['measure'])
              amount = ingredient['number']
            if ingredient['name'] not in new_recipe['ingredients']:
              new_recipe['ingredients'][ingredient['name']] = amount
            else:
              new_recipe['ingredients'][ingredient['name']] += amount
          new_recipe['instructions'] = recipe['directions'].split("\n") + new_recipe['instructions']
          new_recipe['seconds'] += duration.from_str(recipe['time']).total_seconds()
          break
      # Remove all the products
      for recipe_to_add in recipes:
        if recipe_to_add in new_recipe['ingredients']:
          print("REMOVING" + recipe_to_add)
          new_recipe['ingredients'].pop(recipe_to_add,None)
      return new_recipe

    def generate_recipe(self,main_ingredient,other_ingredients):
      recipes_to_combine = self.determine_ordering(other_ingredients,main_ingredient)
      finished = self.combine_recipes(recipes_to_combine)
      recipe = {}
      recipe['name'] = main_ingredient
      recipe['time'] = duration.get_total_time_string(finished['seconds'])
      recipe['ingredients'] = []
      for ingredient, amount in finished['ingredients'].items():
          recipe['ingredients'].append({"text":"{} {}".format(amount, ingredient),"name":ingredient,'has_data':self.recipe_has_data[ingredient]})
      recipe['instructions'] = [] 
      for instruction in finished['instructions']:
        if len(instruction.strip()) > 0:
          recipe['instructions'].append(instruction)
      print(recipes_to_combine)
      return recipe