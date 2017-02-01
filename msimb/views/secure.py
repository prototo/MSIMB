from flask import request, render_template, redirect, url_for, flash, jsonify
from flask_wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from flask_login import LoginManager, login_required, login_user, logout_user
from msimb import app, db
from msimb.models import Note, User


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/secure/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username, password = request.form.get('username', None), request.form.get('password', None)
        if username and password:
            user = User.query.filter_by(username=username).first()
            if user and user.validate(password):
                login_user(user)
                next = request.args.get('next')
                return redirect(next)
    return render_template('secure/login.html'), 200

@app.route('/secure/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/secure/notes')
@login_required
def secure_notes():
    notes = Note.query.all()
    return render_template('secure/notes.html', notes=notes), 200

@app.route('/secure/notes/<int:note_id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def secure_note(note_id):
    note = Note.query.get(note_id)
    if request.method == 'GET' and not note:
        flash('Note {} doesn\'t exist'.format(note_id))
        return redirect(url_for('secure_notes'))
    elif request.method == 'DELETE':
        if note:
            # db.session.delete(note)
            # db.session.commit()
            pass
        return jsonify(redirect=url_for('secure_notes')), 200
    elif request.method == 'POST':
        # do the updates
        pass
    return render_template('secure/note.html', note=note)
