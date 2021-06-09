from flask import Flask, render_template, request, jsonify, session
from flask.helpers import url_for
from flask.wrappers import Request, Response
from flask import Flask
import os
import json

from sqlalchemy.orm import query

from models import *

from werkzeug.utils import redirect

app = Flask(__name__)

app.secret_key = '12345678910'

#DB config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pnpgzwyvgxkqsq:c679eba76897107ff58e453bd485504045037c91c313f328e8dcd0939e7955da@ec2-3-234-85-177.compute-1.amazonaws.com:5432/d83bs9vmmebtt8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signInButton')
def signInButton():
    return render_template('signIn.html')

@app.route('/signIn', methods=['POST'])
def signIn():
    name = request.form.get('name', '')
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    type = request.form['type']
    
    person = Person(name=name, email = email, password = password, type = type)
    db.session.add(person)
    db.session.commit()

    return render_template('index.html')

@app.route('/logInButton')
def logInButton():
    return render_template('logIn.html')

@app.route('/createPost')
def createPost():
    return render_template('createPost.html')

@app.route('/post/create', methods =['POST'])
def create_post():
    response = {}
    error = False

    comment = request.get_json()['comment']
    post = Post(id_persona=session.get('id'), comment = comment, valoracion='value')
    person = Person.query.get(session.get('id'))
    
    response['comment'] = comment
    person = Person.query.filter_by(id=session.get('id')).first()
    response['name'] = person.name

    db.session.add(post)
    db.session.commit()
    db.session.close()

    return jsonify(response)

@app.route('/logIn', methods=['POST'])
def logIn():

    response = {}
    error = False

    email = request.get_json()['email']
    password = request.get_json()['password']
    
    person = Person.query.filter_by(email=email).first()
    
    

    if(person.password == password):
        session['id'] = person.id
    #else: manejar errores
    #    return render_template('logIn.html')

    return jsonify(response)

@app.route('/main')
def main():
    return render_template('main.html', data = Post.query.all(), persons = Person.query.all())


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)