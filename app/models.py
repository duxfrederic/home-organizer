from app import db, login
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

etages = {1:"rez-de-chaussée", 0: "sous-sol", 2:"1er étage", 3:"grenier"}
buildings = ["Maison", "Garage", "Cabane", "Dehors"]


class User(UserMixin, db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    timestamp     = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    username      = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    
    items         = db.relationship('Item', backref='item_creator', lazy='dynamic')
    locations     = db.relationship('Location', backref='location_creator', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}, id no {self.id}, registered on {self.timestamp}>'

class Item(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    created      = db.Column(db.DateTime, default=datetime.utcnow)
    lastmodified = db.Column(db.DateTime, default=datetime.utcnow)
    name         = db.Column(db.String(128))
    comment      = db.Column(db.String(256), default="")
    number       = db.Column(db.Integer, default=1)
    location_id  = db.Column(db.Integer, db.ForeignKey('location.id'))
    location     = db.relationship("Location")
    user_id      = db.Column(db.Integer, db.ForeignKey('user.id'))
    photopath    = db.Column(db.String(128))
    def __repr__(self):
        return f"Objet {self.name}, se trouve: {self.location.__repr__()}"
    def __str__(self):
        return self.__repr__()

class Location(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    batiment  = db.Column(db.String(64))
    etage     = db.Column(db.Integer)
    piece     = db.Column(db.String(64))
    nom       = db.Column(db.String(64))
    description = db.Column(db.String(256), default='')
    photopath = db.Column(db.String(128), default='')
    
    user_id   = db.Column(db.Integer, db.ForeignKey('user.id'))
    items     = db.relationship('Item', backref='item_location', lazy='dynamic')

    def __repr__(self):
        return f"{self.batiment}, {etages[self.etage]}, {self.piece}, {self.nom}"
    def __str__(self):
        return self.__repr__()
