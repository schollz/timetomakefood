# Time To Make Food

## Run

```
python3 -m pip install -r requirements.txt
export FLASK_APP=timetomakefood.py   (WIN: $env:FLASK_APP="timetomakefood.py")
export FLASK_DEBUG=1                 (WIN: $env:FLASK_DEBUG=1)
flask run --debugger
```

## Axioms

1. Every recipe is composed of "*ingredients*".
2. A recipe reaction has "*ingredients*", "*products*", and "*directions*" .
3. The *ingredients* is a list of ingredients that are needed to complete that reaction.
4. The *products* is a list of ingredients that come out of that reaction.
5. The *directions* is text that explains exactly how the process is transformed, e.g. how much of each ingredient, how long it will take, all the actions that need to be performed.
6. The same ingredients and the same directions always create the same product(s). i.e. You can have the same ingredients but different directions to produce a different product. Also the inverse is not nessecarily true: the same product can be made by different reactants (see bread dough, below).


