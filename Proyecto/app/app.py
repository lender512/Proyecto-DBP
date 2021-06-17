from operator import add
from flask import Flask, render_template, request, jsonify

from flask.helpers import flash, url_for
from flask.wrappers import Request, Response
from flask import Flask
from flask_login import LoginManager, login_user, current_user
from passlib.hash import pbkdf2_sha256
import os
import json
from flask_login.utils import login_required

from sqlalchemy.orm import query

from models import *

from werkzeug.utils import redirect

from flask_migrate import Migrate
import re

app = Flask(__name__)

app.secret_key = '12345678910'

#DB config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pnpgzwyvgxkqsq:c679eba76897107ff58e453bd485504045037c91c313f328e8dcd0939e7955da@ec2-3-234-85-177.compute-1.amazonaws.com:5432/d83bs9vmmebtt8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



migrate = Migrate(app, db)
#db.create_all()
#db.session.commit()

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

def valid_email(email): #email validation
  return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

@app.route('/signIn', methods=['POST'])
def signIn():
    
    error = False
    response = {}
    try:
        name = request.get_json()['name']
        email = request.get_json()['email']
        password = request.get_json()['password']
        checkPassword = request.get_json()['checkPassword']

        if name.isspace() or len(name) == 0:
            error = True
            response['error_msg'] = 'Please write a valid name'

        elif email.isspace() or len(email) == 0 or not valid_email(email) :
            error = True
            response['error_msg'] = 'Please write a valid email'
        
        elif password.isspace() or len(password) == 0:
            error = True
            response['error_msg'] = 'Please write a valid password'

        elif len(password) < 8:
            error = True
            response['error_msg'] = 'Password must have at least 8 characters'

        elif password != checkPassword:
            error = True
            response['error_msg'] = 'Passwords do not match'

        else:
            hashed_pasword = pbkdf2_sha256.hash(password)
        
            person = Person(name=name, email = email, password = hashed_pasword)
            db.session.add(person)
            db.session.commit()
    except:
        error = True
        response['error_msg'] = 'Email already taken'
        db.session.rollback()

    finally:
        db.session.close()
        response['error'] = error

    return jsonify(response)

@app.route('/logIn', methods=['POST'])
def logIn():

    response = {}
    error = False
    
    email = request.get_json()['email']

    password = request.get_json()['password']
    try: 
        person = Person.query.filter_by(email=email).first()
        if person is None:
            error = True
            response['error_msg'] = 'Invalid email'
        elif not pbkdf2_sha256.verify(password, person.password):
            error = True
            response['error_msg'] = 'Invalid password'
            
        else:
            login_user(person)
    except:
        error = True
        response['error_msg'] = 'Something went wrong'
        
    finally:
        response['error'] = error

    return jsonify(response)

@app.route('/logInButton')
def logInButton():
    return render_template('login2.html')


@app.route('/post/create', methods =['POST'])
def create_post():
    response = {}
    error = False

    try:
        comment = request.get_json()['comment']
        address = request.get_json()['address']

        if address.isspace() or len(address) == 0:
            error = True
            response['error_msg'] = 'Create or select an address first'
        elif comment.isspace() or len(comment) == 0:
            error = True
            response['error_msg'] = 'Can not create empty post'
        else: 
            apt = Apartment.query.filter_by(address = address).first()
            
            post = Post(id_persona=current_user.id, comment = comment, valoracion=0, address = address, district = apt.district)
            
            db.session.add(post)
            db.session.commit()

            response['comment'] = comment
            response['name'] = current_user.name
            response['address'] = address
            response['district'] = apt.district
    except:
        error = True
        response['error_msg'] = 'Something went wrong'
        db.session.rollback()
    finally:
        db.session.close()
        response['error'] = error


    return jsonify(response)

@app.route('/post/edit', methods =['POST'])
def edit_post():
    response = {}
    error = False

    comment = request.get_json()['comment']
    post_id = request.get_json()['post_id']

    try:
        if comment.isspace() or len(comment) == 0:
            error = True
            response['error_msg'] = 'Can not create empty post'
        else:
            post = db.session.query(Post).filter(Post.id == post_id).first()
            db.session.expunge(post)
            post.comment = comment
            db.session.add(post)
            db.session.commit()
            response['comment'] = comment
            response['id'] = post_id

    except:
        error = True
        response['error_msg'] = 'Something went wrong'
        db.session.rollback()
    finally:
        db.session.close()
        response['error'] = error


    return jsonify(response)

