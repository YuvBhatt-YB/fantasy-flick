from FantasyFlick.app import db
from flask_login import UserMixin

class User(db.Model,UserMixin):

    __tablename__ = "users"

    uid = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,nullable=False,unique=True)
    email = db.Column(db.String,nullable=False)
    password = db.Column(db.String,nullable=False)
    role = db.Column(db.String,nullable=False)
    wallet_balance = db.Column(db.Integer,default=1000)

    def __repr__(self):
        return f"<User : {self.username} , role : {self.role}>"
    
    def get_id(self):
        return self.uid

