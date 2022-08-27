from enum import Enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class Nature(Enum):
    planets = "planets" 
    people = "people"




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False)
    favorites = db.relationship('Favorites', backref="user", uselist=True)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name
        }

        
    def __repr__(self):
        return '<User %r>' % self.name





class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nature = db.Column(db.Enum(Nature), nullable=False)
    people_id = db.Column(db.String(120))
    planet_id = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    # __table_args__ = (db.UniqueConstraint(
    #     "user_id",
    #     "name_favorite",
    #     name = "unique_favorites_for_user"
    # ),)
    



class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    eye_color = db.Column(db.String(200), nullable=False)
    skin_color = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "eye_color": self.eye_color,
            "skin_color": self.eye_color,
            "location": self.location
        }
    



class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    population = db.Column(db.String(200), nullable=False)
    terrain = db.Column(db.String(200), nullable=False)
    climate = db.Column(db.String(200), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain,
            "climate": self.climate
        }
  
    

    

    