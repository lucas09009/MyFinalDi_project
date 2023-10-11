from wtforms import StringField, PasswordField, SubmitField, DateField,FloatField, TextAreaField, FileField, IntegerField,SelectField
from wtforms.validators import DataRequired, Optional
from flask_wtf import FlaskForm
from .utils import ChoixDeCategories
class SignupForm(FlaskForm):
    Username = StringField("Username",  validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    Password = PasswordField("Password",  validators=[DataRequired()])
    confirm_Password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("S'inscrire")

class LoginForm(FlaskForm):
    Username = StringField("Username",  validators=[DataRequired()])
    Password = PasswordField("Password",  validators=[DataRequired()])
    submit = SubmitField('Se connecter')


class AjouterCategorieForm(FlaskForm):
    name = StringField('Nom de la catégorie', )
    icon_name = StringField('Icone Name', validators=[DataRequired()])
    submit = SubmitField('Ajouter')


# class PromoCategoryForm(FlaskForm):
#     promo_name = StringField('Promo Name', validators=[DataRequired()])
#     duree_de_la_promo = IntegerField("duree de la promo en jours", validators = [DataRequired()])
#     reduction = IntegerField('reduction', validators = [DataRequired()])
#     submit = SubmitField('Ajouter')

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


class PromotionsForm(FlaskForm):
    nom_de_la_promotion = StringField('Nom de la promotion')
    duree_de_la_promo = IntegerField("duree de la promo en jours", validators = [DataRequired()])
    reduction = IntegerField('reduction', validators = [DataRequired()])
    details = StringField('details', validators = [DataRequired()])
    image = FileField('image', validators = [DataRequired()])
    submit = SubmitField('Enregistrer')



class ModifierArticleForm(FlaskForm):
    id = IntegerField("article_id", validators=[DataRequired()])
    name = StringField("name", validators=[Optional()])
    name = StringField("name", validators=[DataRequired()])
    category = SelectField("category", validators=[DataRequired()] )        
    Description = StringField("Description", validators=[DataRequired()])
    date_arrive = DateField("date_arrive ", validators=[DataRequired()])
    details = TextAreaField("details", validators=[DataRequired()])
    price = IntegerField("price", validators=[DataRequired()])
    quantity = IntegerField("quantity", validators=[DataRequired()])
    image = FileField("image",  validators=[DataRequired()])
    submit = SubmitField("submit", validators=[DataRequired()])


class DeleteArticleForm(FlaskForm):
    id = IntegerField("article_id", validators=[DataRequired()])
    name = StringField("name",  validators=[Optional()])
    submit = SubmitField("submit", validators=[DataRequired()])


class EditArticleForm(FlaskForm):
    id = IntegerField("article_id", validators=[DataRequired()])
    name = StringField("name", validators=[Optional()])
    submit = SubmitField("submit", validators=[DataRequired()])

class PayementForm(FlaskForm):
    id = IntegerField("userId", validators=[DataRequired()], render_kw={'readonly': False})
    name = StringField('Nom', validators=[DataRequired()], render_kw={'readonly': True})
    prix_total = IntegerField('Prix Total', validators=[DataRequired()] , render_kw={'readonly': True})
    submit = SubmitField("submit", validators=[DataRequired()])


class CommentaireForm(FlaskForm):
    # id = IntegerField("userId", validators=[DataRequired()])
    # name = StringField('Nom', validators=[DataRequired()])
    commentaires = TextAreaField('Commentaires',validators=[DataRequired()])
    submit = SubmitField("submit", validators=[DataRequired()])




# class ResetPasswordRequestForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired()])
#     subject = StringField('Subject', validators=[DataRequired()])
#     message = StringField('TextField', validators=[DataRequired()])
#     submit = SubmitField('Request Password Reset')