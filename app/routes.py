import json

from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, TodoForm
from app import app, db
from app.models import User, Todo


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@login_required
@app.route('/todo')
def todo():
    form = TodoForm()
    todos = current_user.todos.order_by(Todo.timestamp.desc()).all()
    return render_template('todo.html', form=form, todos=todos)


@login_required
@app.route('/newtodo', methods=['POST'])
def update():
    form = TodoForm()
    new_todo = Todo(body=form.todo.data, owner=current_user)
    db.session.add(new_todo)
    db.session.commit()
    todos = current_user.todos.order_by(Todo.timestamp.desc()).all()
    return render_template('todolist.html', todos=todos)

@login_required
@app.route('/delete', methods=['POST'])
def delete():
    deleteid = request.form['id']
    Todo.query.filter_by(id=deleteid).delete()
    db.session.commit()
    todos = current_user.todos.order_by(Todo.timestamp.desc()).all()
    return render_template('todolist.html', todos=todos)
