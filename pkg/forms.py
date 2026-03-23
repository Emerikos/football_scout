from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,PasswordField,TextAreaField,SubmitField,BooleanField,SelectField,RadioField,SelectMultipleField,DateField
from wtforms.validators import DataRequired,Email,EqualTo,Length,Regexp
from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms.widgets import ListWidget,CheckboxInput


class RegisterPlayer(FlaskForm):
    firstname = StringField('Firstname:',validators=[DataRequired(message='Please input your first name')])
    lastname = StringField('Lastname:',validators=[DataRequired(message='Please input your last name')])
    email = EmailField('Email:',validators=[DataRequired(message='Please input your email address'),Email()])
    password = PasswordField('Password:',validators=[DataRequired(message='Please choose a password'),Length(min=4,message='Your password should have a minimum of 4 characters')])
    repeat_password = PasswordField('Confirm Password:',validators=[DataRequired(),EqualTo('password',message='Passwords do not match')])
    dob = DateField('Date of birth:',format='%Y-%m-%d',validators=[DataRequired()])
    country = StringField('Country of origin:',validators=[DataRequired()])
    primary_position = SelectField('Primary Position:',coerce=int,validators=[DataRequired(message="Please select a primary position")])
    secondary_positions = SelectMultipleField('Secondary Position(s):',coerce=int,option_widget=CheckboxInput(),widget=ListWidget(prefix_label=False))
    # preferred_foot = RadioField('Preferred foot:',choices=[('left','left'),('right','right'),('both','both')],validators=[DataRequired(message="Please choose a preferred foot")])
    height = StringField('Height(CM):')
    phone_number = StringField("Phone Number",validators=[DataRequired(message="Phone number is required"),Length(min=10, max=15),Regexp(r'^\+?\d{10,15}$', message="Enter a valid phone number")])
    confirm = BooleanField('I confirm that the information provided is accurate',validators=[DataRequired(message='Please check the box')])
    terms = BooleanField('I agree to the terms and conditions',validators=[DataRequired(message='Please check the box')])
    submit_player = SubmitField('Register Player')


class RegisterScout(FlaskForm):
    firstname_scout = StringField('Firstname',validators=[DataRequired(message='Please input your first name')])
    lastname_scout = StringField('Lastname',validators=[DataRequired(message='Please input your last name')])
    email_scout = EmailField('Email',validators=[DataRequired(message='Please input your email address'),Email()])
    password_scout = PasswordField('Password',validators=[DataRequired(message='Please choose a password'),Length(min=4,message='Your password should have a minimum of 4 characters')])
    repeat_password_scout = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password_scout',message='Passwords do not match')])
    agree = BooleanField('I agree to use this platform for scouting purposes only',validators=[DataRequired(message="Please check the box")])
    submit_scout = SubmitField('Register Scout')



class Login(FlaskForm):
    email = EmailField('Email Address',validators=[Email(),DataRequired(message="Please input your username")])
    password = PasswordField('Password',validators=[DataRequired(message="please input your password")])
    submit = SubmitField('Login')




def safe_enum(value: str, allowed_values: list[str]):
    normalized = value.lower()
    if normalized not in allowed_values:
        raise ValueError(f"Invalid value: {value}")
    return normalized




class Profileform(FlaskForm):
    firstname=StringField("Firstname:",validators=[DataRequired(message='Specify the firstname')])
    lastname=StringField("Lastname:",validators=[DataRequired(message='Specify the lastname')])
    phone_number = StringField("Phone Number",validators=[Length(min=10, max=15),Regexp(r'^\+?\d{10,15}$', message="Enter a valid phone number")])
    dob = DateField('Date of birth:',format='%Y-%m-%d')
    video_caption=StringField("Caption:")
    video_link=StringField("Video Link:")
    video_description=TextAreaField("Description:")
    email = EmailField('Email:')
    btnsubmit=SubmitField("Apply")


class ScoutProfileform(FlaskForm):
    firstname=StringField("Firstname:",validators=[DataRequired(message='Specify the firstname')])
    lastname=StringField("Lastname:",validators=[DataRequired(message='Specify the lastname')])
    email = EmailField('Email:')
    btnsubmit=SubmitField("Apply")



class PhotoForm(FlaskForm):
    photo = FileField(validators=[FileRequired(),FileAllowed(['jpg','png','jpeg'],message="Invalid File type")])
    btn=SubmitField("Upload File")