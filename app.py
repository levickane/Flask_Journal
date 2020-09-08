from flask import (Flask, g, render_template, flash, redirect, url_for, 
                    abort, request)

import forms
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'daohlweiuhtrq2@#%#$^#$^%UERJY!#$TYsdfhgsdhsth:@#%#$%236823'

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

@app.route('/')
@app.route('/entries')
def index():
    entries = models.Entry.select().order_by(models.Entry.timestamp.desc())
    return render_template('entries.html', entries=entries)

@app.route('/entries/new', methods=('GET', 'POST'))
def add_entry():
    form = forms.EntryForm()
    if form.validate_on_submit():
        models.Entry.create(
            title = form.title.data,
            timespent = form.timespent.data,
            stuff_learned = form.stuff_learned.data.strip(),
            resources_to_remember = form.resources_to_remember.data.strip()
        ).save()
        
        flash("Entry Saved!", "Success!")
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route('/entries/<int:id>')
def view_entry(id):
    try:
        entry = models.Entry.get(models.Entry.entry_id == id)
    except models.DoesNotExist:
        abort(404)
    return render_template('detail.html', entry=entry)


@app.route('/entries/<int:id>/edit', methods = ('GET', 'POST'))
def edit_entry(id):
    try:
        entry = models.Entry.get(models.Entry.entry_id == id)
    except models.DoesNotExist:
        abort(404)
    form = forms.EntryForm()

    if form.validate_on_submit():
        entry.title = form.title.data
        entry.timespent = form.timespent.data
        entry.stuff_learned = form.stuff_learned.data
        entry.resources_to_remember = form.resources_to_remember.data
        entry.save()
        return redirect(url_for('index'))
    return render_template('edit.html', form=form, entry=entry)

@app.route('/entries/<int:id>/delete')
def delete_entry(id):
    models.Entry.get(models.Entry.entry_id == id).delete_instance()
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)
