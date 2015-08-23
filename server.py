from markdown import markdown
from flask import Flask, render_template, url_for, request
from parser import * 

app = Flask(__name__)
cookbook = Recipes()

@app.route("/", methods=['GET','POST'])
def hello():
    error = None
    data = {}
    data['recipes'] = cookbook.getRecipes()
    data['servings'] = [1,2,3,4,5,6,7,8]
    data['timelimits'] = ['1 min','5 min','10 min','15 min','30 min','1 hour','2 hour','4 hour','12 hour','2 days','1 week','1 year']
    if request.method == 'GET':
        data['recipe_text'] = ['']
        return render_template('index.html',data=data)
    else:
        data['recipe_text'] = cookbook.makeRecipe(request.form['recipe'].lower(), int(request.form['servings']), request.form['timelimit'])
        data['recipe_text'] = markdown(data['recipe_text'])
        print(data)
        return render_template('index.html',data=data)
    
if __name__ == "__main__":
    app.run(host='192.168.1.22',debug=True)
