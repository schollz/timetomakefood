# Formatting

Recipes are collections of ingredients. Any ingredient can be composed of more ingredients using operations. Mix statements are redundant, so don't feel a need to include them as an extra step.

Ingredients at the highest level are template ingredients. Any recipe can use these ingredients, inheriting all their characteristics, unless otherwise modified.

## Example

```
grilled cheese sandwich:
  operation: fry
  info: set grill to medium-high
  time: 3 minutes
  ingredients:
    - 
      name: cheese sandwich
    -
      name: butter
      quantity: 1 tbl

cheese sandwich:
  operation: stack
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

Which should generate the following:

```
Grilled Cheese Sandwich

Take 1/8 loaf of bread. 
Slice the bread into sliced bread. Two pieces.
Stack 1 slice of cheese and the sliced bread to make a cheese sandiwch.
Fry the cheese sandwich with 1 tbl of oil for 3 minutes. Set grill to medium-high.
```

# Todo

1. Define fundamental ingredients
2. Add recipes
3. Support for SR27 nutrients
