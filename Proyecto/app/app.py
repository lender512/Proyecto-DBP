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
import sys

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

@app.route('/signIn', methods=['POST'])
def signIn():
    name = request.form.get('name', '')
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    type = request.form.get('type', '')
    
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
    address = request.get_json()['address']
    print(address)
    apt = Apartment.query.filter_by(address = address).first()
    
    post = Post(id_persona=current_user.id, comment = comment, valoracion=0, address = address, district = apt.district)

    db.session.add(post)
    db.session.commit()
    #db.session.close()
    response['comment'] = comment
    response['name'] = current_user.name
    response['address'] = address
    response['district'] = apt.district
    

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

@app.route('/post/delete', methods =['POST'])
def delete_post():
    response = {}
    error = False

    post_id = request.get_json()['post_id']

    post = db.session.query(Post).get(int(post_id))
    
    #Post.query.filter(Post.id == int(post_id)).delete()
    db.session.delete(post)
    db.session.commit()
    db.session.close()
    #db.session.expire_all()

    response['id'] = post_id

    return jsonify(response)

@app.route('/post/upvote', methods =['POST'])
def upvote_post():
    response = {}
    error = False

    post_id = request.get_json()['post_id']
    print(post_id)

    post = db.session.query(Post).get(int(post_id))

    post.valoracion = post.valoracion + 1
    
    db.session.add(post)
    db.session.commit()
    db.session.close()
    #db.session.expire_all()

    response['id'] = post_id

    return jsonify(response)

@app.route('/apartments/create', methods =['POST'])
def create_apartment():
    response = {}
    error = False
    try:
        district = request.get_json()['district']
        address = request.get_json()['address']
        apartment = Apartment(id_persona=current_user.id, district = district, address= address)
        db.session.add(apartment)
        db.session.commit()
        response['address'] = apartment.address
        response['district'] = apartment.district
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        response['error_message'] = 'Something Went Wrong!'
    response['error']= error

    return jsonify(response)

@app.route('/apartments/<apartment_id>/update', methods=['POST'])
def update_apartment_by_id(apartment_id):
    response = {}
    error = False
    try:
        apartment = Apartment.query.get_or_404(apartment_id)
        if apartment is None:
            response['error_message'] = apartment_id + 'not found in database!'
        new_apartment = request.get_json()['apartment']
        apartment.address = new_address
        apartment.district = new_district
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        response['error_message2'] = 'something went wrong updating!'
    return jsonify(response)

@app.route('/apartments/<apartment_id>/delete-apartment', methods=['DELETE'])
def delete_apartment_by_id(apartment_id):
    response = {}
    error = False
    try:
        apartment = Apartment.query.get_or_404(apartment_id)
        if apartment is None:
            response['error_message'] = apartment_id + 'not found in database!'
        #db.session.delete(apartment)
        Apartment.query.filter_by(id=apartment_id).delete()
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    response['success'] = error
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
    return render_template('main.html', data = Post.query.all(), persons = Person.query.all(), apartments = Apartment.query.all(), user = current_user)

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
        return render_template('search.html', data = Post.query.filter_by(district=district_searched).all(), modelo = Person, empty = False,  not_search = False,user = current_user)
    else:
        return render_template('search.html', data = [], modelo = Person, empty = True, not_search = False,user = current_user)

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

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)