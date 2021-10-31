from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
import os
import module

app = Flask(__name__)

categories = ['Technology', 'Food', 'Entertainment', 'Animation', 'Outdoor', 'BoardGame', 'Sport', 'Investment']

@app.route('/insert_user')
def insert_user():
    name = request.args.get('name')
    categories = request.args.get('categories')
    feedback = request.args.get('feedback')
    tb = module.Users()
    result = tb.create(name,categories,feedback)
    return result

@app.route('/clear_all_user')
def drop_all_user():
    tb = module.Users()
    tb.dropTable()
    return "emptyUserTableNow"

##/update_user?name=zhengkai%20zhang&categories=Technology,Food,Entertainment&feedback=pokemon
@app.route('/update_user')
def update_user():
    name = request.args.get('name')
    categories = request.args.get('categories')
    feedback = request.args.get('feedback')
    tb = module.Users()
    return tb.updateUser(name,categories,feedback)

@app.route('/', methods=['GET','POST'])
def root():
    errors = []
    result = {}
    allUsers = []
    try:
        tb = module.Users()
        allUsers = tb.allUsers()
    except:
        errors.append('not able to fetch user db')
    if request.method == "POST":
        try:
            url = request.form['url']
            user = request.form['user']
            result = {
                'user': user,
                'url': url
            }
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
    return render_template('index.html', errors=errors, result=result,allUsers=allUsers)

@app.route('/user', methods=['GET','POST'])
def userPage():
    errors = []
    result = ''
    if request.method == "POST":
        try:
            categoriesForUser = request.form.getlist('categories')
            categoriesForUser = ','.join(categoriesForUser)
            userName = request.form.get('userName')
            tb = module.Users()
            result = tb.create(userName,categoriesForUser,'')
            print(result)
        except:
            errors.append(
                "Unable add user name may duplicated."
            )
    return render_template('user.html',categories=categories, result=result, errors=errors)

@app.route('/feedback', methods=['GET'])
def feedback():
    userName = request.args.get('user')
    tb = module.Users()
    tb.insertFeedBack(userName, 'new feedback')
    return "ok"

if __name__ == '__main__':
    app.run()