@app.route('/post/delete', methods =['DELETE'])
def delete_post():
    response = {}
    error = False

    try:
        post_id = request.get_json()['post_id']
        post = db.session.query(Post).get(int(post_id))
    
        db.session.delete(post)
        response['id'] = post_id
        db.session.commit()
    except:
        error = True
        response['error_msg'] = 'Something went wrong'
        db.session.rollback()

    finally:
        db.session.close()
        response['error'] = error
    
    return jsonify(response)

@app.route('/post/upvote', methods =['POST'])
def upvote_post():
    response = {}
    error = False

    try:
        post_id = request.get_json()['post_id']
        
        post = db.session.query(Post).get(int(post_id))
        like = db.session.query(Like).filter_by(id_persona = current_user.id).filter_by(id_post = post.id).first()
        if (like is None):
            like = Like(id_persona = current_user.id, id_post = post_id)
            post.valoracion = post.valoracion + 1
            db.session.add(like)
            response['action'] = 'up'
        else:
            db.session.delete(like)
            post.valoracion = post.valoracion - 1
            response['action'] = 'down'

        response['id'] = post_id
        db.session.add(post)
        db.session.commit()
    except: 
        error = True
        response['error_msg'] = 'Something went wrong'
        db.session.rollback()
    finally:
        db.session.close()
        response['error'] = error

    return jsonify(response)

@app.route('/apartments/create', methods =['POST'])
def create_apartment():
    response = {}
    error = False
    try:
        district = request.get_json()['district']
        address = request.get_json()['address']
        if district.isspace() or len(district) == 0:
            error = True
            response['error_msg'] = 'Insert valid district'
        elif address.isspace() or len(address) == 0:
            error = True
            response['error_msg'] = 'Insert valid address'
        else:
            apartment = Apartment(id_persona=current_user.id, district = district, address= address)
            db.session.add(apartment)
            db.session.commit()
            response['address'] = apartment.address
            response['district'] = apartment.district
    except:
        error = True
        response['error_msg'] = 'Something Went Wrong!'
        db.session.rollback()
    finally:
        db.session.close()
        response['error']= error

    return jsonify(response)


@app.route('/apartments/delete', methods=['DELETE'])
def delete_apartment():
    response = {}
    error = False
    try:
        apartment_id = request.get_json()['apartment_id']
        apartment = db.session.query(Apartment).get(int(apartment_id))
        db.session.delete(apartment)
        db.session.commit()
    except:
        error = True
        response['error_msg'] = 'Something went wrong'
        db.session.rollback()
    finally:
        db.session.close()
    response['id'] = apartment_id
    return jsonify(response)



@app.route('/main')
@login_required
def main():
    db.session.commit()
    return render_template('main.html', data = Post.query.all(), persons = Person.query.all(), apartments = Apartment.query.all(), likes = Like.query.all(), user = current_user)

@app.route('/edit')
@login_required
def edit():
    return render_template('edit.html', data = Post.query.all(), persons = Person.query.all(), user = current_user)

### SEARCHER
@app.route('/main', methods=['POST'])
def search_by_district():
    district_searched = request.form.get('search_district_input', '**distrito no encontrado**')
    return redirect('search/'+district_searched)

@app.route('/search/<district_searched>')
def search(district_searched):
    length = len(Post.query.filter_by(district=district_searched).all())
    if length > 0:
        return render_template('search.html', data = Post.query.filter_by(district=district_searched).all(), modelo = Person, empty = False,  not_search = False,user = current_user, likes = Like.query.all())
    else:
        return render_template('search.html', data = [], modelo = Person, empty = True, not_search = False,user = current_user, likes = Like.query.all())

@app.route('/search/<district_searched>', methods=['POST'])
def search_post(district_searched):
    district_searched = request.form.get('search_district_input', '**distrito no encontrado**')
    print(district_searched)
    return redirect(district_searched)

@app.route('/search/')
def search_empty():
    return redirect(url_for('search_empty2'))

@app.route('/search/not_search')
def search_empty2():
    return render_template('search.html', data = [], modelo = Person, empty = False, not_search = True,user = current_user)
### SEARCHER END

# Error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(401)
def page_not_found(e):
    return render_template('401.html'), 401

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

@app.errorhandler(410)
def page_not_found(e):
    return render_template('410.html'), 410

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)