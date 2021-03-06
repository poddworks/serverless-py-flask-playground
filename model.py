import os
from application import app


from flask_sqlalchemy import SQLAlchemy
if os.environ.get('DEPLOY_STATUS', 'development') == 'development':
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///db.sqlite3"
else:
    from environment import POSTGRES_USER, POSTGRES_PW, POSTGRES_URL, POSTGRES_DB
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_URL}/{POSTGRES_DB}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Let's build our SQLAlchemy database reference
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def as_dict(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.String(512), nullable=False)
    hash_key = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return f'<Entry {self.created_at}::{self.content.slice(64)}...>'

    def as_dict(self):
        return {'id': self.id, 'created_at': self.created_at, 'hash_key': self.hash_key, 'content': self.content}
