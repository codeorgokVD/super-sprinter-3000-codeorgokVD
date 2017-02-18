# all the imports
import os
from .models import *
from super_sprinter_3000.connectdatabase import ConnectDatabase
from super_sprinter_3000.models import Stories
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app

app = Flask(__name__) # create the application instance :)


def init_db():
    ConnectDatabase.db.connect()
    if Stories.table_exists():
        Stories.drop_table()
    if Options.table_exists():
        Options.drop_table()
    ConnectDatabase.db.create_tables([Stories, Options], safe=True)


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    status = ["Planning", "To Do", "In Progress", "Review", "Done"]
    for stat in status:
        Options.create(status=stat)
    print('Initialized the database and insterted statuses to Options table.')


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'postgre_db'):
        g.postgre_db.close()


@app.route('/list', methods=['GET'])
@app.route('/', methods=['GET'])
def list_stories():
    stories = Stories.select().order_by(Stories.id.desc())
    return render_template('list.html', stories=stories)


@app.route('/form', methods=['GET'])
def list_statuses():
    story=[]
    statuses = Options.select()
    return render_template('form.html', story=story, statuses=statuses, header="- Add new Story", button_label="Create")


@app.route('/story/', methods=['POST'])
def add_story():
    Stories.create(title=request.form['story_title'],
                   user_story=request.form['user_story'],
                   acceptance_criteria=request.form['acceptance_criteria'],
                   business_value=request.form['business_value'],
                   estimated_time=request.form['estimated_time'],
                   status=request.form['status'])
    return redirect(url_for('list_stories'))


@app.route('/story/<story_id>', methods=['GET'])
def get_story_to_update(story_id):
    story = Stories.select().where(Stories.id == story_id).get()
    statuses = Options.select()
    return render_template('form.html', story=story, statuses=statuses, header="- Edit Story", button_label="Update")


@app.route('/story/<story_id>', methods=['POST'])
def update_story(story_id):
    update_story = Stories.update(title=request.form['story_title'],
                                  user_story=request.form['user_story'],
                                  acceptance_criteria=request.form['acceptance_criteria'],
                                  business_value=request.form['business_value'],
                                  estimated_time=request.form['estimated_time'],
                                  status=request.form['status']).where(Stories.id == story_id)
    update_story.execute()
    return redirect(url_for('list_stories'))


@app.route('/remove/<story_id>', methods=['GET'])
def remove_story(story_id):
    story_to_delete = Stories.select().where(Stories.id == story_id).get()
    story_to_delete.delete_instance()
    story_to_delete.save()
    return redirect(url_for('list_stories'))