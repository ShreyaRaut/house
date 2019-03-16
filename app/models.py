from app import db,login_manager
from flask_login import UserMixin
from sqlalchemy import ForeignKey


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id=db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    fname=db.Column(db.String(20),nullable=False)
    mname=db.Column(db.String(20),)
    lname=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(20),nullable=False,unique=True)
    mobile=db.Column(db.Integer,nullable=False)
    password=db.Column(db.String(60),nullable=False)
    #aadhar=db.relationship('Aadhar',backref='author',lazy=True)

    def __repr__(self):
        return f"User('{self.username}',{self.fname}','{self.lname}','{self.email}','{self.mobile}')"


class Aadhar(db.Model,UserMixin):
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    fname=db.Column(db.String(20),nullable=False)
    mname=db.Column(db.String(20))
    lname=db.Column(db.String(20),nullable=False)
    address=db.Column(db.String(100),nullable=False)
    gender=db.Column(db.String(6),nullable=False)
    birthday=db.Column(db.DateTime,nullable=False)
    adno=db.Column(db.String(12),nullable=False,primary_key=True)


    def __repr__(self):
        return f"Aadhar('{self.fname}',{self.mname}','{self.lname}','{self.birthday}',{self.adno}')"

# class Uploadaadhar(db.Model,UserMixin):
#     user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False,primary_key=True)
#     # = db.Column(db.LargeBinary)

    # def __repr__(self):
    #     return f"Uploadaadhar('{self.aadimage}')"
