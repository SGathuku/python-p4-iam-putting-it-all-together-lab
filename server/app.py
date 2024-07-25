#!/usr/bin/env python3

from flask import request, session, jsonify
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe

class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        image_url = data.get('image_url')
        bio = data.get('bio')

        user = User(username=username, password_hash=password, image_url=image_url, bio=bio)
        try:
            db.session.add(user)
            db.session.commit()
            return jsonify(user.to_dict())
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Username already taken'}, 400

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Not logged in'}, 401

        user = User.query.get(user_id)
        return jsonify(user.to_dict())

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.authenticate(password):
            session['user_id'] = user.id
            return jsonify(user.to_dict())
        else:
            return {'error': 'Invalid credentials'}, 401

class Logout(Resource):
    def post(self):
        session.pop('user_id', None)
        return {'message': 'Logged out successfully'}

class RecipeIndex(Resource):
    def get(self):
        recipes = Recipe.query.all()
        return jsonify([recipe.to_dict() for recipe in recipes])

    def post(self):
        data = request.get_json()
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Not logged in'}, 401

        user = User.query.get(user_id)
        title = data.get('title')
        instructions = data.get('instructions')
        minutes_to_complete = data.get('minutes_to_complete')

        recipe = Recipe(user=user, title=title, instructions=instructions, minutes_to_complete=minutes_to_complete)
        db.session.add(recipe)
        db.session.commit()
        return jsonify(recipe.to_dict())

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
