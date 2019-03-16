from flask import Flask,render_template,request,session,logging,url_for,redirect,flash
from app import app, db, bcrypt
from app.forms import RegistrationForm,LoginForm,AadharForm,UploadAadharForm
from app.models import User
from flask_login import login_user,current_user,logout_user,login_required
import app.mod_ocr.aad_ocr as ado

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
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
        flash(f'kyc done successfully {form.fname.data}!', 'success')
        return redirect(url_for('home'))
    else:
        print(form.errors)
    return render_template('aadhar.html', title='Aadhar', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@login_required
@app.route("/uploadaadhar",methods=['GET','POST'])
def uploadaadhar():
    form=UploadAadharForm()
    if form.validate_on_submit():
        Name,Middle_Name,Surname,bdate,Gender,aadnum=ado.scan(form.aadimage.data)
        form1=AadharForm()
        form1.fname.data=Name
        form1.mname.data=Middle_Name
        form1.lname.data=Surname
        form1.birthday.data=bdate
        form1.gender.data=Gender
        form1.adno.data=aadnum

        return render_template('aadhar.html',title='Aadhar',form=form1)
    else:
        flash('Please upload a valid image')
    return render_template('uploadaadhar.html',title='UploadAadhar',form=form)



@app.route("/pancard",methods=['GET','POST'])
def pancard():
    form = PanForm() 
    if form.validate_on_submit():
        flash(f'kyc done successfully {form.fname.data}!', 'success')
        return redirect(url_for('home'))
    else:
        print(form.errors)
    return render_template('pancard.html', title='PanCard', form=form)

@app.route("/voterid",methods=['GET','POST'])
def voter():
    form = VoterForm() 
    if form.validate_on_submit():
        flash(f'kyc done successfully {form.fname.data}!', 'success')
        return redirect(url_for('home'))
    else:
        print(form.errors)
    return render_template('voterid.html', title='VoterID', form=form)


@app.route("/drivinglicense",methods=['GET','POST'])
def driver():
    form = DriverForm() 
    if form.validate_on_submit():
        flash(f'kyc done successfully {form.fname.data}!', 'success')
        return redirect(url_for('home'))
    else:
        print(form.errors)
    return render_template('driving.html', title='DrivingLicense', form=form)

@app.route("/passport",methods=['GET','POST'])
def passport():
    form = PassportForm() 
    if form.validate_on_submit():
        flash(f'kyc done successfully {form.fname.data}!', 'success')
        return redirect(url_for('home'))
    else:
        print(form.errors)
    return render_template('passport.html', title='Passport', form=form)

