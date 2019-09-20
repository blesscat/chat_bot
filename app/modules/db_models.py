from app import db


class Beauty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)

    def __init__(self, url):
        self.url = url


class Ban(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer)   
    user_id = db.Column(db.Integer)
    
    def __init__(self, chat_id, user_id):
        self.chat_id = chat_id
        self.user_id = user_id

class Launch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
        }


class GqLaunch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
        }
