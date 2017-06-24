import os
import json
from operator import itemgetter
import hashlib
import logging
logger = logging.getLogger('timetomakefood.recipes')


import toml
from networkx import DiGraph, all_simple_paths, shortest_path, dag_longest_path
import pint
from unidecode import unidecode
ureg = pint.UnitRegistry()

import lib.duration as duration
from lib.fractions import *

def md5(s):
    return str(hashlib.md5(s.encode('utf-8')).hexdigest())


class RecipeNetwork(object):
    """A network of recipes

    Attributes:
      ?
    """

    def __init__(self):
        """Return a RecipeNetwork object"""
        self.load_recipes()

    def load_recipes(self):
        self.all_recipes = toml.load(open('datav2/data.toml', 'r'))['recipe']
        self.recipe_has_data = {}
        for recipe in self.all_recipes:
            for product in recipe['product']:
                self.recipe_has_data[product['name']] = True
        for recipe in self.all_recipes:
            for reactant in recipe['reactant']:
                if reactant['name'] not in self.recipe_has_data:
                    self.recipe_has_data[reactant['name']] = False

    def generate_graphviz(self, recipes):
        name = md5(json.dumps(sorted(recipes)))
        if os.path.isfile("./static/img/graph/%s.png" % name):
            return name
        all_recipes = []
        for recipe in self.all_recipes:
            for product in recipe['product']:
                if product['name'] in recipes:
                    all_recipes.append(recipe)

        graphviz = ["digraph G { \ngraph [ dpi = 300 ];\nbgcolor=transparent;\ntruecolor=true; \n"]
        all_reactants = []
        all_products = []
        for recipe in all_recipes:
            products = []
            for product in recipe['product']:
                if product['name'] not in products:
                    products.append('"%s"' % product['name'])
                    all_products.append(product['name'])
            for reactant in recipe['reactant']:
                reactants = []
                if reactant['name'] not in reactants:
                    reactants.append('"%s"' % reactant['name'])
                    all_reactants.append(reactant['name'])
                graphviz_string = "\t{ " + " ".join(
                    reactants) + "} -> { " + " ".join(products) + " };\n"
                if graphviz_string not in graphviz:
                    graphviz.append(graphviz_string)

        all_products = list(set(all_products))
        for reactant in list(set(all_reactants)):
            if reactant not in all_products:
                graphviz.append('\n"{}" [fillcolor=tomato, style=filled]'.format(reactant))
            else:
                graphviz.append('\n"{}" [fillcolor=palegoldenrod, style=filled]'.format(reactant))
                
        graphviz.append('\n"{}" [fillcolor=springgreen, style=filled]'.format(recipes[0]))
        graphviz.append("}")

        with open("temp-%s" % name, "w") as f:
            f.write("".join(graphviz))

        os.system("dot -O -Tpng temp-%s" % name)
        os.remove("temp-%s" % name)
        try:
            os.rename("./temp-%s.png" %
                      name, "./static/img/graph/%s.png" % name)
        except:
            pass
        return name

    def generate_graph(self, recipes):
        """Generate a network of recipes with edges weighted by the time to create the recipe"""
        self.generate_graphviz(recipes)
        all_recipes = []
        for recipe in self.all_recipes:
            for product in recipe['product']:
                if product['name'] in recipes:
                    all_recipes.append(recipe)

        G = DiGraph()
        # Add nodes
        for recipe in all_recipes:
            for product in recipe['product']:
                if product['name'] not in G.nodes():
                    G.add_node(product['name'])
            for reactant in recipe['reactant']:
                if reactant['name'] not in G.nodes():
                    G.add_node(reactant['name'])

        # Determine times to make each reactant
        self.time_to_make = {}
        for recipe in all_recipes:
            how_long = duration.from_str(recipe['time']).total_seconds()
            for product in recipe['product']:
                if product['name'] not in self.time_to_make:
                    self.time_to_make[product['name']] = duration.from_str(
                        recipe['time']).total_seconds()

        # Add edges
        for recipe in all_recipes:
            how_long = duration.from_str(recipe['time']).total_seconds()
            for product in recipe['product']:
                for reactant in recipe['reactant']:
                    G.add_edge(product['name'], reactant[
                               'name'], weight=how_long)

        return G

    def determine_ordering(self, recipes, final_recipe):
        """
        Input:
          recipes = ["salt","cheese sandwich"]
          final_recipe = "grilled cheese sandwich"
        Output:
          ["salt","cheese sandwich","grilled cheese sandwich"]
        """
        G = self.generate_graph(recipes + [final_recipe])

        graph_traversal = []
        for starting_recipe in recipes:
            if starting_recipe not in G.nodes():
                continue
            for path in all_simple_paths(G, source=final_recipe, target=starting_recipe):
                path_length = 0
                for node in path:
                    if node in self.time_to_make:
                        path_length += self.time_to_make[node]
                graph_traversal.append(
                    (starting_recipe, path_length, len(path)))

        recipe_ordering = []
        import operator
        recipe_ordering.append(final_recipe)
        for item in sorted(graph_traversal, key=itemgetter(1, 2), reverse=False):
            if item[0] not in recipe_ordering:
                recipe_ordering.append(item[0])
        return recipe_ordering

    def combine_recipes(self, recipes):
        new_recipe = {'reactants': {}, 'instructions': [], 'seconds': 0}
        instruction_count = 1
        for recipe_to_add in reversed(recipes):
            for recipe in self.all_recipes:
                found_it = False
                for product in recipe['product']:
                    if product['name'] == recipe_to_add:
                        found_it = True
                        break
                if not found_it:
                    continue
                for reactant in recipe['reactant']:
                    try:
                        amount = reactant[
                            'number'] * ureg.parse_expression(reactant['measure'])
                    except:
                        amount = reactant['number']
                    if reactant['name'] not in new_recipe['reactants']:
                        new_recipe['reactants'][reactant['name']] = amount
                    else:
                        new_recipe['reactants'][reactant['name']] += amount
                subrecipe = {'name': recipe_to_add, 'instructions': []}
                for instruction in recipe['directions'].replace('Â', '').split("\n"):
                    if len(instruction.strip()) == 0:
                        continue
                    subrecipe['instructions'].append(
                        {'text': instruction, 'count': instruction_count})
                    instruction_count += 1
                new_recipe['instructions'].append(subrecipe)
                new_recipe[
                    'seconds'] += duration.from_str(recipe['time']).total_seconds()
                break
        # Remove all the products
        for recipe_to_add in recipes:
            if recipe_to_add in new_recipe['reactants']:
                new_recipe['reactants'].pop(recipe_to_add, None)
        return new_recipe

    def generate_recipe(self, main_reactant, other_reactants):
        recipes_to_combine = self.determine_ordering(
            other_reactants, main_reactant)
        logger.debug(recipes_to_combine)
        finished = self.combine_recipes(recipes_to_combine)
        recipe = {}
        recipe['name'] = main_reactant
        recipe['time'] = duration.get_total_time_string(finished['seconds'])
        recipe['reactants'] = []
        for reactant, amount in finished['reactants'].items():
            try:
                amount_str = "{} {}".format(get_fraction(amount.magnitude),amount.units)
            except:
                amount_str = "{} whole".format(get_fraction(amount))
            recipe['reactants'].append(
                {"amount": amount_str, "name": reactant, 'has_data': self.recipe_has_data[reactant]})
        recipe['instructions'] = []
        for instruction in finished['instructions']:
            recipe['instructions'].append(instruction)
        return recipe
