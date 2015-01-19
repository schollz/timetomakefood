# Formatting
```bash
ingredient = ^NUMBER^UNIT^<food>
heat = ^NUMBER^UNIT^
time = ^NUMBER^UNIT^
chill ( ingredient, time )
mix ( ingredient1, ingredient2, .... ingredientN )
nuke ( ingredient, time )
cook ( ingredient, time, heat ) 
chop ( ingredient, time )
drain ( ingredient )
```

# Recipe grammar

If the ```<food>``` does not exist in this grammar table, find the closest thing in the SR27 database. I.e. "```<olive-oil>```" does not exist in the examples below, so those recipes will search for anything that has "olive" and "oil" in SR27 and use that.

Total times are calculated by adding all the operation times.

Total nutrition is calculated by adding all the ingredients nutritions.

Also note that ```cook``` is a little bit of a catch-all. I'm assuming if you mix something with a ton of water you want to boil it, if you mix it with a little oil then you want to saute it, otherwise its your discretion/common-sense.

## Oatmeal recipe
```bash
<cooked-oatmeal> = chill ( nuke ( mix ( ^1^cup^<oatmeal>, ^1^cup^<milk>, chop(^1^whole^<banana>, ^1^minute^) ), ^3^minute^ ), ^1^minute^)
```
## Spaghetti recipe with alternate sauces

```bash
<spaghetti> = mix( drain ( cook ( mix ( ^1^pound^<pasta>, ^500^ml^<water> ), ^10^minute^, ^200^F^ ), <sauce> )
<sauce> = <tomato-cream-sauce> | <roasted-red-pepper-sauce>
<tomato-cream-sauce> = mix( ^2^tbl^<olive-oil>, nuke(^2^tbl^<butter>, ^1^minute), chop(^1^whole^<onion>, ^1^minute^) ,  chop(^1^whole^<tomato>, ^1^minute^) )
<roasted-red-pepper-sauce> = mix ( ^1^can^<tomato-sauce>, cook ( mix( chop( ^3^whole^<pepper>, ^1^minute^), ^2^tbl^<olive-oil>), ^6^minute^, ^200^F^ ) )
```

```bash
<hard-boiled-egg> = chill ( drain ( cook ( mix ( ^1^whole^<raw-egg>, ^500^ml^<water> ), ^10^minute^, ^212^F^ ) ), ^10^minute^ )
```
```
