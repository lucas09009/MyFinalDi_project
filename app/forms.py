from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class SignupForm(FlaskForm):
    Username = StringField("Pseudo",  validators=[DataRequired()])
    Password = PasswordField("Password",  validators=[DataRequired()])
    confirm_Password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("S'inscrire")


class LoginForm(FlaskForm):
    Username = StringField("Pseudo",  validators=[DataRequired()])
    Password = PasswordField("Password",  validators=[DataRequired()])
    submit = SubmitField('Se connecter')


    
