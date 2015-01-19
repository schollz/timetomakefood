# Formatting

Recipes are collections of ingredients and operations.

Ingredient/recipe:

```yaml
ingredient:
 name: NAME
 amount: NUMBER UNIT
 class: GENERAL NAME (optional, used on ingredient leafs)
```

Operations act on encapsulated ingredient or operation:

```yaml
cook:
 type: (nuke, saute, fry, bake, boil, bake)
 temp: NUMBER UNIT OR setting (optional)
 time: NUMBER UNIT
 (ingredient)
 
mix:
 (ingredient1)
 (ingredient2)
 ...
 (ingredientN)

cut:
 type: (chop, slice, grate)
 pieces: NUMBER UNIT (optional)
 (ingredient)

set:
 type: (drain, cool) (optional)
 time: NUMBER UNIT
 (ingredient)
```

# Grammar rules

If the ```ingredient``` does not exist in YAML list, then first search to see if the ```ingredient.class``` exists and use one of those at random from YAML list. If that doesn't exist either, then find the closest thing in the SR27 database. Things from the SR27 have time of 0 since they are assumed to be already purchased/premade.

Total times are calculated by adding all the operation times.

Total nutrition is calculated by adding all the ingredients nutritions.

# Examples

```python
stream = open('recipes.yaml','r')
data = yaml.load(stream, yaml.SafeLoader)
print start_print_dict('grilled cheese sandwich',data,True)
```

Output:
```bash
To make 1 whole grilled cheese sandwich:

Take 1000 g white flour and 720 g water
Mix them together
Set for 30 minute
Take 4 g yeast and 21 g salt
Mix them together
Set for 4 hour
bake at 475 F for 40 minute

Take 1/5 whole white bread
slice into 2 slices
Take 1 slice cheese
Mix them together

Take 1 whole cheese sandwich and 2 tbl oil
Mix them together
fry at high for 1 minute
```
