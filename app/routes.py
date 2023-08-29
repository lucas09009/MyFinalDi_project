########## MES-IMPORTATIONS ##########
from flask import render_template, redirect, url_for, request, flash, session, make_response, jsonify, json
from app import app, bcrypt, db, login_manager
from .models import ImageDefilante, Articles, UsersData, Panier, Payement, Category
from .forms import LoginForm, SignupForm, PublierArticles,EditProfileForm, ImageDefilanteForm, DeleteArticleForm, EditArticleForm, PayementForm, AjouterCategorieForm
from flask_login import login_user, logout_user, current_user
import flask_login
import os, random
from werkzeug.utils import secure_filename
from functools import wraps
from .utils import ChoixDeCategories, get_categories_with_icons


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
    categories_with_icons = get_categories_with_icons()
    isd = ChoixDeCategories()

    return render_template('home.html', articles=articles, imagesdefilante=imagesdefilante, categories_with_icons=categories_with_icons, isd=isd )

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
        
        return redirect(url_for('home'))
    return view_decorate    


############# CETTE ROUTE EST RESERVEE AUX Utilisateurs connectes, ELLE PERMET AUX utilisateurs DE MODIFIER LEURS PROFIL
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
                new_path = filename
                # image = image_path
                # path_list = image.split('/')[1:]
                # new_path = '/'.join(path_list)
                # new_path = new_path.replace('\\', '/')

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





@app.route('/ajouterCategorie', methods=['GET', 'POST'])
def ajouterCategorie():
    form = AjouterCategorieForm()
    print( form.validate_on_submit())
    if form.validate_on_submit():
        name=form.name.data,
        icon_name=form.icon_name.data,

        new_category = Category(name=name, icon_name=icon_name)
        db.session.add(new_category)
        db.session.commit()

        

        flash("La catégorie a été ajoutée avec succès")
        return redirect(url_for('ajouterCategorie')) 

    return render_template('ajouterCategorie.html', form=form)





############# CETTE ROUTE PERMET AUX Utilisateurs DE PUBLIER DES ARTICLES ###########

    # form.category.choices = [(category.id, category.name) for category in Category.query.all()]
@app.route('/publierArticles', methods=['GET', 'POST'])
def publierArticles():
    form = PublierArticles()
    form.category.choices = ChoixDeCategories()
    if form.validate_on_submit():
        name = form.name.data
        category = form.category.data
        Description = form.Description.data
        date_arrive = form.date_arrive.data
        details = form.details.data
        price = form.price.data
        quantity = form.quantity.data
        uploaded_file = form.image.data

        filename = secure_filename(uploaded_file.filename)
        image_path = os.path.join(app.config['UPLOAD_PATH'], filename)
        uploaded_file.save(image_path)
        path_list = image_path.split('/')[1:]
        new_path = '/'.join(path_list)

        category_recupere = Category.query.get(category)

        new_article = Articles(
            name=name,
            Description=Description,
            category = category_recupere,
            date_arrive=date_arrive,
            details=details, 
            price=price,
            quantity=quantity,
            image=new_path,
            user_id=current_user.id,
            user_name=current_user.Username
        )
        db.session.add(new_article)
        db.session.commit()
        flash("L'article a été ajouté avec succès")
        # return redirect(url_for('index')) 
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


@app.route('/deleteArticle', methods=['GET', 'POST']) 
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


@app.route('/editArticle/<int:article_id>', methods=['GET', 'POST'])
def editArticle(article_id):
    article_to_edit = Articles.query.get(article_id)
    if article_to_edit:
        form = PublierArticles(obj=article_to_edit)

        if form.validate_on_submit():
            article_to_edit.name = form.name.data
            article_to_edit.category = form.category.data
            article_to_edit.Description = form.Description.data
            article_to_edit.date_arrive = form.date_arrive.data
            article_to_edit.details = form.details.data
            article_to_edit.price = form.price.data
            article_to_edit.quantity = form.quantity.data
            article_to_edit.image = form.image.data

            uploaded_file = form.image.data
            filename = secure_filename(uploaded_file.filename)
            image_path = os.path.join(app.config['UPLOAD_PATH'], filename)
            uploaded_file.save(image_path)
            image = image_path
            path_list = image.split('/')[1:]
            new_path = '/'.join(path_list)
            article_to_edit.image = new_path
            db.session.commit()
            flash(f"L'article a été ajouté avec succes")

    return render_template('edit_article.html', form=form)


@flask_login.login_required
@app.route('/Mes_articles')
def MesArticles():
    mes_articles = Articles.query.filter_by(user_id=current_user.id).all()
    return render_template('mes_articles.html', mes_articles=mes_articles)



# @app.route('/panier', methods=['GET', 'POST'])
# def panier():

#     if request.method == 'POST':
#         article_id = request.form.get('article_id')
#         article = Articles.query.get(article_id)
#         print
#         if 'panier' not in session:
#             session['panier'] = []

#         article_dict = {
#             'id': article_id,
#             'name': article.name,
#             'category': article.category,
#             'Description': article.Description,
#             'date_arrive': article.date_arrive,
#             'details': article.details,
#             'price': article.price,
#             'quantity': article.quantity,
#             'image': article.image,
#         }
    
#         session['panier'].append(article_dict)
#         print(session['panier'])

#         response = {'articleAdded': True, 'cartItemCount': len(session['panier'])}
#         return jsonify(response)

#     return render_template('mon_panier.html')


    # return render_template('panier.html', panier_articles=panier_articles, articles=articles)



@app.route('/supprimer_article_panier/<int:article_id>', methods=['GET', 'POST'])
def supprimer_article_panier(article_id):
    if 'panier' in session:
        print("Avant suppression :", session['panier'])
        updated_cart = []

        for item in session['panier']:
            if item['id'] != article_id:
                updated_cart.append(item)
        
        session['panier'] = updated_cart
        print("Après suppression :", session['panier'])

    return redirect(url_for('MonPanier'))









@app.route('/searchFor', methods=['GET', 'POST'])
def SearchFor():
    search_query = request.args.get('saisie')
    if search_query:
        articles = Articles.query.filter(Articles.name.ilike(f"%{search_query}%")).all()
        return render_template('home.html', articles=articles, search_query=search_query)
    
    return render_template('home.html')



@app.route('/payement/<int:article_id>', methods=['GET', 'POST'])
@flask_login.login_required
def payement(article_id):
    article = Articles.query.get(article_id)
    article_name = article.name
    Montant_Total = article.price

    form = PayementForm(article_name=article_name,  prix_total=Montant_Total)
    payement = Payement(article_name=article_name, prix_total=Montant_Total)

# , user_id=current_user.id

    db.session.add(payement)
    db.session.commit()
    flash(f"Votre demande est en cours de traitement, vous serez contactez dans un instant ")

    return render_template('payement.html', form=form, article=article)





@app.route('/articles_details/<int:article_id>', methods=['GET', 'POST'])
def ArticlesDetails(article_id):
    article = Articles.query.get(article_id) 
    print(article)  
    articles = Articles.query.all()
    for items in articles :
        items.image = '/'.join(''.join(items.image.split('/')[1:]).split('\\'))
    return render_template('articles_details.html', articles=articles, article= article)





@app.route('/vider_panier', methods=['POST'])
def vider_panier():
    session.clear()
    flash("Le panier a été vidé", 'info')
    return redirect(url_for('MonPanier'))
