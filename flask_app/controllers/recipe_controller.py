from flask_app.config.mysqlconnection import connectToMySQL
# you need to import from the app
# you need to import the following from flask to render, redirect, request, session, and flash. <--- anything that controls what the front-end user will see or go to.
# you will need to import your model associated with the controller.

from flask import render_template,redirect,request,session,flash
from flask_app import app
from flask_app.models import recipe_model, user_model


@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect("/")
    user = user_model.Users.get_one({'id':session['user_id']})
    all_recipes = recipe_model.Recipe.get_all()
    return render_template("dashboard.html", user = user, all_recipes = all_recipes)

@app.route("/recipes/<int:id>")
def show_recipe(id):
    if 'user_id' not in session:
        return redirect("/")
    user = user_model.Users.get_one({'id':session['user_id']})
    recipe = recipe_model.Recipe.get_one({'id': id})
    return render_template("recipe.html", user = user, recipe = recipe)

@app.route("/create_recipe")
def create_recipe():
    if 'user_id' not in session:
        return redirect("/")
    user = user_model.Users.get_one({'id':session['user_id']})
    return render_template("create_recipe.html", user = user)

@app.route("/process_recipe", methods=['POST'])
def process_recipe():
    if not recipe_model.Recipe.validate_recipe(request.form):
        return redirect("/create_recipe")
    recipe_model.Recipe.create(request.form)
    return redirect("/dashboard")

@app.route("/edit_recipe/<int:id>")
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect("/")
    recipe = recipe_model.Recipe.get_one({'id': id})
    session['recipe_id'] = id
    return render_template("edit_recipe.html", recipe = recipe)

@app.route("/process_edit", methods=['POST'])
def process_edit():
    if not recipe_model.Recipe.validate_recipe(request.form):
        return redirect(f"/edit_recipe/{session['recipe_id']}")
    recipe_model.Recipe.update(request.form)
    session.pop('recipe_id')
    return redirect("/dashboard")

@app.route("/delete_recipe/<int:id>")
def delete_recipe(id):
    recipe_model.Recipe.delete({'id' : id})
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.pop('user_id')
    return redirect("/")