from flask import Flask, render_template, request
from flask.helpers import url_for
from flask.wrappers import Request, Response
from flask import Flask
import os
import json

from models import *

from werkzeug.utils import redirect

app = Flask(__name__)

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
    
    if bool(Person.query.filter_by(name=name).first()):
        return redirect(url_for('index'))

    person = Person(name=name, email = email, password = password, type = type)
    db.session.add(person)
    db.session.commit()

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
    post = Post(id_persona=1, comment = comment, valoracion='value')
    db.session.add(post)
    db.session.commit()
    db.session.close()

@app.route('/logIn', methods=['POST'])
def logIn():
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    
    person = Person.query.filter_by(email=email).first()

    if(person.password == password):
        return redirect(url_for('main'))
    else:
        return render_template('logIn.html')

@app.route('/main')
def main():
    return render_template('main.html', data =Post.query.all())


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)