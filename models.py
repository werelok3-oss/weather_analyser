from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WeatherHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    temp = db.Column(db.Integer)
    description = db.Column(db.String(100))