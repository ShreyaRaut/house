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
    # aadharid = db.Column(db.Integer,db.ForeignKey('aadhar.id'),nullable=False,unique=True)
    # panid = db.Column(db.Integer,db.ForeignKey('pan.id'),nullable=False,unique=True)
    # voterid = db.Column(db.Integer,db.ForeignKey('voter.id'),nullable=False,unique=True)
    aadhar=db.relationship('Aadhar',backref='user',lazy=True)
    pan=db.relationship('Pan',backref='user',lazy=True)
    voter=db.relationship('Voter',backref='user',lazy=True)
    driver=db.relationship('Driving',backref='user',lazy=True)
    # pass=db.relationship('Pass',backref='user',lazy=True)

    def __repr__(self):
        return f"User('{self.id}','{self.username}','{self.fname}','{self.lname}','{self.email}','{self.mobile},','{self.aadhar}','{self.pan}','{self.voter}','{self.driver}')"


class Aadhar(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True)
    fname=db.Column(db.String(20),nullable=False)
    mname=db.Column(db.String(20))
    lname=db.Column(db.String(20),nullable=False)
    address=db.Column(db.String(500),nullable=False)
    gender=db.Column(db.String(6),nullable=False)
    birthday=db.Column(db.String(10),nullable=False)
    adno=db.Column(db.String(12),nullable=False)
    # user=db.relationship('User',backref='aadhar',lazy=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False,unique=True)


    def __repr__(self):
        return f"Aadhar('{self.fname}','{self.mname}','{self.lname}','{self.address}','{self.gender}','{self.birthday}','{self.adno}''{self.id}'),'{self.user_id}'"




class Pan(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True)
    fname=db.Column(db.String(20),nullable=False)
    mname=db.Column(db.String(20))
    lname=db.Column(db.String(20),nullable=False)
    father=db.Column(db.String(20),nullable=False)
    birthday=db.Column(db.String(10),nullable=False)
    panno=db.Column(db.String(10),nullable=False)
    # user=db.relationship('User',backref='pan',lazy=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False,unique=True)

    def __repr__(self):
        return f"Aadhar('{self.fname}','{self.mname}','{self.lname}','{self.father}','{self.birthday}','{self.panno}','{self.id}','{self.user_id}')"


class Voter(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True)
    fname=db.Column(db.String(20),nullable=False)
    mname=db.Column(db.String(20))
    lname=db.Column(db.String(20),nullable=False)
    gender=db.Column(db.String(6),nullable=False)
    birthday=db.Column(db.String(10),nullable=False)
    address=db.Column(db.String(500),nullable=False)
    doi=db.Column(db.String(10),nullable=False)
    voterno=db.Column(db.String(10),nullable=False)
    # user=db.relationship('User',backref='voter',lazy=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False,unique=True)

    def __repr__(self):
        return f"Voter('{self.fname}','{self.mname}','{self.lname}','{self.gender}','{self.birthday}','{self.address}','{self.doi}','{self.voterno}','{self.id}')"


# class Pass(db.Model):
#     id=db.Column(db.Integer,primary_key=True,unique=True)
#     fname=db.Column(db.String(20),nullable=False)
#     lname=db.Column(db.String(20),nullable=False)
#     nationality=db.Column(db.String(20),nullable=False)
#     gender=db.Column(db.String(6),nullable=False)
#     birthday=db.Column(db.String(10),nullable=False)
#     doi=db.Column(db.String(10),nullable=False)
#     passportno=db.Column(db.String(10),nullable=False)
#     user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False,unique=True)

#     def __repr__(self):
#         return f"Pass('{self.fname}','{self.lname}','{self.nationality}','{self.gender}','{self.birthday}','{self.doi}','{self.passportno}','{self.user_id}')"


class Driving(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True)
    name=db.Column(db.String(20),nullable=False)
    birthday=db.Column(db.String(20),nullable=False)
    address=db.Column(db.String(100),nullable=False)
    dov=db.Column(db.String(20),nullable=False)
    dlno=db.Column(db.String(10),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False,unique=True)

    def __repr__(self):
        return f"Driving('{self.fname}','{self.lname}','{self.nationality}','{self.gender}','{self.birthday}','{self.doi}','{self.passportno}','{self.user_id}')"
