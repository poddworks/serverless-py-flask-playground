from application import app
from model import db
import click

@app.cli.command('create_db')
def create_db_command():
  db.create_all()

@app.cli.command('create_user')
@click.option('--username', help='Username for the user')
@click.option('--email', help='Email for the created user')
def create_user_command(username, email):
  from model import User
  db.session.add(User(username=username, email=email))
  db.session.commit()
