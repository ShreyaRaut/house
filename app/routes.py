from flask import Flask,render_template,request,session,logging,url_for,redirect,flash
from app import app, db, bcrypt
from app.forms import RegistrationForm,LoginForm,AadharForm,UploadAadharForm,ForgotForm,UploadPanForm,PanForm,ChooseForm,UploadVoterForm,VoterForm,UploadDriverForm,DriverForm
from app.models import User,Aadhar,Pan,Voter,Driving
from flask_login import login_user,current_user,logout_user,login_required
import app.mod_ocr.aad_ocr as ado
import app.mod_ocr.aadA_ocr as ada
import app.mod_ocr.pan_ocr as pan
import app.mod_ocr.vote_ocr as vote
import app.mod_ocr.voteA_ocr as votea
import app.mod_ocr.dri_ocr as driv
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


@app.route("/chooseform")
def chooseform():
    form=ChooseForm()
    return render_template('chooseform.html',form=form, title='Choose_Form')


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
    reqid=User.query.get_or_404(user_id)
    aadid=reqid.aadhar[1]
    print("Hey there:"+str(aadid))
    aad= Aadhar.query.get_or_404(aadid)

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
        aad= User.query.get_or_404(current_user.id)
        aadharid=aad.aadhar
        if len(aadharid)!=0:
            flash(f'Your aadhar card is already registered ','success')
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
        pann=User.query.get_or_404(current_user.id)
        panid=pann.pan
        if len(panid)!=0:
            flash(f'Your pan card is already registered ','success')
            return redirect(url_for('pancard',user_id=current_user.id))
        else:
            print(form.errors)
    return render_template('uploadpan.html',title='uploadpancard',form=form)


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

@app.route("/uploadvoter",methods=['GET','POST'])
def uploadvoter():
    form = UploadVoterForm() 
    if form.validate_on_submit():
        f=form.photo.data
        fa=form.addphoto.data
        filename=secure_filename(f.filename)
        addfile=secure_filename(fa.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        fa.save(os.path.join(app.config['UPLOAD_FOLDER'],addfile))


        Name,Middle_Name,Surname,Gender,bdate,voterno=vote.scan_vote(f.filename)
        add,doi=votea.scan_voteA(fa.filename)
        # hashvote=bcrypt.generate_password_hash(voterno).decode('utf-8')
        user=Voter(fname=Name,mname=Middle_Name,lname=Surname,gender=Gender,birthday=bdate,address=add,doi=doi,voterno=voterno,user_id=current_user.id)
        db.session.add(user)
        db.session.commit()
        flash(f'kyc done successfully !', 'success')
        return redirect(url_for('voterid',user_id=current_user.id))
    else:
        vot=User.query.get_or_404(current_user.id)
        voteid=vot.voter
        if len(voteid)!=0:
            flash(f'Your voter id is already registered ','success')
            return redirect(url_for('voterid',user_id=current_user.id))
        else:
            print(form.errors)
    return render_template('uploadvoter.html', title='uploadvoter', form=form)

@app.route("/voter/<int:user_id>/edit",methods=['GET','POST'])
def voterid(user_id):
    # user_id=current_user.id
    aad= Voter.query.get_or_404(user_id)

    form=VoterForm()

    if form.validate_on_submit():
        aad.fname=form.fname.data
        aad.mname=form.mname.data
        aad.lname=form.lname.data
        aad.gender=form.gender.data
        aad.birthday=form.birthday.data
        aad.address=form.address.data
        aad.doi=form.doi.data
        aad.voterno=form.voterno.data
        db.session.commit()

        flash(f'Your voter id details are updated!', 'success')
        return redirect(url_for('viewvote',user_id=current_user.id))
    else:
        print(form.errors)
    return render_template('voterid.html',title='voter', form=form,fname=aad.fname,
    lname=aad.lname,
    mname=aad.mname,
    gender=aad.gender,
    birthday=aad.birthday,
    address=aad.address,
    doi=aad.doi,
    voterno=aad.voterno)

@app.route("/voter/<int:user_id>/view")
def viewvote(user_id):
    aad= Voter.query.get_or_404(user_id)

    return render_template('viewvote.html',title='viewvote',fname=aad.fname,mname=aad.mname,lname=aad.lname)

@app.route("/uploaddriver",methods=['GET','POST'])
def uploaddriver():
    form = UploadDriverForm() 
    if form.validate_on_submit():
        f=form.photo.data
        filename=secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

        Name,Address,dlno,dov,dob=driv.scan_driver(f.filename)
        # hashvote=bcrypt.generate_password_hash(voterno).decode('utf-8')
        user=Driving(name=Name,address=Address,dlno=dlno,dov=dov,birthday=dob,user_id=current_user.id)
        db.session.add(user)
        db.session.commit()
        flash(f'kyc done successfully !', 'success')
        return redirect(url_for('driver',user_id=current_user.id))
    else:
        vot=User.query.get_or_404(current_user.id)
        driver=vot.driver
        if len(driver)!=0:
            flash(f'Your driving license  is already registered ','success')
            return redirect(url_for('driver',user_id=current_user.id))
        else:
            print(form.errors)
    return render_template('uploaddriver.html', title='uploaddriver', form=form)

@app.route("/driver/<int:user_id>/edit",methods=['GET','POST'])
def driver(user_id):
    # user_id=current_user.id
    aad= Driving.query.get_or_404(user_id)

    form=DriverForm()

    if form.validate_on_submit():
        aad.name=form.name.data
        aad.birthday=form.birthday.data
        aad.address=form.address.data
        aad.dlno=form.dlno.data
        aad.dov=form.dov.data
        db.session.commit()

        flash(f'Your driving license details are updated!', 'success')
        return redirect(url_for('viewdriver',user_id=current_user.id))
    else:
        print(form.errors)
    return render_template('driving.html',title='driver', form=form,name=aad.name,
    birthday=aad.birthday,
    address=aad.address,
    dlno=aad.dlno,
    dov=aad.dov)

@app.route("/driver/<int:user_id>/view")
def viewdriver(user_id):
    aad= Driving.query.get_or_404(user_id)

    return render_template('viewdriver.html',title='viewdriver',name=aad.name)

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

