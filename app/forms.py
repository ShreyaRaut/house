from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,ValidationError,IntegerField,DateTimeField,FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from app.models import User
from flask_wtf.file import FileField,FileRequired
import phonenumbers

class RegistrationForm(FlaskForm):
    username = StringField('User Name',validators=[DataRequired(), Length(min=5, max=20)])
    fname = StringField('First Name',validators=[DataRequired(), Length(min=2, max=20)])
    mname = StringField('Middle Name',validators=[Length(min=2, max=20)])
    lname = StringField('Last name',validators=[Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    mobile=StringField('Mobile',validators=[DataRequired(),Length(10)])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=6,max=15)])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')



    def validate_email(self,email):

        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email address already exist!')



class LoginForm(FlaskForm):
    username=StringField('User Name',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UploadAadharForm(FlaskForm):
    photo=FileField(validators=[FileRequired()])
    submit = SubmitField('Upload')

class AadharForm(FlaskForm):
    fname = StringField('First Name',validators=[DataRequired(), Length(min=2, max=20)])
    mname = StringField('Middle Name',validators=[Length(min=2, max=20)])
    lname = StringField('Last name',validators=[Length(min=2, max=20)])
    address=StringField('Address',validators=[Length(min=5,max=100)])
    gender = StringField('Gender',validators=[Length(min=4, max=6)])
    birthday= DateTimeField('Date of Birth', format='%d/%m/%y')
    adno=StringField('Aadhar No',validators=[DataRequired(),Length(min=12,max=12)])
    submit = SubmitField('Submit')

class PanForm(FlaskForm):
    fname = StringField('First Name',validators=[DataRequired(), Length(min=2, max=20)])
    mname = StringField('Middle Name',validators=[Length(min=2, max=20)])
    lname = StringField('Last name',validators=[Length(min=2, max=20)])
    father=StringField('Father\'s Name',validators=[Length(min=5,max=100)])
    birthday= DateTimeField('Date of Birth', format='%d/%m/%y')
    panno=StringField('Pancard No',validators=[DataRequired(),Length(min=12,max=12)])
    submit = SubmitField('Submit')

class VoterForm(FlaskForm):
    fname = StringField('First Name',validators=[DataRequired(), Length(min=2, max=20)])
    mname = StringField('Middle Name',validators=[Length(min=2, max=20)])
    lname = StringField('Last name',validators=[Length(min=2, max=20)])
    gender = StringField('Gender',validators=[Length(min=4, max=6)])
    birthday= DateTimeField('Date of Birth', format='%d/%m/%y')
    address=StringField('Address',validators=[Length(min=5,max=100)])
    doc= DateTimeField('Date of Creation', format='%d/%m/%y')
    voterno=StringField('Voter No',validators=[DataRequired(),Length(min=12,max=12)])
    submit = SubmitField('Submit')

class DriverForm(FlaskForm):
    name = StringField('First Name',validators=[DataRequired(), Length(min=2, max=20)])
    birthday= DateTimeField('Date of Birth', format='%d/%m/%y')
    address=StringField('Address',validators=[Length(min=5,max=100)])
    dov= DateTimeField('Date of Issue', format='%d/%m/%y')
    dlno=StringField('Driving License No',validators=[DataRequired(),Length(min=12,max=12)])
    submit = SubmitField('Submit')

class PassportForm(FlaskForm):
    fname = StringField('First Name',validators=[DataRequired(), Length(min=2, max=20)])
    lname = StringField('Last name',validators=[Length(min=2, max=20)])
    nationality=StringField('Nationality',validators=[Length(min=5,max=100)])
    gender = StringField('Gender',validators=[Length(min=1, max=1)])
    birthday= DateTimeField('Date of Birth', format='%d/%m/%y')
    placeofbirth=StringField('Place of Birth',validators=[Length(min=5,max=100)])
    doi= DateTimeField('Date of Issue', format='%d/%m/%y')
    passportno=StringField('Passport No',validators=[DataRequired(),Length(min=12,max=12)])
    submit = SubmitField('Submit')

class ForgotForm(FlaskForm):
    username=StringField('User Name',validators=[DataRequired()])
    submit = SubmitField('Send Temporary Password')