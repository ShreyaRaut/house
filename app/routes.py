from flask import Flask,render_template,request,session,logging,url_for,redirect,flash
from app import app, db, bcrypt
from app.forms import RegistrationForm,LoginForm,AadharForm,UploadAadharForm
from app.models import User
from flask_login import login_user,current_user,logout_user,login_required
import app.mod_ocr.aad_ocr as ado
import os
from werkzeug import secure_filename
from flask_login import login_user,current_user,logout_user
import nexmo


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


@app.route("/aadhar",methods=['GET','POST'])
def aadhar():
    form = AadharForm() 
    if form.validate_on_submit():
        # user=Aadhar(fname=form.fname.data,mname=form.mname.data,lname=form.lname.data,mobile=form.mobile.data,email=form)
        # db.session.add(user)
        # db.session.commit()
        flash(f'kyc done successfully {form.fname.data}!', 'success')
        return redirect(url_for('home'))
    else:
        print(form.errors)
    return render_template('aadhar.html', title='aadhar', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@login_required
@app.route("/uploadaadhar",methods=['GET','POST'])
def uploadaadhar():
    form=UploadAadharForm()
    form1=AadharForm()
    if form.validate_on_submit():
        f=form.photo.data
        filename=secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))


        Name,Middle_Name,Surname,bdate,Gender,aadnum=ado.scan(f.filename)
        print(""+Name)
        print(""+bdate)
        # form1=AadharForm()
        # print("hi fname"+form1.fname.data)
        # form1.current_user.fname=Name
        # form1.mname.data=Middle_Name
        # form1.lname.data=Surname
        # form1.birthday.data=bdate
        # form1.gender.data=Gender
        # form1.adno.data=aadnum
        return render_template('aadhar.html',fname=Name,mname=Middle_Name,lname=Surname,birthday=bdate,gender=Gender,adno=aadnum,form=form1)
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
    return render_template('forgot.html',title='Message')

@app.route("/send",methods=['GET','POST'])
def send():
    Message='564327'
    hashed_password = bcrypt.generate_password_hash(Message).decode('utf-8')
    current_user.password=hashed_password
    response=client.send_message({'from': 'Nexmo', 'to':'919833760985','text':'Your temporary password is'+qMessage})

    return redirect(url_for('login'))

