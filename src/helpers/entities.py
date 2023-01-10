from helpers.db_helper import DBHelper

db = DBHelper()
print('DB FROM ENTITIES ', db)

class User(db.Model):

    __tablename__ = 'User'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, name, date):
        self.name = name
        self.date = date

    def __repr__(self):
        return f'<User {self.id}, {self.name}, {self.date}>'

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': str(self.date)
        }