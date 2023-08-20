########## MES-IMPORTATIONS ##########
from flask import render_template, redirect, url_for, request, flash, session
from app import app, bcrypt, db, login_manager
from .models import ImageDefilante, Articles, UsersData, Panier
from .forms import LoginForm, SignupForm, PublierArticles,EditProfileForm, ImageDefilanteForm, DeleteArticleForm, EditArticleForm 
from flask_login import login_user, logout_user, current_user
import flask_login
import os, random
from werkzeug.utils import secure_filename
from functools import wraps


####### CETTE ROUTE PERMET DE CHARGER D'UN UTILISATEUR DEPUIS LA DATABASE UsersData A PARTIR DE SON ID #########
@login_manager.user_loader
def load_user(user_id):
    return UsersData.query.get(int(user_id))

#######CETTE ROUTE RENVOIE LES IMAGES ET LES ARTICLES A LA PAGE D'ACCEUIL ###########
@app.route('/', methods=['GET', ' POST'])
def home():
    articles = Articles.query.all()
    random.shuffle(articles)

    imagesdefilante = ImageDefilante.query.all()

    print('MES IMAGES', imagesdefilante)

    return render_template('home.html', articles=articles, imagesdefilante=imagesdefilante )

######### CETTE ROUTE RETURNE LE TEMPLATE home.html UNE FOIS QU'ON ACCEDE A L'URL '/ADMIN' 
@app.route('/admin')
def viewsForAdmin():
    return render_template('home.html')

####### CE CODE RESTREINT L'ACCES A CERTAINES ROUTES 

def admin_required(view):                 
    @wraps(view)
    def view_decorate(*args, **kwargs):
        if current_user.is_authenticated and current_user.is_admin:
            return view(*args, **kwargs)
        
        return redirect(url_for('index'))
    return view_decorate    


############# CETTE ROUTE EST RESERVEE AUX Utilisateurs connectes, ELLE PERMET AUX utilisateurs DE MODIFIER LEURS PROFILS

@flask_login.login_required
@app.route('/editProfile/<int:user_id>', methods=['GET', 'POST'])
def editProfile(user_id):
    user = UsersData.query.get_or_404(user_id)
    form = EditProfileForm(obj=user)
    if user:
        articles = user.articles
        print('MES ARTICLES',articles)
        if form.validate_on_submit():
            user.Username = form.Username.data
            user.Biographie = form.Biographie.data

            if form.Image.data:
                uploaded_file = form.Image.data
                filename = secure_filename(uploaded_file.filename)
                image_path = os.path.join(app.config['UPLOAD_PATH'], filename)
                uploaded_file.save(image_path)
                image = image_path
                path_list = image.split('/')[1:]
                new_path = '/'.join(path_list)

                user.Image = new_path
                db.session.commit()
                return redirect(url_for('editProfile', user_id=user.id))
            db.session.commit()
            flash('Les modifications ont été enregistrées')

        return render_template('userProfile.html', form=form, articles=articles)
    return "User non trouvé"
    
############# CETTE ROUTE PERMET AUX Utilisateurs DE SE CONNECTER ###########


@app.route('/Login', methods=['GET', 'POST'])
def Login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.Username.data
        password = form.Password.data
    
        user = UsersData.query.filter_by(Username=username).first()
        if user:
            if bcrypt.check_password_hash(user.Password, password):
                login_user(user)
                next = request.args.get('next')
                if user.is_admin:
                    return redirect(next or url_for('viewsForAdmin'))   
                else:
                    return redirect(next or url_for('home'))
            else:
                flash("Identifiants ou mot de passe incorrect. Veuillez réessayer.", 'error')
                return redirect(url_for('Login'))
    return render_template('login.html', form=form)


############# CETTE ROUTE PERMET AUX Utilisateurs DE SE DECONNECTER ###########


@app.route('/Logout')
def Logout():
    logout_user()
    return redirect(url_for('home'))


############# CETTE ROUTE PERMET AUX Utilisateurs DE S'INSCRIRE ###########

@app.route('/Signup', methods=['GET', 'POST'])
def Signup():
    form = SignupForm()
    if  form.validate_on_submit():
        username = form.Username.data
        password = form.Password.data
        confirm_password = form.confirm_Password.data
        user_existe_deja = UsersData.query.filter_by(Username=username).first() 

        if user_existe_deja:
            flash('Cet nom d\'utilisateur est déjà utilisé pour un autre compte.')
            return redirect(url_for('Signup'))
        
        elif password != confirm_password:
            flash("Vous avez saisi deux mots de passes différents")
            return redirect(url_for('Signup'))

        password_encrypte = bcrypt.generate_password_hash(password).decode('utf8')
        new_user = UsersData(Username=username,  Password = password_encrypte)

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for('home'))
    return render_template('Signup.html', form =form)


