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
    photo=FileField('Details',validators=[FileRequired()])
    addphoto=FileField('Address Details',validators=[FileRequired()])
    submit = SubmitField('Upload')

class AadharForm(FlaskForm):
    fname = StringField('First Name',validators=[DataRequired(), Length(min=2, max=20)])
    mname = StringField('Middle Name',validators=[Length(min=2, max=20)])
    lname = StringField('Last name',validators=[Length(min=2, max=20)])
    address=StringField('Address',validators=[Length(min=5)])
    gender = StringField('Gender',validators=[Length(min=4, max=6)])
    birthday= StringField('Date of Birth',validators=[DataRequired(),Length(min=10,max=10)])
    adno=StringField('Aadhar No',validators=[DataRequired(),Length(min=12,max=12)])
    submit = SubmitField('Submit')

class UploadPanForm(FlaskForm):
    photo=FileField('Details',validators=[FileRequired()])
    submit = SubmitField('Upload')

class UploadVoterForm(FlaskForm):
    photo=FileField('Details',validators=[FileRequired()])
    addphoto=FileField('Address Details',validators=[FileRequired()])
    submit = SubmitField('Upload')

class PanForm(FlaskForm):
    fname = StringField('First Name',validators=[DataRequired(), Length(min=2, max=20)])
    mname = StringField('Middle Name',validators=[Length(min=2, max=20)])
    lname = StringField('Last name',validators=[Length(min=2, max=20)])
    father=StringField('Father\'s Name',validators=[Length(min=5,max=100)])
    birthday= StringField('Date of Birth', validators=[Length(max=10)])
    panno=StringField('Pancard No',validators=[DataRequired(),Length(min=10,max=10)])
    submit = SubmitField('Submit')

class VoterForm(FlaskForm):
    fname = StringField('First Name',validators=[DataRequired(), Length(min=2, max=20)])
    mname = StringField('Middle Name',validators=[Length(min=2, max=20)])
    lname = StringField('Last name',validators=[Length(min=2, max=20)])
    gender = StringField('Gender',validators=[Length(min=4, max=6)])
    birthday= StringField('Date of Birth',validators=[Length(min=5, max=10)] )
    address=StringField('Address',validators=[Length(min=5,max=500)])
    doi= StringField('Date of Issue', validators=[Length(min=5,max=500)])
    voterno=StringField('Voter No',validators=[DataRequired(),Length(min=10,max=10)])
    submit = SubmitField('Submit')

class UploadDriverForm(FlaskForm):
    photo=FileField('Details',validators=[FileRequired()])
    submit = SubmitField('Upload')

class DriverForm(FlaskForm):
    name = StringField('First Name',validators=[DataRequired(), Length(min=2, max=20)])
    birthday= StringField('Date of Birth', validators=[Length(max=10)])
    address=StringField('Address',validators=[Length(min=5,max=100)])
    dov= StringField('Date of Issue', validators=[Length(max=10)])
    dlno=StringField('Driving License No',validators=[DataRequired(),Length(min=12,max=12)])
    submit = SubmitField('Submit')

# class UploadPassForm(FlaskForm):
#     photo=FileField('Details',validators=[FileRequired()])
#     submit = SubmitField('Upload')

# class PassportForm(FlaskForm):
#     fname = StringField('First Name',validators=[DataRequired(), Length(min=2, max=20)])
#     lname = StringField('Last name',validators=[Length(min=2, max=20)])
#     nationality=StringField('Nationality',validators=[Length(min=5,max=100)])
#     gender = StringField('Gender',validators=[Length(min=1, max=1)])
#     birthday= StringField('Date of Birth', validators=[Length(max=10)])
#     placeofbirth=StringField('Place of Birth',validators=[Length(min=5,max=100)])
#     doi= StringField('Date of Issue', validators=[Length(max=10)])
#     passportno=StringField('Passport No',validators=[DataRequired(),Length(min=12,max=12)])
#     submit = SubmitField('Submit')

class ForgotForm(FlaskForm):
    username=StringField('User Name',validators=[DataRequired()])
    submit = SubmitField('Send Temporary Password')

class ChooseForm(FlaskForm):
    choice_a = SubmitField('Aadhar Card')
    choice_b = SubmitField('Pan Card')
    choice_c = SubmitField('Voters Id')
    choice_d = SubmitField('Driving License')


    