from app import db,login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname=db.Column(db.String(20),nullable=False)
    mname=db.Column(db.String(20),)
    lname=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(20),nullable=False,unique=True)
    mobile=db.Column(db.Integer,nullable=False)
    password=db.Column(db.String(60),nullable=False)

    def __repr__(self):
        return f"User('{self.id}',{self.fname}','{self.lname}','{self.email}','{self.mobile}')"
