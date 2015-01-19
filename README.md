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


YAML list: 

```yaml
grilled cheese sandwich:
 amount: 1 whole
 cook: 
  type: fry
  time: 1 minute
  heat: high
  mix:
   ingredient:
    - {name: cheese sandwich, amount: 1 whole}
    - {name: oil, amount: 2 tbl}
  
cheese sandwich:
 amount: 1 whole
 mix:
  cut:
   type: slice
   pieces: 2 slices
   ingredient:
    - {name: bread, amount: 1/5 whole}
  ingredient:
   - {name: cheese, amount: 1 slice}
  
white bread:
 class: bread
 amount: 2 whole
 cook:
   type: bake
   time: 40 minute
   temp: 475 F
   set:
    time: 4 hour
    mix:
     ingredient:
      - { name: yeast, amount: 4 g}
      - { name: salt, amount: 21 g}
     set:
      time: 30 minute
      mix:
       ingredient:
        - {name: white flour, amount: 1000 g}
        - {name: water, amount: 720 g}
        
grilled cheese sandwich:
 amount: 1 whole
 cook: 
  type: fry
  time: 1 minute
  heat: high
  mix:
   ingredient:
    - {name: cheese sandwich, amount: 1 whole}
    - {name: oil, amount: 2 tbl}
  
cheese sandwich:
 amount: 1 whole
 mix:
  cut:
   type: slice
   pieces: 2 slices
   ingredient:
    - {name: bread, amount: 1/5 whole}
  ingredient:
   - {name: cheese, amount: 1 slice}
  
wheat bread:
 class: bread
 amount: 2 whole
 cook:
   type: bake
   time: 40 minute
   temp: 475 F
   set:
    time: 4 hour
    mix:
     ingredient:
      - { name: yeast, amount: 4 g}
      - { name: salt, amount: 21 g}
     set:
      time: 30 minute
      mix:
       ingredient:
        - {name: white flour, amount: 600 g}
        - {name: wheat flour, amount: 400 g}
        - {name: water, amount: 720 g}
```

OLD:
BACKUS-NAUR:
```bash
<grilled-cheese-sandwich> = cook ( mix ( ^1^whole^<sandwich>, ^2^tbl^<oil> ), ^5^minute^, ^400^F^ )
<cheese-sandwich> = mix ( cut ( ^1/5^whole^<bread>, 2 ), <cheese> )
<bread> = cook ( set ( mix ( set ( mix ( ^1000^g^<white-flour>, cook ( ^720^g^<water>, ^1^minute^, ^95^F^ ) ), ^30^minute^ ), ^21^g^<salt>, ^4^g^<yeast> ), ^4^hour^ ), ^40^minute^, ^475^F^ )
<spaghetti> = mix( drain ( cook ( mix ( ^1^pound^<pasta>, ^500^ml^<water> ), ^10^minute^, ^200^F^ ), <sauce> )
<sauce> = <tomato-cream-sauce> | <roasted-red-pepper-sauce>
<tomato-cream-sauce> = mix( ^2^tbl^<olive-oil>, nuke(^2^tbl^<butter>, ^1^minute), chop(^1^whole^<onion>, 100) ,  chop(^1^whole^<tomato>, ^1^minute^) )
<roasted-red-pepper-sauce> = mix ( ^1^can^<tomato-sauce>, cook ( mix( chop( ^3^whole^<pepper>, 100), ^2^tbl^<olive-oil>), ^6^minute^, ^200^F^ ) )
<hard-boiled-egg> = chill ( drain ( cook ( mix ( ^1^whole^<raw-egg>, ^500^ml^<water> ), ^10^minute^, ^212^F^ ) ), ^10^minute^ )
<flour-tortilla> = cook ( chop ( set ( mix ( mix ( ^3^cup^<white-flour>, ^5^tbl^<oil> ), ^3/4^cup^<water> ), ^30^minute^ ), 12 ), ^20^minute^)
<cooked-oatmeal> = chill ( nuke ( mix ( ^1^cup^<oatmeal>, ^1^cup^<milk>, chop(^1^whole^<banana>, 6) ), ^3^minute^ ), ^1^minute^)
```
