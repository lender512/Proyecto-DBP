from flask import Flask, render_template, request, jsonify

from flask.helpers import url_for
from flask.wrappers import Request, Response
from flask import Flask
from flask_login import LoginManager, login_user, current_user
import os
import json
from flask_login.utils import login_required

from sqlalchemy.orm import query

from models import *

from werkzeug.utils import redirect

from flask_migrate import Migrate

app = Flask(__name__)

app.secret_key = '12345678910'

#DB config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pnpgzwyvgxkqsq:c679eba76897107ff58e453bd485504045037c91c313f328e8dcd0939e7955da@ec2-3-234-85-177.compute-1.amazonaws.com:5432/d83bs9vmmebtt8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
<<<<<<< Updated upstream
=======
migrate = Migrate(app, db)
#db.create_all()
#db.session.commit()
>>>>>>> Stashed changes

#login config
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_person(id):
    return Person.query.get(int(id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signInButton')
def signInButton():
    return render_template('register.html')

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
    return render_template('login2.html')

@app.route('/createPost')
def createPost():
    return render_template('createPost.html')

@app.route('/post/create', methods =['POST'])
def create_post():
    response = {}
    error = False

    comment = request.get_json()['comment']
    post = Post(id_persona=current_user.id, comment = comment, valoracion='value')

    db.session.add(post)
    db.session.commit()
    #db.session.close()
    response['comment'] = comment
    response['name'] = current_user.name
    

    return jsonify(response)

@app.route('/post/edit', methods =['POST'])
def edit_post():
    response = {}
    error = False

    comment = request.get_json()['comment']
    post_id = request.get_json()['post_id']

    post = db.session.query(Post).filter(Post.id == post_id).first()
    db.session.expunge(post)
    #setattr(post, 'comment', comment)
    post.comment = comment
    db.session.add(post)
    db.session.commit()
    db.session.close()
    #db.session.expire_all()

    response['comment'] = comment
    response['id'] = post_id

    return jsonify(response)

@app.route('/logIn', methods=['POST'])
def logIn():

    response = {}
    error = False

    email = request.get_json()['email']
    password = request.get_json()['password']
    
    person = Person.query.filter_by(email=email).first()

    if(person.password == password):
        #session['id'] = person.id
        login_user(person)
        response['succes'] = True
    else:
        response['succes'] = False

    return jsonify(response)

@app.route('/main')
@login_required
def main():
    db.session.commit()
    return render_template('main.html', data = Post.query.all(), persons = Person.query.all())

@app.route('/edit')
@login_required
def edit():
    return render_template('edit.html', data = Post.query.all(), persons = Person.query.all(), user = current_user)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)