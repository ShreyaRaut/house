from flask import Flask,render_template,request,session,logging,url_for,redirect,flash
from app import app, db, bcrypt
from app.forms import RegistrationForm,LoginForm,AadharForm,UploadAadharForm,ForgotForm,UploadPanForm,PanForm
from app.models import User,Aadhar,Pan
from flask_login import login_user,current_user,logout_user,login_required
import app.mod_ocr.aad_ocr as ado
import app.mod_ocr.aadA_ocr as ada
import app.mod_ocr.pan_ocr as pan
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
app.config['TESTING']=False

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
@app.route("/aadhar/<int:user_id>/edit",methods=['GET','POST'])
def aadhar(user_id):
    # user_id=current_user.id
    aad= Aadhar.query.get_or_404(user_id)

    form=AadharForm()

    if form.validate_on_submit():
        aad.fname=form.fname.data
        aad.mname=form.mname.data
        aad.lname=form.lname.data
        aad.address=form.address.data
        aad.gender=form.gender.data
        aad.birthday=form.birthday.data
        aad.adno=form.adno.data
        db.session.commit()

        flash(f'Your aadhar details are updated!', 'success')
        return redirect(url_for('viewaadhar',user_id=current_user.id),)
    else:
        print(form.errors)
    return render_template('aadhar.html',title='aadhar', form=form,fname=aad.fname,
    lname=aad.lname,
    mname=aad.mname,
    address=aad.address,
    gender=aad.gender,
    birthday=aad.birthday,
    adno=aad.adno)

@app.route("/aadhar/<int:user_id>/view")
def viewaadhar(user_id):
    aad= Aadhar.query.get_or_404(user_id)

    return render_template('viewaadhar.html',title='viewaadhar',fname=aad.fname,mname=aad.mname,lname=aad.lname)

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
        fa=form.addphoto.data


        Name,Middle_Name,Surname,bdate,Gender,aadnum=ado.scan(f.filename)
        address=ada.scan_aada(fa.filename)
        # hashaad=bcrypt.generate_password_hash(aadnum).decode('utf-8')
        user=Aadhar(fname=Name,mname=Middle_Name,lname=Surname,address=address,gender=Gender,birthday=bdate,adno=aadnum,user_id=current_user.id)
        db.session.add(user)
        db.session.commit()
        flash(f'kyc done successfully !', 'success')
        return redirect(url_for('aadhar',user_id=current_user.id))
    else:
        print(form.errors)

    return render_template('uploadaadhar.html',title='uploadaadhar',form=form)



@app.route("/uploadpancard",methods=['GET','POST'])
def uploadpancard():
    form = UploadPanForm() 
    if form.validate_on_submit():
        f=form.photo.data
        filename=secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))



        Name,Middle_Name,Surname,Father,bdate,panno=pan.scan_pan(f.filename)
        user=Pan(fname=Name,mname=Middle_Name,lname=Surname,father=Father,birthday=bdate,panno=panno,user_id=current_user.id)
        db.session.add(user)
        db.session.commit()
        flash(f'kyc done successfully !', 'success')
        return redirect(url_for('pancard',user_id=current_user.id))
    else:
        print(form.errors)
    return render_template('uploadpan.html', title='PanCard', form=form)

@app.route("/pancard/<int:user_id>/edit",methods=['GET','POST'])
def pancard(user_id):
    # user_id=current_user.id
    aad= Pan.query.get_or_404(user_id)

    form=PanForm()

    if form.validate_on_submit():
        aad.fname=form.fname.data
        aad.mname=form.mname.data
        aad.lname=form.lname.data
        aad.father=form.father.data
        aad.birthday=form.birthday.data
        aad.panno=form.panno.data
        db.session.commit()

        flash(f'Your pan card details are updated!', 'success')
        return redirect(url_for('viewpan',user_id=current_user.id))
    else:
        print(form.errors)
    return render_template('pancard.html',title='pancard', form=form,fname=aad.fname,
    lname=aad.lname,
    mname=aad.mname,
    father=aad.father,
    birthday=aad.birthday,
    panno=aad.panno)

@app.route("/pancard/<int:user_id>/view")
def viewpan(user_id):
    aad= Pan.query.get_or_404(user_id)

    return render_template('viewpan.html',title='viewpan',fname=aad.fname,mname=aad.mname,lname=aad.lname)

# @app.route("/voterid",methods=['GET','POST'])
# def voter():
#     form = VoterForm() 
#     if form.validate_on_submit():
#         f=form.photo.data
#         filename=secure_filename(f.filename)
#         f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))


#         Name,Middle_Name,Surname,Gender,bdate,add,doi,voterno=vote.scan_vote(f.filename)
#         add=votea.scan_voteA(f.filename)
#         bdate=datetime.datetime.strptime('30-01-12', '%d-%m-%y').date()
#         hashvote=bcrypt.generate_password_hash(voterno).decode('utf-8')
#         user=Voter(fname=Name,mname=Middle_Name,lname=Surname,gender=Gender,birthday=bdate,doi=doi,voterno=hashvote,user_id=current_user.id)
#         db.session.add(user)
#         db.session.commit()
#         flash(f'kyc done successfully !', 'success')
#         return redirect(url_for('vote_edit'))
#     else:
#         print(form.errors)
#     return render_template('voterid.html', title='VoterID', form=form)


# @app.route("/drivinglicense",methods=['GET','POST'])
# def driver():
#     form = DriverForm() 
#     if form.validate_on_submit():
#         f=form.photo.data
#         filename=secure_filename(f.filename)
#         f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
#         Name,bdate,add,dov,dlno=driv.scan_dri(f.filename)
#         bdate=datetime.datetime.strptime('30-01-12', '%d-%m-%y').date()
#         dov=datetime.datetime.strptime('30-01-12', '%d-%m-%y').date()
#         hashdl=bcrypt.generate_password_hash(dlno).decode('utf-8')
#         user=Driving(name=Name,birthday=bdate,dlno=hashdl,dov=dov,address=add,user_id=current_user.id)
#         db.session.add(user)
#         db.session.commit()
#         flash(f'kyc done successfully !', 'success')
#         return redirect(url_for('driv_edit'))
#     else:
#         print(form.errors)
#     return render_template('driving.html', title='DrivingLicense', form=form)

# @app.route("/passport",methods=['GET','POST'])
# def passport():
#     form = PassportForm() 
#     if form.validate_on_submit():
#         f=form.photo.data
#         filename=secure_filename(f.filename)
#         f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
#         Name,Surname,nat,gender,bdate,doi,passno=pass.scan_pass(f.filename)
#         bdate=datetime.datetime.strptime('30-01-12', '%d-%m-%y').date()
#         doi=datetime.datetime.strptime('30-01-12', '%d-%m-%y').date()
#         hashpas=bcrypt.generate_password_hash(passno).decode('utf-8')
#         user=Pass(fname=Name,lname=Surname,nationality=nat,birthday=bdate,dlno=hashdl,dov=dov,address=add,user_id=current_user.id)
#         db.session.add(user)
#         db.session.commit()
#         flash(f'kyc done successfully !', 'success')
#         return redirect(url_for('driv_edit'))
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

