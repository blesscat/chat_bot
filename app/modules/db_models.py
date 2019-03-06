from app import db


class Beauty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)

    def __init__(self, url):
        self.url = url


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
