# Formatting

Recipes are collections of ingredients. Any ingredient can be composed of more ingredients using operations. Mix statements are redundant, so don't feel a need to include them as an extra step.

Ingredients at the highest level are template ingredients. Any recipe can use these ingredients, inheriting all their characteristics, unless otherwise modified.

## Example

```
hard-boiled egg:
  operation: boil
  time: 10 min
  makes: 1 whole
  ingredients:
    -
      name: egg
      quantity: 1 whole
    -
      name: boiling water
      quantity: 6 cups
      
boiling water:
  operation: boil
  time: 5 min
  makes: 1 cup
  ingredients:
    -
      name: water
      quantity: 1 cup
```

Which should generate the following:

```
Hard-boiled egg
Makes 1 whole hard-boiled egg.

Boil 6 cups of water for 5 min to make boiling water. // The boiling recipe was multiplied by 6 cups / 1 cups as it inherited the new quantity
Mix 1 whole egg and 6 cups of boiling water.  // Mixing is implied when multiple ingredients exist
Boil for 10 minutes.  // operation
```

# Todo

1. Define fundamental ingredients
2. Add recipes
3. Support for SR27 nutrients
