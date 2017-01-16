# Recursive Recipes (v0.3)

## Axioms

1. Every recipe is composed of "*reactions*".
2. A recipe reaction has "*reactants*", "*products*", and "*directions*" .
3. The *reactants* is a list of ingredients that are needed to complete that reaction.
4. The *products* is a list of ingredients that come out of that reaction.
5. The *directions* is text that explains exactly how the process is transformed, e.g. how much of each ingredient, how long it will take, all the actions that need to be performed.
6. The same reactants and the same directions always create the same product. i.e. You can have the same reactants but different directions to produce a different product. Also the inverse is not nessecarily true: the same product can be made by different reactants (see bread dough, below).

## Example (grilled cheese)

This is the [recipe for a grilled cheese sandwich](http://www.foodnetwork.com/recipes/articles/50-grilled-cheese.html):

> Heat 1 tablespoon salted butter in a cast-iron or nonstick skillet over medium-low heat. 2. Press the sandwich slightly and place it in the skillet. Cook until golden on the bottom, 3 to 5 minutes. 3. Flip, adding more butter to the pan if needed, and cook until the other side is golden and the cheese melts, 3 to 5 more minutes.

The recipe reaction would be:

```json
[
  {
    "reactants": [
      "cheese_sandwich",
      "butter"
    ],
    "directions": "Heat 1 tablespoon salted butter in a cast-iron or nonstick skillet over medium-low heat. Press the sandwich slightly and place it in the skillet. Cook until golden on the bottom, 3 to 5 minutes. Flip, adding more butter to the pan if needed, and cook until the other side is golden and the cheese melts, 3 to 5 more minutes.",
    "products": [
      "grilled_cheese_sandwich"
    ]
  }
]
```



All recipe reactions can form a directed acyclic graph (DAG). A product has arrows leading toward it. The arrows represent directions. Arrows *should be colored* because different directions can lead to different products of the same reactants. The base of each arrow represents the reactants. For example, here is [the grilled cheese DAG](https://cowyo.com/grilled_cheese_sandwich_dag):

![](http://i.imgur.com/83YIFMC.png)


## Example (breads)

Axiom #6 allows recipes to be subdivided in order to be used for other recipes. For example, consider bread:

> Mix yeast, salt, water, flour into a dough. Let dough rise. Push down and form loaves. Put loaves in oven at 450F for 20 minutes.

This can be broken into two reactions:

```json
[  
   {  
      "reactants":[  
         "yeast",
         "flour",
         "salt",
         "water"
      ],
      "directions":"Mix yeast, salt, water, flour into a dough.",
      "products":[  
         "bread_dough"
      ]
   },
   {  
      "reactants":[  
         "bread_dough"
      ],
      "directions":"Let dough rise. Push down and form loaves. Put loaves in oven at 450F for 20 minutes.",
      "products":[  
         "bread"
      ]
   }
]
```

to which the DAG would be:

![](http://i.imgur.com/gimj9EY.png)

The advantage for this, is that you can then use different kinds of directions / reactants to create the same product. This is useful for when the same reactant and directions is used multiple times (in the case of bread dough and bread). For example, for Challah you would only need one more reaction:

```json
[  
   {  
      "reactants":[  
         "yeast",
         "flour",
         "salt",
         "water",
         "egg",
         "sugar",
      ],
      "directions":"Mix yeast, salt, water, flour, egg and sugar into a dough.",
      "products":[  
         "bread_dough"
      ]
   }
]
```

To which the [DAG for Challah/bread](https://cowyo.com/bread_dag) would look like:

![](http://i.imgur.com/1hwnBzC.png)

(since colored arrows indicate different directions).

# Full graph

Eventually, you can follow every product to the very beginning, in a [large DAG of all recipes](https://cowyo.com/recipe_reactions):

![](http://i.imgur.com/HlSDW1n.png)

