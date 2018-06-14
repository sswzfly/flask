from flask import Flask, session, redirect, url_for, flash
from flask import request
from flask import make_response
from flask_script import Manager
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
from flask_script import Shell
from flask_migrate import Migrate, MigrateCommand
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
manager = Manager(app)
moment = Moment(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

class NameForm(Form):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user  = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
                           current_time=datetime.utcnow(), form=form, name=session.get('name'),
                           known=session.get('known', False))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    manager.run()