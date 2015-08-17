# Formatting

Recipes are collections of ingredients. Any ingredient can be composed of more ingredients using operations. Mix statements are redundant, so don't feel a need to include them as an extra step.

Ingredients at the highest level are template ingredients. Any recipe can use these ingredients, inheriting all their characteristics, unless otherwise modified.

## Example

```
name: grilled cheese sandwich
operation: fry
info: set grill to medium-high
time: 3 minutes
ingredients:
  - 
    name: cheese sandwich
  -
    name: butter
    quantity: 1 tbl

name: cheese sandwich
operation: stack
time: 3 min
ingredients:
  -
    name: cheese
    quantity: 1 slice
  -
    name: sliced bread
    operation: slice
    info: two pieces
    ingredients:
      -
        name: bread
        quantity: 1/8 loaf
```

# Todo

1. Define fundamental ingredients
2. Add recipes
3. Support for SR27 nutrients
