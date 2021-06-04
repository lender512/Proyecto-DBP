from flask import Flask, render_template, request
from flask.helpers import url_for
from flask.wrappers import Request
from flask import Flask
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

import os
import json

from werkzeug.utils import redirect


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pnpgzwyvgxkqsq:c679eba76897107ff58e453bd485504045037c91c313f328e8dcd0939e7955da@ec2-3-234-85-177.compute-1.amazonaws.com:5432/d83bs9vmmebtt8'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    posts = relationship("Post")
    apartaments = relationship("Apartment")


    def __repr__(self):
        return f'Person: {self.id}, {self.name}'

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    id_persona = db.Column(db.Integer, db.ForeignKey(Person.id), nullable=False, )
    comment = db.Column(db.String(500), nullable=False)
    valoracion = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'Post: {self.id}, {self.id_persona}, {self.comment}'

class Apartment(db.Model):
    __tablename__ = 'apartments'
    id = db.Column(db.Integer, primary_key=True)
    id_persona = db.Column(db.Integer, db.ForeignKey(Person.id), nullable=False, )
    district = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f'Apartment: {self.id}, {self.id_persona}, {self.district}, {self.address}'


db.create_all()
db.session.commit()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signInButton')
def signInButton():
    return render_template('signIn.html')

@app.route('/logInButton')
def logInButton():
    return render_template('logIn.html')

@app.route('/signIn', methods=['POST'])
def signIn():
    name = request.form.get('name', '')
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    type = request.form['type']
    
    if bool(Person.query.filter_by(name=name).first()):
        return redirect(url_for('index'))

    person = Person(name=name, email = email, password = password, type = type)
    db.session.add(person)
    db.session.commit()

    return redirect(url_for('main'))

@app.route('/main')
def main():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)