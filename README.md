# Recursive Recipes (v0.3)

## Run

```
sudo apt-get install graphviz
go run run.go
```

# Ideas

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
    "directions": {
      "text":"Heat 1 tablespoon salted butter in a cast-iron or nonstick skillet over medium-low heat. Press the sandwich slightly and place it in the skillet. Cook until golden on the bottom, 3 to 5 minutes. Flip, adding more butter to the pan if needed, and cook until the other side is golden and the cheese melts, 3 to 5 more minutes.",
      "time":"10m"
    },
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
      "directions":{
        "text":"Mix yeast, salt, water, flour into a dough.",
        "time":"30m"
      },
      "products":[  
         "bread_dough"
      ]
   },
   {  
      "reactants":[  
         "bread_dough"
      ],
      "directions":{
        "text":"Let dough rise. Push down and form loaves. Put loaves in oven at 450F for 20 minutes.",
        "time":"8h"
      },
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
      "subtypes":[
        "challah"
      ],
      "reactants":[  
         "yeast",
         "flour",
         "salt",
         "water",
         "egg",
         "sugar",
      ],
      "directions":{
        "text":"Mix yeast, salt, water, flour, egg and sugar into a dough.",
        "time:":"20m"
      },
      "products":[  
         "bread_dough"
      ]
   }
]
```

To which the [DAG for Challah/bread](https://cowyo.com/bread_dag) would look like:

![](http://i.imgur.com/1hwnBzC.png)

In the case of Challah, there is a `subtypes` array which is an optional declaration for specifying specific bundles of ingredients. In this case, this product `bread_dough` occurs twice. To distinguish `bread` for `bread_dough` that uses the Challah recipe, you must specify the subtype in the final product. For example, for Challah, you would generate `bread` normally, but then override any products which have subtype `challah` in them.

# Full graph

Eventually, you can follow every product to the very beginning, in a [large DAG of all recipes](https://gist.github.com/schollz/c3614e5a53e782befd1822ffb4aa15dc):

![](http://i.imgur.com/qDNXaF0.png)

