from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)
    favorites = db.relationship('Favorite', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, it's a security breach
        }


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    climate = db.Column(db.String(200), nullable=False)
    diameter = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Planet {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
        }


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    height = db.Column(db.String(200), nullable=False)
    mass = db.Column(db.String(200), nullable=False)
    hair_color = db.Column(db.String(100), nullable=False)
    skin_color = db.Column(db.String(100), nullable=False)
    eye_color = db.Column(db.String(100), nullable=False)
    birth_year = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<People {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
        }


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)

    planet = db.relationship('Planet', lazy=True)
    people = db.relationship('People', lazy=True)

    def __repr__(self):
        return f'<Favorite User:{self.user_id} Planet:{self.planet_id} People:{self.people_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "people_id": self.people_id,
        }