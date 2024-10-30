from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
from database import db
from dotenv import load_dotenv
from models import User
import os

load_dotenv()
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Initialize SQLAlchemy with the app

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/tasks')
def tasks():
    return render_template('tasks.html')

@app.route('/automations')
def automations():
    return render_template('automations.html')

@app.route('/interactions')
def interactions():
    return render_template('interactions.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

# User Resource with CRUD methods
class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            # Retrieve a specific user by ID
            user = User.query.get(user_id)
            if user:
                return jsonify({"id": user.id, "name": user.name, "email": user.email})
            return {"message": "User not found"}, 404
        else:
            # Retrieve all users
            users = User.query.all()
            return jsonify([{"id": u.id, "name": u.name, "email": u.email} for u in users])

    def post(self):
        data = request.get_json()
        new_user = User(name=data['name'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created", "user": {"id": new_user.id, "name": new_user.name, "email": new_user.email}}, 201

    def put(self, user_id):
        user = User.query.get(user_id)
        if user:
            data = request.get_json()
            user.name = data.get('name', user.name)
            user.email = data.get('email', user.email)
            db.session.commit()
            return {"message": "User updated", "user": {"id": user.id, "name": user.name, "email": user.email}}
        return {"message": "User not found"}, 404

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted"}
        return {"message": "User not found"}, 404

    # Add UserResource routes
api.add_resource(UserResource, '/user', '/user/<int:user_id>')


#Here we define application context witht the database to create it
with app.app_context():
    db.create_all()

#Here we run the app and define its port number
if __name__ == "__main__":
    app.run(debug=True, port=5002)



