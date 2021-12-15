# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model
from flask import flash
# model the class after the friend table from our database
class Recipe:
    def __init__( self , data ):
        #put attributes here
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.under_30 = data['under_30']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.created_at = data['updated_at']
        self.user_id = data['user_id']
        self.users = []


    # 1.Now we use class methods to query our database
    # 2.In our methods, we always need a query
    # 3.we need a variable to hold our results when calling connectToMySQL to our database.query_db(*query*)
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('recipes_db').query_db(query)
        # Create an empty list to append our instances of data
        users = []
        # Iterate over the db results and create instances of data with cls.
        for data in results:
            users.append( cls(data) )
        return users

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE recipes.id = %(id)s;"
        results = connectToMySQL('recipes_db').query_db(query, data)
        return cls(results[0])

    @classmethod
    def create(cls, data):
        query = "INSERT INTO recipes(name, description, instruction, under_30, date_made, user_id) VALUES (%(name)s, %(description)s, %(instruction)s, %(under_30)s, %(date_made)s, %(user_id)s );"
        results = connectToMySQL('recipes_db').query_db(query, data)
        return results

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instruction = %(instruction)s, under_30 = %(under_30)s, date_made = %(date_made)s WHERE (id = %(id)s);" 
        return connectToMySQL('recipes_db').query_db(query,data)
            
    @classmethod
    def delete(cls, data):
        query =  "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('recipes_db').query_db(query,data)

    @staticmethod
    def validate_recipe(user):
        is_valid = True
        if len(user['name']) < 1:
            flash("please fill out the name.", 'recipe')
            is_valid = False
        if len(user['description']) < 1:
            flash("please fill out the description.", 'recipe')
            is_valid = False
        if len(user['instruction']) < 1:
            flash("please fill out the instruction.", 'recipe')
            is_valid = False
        if len(user['date_made']) < 1:
            flash("please fill out date", 'recipe')
            is_valid = False
        return is_valid