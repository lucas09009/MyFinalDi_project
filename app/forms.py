from wtforms import StringField, PasswordField, SubmitField, DateField, TextAreaField, FileField, IntegerField,SelectField
from wtforms.validators import DataRequired, Optional
from flask_wtf import FlaskForm

class SignupForm(FlaskForm):
    Username = StringField("Username",  validators=[DataRequired()])
    Password = PasswordField("Password",  validators=[DataRequired()])
    confirm_Password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("S'inscrire")

class LoginForm(FlaskForm):
    Username = StringField("Username",  validators=[DataRequired()])
    Password = PasswordField("Password",  validators=[DataRequired()])
    submit = SubmitField('Se connecter')

class PublierArticles(FlaskForm):
        name = StringField("name", validators=[DataRequired()])
        category = SelectField("category", validators=[DataRequired()], choices=[
        'HIGH-TECH',
        'Vetements',
        'Sous-Vetements',
        'Chaussures',
        'Sacs',
        'Education',
        'Sport',
        'Beauté-Esthétique',
        'Meubles pour maison'
    ])        
        Description = StringField("Description", validators=[DataRequired()])
        date_arrive = DateField("date_arrive ", validators=[DataRequired()])
        details = TextAreaField("details", validators=[DataRequired()])
        price = IntegerField("price", validators=[DataRequired()])
        quantity = IntegerField("quantity", validators=[DataRequired()])
        image = FileField("image",  validators=[DataRequired()])
        submit = SubmitField("submit", validators=[DataRequired()])         

class EditProfileForm(FlaskForm):
    Username = StringField("Username",  validators=[DataRequired()])
    Image = FileField("Image",  validators=[Optional()])
    Biographie = TextAreaField(('Bio'), validators=[Optional()])
    submit = SubmitField('Enregistrer')