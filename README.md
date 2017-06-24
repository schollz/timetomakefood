# Time To Make Food

## Production

```
python timetomakefood.py
```

Optionally, create static site:

```
wget -m localhost:8082
```

## Dev

```
python3 -m pip install -r requirements.txt
export FLASK_APP=timetomakefood.py   (WIN: $env:FLASK_APP="timetomakefood.py")
export FLASK_DEBUG=1                 (WIN: $env:FLASK_DEBUG=1)
flask run --debugger
```

## More information

See my blog post: https://rpiai.com/ingredients-ingredients/
