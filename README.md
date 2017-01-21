# Recursive Recipes (v0.3)

Current full graph:

![](https://timetomakefood.com/img/graph/all.png)

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

```toml
products = [
        "grilled_cheese_sandwich"
]

reactants = [
        "cheese_sandwich", 
        "butter", 
]

ingredients = """
1 cheese sandwich
1 tbl. butter
"""

directions = """
Heat 1 tablespoon salted butter in a cast-iron or nonstick skillet over medium-low heat. 
Press the sandwich slightly and place it in the skillet. 
Cook until golden on the bottom, 3 to 5 minutes. 
Flip, adding more butter to the pan if needed, and 
cook until the other side is golden and the cheese melts, 3 to 5 more minutes.
"""

time = "20m"
```

All recipe reactions can form a directed acyclic graph (DAG). A product has arrows leading toward it. The arrows represent directions. Arrows *should be colored* because different directions can lead to different products of the same reactants. The base of each arrow represents the reactants. For example, here is [the grilled cheese DAG](https://cowyo.com/grilled_cheese_sandwich_dag):

![](http://i.imgur.com/83YIFMC.png)


## Example (breads)

Axiom #6 allows recipes to be subdivided in order to be used for other recipes. For example, consider bread:

> Mix yeast, salt, water, flour into a dough. Let dough rise. Push down and form loaves. Put loaves in oven at 450F for 20 minutes.

This can be broken into two reactions:

```toml
products = [
        "bread_dough"
]

reactants = [
        "yeast", 
        "salt", 
        "water",
        "flour"
]

ingredients = """
1 tbl. yeast
760 g. water
1000 g. flour
20 g. salt
"""

directions = """
Mix warm water and flour together. Let it rest for 20 minutes. 
For foccia bread, add yeast to warm water seperately. 
For regular bread, add yeast to the top of the dough after 20 minutes.
Add the salt to the top of the dough and mix together.
Wet hands and knead in a big bowl. Cut with fingers several times and then let rest.
"""

time = "35m"
```
and

```toml
products = [
        "bread"
]

reactants = [
        "bread_dough"
]

ingredients = """
bread dough
"""

directions = """
Let the bread dough rest for 20 minutes. Then knead a little bit.
Let the bread rise for 4 to 6 hours. Then flour a small bowl and put loaf into bowl.
Let the bread rise again for 30 minutes, preheat a oven to 450F.
Bake the bread in a pre-heated dutch oven for 20 minutes. Take off the lid and bake for another 5-10 minutes.
Take out the bread and let it rest for 20 minutes.
"""

time = "6h50m"
```
to which the DAG would be:

![](http://i.imgur.com/gimj9EY.png)

The advantage for this, is that you can then use different kinds of directions / reactants to create the same product. This is useful for when the same reactant and directions is used multiple times (in the case of bread dough and bread). For example, for Challah you would only need one more reaction:

```toml
products = [
        "bread_dough"
]

reactants = [
        "yeast", 
        "salt", 
        "water",
        "flour",
        "egg",
        "sugar"
]

variant = "challah"

ingredients = """
1 1/2 packages active dry yeast (1 1/2 tablespoons)
1 tablespoon plus 1/2 cup sugar
1/2 cup vegetable oil, more for greasing bowl
5 large eggs
1 tablespoon salt
8 to 8 1/2 cups all-purpose flour
"""

directions = """
In a large bowl, dissolve yeast and 1 tablespoon sugar in 2 3/4 cups lukewarm water.
Whisk oil into yeast, then beat in 4 eggs, one at a time, with remaining sugar and salt. Gradually add flour. When dough holds together, it is ready for kneading. (You can also use a mixer with a dough hook for both mixing and kneading.)
"""

time = "30m"
```

To which the [DAG for Challah/bread](https://cowyo.com/bread_dag) would look like:

![](http://i.imgur.com/1hwnBzC.png)

In the case of Challah, there is a `variant` which is an optional declaration for specifying specific bundles of ingredients. In this case, this product `bread_dough` occurs twice. To distinguish `bread` for `bread_dough` that uses the Challah recipe, you must specify the variant in the final product. For example, for Challah, you would generate `bread` normally, but then override any products which have variant `challah` in them.


