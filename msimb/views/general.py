from flask import request, render_template, redirect, url_for, flash, get_flashed_messages
from flask_wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from functools import wraps
import json

from msimb import app, db
from msimb.models import Note


"""
    Decorator to return SPF formatted responses with just the body
    part of the content, or the whole content for regular requests
"""
def handle_spf(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        spf = wants_spf()
        content, status = f(*args, spf=spf, **kwargs)
        if spf:
            flashes = render_template('flashes.html', messages=get_flashed_messages())

            # put the page content into a format spf will handle
            content = json.dumps({
                'body': {
                    'content': content,
                    'flashes': flashes
                }
            })
        return content, status
    return decorated

# spfjs sends ?spf=navigation for its requests, not application/json?
def wants_spf():
    return request.args.get('spf', False)

@app.route('/')
@handle_spf
def home(spf=False):
    status = 200
    return render_template('home.html', spf=spf), status

# @app.route('/notes', methods=['GET', 'POST'])
@handle_spf
def notes(spf=False):
    status = 200
    NoteForm = model_form(Note, Form, only=['text', 'image'])
    form = NoteForm(request.form)

    if request.method == 'POST' and form.validate():
        err = Note.is_spam(request.remote_addr)
        if err:
            flash(err)
        else:
            data = request.get_json()
            db.session.add(Note(form.text.data, form.image.data, request.remote_addr))
            db.session.commit()
            form = NoteForm()
            status = 201
    notes = Note.query.all()

    return render_template('notes.html', form=form, notes=notes, spf=spf), status

# @app.route('/notes/<int:note_id>')
@handle_spf
def note(note_id, spf=False):
    note = Note.query.get(note_id)
    return str(note), 200

# @app.route('/about')
@handle_spf
def about(spf=False):
    return render_template('about.html', spf=spf), 200

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('home'))

