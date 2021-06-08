from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

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
    valoracion = db.Column(db.Integer, nullable=False)

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

#db.create_all()
#db.session.commit()