############# CETTE ROUTE PERMET AUX Utilisateurs DE PUBLIER DES ARTICLES ###########

@app.route('/publierArticles', methods = ['GET', 'POST'])
def publierArticles():
    form = PublierArticles()
    if form.validate_on_submit():
            name = form.name.data
            category = form.category.data
            Description = form.Description.data
            date_arrive = form.date_arrive.data
            details = form.details.data
            price = form.price.data
            quantity = form.quantity.data
            image = form.image.data


            uploaded_file = form.image.data
            filename = secure_filename(uploaded_file.filename)
            image_path = os.path.join(app.config['UPLOAD_PATH'], filename)
            uploaded_file.save(image_path)
            image = image_path
            path_list = image.split('/')[1:]
            new_path = '/'.join(path_list)


            new_articles = Articles(name=name, category=category, 
                            Description=Description, 
                            date_arrive=date_arrive,
                            details=details,
                            price=price,
                            quantity=quantity, 
                            image=new_path,
                            user_id = current_user.id)  
            db.session.add(new_articles)
            db.session.commit()
            
            flash(f"L'article a été ajouté avec succes")
    return render_template('publierArticles.html', form=form)


############# CETTE ROUTE PERMET AUX ADMINS POUR PROMOUVOIR DES ARTICLES OU FAIRE DES ANNONCES ###########


@admin_required
@app.route('/newAd', methods = ['GET', 'POST'])
def MakeNewAds():
    form = ImageDefilanteForm()
    if form.validate_on_submit():
            details = form.details.data
            image = form.image.data
      

            uploaded_file = form.image.data
            filename = secure_filename(uploaded_file.filename)
            image_path = os.path.join(app.config['UPLOAD_PATH'], filename)
            uploaded_file.save(image_path)
            image = image_path
            path_list = image.split('/')[1:]
            new_path = '/'.join(path_list)


            newAd = ImageDefilante(details=details, image=new_path)  
            db.session.add(newAd)
            db.session.commit()
            
            flash(f"L'article a été ajouté avec succes")
    return render_template('ImageDefilante.html', form=form)


############# CETTE ROUTE PERMET AUX ADMINS DE MODIFIER DES ARTICLES ###########



############# CETTE ROUTE PERMET AUX ADMINS DE SUPPRIMER DES ARTICLES ###########


@app.route('/admin/deleteArticle', methods=['GET', 'POST'])
@admin_required 
def deleteArticle():
    form = DeleteArticleForm()
    if  form.validate_on_submit():
        id = form.id.data
        name = form.name.data
        article_to_delete = Articles.query.get(id)
        if article_to_delete and (article_to_delete.name == name or article_to_delete.id == id):
            db.session.delete(article_to_delete)
            db.session.commit()
            flash(f"L'article a été supprimé avec succès")
        else:
            flash(f"Erreur: L'article avec cet ID ou ce nom n'a pas été trouvée ou les informations ne correspondent pas.")
            return redirect(url_for('delete_article'))
    return render_template('delete_article.html', form=form)




@app.route('/editArticle/', methods=['GET', 'POST'])
def editArticle():
    article_to_edit = Articles.query.get(id)
    if article_to_edit and (article_to_edit.name == name or article_to_edit.id == id):
        flash(f"L'article avec l'ID {id} n'a pas été trouvé.")
        return redirect(url_for('editArticle'))  

    form = PublierArticles(obj=article_to_edit)

    if form.validate_on_submit():
        form.populate_obj(article_to_edit)
        db.session.commit()
        flash(f"L'article a été modifié avec succès")
        return redirect(url_for('editArticle'))

    return render_template('edit_article.html', form=form, article=article_to_edit)



@app.route('/monpanier', methods=['GET','POST'])
def MonPanier():
    if request.method == 'POST':
        article_id = request.form.get('article_id') 
        if 'panier' not in session:
            session['panier'] = []
        
        if article_id not in session['panier']:
            session['panier'].append(article_id)
        
        nouvel_ajout = Panier(user_id=current_user.id, article_id=article_id, quantite=1)
        db.session.add(nouvel_ajout)
        db.session.commit()

        session['panier'].append(article_id)

    articles_dans_le_panier = Articles.query.all()
    return render_template('mon_panier.html', articles_dans_le_panier= articles_dans_le_panier)




@app.route('/supprimer_article_panier/<int:article_id>', methods=['GET', 'POST'])
def supprimer_article_panier(article_id):
    if 'panier' in session and article_id in session['panier']:
        session['panier'].remove(article_id)
        
        panier_a_supprimer = Panier.query.filter_by(user_id=current_user.id, article_id=article_id).first()
        if panier_a_supprimer:
            db.session.delete(panier_a_supprimer)
            db.session.commit()

    return redirect(url_for('MonPanier'))
