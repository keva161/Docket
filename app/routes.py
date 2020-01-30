from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, TodoForm
from app import app, db
from app.models import User, Todo
import uuid

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('todo'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('todo')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(api_token=str(uuid.uuid4()), username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/todo')
def todo():
    if current_user.is_authenticated:
        form = TodoForm()
        todos = current_user.todos.order_by(Todo.timestamp.desc()).all()
        return render_template('todo.html', form=form, todos=todos)
    return redirect(url_for('index'))



@app.route('/newtodo', methods=['POST'])
def update():
    form = TodoForm()
    new_todo = Todo(body=form.todo.data, owner=current_user)
    db.session.add(new_todo)
    db.session.commit()
    todos = current_user.todos.order_by(Todo.timestamp.desc()).all()
    return render_template('todolist.html', todos=todos)


@login_required
@app.route('/deletetodo', methods=['POST'])
def delete():
    deleteid = request.form['id']
    Todo.query.filter_by(id=deleteid).delete()
    db.session.commit()
    todos = current_user.todos.order_by(Todo.timestamp.desc()).all()
    return render_template('todolist.html', todos=todos)


@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        return render_template('profile.html', User=current_user)
    return redirect(url_for('index'))

# @app.route('/api/user', methods=['GET'])
# def get_one_user():
#     key = request.args.get('key')
#     user = models.py.query.filter_by(api_token=key).first()
#
#     if not user:
#         return jsonify({'message':'No user found'})
#     else:
#         output = []
#         user_data = {'username': user.username, 'email': user.email}
#         return jsonify({'user': user_data})
#
# @app.route('/api/user', methods=['POST'])
# def create_user():
#     data = request.get_json()
#
#     if not data:
#         return jsonify({'message':'Please enter some user data'})
#     else:
#         user = models.py(api_token=str(uuid.uuid4()), username=data['username'], email=data['email'])
#         user.set_password(data['password'])
#         db.session.add(user)
#         db.session.commit()
#         return jsonify({'message': 'New user created! : ' + user.api_token})
#
#
# @app.route('/api/user/all', methods=['GET'])
# def get_all_users():
#     key = request.args.get('key')
#     valid_user = models.py.query.filter_by(api_token=key).first()
#
#     if not valid_user:
#         return jsonify({'message':'Missing, or invalid API auth.py'})
#     else:
#         users = models.py.query.all()
#         output = []
#
#         for user in users:
#             output.append({'username': user.username, 'email': user.email})
#         return jsonify(output)
#
# @app.route('/api/user', methods=['DELETE'])
# def delete_current_user():
#     key = request.args.get('key')
#     user = models.py.query.filter_by(api_token=key).first()
#
#     if not user:
#         return jsonify({'message':'No user found'})
#     else:
#         models.py.query.filter_by(api_token=key).delete()
#         db.session.commit()
#         return jsonify({'message': 'Current user deleted'})
#
# @app.route('/api/todo', methods=['GET'])
# def get_todo():
#     key = request.args.get('key')
#     user = models.py.query.filter_by(api_token=key).first()
#
#     if not user:
#         return jsonify({'message':'Missing, or invalid API auth.py'})
#     else:
#         todos = Todo.query.filter_by(user_id=user.id).order_by(Todo.timestamp.desc()).all()
#         output=[]
#
#         for todo in todos:
#             output.append({'id': todo.id, 'body': todo.body, 'created': todo.timestamp})
#         return jsonify(output)
#
# @app.route('/api/todo', methods=['POST'])
# def add_todo():
#     key = request.args.get('key')
#     data = request.get_json()
#     user = models.py.query.filter_by(api_token=key).first()
#
#     if not user:
#         return jsonify({'message':'Missing, or invalid API auth.py'})
#     else:
#         new_todo = Todo(body=data['body'], owner=user)
#         db.session.add(new_todo)
#         db.session.commit()
#         return jsonify({'message': 'Todo added!'})
#
# @app.route('/api/todo/<todo_id>', methods=['POST'])
# def delete_todo(todo_id):
#     key = request.args.get('key')
#     id = todo_id
#     user = models.py.query.filter_by(api_token=key).first()
#
#     if not user:
#         return jsonify({'message':'Missing, or invalid API auth.py'})
#     else:
#         if not todo_id:
#             return jsonify({'message': 'Missing, or invalid Todo id'})
#         else:
#             Todo.query.filter_by(id=id).delete()
#             db.session.commit()
#             return jsonify({'message': 'Todo deleted!'})

