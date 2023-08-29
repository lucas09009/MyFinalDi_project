from wtforms import StringField, PasswordField, SubmitField, DateField, TextAreaField, FileField, IntegerField,SelectField
from wtforms.validators import DataRequired, Optional
from flask_wtf import FlaskForm
from .utils import ChoixDeCategories
class SignupForm(FlaskForm):
    Username = StringField("Username",  validators=[DataRequired()])
    Password = PasswordField("Password",  validators=[DataRequired()])
    confirm_Password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("S'inscrire")

class LoginForm(FlaskForm):
    Username = StringField("Username",  validators=[DataRequired()])
    Password = PasswordField("Password",  validators=[DataRequired()])
    submit = SubmitField('Se connecter')


class AjouterCategorieForm(FlaskForm):
    name = StringField('Nom de la catégorie', validators=[DataRequired()])
    icon_name = StringField('Icone Name', validators=[DataRequired()])
    submit = SubmitField('Ajouter')

class PublierArticles(FlaskForm):
        name = StringField("name", validators=[DataRequired()])
        category = SelectField("Category", choices=[])        
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


class ImageDefilanteForm(FlaskForm):
    image = FileField("image",  validators=[DataRequired()])
    details = StringField("details,", validators=[DataRequired()])
    submit = SubmitField('Enregistrer')



class ModifierArticleForm(FlaskForm):
    id = IntegerField("article_id", validators=[DataRequired()])
    name = StringField("name", validators=[Optional()])
    name = StringField("name", validators=[DataRequired()])
    category = SelectField("category", validators=[DataRequired()], choices=[])        
    Description = StringField("Description", validators=[DataRequired()])
    date_arrive = DateField("date_arrive ", validators=[DataRequired()])
    details = TextAreaField("details", validators=[DataRequired()])
    price = IntegerField("price", validators=[DataRequired()])
    quantity = IntegerField("quantity", validators=[DataRequired()])
    image = FileField("image",  validators=[DataRequired()])
    submit = SubmitField("submit", validators=[DataRequired()])


class DeleteArticleForm(FlaskForm):
        id = IntegerField("article_id", validators=[DataRequired()])
        name = StringField("name", validators=[Optional()])
        submit = SubmitField("submit", validators=[DataRequired()])


class EditArticleForm(FlaskForm):
    id = IntegerField("article_id", validators=[DataRequired()])
    name = StringField("name", validators=[Optional()])
    submit = SubmitField("submit", validators=[DataRequired()])

class PayementForm(FlaskForm):
    id = IntegerField("userId", validators=[DataRequired()])
    article_name = StringField('Nom', validators=[DataRequired()], render_kw={'readonly': True})
    prix_total = IntegerField('Prix Total', validators=[DataRequired()] , render_kw={'readonly': True})

    submit = SubmitField("submit", validators=[DataRequired()])
