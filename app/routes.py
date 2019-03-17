from flask import Flask,render_template,request,session,logging,url_for,redirect,flash
from app import app, db, bcrypt
from app.forms import RegistrationForm,LoginForm,AadharForm,UploadAadharForm,ForgotForm
from app.models import User,Aadhar
from flask_login import login_user,current_user,logout_user,login_required
import app.mod_ocr.aad_ocr as ado
import os
from werkzeug import secure_filename
from flask_login import login_user,current_user,logout_user
import nexmo
import datetime
import random


# APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
UPLOAD_FOLDER = os.path.basename('./uploads/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client=nexmo.Client(key='d6ab2286', secret='2StTxLOOxYq5OaxF')

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,fname=form.fname.data,mname=form.mname.data,lname=form.lname.data,mobile=form.mobile.data,email=form.email.data,password=hash)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created successfully {form.username.data}!', 'success')
        return redirect(url_for('login'))
    else:
        print(form.errors)
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# form1=AadharForm()
@app.route("/aadhar",methods=['GET','POST'])
def aadhar():
    user_id=current_user.id
    aad= Aadhar.query.get_or_404(user_id)

    flash(f'First Name:{aad.fname}')
    flash(f'Middle Name:{aad.mname}')
    flash(f'Last Name:{aad.lname}')
    flash(f'Address:{aad.address}')
    flash(f'Gender:{aad.gender}')
    flash(f'Birthday:{aad.birthday}')
    flash(f'Aadhar Number:{aad.adno}')
    # print("fvdfvdf"+user_id)
    form=AadharForm()
    
    
    # form.fname.data=aad.fname
    # form.mname.data=aad.mname
    # form.lname.data=aad.lname
    # form.address.data=aad.address
    # form.gender.data=aad.gender
    # form.birthday.data=aad.birthday
    # form.adno.data=aad.adno

    # if form.validate_on_submit():
    #     aad.fname=form.fname.data
    #     aad.mname=form.mname.data
    #     aad.lname=form.lname.data
    #     aad.address=form.address.data
    #     aad.gender=form.gender.data
    #     aad.birthday=form.birthday.data
    #     aad.adno=form.adno.data
    #     db.session.commit()

    #     # print("aadhar form")
    #     # hashaad=bcrypt.generate_password_hash(form.adno.data).decode('utf-8')
    #     # user=Aadhar(fname=form.fname.data,mname=form.mname.data,lname=form.lname.data,address=form.address.data,gender=form.gender.data,birthday=form.birthday.data,adno=hashaad)
    #     # print("hi"+ form.fname.data)
    #     # print("your aadhar no "+form.adno.data)
    #     # db.session.add(user)
    #     # db.session.commit()
    #     flash(f'Your aadhar details are updated!', 'success')
    #     return redirect(url_for('home'),)
    # elif request.method=='GET':
    #     form.fname.data=aad.fname
    #     form.mname.data=aad.mname
    #     form.lname.data=aad.lname
    #     form.address.data=aad.address
    #     form.gender.data=aad.gender
    #     form.birthday.data=aad.birthday
    #     form.adno.data=aad.adno
    # else:
    #     print(form.errors)
    return render_template('aadhar.html',title='aadhar', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@login_required
@app.route("/uploadaadhar",methods=['GET','POST'])
def uploadaadhar():
    form=UploadAadharForm()
    if form.validate_on_submit():
        f=form.photo.data
        filename=secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))


        Name,Middle_Name,Surname,bdate,Gender,aadnum=ado.scan(f.filename)
        print(current_user.id)
        bdate=datetime.datetime.strptime('30-01-12', '%d-%m-%y').date()
        hashaad=bcrypt.generate_password_hash(aadnum).decode('utf-8')
        user=Aadhar(fname=Name,mname=Middle_Name,lname=Surname,address='            ',gender=Gender,birthday=bdate,adno=hashaad,user_id=current_user.id)
        db.session.add(user)
        db.session.commit()
        flash(f'kyc done successfully !', 'success')
        return redirect(url_for('aadhar'))
        # form1=AadharForm()
        # print("hi fname"+form1.fname.data)
        # form1.current_user.fname=Name
        # form1.mname.data=Middle_Name
        # form1.lname.data=Surname
        # form1.birthday.data=bdate
        # form1.gender.data=Gender
        # form1.adno.data=aadnum
        # return render_template('aadhar.html',fname=Name,mname=Middle_Name,lname=Surname,birthday=bdate,gender=Gender,adno=aadnum,form=form1)
        # if form1.validate_on_submit()
    else:
        print(form.errors)

    return render_template('uploadaadhar.html',title='uploadaadhar',form=form)



# @app.route("/pancard",methods=['GET','POST'])
# def pancard():
#     form = PanForm() 
#     if form.validate_on_submit():
#         flash(f'kyc done successfully {form.fname.data}!', 'success')
#         return redirect(url_for('home'))
#     else:
#         print(form.errors)
#     return render_template('pancard.html', title='PanCard', form=form)

# @app.route("/voterid",methods=['GET','POST'])
# def voter():
#     form = VoterForm() 
#     if form.validate_on_submit():
#         flash(f'kyc done successfully {form.fname.data}!', 'success')
#         return redirect(url_for('home'))
#     else:
#         print(form.errors)
#     return render_template('voterid.html', title='VoterID', form=form)


# @app.route("/drivinglicense",methods=['GET','POST'])
# def driver():
#     form = DriverForm() 
#     if form.validate_on_submit():
#         flash(f'kyc done successfully {form.fname.data}!', 'success')
#         return redirect(url_for('home'))
#     else:
#         print(form.errors)
#     return render_template('driving.html', title='DrivingLicense', form=form)

# @app.route("/passport",methods=['GET','POST'])
# def passport():
#     form = PassportForm() 
#     if form.validate_on_submit():
#         flash(f'kyc done successfully {form.fname.data}!', 'success')
#         return redirect(url_for('home'))
#     else:
#         print(form.errors)
#     return render_template('passport.html', title='Passport', form=form)


@app.route("/forgotpassword",methods=['GET','POST'])
def index():
    form=ForgotForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        # number="91"+str(user.mobile)
        number='919833760985'
        Message=str(random.randint(100000,999999))
        hashed_password = bcrypt.generate_password_hash(Message).decode('utf-8')
        user.password=hashed_password
        db.session.commit()
        response=client.send_message({'from': 'Nexmo', 'to':number,'text':'Your temporary password is '+Message})

        return redirect(url_for('login'))
    else:
         print(form.errors)
    return render_template('forgot.html',title='Message',form=form)

