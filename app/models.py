from app import db,login_manager
from flask_login import UserMixin
from sqlalchemy import ForeignKey


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    fname=db.Column(db.String(20),nullable=False)
    mname=db.Column(db.String(20))
    lname=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(20),nullable=False,unique=True)
    mobile=db.Column(db.Integer,nullable=False)
    password=db.Column(db.String(60),nullable=False)
    aadhar=db.relationship('Aadhar',backref='user',lazy=True)

    def __repr__(self):
        return f"User('{self.id}',{self.username}',{self.fname}','{self.lname}','{self.email}','{self.mobile}')"


class Aadhar(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True)
    fname=db.Column(db.String(20),nullable=False)
    mname=db.Column(db.String(20))
    lname=db.Column(db.String(20),nullable=False)
    address=db.Column(db.String(100),nullable=False)
    gender=db.Column(db.String(6),nullable=False)
    birthday=db.Column(db.DateTime,nullable=False)
    adno=db.Column(db.String(12),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    # print(user_id)


    def __repr__(self):
        # print("user id")
        # print(user_id)
        test = f"Aadhar('{self.fname}','{self.mname}','{self.lname}','{self.address}','{self.gender}','{self.birthday}','{self.adno}','{self.id}')"
        # print(test)
        # print(self.user_id)
        return test

# class Uploadaadhar(db.Model,UserMixin):
#     user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False,primary_key=True)
#     # = db.Column(db.LargeBinary)

    # def __repr__(self):
    #     return f"Uploadaadhar('{self.aadimage}')"
