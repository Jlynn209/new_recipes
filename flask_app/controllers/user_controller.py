# you need to import from the app
# you need to import the following from flask to render, redirect, request, session, and flash. <--- anything that controls what the front-end user will see or go to.
# you will need to import your model associated with the controller.

from flask import render_template,redirect,request,session,flash
from flask_app import app
from flask_app.models import user_model, recipe_model
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route("/")
def home():
    return render_template("reg_log.html")

@app.route("/create_user", methods=['POST'])
def create_user():
    if not user_model.Users.validate_reg(request.form):
        return redirect("/")
    
    pw_hash = bcrypt.generate_password_hash(request.form['pw'])

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "pw" : pw_hash
    }
    user_model.Users.create(data)
    return redirect("/")

@app.route("/processlogin", methods=['POST'])
def process_login():

    user_in_db = user_model.Users.get_one_email(request.form)

    if not user_in_db:
        flash("Invalid Email/Password", 'log')
        return redirect("/")
    
    if not bcrypt.check_password_hash(user_in_db.pw, request.form['pw']):
        flash("Invalid Email/Password",'log')
        return redirect("/")
    
    session['user_id'] = user_in_db.id


    return redirect("/dashboard")



