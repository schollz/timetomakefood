# Install

Installing requires Python 3.

To install use:

```
make
```

# Formatting

Recipes are collections of ingredients. Any ingredient can be composed of more ingredients using operations. Mix statements are redundant, so don't feel a need to include them as an extra step.

Ingredients at the highest level are template ingredients. Any recipe can use these ingredients, inheriting all their characteristics, unless otherwise modified.

## Example


# Todo

- BUG: When recipe returns nothing, tell user to buy ingredient
- BUG: When time is too short, tell user what ingredients they need to start (Add ingredient list?)
- Better README
- Add recipes
- Web server support (Flask?)
- Gnatt chart?
- Support for SR27 nutrients
