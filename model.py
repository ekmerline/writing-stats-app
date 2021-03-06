from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()
db.session.expire_on_commit = False

class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<User user_name={self.user_name} email={self.email}>'


class Project(db.Model):

    __tablename__ = 'projects'

    project_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)
    project_type_id = db.Column(UUID(as_uuid=True), db.ForeignKey('project_types.project_type_id'), nullable=False)
    project_name = db.Column(db.String, nullable=False)
    project_description = db.Column(db.Text)
    project_create_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref='users')
    project_type = db.relationship('Project_Type', backref='project_types')

    def __repr__(self):
        return f'<Project project_id={self.project_id} project_name={self.project_name}>'

    def to_dict(self):
        return {
            'project_id': self.project_id,
            'user_id': self.user_id,
            'project_type_id': self.project_type_id,
            'project_type_name': self.project_type.project_type_name,
            'project_name': self.project_name,
            'project_description': self.project_description,
            'project_create_date': self.project_create_date
        }

class Entry(db.Model):

    __tablename__ = 'entries'

    entry_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey('projects.project_id'), nullable=False)
    entry_type_id = db.Column(UUID(as_uuid=True), db.ForeignKey('entry_types.entry_type_id'), nullable=False)

    entry_minutes = db.Column(db.Integer, nullable=False)
    entry_words = db.Column(db.Integer)
    entry_note = db.Column(db.Text)
    entry_datetime = db.Column(db.DateTime, default=db.func.current_timestamp())

    project = db.relationship('Project', backref='projects')
    entry_type = db.relationship('Entry_Type', backref='entry_types')

    def __repr__(self):
        return f'<Entry entry_id={self.entry_id} entry_quantity={self.entry_quantity}>'

    def to_dict(self):
        return {
            'entry_id': self.entry_id,
            'project_id': self.project_id,
            'entry_type_id': self.entry_type_id,
            'entry_type_name': self.entry_type.entry_type_name,
            'project_name': self.project.project_name,
            'entry_minutes': self.entry_minutes,
            'entry_words': self.entry_words,
            'entry_note': self.entry_note,
            'entry_datetime': self.entry_datetime
        }

class Project_Type(db.Model):

    __tablename__ = 'project_types'

    project_type_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_type_name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Project_Type project_type_id={self.project_type_id} project_type_name={self.project_type_name}>'

    def to_dict(self):
        return {
            'project_type_id': self.project_type_id,
            'project_type_name': self.project_type_name
        }

class Entry_Type(db.Model):

    __tablename__ = 'entry_types'

    entry_type_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entry_type_name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Entry_Type entry_type_id={self.entry_type_id} entry_type_name={self.entry_type_name}>'
    
    def to_dict(self):
        return {
            'entry_type_id': self.entry_type_id,
            'entry_type_name': self.entry_type_name
        }
        
def connect_to_db(flask_app, db_uri='postgresql:///testwritingstats', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    connect_to_db(app)
