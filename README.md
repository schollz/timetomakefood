# Formatting
```bash
ingredient = ^NUMBER^UNIT^<food>
heat = ^NUMBER^UNIT^
time = ^NUMBER^UNIT^
chill ( ingredient, time )
mix ( ingredient1, ingredient2, .... ingredientN )
nuke ( ingredient, time )
cook ( ingredient, time, heat ) 
chop ( ingredient, pieces )
set ( ingredient, time )
drain ( ingredient )
```

# Grammar rules

If the ```<food>``` does not exist in this grammar table, find the closest thing in the SR27 database. I.e. "```<olive-oil>```" does not exist in the examples below, so those recipes will search for anything that has "olive" and "oil" in SR27 and use that.

Total times are calculated by adding all the operation times.

Total nutrition is calculated by adding all the ingredients nutritions.

Note that ```cook``` is a little bit of a catch-all. I'm assuming if you mix something with a ton of water you want to boil it, if you mix it with a little oil then you want to saute it, otherwise its your discretion/common-sense.

Note that ```chop``` is also used to divide depending on the number of pieces. If the number of pieces >99, then its chop. If its <30 it probably means to divide it that number of portions.

The unit type ```whole``` is usually prefaced by the percentage to be taken from the whole item. I.e. Bread slices are really 1/5 the whole loaf of bread.

# Examples

```bash
<grilled-cheese-sandwich> = cook ( mix ( ^1^whole^<sandwich>, ^2^tbl^<oil> ), ^5^minute^, ^400^F^ )
<cheese-sandwich> = mix ( cut ( ^1/5^whole^<bread>, 2 ), <cheese> )
<bread> = cook ( set ( mix ( set ( mix ( ^1000^g^<white-flour>, cook ( ^720^g^<water>, ^1^minute^, ^95^F^ ) ), ^30^minute^ ), <spaghetti> = mix( drain ( cook ( mix ( ^1^pound^<pasta>, ^500^ml^<water> ), ^10^minute^, ^200^F^ ), <sauce> )
<sauce> = <tomato-cream-sauce> | <roasted-red-pepper-sauce>
<tomato-cream-sauce> = mix( ^2^tbl^<olive-oil>, nuke(^2^tbl^<butter>, ^1^minute), chop(^1^whole^<onion>, 100) ,  chop(^1^whole^<tomato>, ^1^minute^) )
<roasted-red-pepper-sauce> = mix ( ^1^can^<tomato-sauce>, cook ( mix( chop( ^3^whole^<pepper>, 100), ^2^tbl^<olive-oil>), ^6^minute^, ^200^F^ ) )
<hard-boiled-egg> = chill ( drain ( cook ( mix ( ^1^whole^<raw-egg>, ^500^ml^<water> ), ^10^minute^, ^212^F^ ) ), ^10^minute^ )
^21^g^<salt>, ^4^g^<yeast> ), ^4^hour^ ), ^40^minute^, ^475^F^ )
<flour-tortilla> = cook ( chop ( set ( mix ( mix ( ^3^cup^<white-flour>, ^5^tbl^<oil> ), ^3/4^cup^<water> ), ^30^minute^ ), 12 ), ^20^minute^)
<cooked-oatmeal> = chill ( nuke ( mix ( ^1^cup^<oatmeal>, ^1^cup^<milk>, chop(^1^whole^<banana>, 6) ), ^3^minute^ ), ^1^minute^)
```
