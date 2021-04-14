from flask import (Flask, jsonify, render_template, request, flash, session,
                   redirect)
from jinja2 import StrictUndefined
from model import connect_to_db
import crud
from datetime import datetime
import json

app = Flask(__name__)

app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage."""
    is_logged_in = session.get('is_logged_in', False)
    if is_logged_in:
        projects = crud.get_projects_by_user_id(session['user_id'])
        return render_template('stats-page.html', 
            is_logged_in=session.get('is_logged_in', False), 
            projects=projects)
    else:
        return render_template('homepage.html', is_logged_in=is_logged_in )

@app.route('/login')
def login_page():
    """View login."""
    return render_template('login.html', message='Please log in!', is_logged_in = session.get('is_logged_in', False))

@app.route('/logout')
def logout():
    session.clear()
    return render_template('homepage.html', is_logged_in=False)

@app.route('/new-project')
def new_project_page():
    if session.get('is_logged_in', False):
        project_types = crud.get_project_types()
        return render_template('new-project.html', is_logged_in = session.get('is_logged_in', False), project_types=project_types, message='Enter a new project.')
    else:
        return redirect('/')

@app.route('/new-entry')
def new_entry_page():
    if session.get('is_logged_in', False):
        entry_types = crud.get_entry_types()
        projects = crud.get_projects_by_user_id(session['user_id'])
        return render_template('new-entry.html', is_logged_in = session.get('is_logged_in', False), entry_types=entry_types, projects=projects, message='Enter a new entry.')
    else:
        return redirect('/')

###  ENDPOINTS ####

### USER ###

@app.route('/api/login', methods=['POST'])
def login_user():
    """Logs user in."""
    login_data = json.loads(request.data)
    user_name = login_data['user_name']
    password = login_data['password']
    user = crud.get_user_by_user_name(user_name)
    if user is not None:
        if user.password == password:
            session['is_logged_in'] = True
            session['user_id'] = user.user_id
            session['user_name'] = user.user_name
            return jsonify({'message': 'Success', 'user_id': f'{user.user_id}'})
        else:
            return jsonify({'message': 'Your password was incorrect.'})
    else:
        return jsonify({'message': 'No user was found with that name.'})

@app.route('/api/users', methods=['POST'])
def register_user():
    """Registers a new user."""
    user_data = json.loads(request.data)
    user = crud.create_user(user_data['user_name'], user_data['email'], user_data['password'])
    new_user = crud.get_user_by_id(user.user_id)
    if new_user:
        return jsonify({'message': 'Success', 'data': f'${new_user.to_dict()}'})
    else:
        return jsonify({'message': 'Error'})

@app.route('/api/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates user."""
    new_data = json.loads(request.data)
    updated_user = crud.update_user(user_id, new_data)
    return jsonify(updated_user.to_dict())

@app.route('/api/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes user."""
    return jsonify(crud.delete_user(user_id))


### PROJECT ###

@app.route('/api/projects')
def get_projects_by_user():
    """Gets list of projects for the logged in user."""
    db_projects = crud.get_projects_by_user_id(session['user_id'])
    projects_list = []
    for project in db_projects:
        projects_list.append(project.to_dict())
    return jsonify(projects_list)

@app.route('/api/project/<user_id>', methods=['POST'])
def add_project(user_id):
    """Creates a new project."""
    project_data = json.loads(request.data)
    #user = crud.get_user_by_id(session['user_id'])
    user = crud.get_user_by_id(user_id)
    project_type = crud.get_project_type_by_id(project_data['project_type_id'])
    if user and project_type:
        crud.create_project(user=user, 
            project_type=project_type, 
            project_name=project_data['project_name'], 
            project_description=project_data['project_description'], 
            project_create_date=datetime.now())
    else:
        if not user and not project_type:
            return jsonify({'message': 'User and project_type not found.'})
        elif not project_type:
            return jsonify({'message': 'Project_type not found.'})
        else:
            return jsonify({'message': 'User not found.'})
    return jsonify({'message': 'Success!'})

@app.route('/api/project/<project_id>', methods=['PUT'])
def update_project(project_id):
    """Updates project."""
    new_data = json.loads(request.data)
    updated_project = crud.update_project(project_id, new_data)
    return jsonify(updated_project.to_dict())

@app.route('/api/project/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Deletes project."""
    return jsonify(crud.delete_project(project_id))

### ENTRY ###

@app.route('/api/entry', methods=['POST'])
def create_entry():
    """Creates a new entry."""
    entry_data = json.loads(request.data)
    project = crud.get_project_by_id(entry_data['project_id'])
    entry_type = crud.get_entry_type_by_id(entry_data['entry_type_id'])
    if project and entry_type:
        crud.create_entry(project=project,
                    entry_type=entry_type,
                    entry_words=entry_data['entry_words'],
                    entry_minutes=entry_data['entry_minutes'],
                    entry_note=entry_data['entry_note'],
                    entry_datetime=datetime.now())
    else:
        if not project and not entry_type:
            return jsonify({'message': 'Project and entry_type not found.'})
        elif not entry_type:
            return jsonify({'message': 'Entry_type not found.'})
        else:
            return jsonify({'message': 'Project not found.'})
    return jsonify({'message': 'Success!'})

@app.route('/api/entries')
def get_entries_by_user():
    """Gets list of entries for the logged in user."""
    db_entries = crud.get_entries_by_user_id(session['user_id'])
    entries_list = []
    for entry in db_entries:
        entries_list.append(entry.to_dict())
    return jsonify(entries_list)


### ENTRY TYPE ###
@app.route('/api/entry-types')
def get_entry_types():
    """Gets list of entry types."""
    db_entry_types = crud.get_entry_types()
    entry_types_list = []
    for entry_type in db_entry_types:
        entry_types_list.append(entry_type.to_dict())
    return jsonify(entry_types_list)


### PROJECT TYPE ###
@app.route('/api/project-types')
def get_projects_types():
    """Gets list of project types."""
    db_project_types = crud.get_project_types()
    project_types_list = []
    for project_type in db_project_types:
        project_types_list.append(project_type.to_dict())
    return jsonify(project_types_list)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
    session.clear()
