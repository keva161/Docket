from app import db
from flask_restplus import Resource, Namespace
from app.models import User, Todo
from app.api.models import TodoModel
from app.api.auth import token_required
from flask import jsonify, request

TodosNS = Namespace('Todo', description='Todo related operations')


@TodosNS.route('/')
class Todos(Resource):

    @token_required
    def get(self):
        """Returns all the todos for a user associated with the API token."""
        token = request.headers['Token']
        user = User.query.filter_by(api_token=token).first()
        try:
            todos = Todo.query.filter_by(user_id=user.id).order_by(Todo.timestamp.desc()).all()
            output = []
            for todo in todos:
                output.append({'id': todo.id, 'body': todo.body, 'created': todo.timestamp})
                print("Delivering a users todo items")
            if len(output) < 1:
                return jsonify({'message' : 'There are no todo items currently waiting to be done!'})
            else:
                return jsonify(output)
        except:
            return {'message': 'Invalid user'}

    @TodosNS.expect(TodoModel)
    @token_required
    def post(self):
        """Adds a new todo item to the user todo list."""
        token = request.headers['Token']
        data = request.get_json()
        user = User.query.filter_by(api_token=token).first()

        if not user:
            return jsonify({'message': 'Invalid API token'})
        else:
            try:
                print("Creating a new todo item")
                new_todo = Todo(body=data['Body'], owner=user)
                db.session.add(new_todo)
                db.session.commit()
                return jsonify({'message': 'Todo added!'})
            except:
                return jsonify({'message': 'An error occurred. Please try again'})


@TodosNS.route('/<string:todo_id>')
class Todos(Resource):
    @token_required
    @TodosNS.param('todo_id', 'The todo identifier')
    def delete(self, todo_id):
        """Deletes a specified todo item on the users list of todos."""
        token = request.headers['Token']
        try:
            print("Deleting a todo item")
            user = User.query.filter_by(api_token=token).first()
            Todo.query.filter_by(user_id=user.id).filter_by(id=todo_id).delete()
            db.session.commit()
            return jsonify({'message': 'Todo deleted'})
        except:
            return jsonify({'message': 'Invalid API token, or ID'})
