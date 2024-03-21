########## MES-IMPORTATIONS ##########
from flask import render_template, redirect,abort, url_for, request, flash,current_app, session, make_response, json
from app import app, bcrypt, db, login_manager
from .models import Promotions, Articles, UsersData, Panier, Payement, Category, ArticlesFavoris, Commentaires
from .forms import LoginForm, SignupForm,ResetPasswordRequestForm,change_passwordForm, PublierArticles,EditProfileForm, PromotionsForm,DeleteArticleForm, EditArticleForm, CommentaireForm, PayementForm, AjouterCategorieForm
from flask_login import login_user, logout_user, current_user
import flask_login
import os, random, stripe
from datetime import datetime
from werkzeug.utils import secure_filename
from functools import wraps
from .utils import ChoixDeCategories, get_categories_with_icons, choixDePromo
from flask_mail import Message
from app import mail
from itsdangerous import URLSafeTimedSerializer
########## MA ROUTE POUR MA PAGE D'ACCEUIL ##########
@app.route('/', methods=['GET', ' POST'])
def home():
    articles = Articles.query.all()
    random.shuffle(articles)
    cart_item = []
    liste_des_articles_en_promo = []
    categories_with_icons = get_categories_with_icons()
    articles_en_promo = Promotions.query.all()
    
    for item in articles_en_promo:
        liste_des_articles_en_promo.append(item)
    les_promos = liste_des_articles_en_promo

    page = request.args.get('page', 1, type=int)
    pagination = Articles.query.order_by(Articles.category_id).paginate(page=page, per_page=21, error_out=False)
    
    articles_a_afficher = pagination.items 
    random.shuffle(articles_a_afficher) 
    if current_user.is_authenticated:
        cart_item = Panier.query.filter_by(user_id = current_user.id).all()
    else:        
        pass
    return render_template('home.html',pagination=pagination,articles=articles, les_promos = les_promos,  cart_item = cart_item, categories_with_icons=categories_with_icons)

####### CE CODE RESTREINT L'ACCES A CERTAINES ROUTES 
def admin_required(view):                 
    @wraps(view)
    def view_decorate(*args, **kwargs):
        if current_user.is_authenticated and current_user.is_admin:
            return view(*args, **kwargs)
        
        abort(403)
    return view_decorate    


######### CETTE ROUTE RETOURNE LE TEMPLATE adminhome.html UNE FOIS QU'ON ACCEDE A L'URL '/admin' 
@app.route('/admin')
@admin_required
def viewsForAdmin():
    liste_des_articles_en_promo = []

    articles = Articles.query.all()
    random.shuffle(articles)

    articles_en_promo = Promotions.query.all()
    for item in articles_en_promo:
        liste_des_articles_en_promo.append(item)
    les_promos = liste_des_articles_en_promo

    categories_with_icons = get_categories_with_icons()
    return render_template('adminhome.html', articles=articles, les_promos=les_promos, categories_with_icons=categories_with_icons)


####### CETTE ROUTE PERMET DE CHARGER UN UTILISATEUR DEPUIS LA TABLE UsersData A PARTIR DE SON ID #########
@login_manager.user_loader
def load_user(user_id):
    return UsersData.query.get(int(user_id))

############# CETTE ROUTE DE RECUPERER L'ARTICLE QU'ON SOUHAITE AJOUTER A UNE PROMOTION  ###########

@app.route('/Make_A_Promo/<int:article_id>', methods = ['GET', 'POST'])
def make_new_promo(article_id):
    article = Articles.query.get(article_id)
    liste = choixDePromo()
    return render_template('adminPromotionsPage.html', article=article, liste=liste)


############# CETTE ROUTE EST LA SUITE DE LA ROUTE PRECEDENTE . ELLE PERMET D'AJOUTER A UNE CATEGORIE DE PROMOTIONS  ###########

@app.route('/PromotionsArticles/<int:promo_id>/<int:article_id>', methods = ['GET', 'POST'])
def promotionsArticles(promo_id, article_id):
    article = Articles.query.get(article_id)
    article.promotion_id = promo_id
    db.session.commit()
    return redirect(url_for('home'))

############# CETTE ROUTE EST RESERVEE AUX Utilisateurs connectes, ELLE PERMET AUX utilisateurs DE MODIFIER LEURS PROFIL
@app.route('/editProfile/<int:user_id>', methods = ['GET', 'POST'])
def editProfile(user_id):
    cart_item = Panier.query.filter_by(user_id = current_user.id).all()
    user = UsersData.query.get_or_404(user_id)
    form = EditProfileForm(obj=user)    
    if user:
        if form.validate_on_submit():
            user.Username = form.Username.data
            user.Biographie = form.Biographie.data

            if form.Image.data:     
                uploaded_file = form.Image.data

                filename = secure_filename(uploaded_file.filename)
                image_path = os.path.join(app.config['UPLOAD_PATH'], filename)
                uploaded_file.save(image_path)
                path_list = image_path.split('/')[1:]
                new_path = '/'.join(path_list)

                user.Image = new_path
                db.session.commit()
                flash('Les modifications ont été enregistrées')
                return redirect(url_for('userProfile', user_id=user.id))
        db.session.commit()
        return render_template('editprofile.html', form=form, user=user, cart_item=cart_item)
    return "User non trouvé"


############# CETTE ROUTE PERMET AUX UTILISATEURS DE VOIR LEUR PROFIL ###########

@app.route('/userProfile/<int:user_id>', methods = ['GET', 'POST'])
def userProfile(user_id):
    cart_item = Panier.query.filter_by(user_id = current_user.id).all()
    user = UsersData.query.get_or_404(user_id)
    form = EditProfileForm(obj=user)
    if user:
        db.session.commit()
        return render_template('userProfile.html', form=form, user=user, cart_item=cart_item)

############# CETTE ROUTE PERMET AUX UTILISATEURS DE SE CONNECTER ###########


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
                flash("Identifiants ou mot de passe incorrect. Veuillez réessayer;error")
                return redirect(url_for('Login'))
                        
                        
        flash("Identifiants ou mot de passe incorrect. Veuillez réessayer;error")
        return redirect(url_for('Login'))

    return render_template('login.html', form=form)


############# CETTE ROUTE PERMET AUX UTILISATEURS DE SE DECONNECTER ###########


@app.route('/Logout')
def Logout():
    logout_user()
    return redirect(url_for('home'))


############# CETTE ROUTE PERMET AUX UTILISATEURS DE S'INSCRIRE ###########

@app.route('/Signup', methods=['GET', 'POST'])
def Signup():
    form = SignupForm()
    if  form.validate_on_submit():
        username = form.Username.data
        email = form.email.data
        password = form.Password.data
        confirm_password = form.confirm_Password.data
        user_existe_deja = UsersData.query.filter_by(Username=username).first() 

        if user_existe_deja:
            flash('Cet nom d\'utilisateur est déjà utilisé pour un autre compte;error')
            return redirect(url_for('Signup'))
        
        elif password != confirm_password:
            flash("Vous avez saisi deux mots de passes différents")
            return redirect(url_for('Signup'))

        password_encrypte = bcrypt.generate_password_hash(password).decode('utf8')
        new_user = UsersData(Username=username,email =email, Password = password_encrypte)

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for('home'))
    return render_template('Signup.html', form =form)


############# CETTE ROUTE est reservé à l'ADMIN AFIN DE créer une nouvelle catégorie d'article ###########
@admin_required
@app.route('/ajouterCategorie', methods=['GET', 'POST'])
def ajouterCategorie():
    form = AjouterCategorieForm()
    if form.validate_on_submit():
        name=form.name.data,
        icon_name=form.icon_name.data,

        new_category = Category(name=name, icon_name=icon_name)
        db.session.add(new_category)
        db.session.commit()
        flash("La catégorie a été ajoutée avec succès")
        return redirect(url_for('ajouterCategorie')) 

    return render_template('ajouterCategorie.html', form=form)


############# CETTE ROUTE est reservé à l'ADMIN AFIN DE créer une nouvelle catégorie d'article ###########

@app.route('/ajouterCategorie/Promo', methods=['GET', 'POST'])
@admin_required
def ajouterCategoriePromo():
    form = PromotionsForm()
    # print(form.validate_on_submit())
    if form.validate_on_submit():
        promo_name = form.nom_de_la_promotion.data,
        duree_de_la_promo = form.duree_de_la_promo.data
        reduction = form.reduction.data

        uploaded_file = form.image.data
        filename = secure_filename(uploaded_file.filename)
        image_path = os.path.join(app.config['UPLOAD_PATH'], filename)
        uploaded_file.save(image_path)
        path_list = image_path.split('/')[1:]
        new_path = '/'.join(path_list)

        new_category = Promotions(nom_de_la_promotion=promo_name, duree_de_la_promo=duree_de_la_promo, reduction=reduction, image = new_path)
        print("new_category",new_category)
        db.session.add(new_category)
        db.session.commit()
        flash("La catégorie a été ajoutée avec succès")
        return redirect(url_for('ajouterCategoriePromo')) 

    return render_template('ajouterCategoriePromo.html', form=form)

############# CETTE ROUTE PERMET AUX Utilisateurs DE PUBLIER DES ARTICLES ###########
@app.route('/publierArticles', methods=['GET', 'POST'])
@admin_required
def publierArticles():
    form = PublierArticles()
    form.category.choices = ChoixDeCategories()
    # if current_user.is_authenticated:
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
            user_name=current_user.Username,
        )
        db.session.add(new_article)
        db.session.commit()
        flash("L'article a été ajouté avec succès")
        return redirect(url_for('viewsForAdmin')) 
    return render_template('publierArticles.html', form=form)

############# CETTE ROUTE PERMET AUX ADMINS POUR PROMOUVOIR DES ARTICLES OU FAIRE DES ANNONCES ###########

@app.route('/articles/promotions/<int:promo_id>')
def VoirArticlesEnPromo(promo_id):
    cart_item = []
    liste_des_articles = []
    categories_with_icons = get_categories_with_icons()
    liste = choixDePromo()
    promotion = Promotions.query.get(promo_id)

    articles_en_promo = Articles.query.filter_by(promotion_id = promo_id).all()

    for articles in articles_en_promo:
        liste_des_articles.append(articles)
            
    for items in liste_des_articles:
        items.image = items.image.split('/')[-1]  

    if current_user.is_authenticated:
        cart_item = Panier.query.filter_by(user_id = current_user.id).all()
    else:
        pass
    return render_template('promotions.html',promotion=promotion,cart_item=cart_item, categories_with_icons=categories_with_icons, liste_des_articles=liste_des_articles, articles_en_promo=articles_en_promo, liste=liste)


############# CETTE ROUTE PERMET AUX ADMINS DE SUPPRIMER DES ARTICLES ###########
@admin_required
@app.route('/deleteArticle', methods=['GET', 'POST']) 
def deleteArticle():
    article_id = request.args.get('article_id')
    article_to_delete =  Articles.query.get(article_id)
    form = DeleteArticleForm(obj=article_to_delete)
    if  form.validate_on_submit():
        name = form.name.data
        article_to_delete.id = form.id.data
        if article_to_delete and (article_to_delete.name == name):
            db.session.delete(article_to_delete)
            db.session.commit()
            flash(f"L'article a été supprimé avec succès")
            return redirect(url_for('viewsForAdmin'))
        else:
            flash("Erreur: L'article avec cet ID ou ce nom n'a pas été trouvé ou les informations ne correspondent pas.", "alert-error")
    return render_template('delete_article.html', form=form, article=article_to_delete)


############# CETTE ROUTE PERMET AUX ADMINS DE SUPPRIMER DES ARTICLES ###########

@app.route('/editArticle/<int:article_id>', methods=['GET', 'POST'])
def editArticle(article_id):
    article_to_edit = Articles.query.get(article_id)
    if article_to_edit:
        form = PublierArticles(obj=article_to_edit)
        form.category.choices = ChoixDeCategories()

        if form.validate_on_submit():
            article_to_edit.name = form.name.data
            category = form.category.data
            category_recupere = Category.query.get(category)
            article_to_edit.category=category_recupere
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
            flash(f"L'article a été modidfié avec succes;success")
            # return redirect(url_for('home'))    
        return render_template('edit_article.html', form=form)


############# CETTE ROUTE PERMET AUX ADMINS DE VOIR LES ARTICLES MIS EN VENTE ###########

@admin_required
@flask_login.login_required
@app.route('/Mes_articles')
def MesArticles():
    mes_articles = Articles.query.filter_by(user_id=current_user.id).all()
    cart_item = Panier.query.filter_by(user_id = current_user.id).all()

    print('MES ARTICLES',mes_articles)
    return render_template('mes_articles.html', mes_articles=mes_articles, cart_item=cart_item)


############# CETTE ROUTE PERMET AUX USERS NON CONNECTES D'AJOUTER DES ARTICLES AU PANIER ###########

@app.route('/add_to_cart/without_login/<int:article_id>', methods=['GET', 'POST'])
def add_to_cart_without_login(article_id):
    article = Articles.query.get(article_id)
    if request.method == 'POST':
        if 'panier' not in session:
            session['panier'] = [] 
        else:
            new_add = {
            'id' : article.id,
            'name' : article.name,
            'Description' : article.Description,
            'date_arrive' : article.date_arrive,
            'details' : article.details,
            'price' : article.price,
            'quantity' : article.quantity,
            'image' : article.image.split('static/images\\')[-1],
            'nbr_dajout' : 1  
            }
            # session['panier'].append(new_add)
            if len(session['panier']) == 0: 
                articles = Articles.query.all()
                for items in articles:
                    items.image = '/'.join(''.join(items.image.split('/')[1:]).split('\\'))
                session['panier'].append(new_add)
            else:
                for item in session['panier']:
                    print('item', item)
                    if new_add['id'] == item['id']:
                        item['nbr_dajout'] += 1
                        break
                else:
                    session['panier'].append(new_add)
        flash('Article ajouté au panier avec succès;success')
        return redirect(url_for('home'))
    return render_template('mon_panier.html', articles=articles)

############# CETTE ROUTE PERMET AUX UTILISATEURS NON connectés DE VOIR LE CONTENU DE LEURS PANIERS ###########

@app.route('/panier/Users/NotConnected', methods=['GET', 'POST'])
def panierForUserNonConnecte():
    articles = Articles.query.all()
    for items in articles:
        items.image = '/'.join(''.join(items.image.split('/')[1:]).split('\\'))
    return render_template('mon_panier.html', articles=articles)


############# CETTE ROUTE PERMET AUX USERS CONNECTES D'AJOUTER DES ARTICLES AU PANIER ###########

@app.route('/add_to_cart/<int:user_id>/<int:article_id>', methods=['GET','POST'])
def add_to_cart(user_id, article_id):
    rupture_de_stock = 'False'
    user = UsersData.query.get(user_id)
    article = Articles.query.get(article_id)

    if user and article:
        cart_item = Panier.query.filter_by(user_id=user_id, article_id=article_id).first()
        if cart_item:
            if cart_item.quantite < article.quantity:
                cart_item.quantite += 1
            else:
                rupture_de_stock = 'True'          
        else:
            cart_item = Panier(user_id=user_id, article_id=article_id, quantite=1)
            db.session.add(cart_item)
        db.session.commit()
        return redirect(url_for('home'))
    flash(f"L'article a été ajouté avec succès;success")

    return render_template('mon_panier.html', rupture_de_stock=rupture_de_stock, cart_item=cart_item)


############# CETTE ROUTE PERMET AUX UTILISATEURS connectés DE VOIR LE CONTENU DE LEURS PANIERS ###########
@app.route('/panier', methods=['GET','POST'])
def panier():
    user_id = current_user.id
    articles = Articles.query.all()
    random.shuffle(articles)

    cart_item = Panier.query.filter_by(user_id = current_user.id).all()
    panier_utilisateur = db.session.query(Panier, Articles).filter(Panier.user_id == user_id, Panier.article_id == Articles.id).all()
    # flash(f"L'article a été ajouté au panier;success")
    return render_template('mon_panier.html', articles=articles, panier_utilisateur=panier_utilisateur, cart_item=cart_item)


############# CETTE ROUTE PERMET AUX UTILISATEURS connectés DE SUPPRIMER LE CONTENU DE LEURS PANIERS ###########

@app.route('/supprimer_article_panier/<int:article_id>', methods=['GET', 'POST'])
def supprimer_article_panier(article_id):
    if article_id:
        if current_user.is_authenticated:
            print('nom',current_user.Username)
            article_to_delete = Panier.query.filter_by(user_id=current_user.id, article_id=article_id).first()
            if article_to_delete:
                db.session.delete(article_to_delete)
                db.session.commit()
                flash(f"L'article a été supprimé du panier;success")
            return redirect(url_for('panier'))
        else:
            for item in session['panier']:
                if item['id'] == article_id:
                    article_to_delete = item
                    session['panier'].remove(article_to_delete)
                    session.modified = True
                    flash(f"L'article a été supprimé du panier ;success")
        return redirect(url_for('panierForUserNonConnecte'))
    return render_template('mon_panier.html')


############# CETTE ROUTE PERMET AUX UTILISATEURS connectés DE SUPPRIMER LE CONTENU DE LEURS FQVORIS ###########

@app.route('/supprimer_article_favoris/<int:article_id>', methods=['GET', 'POST'])
def supprimer_article_favoris(article_id):
    user_id = current_user.id
    if article_id:
        article_to_delete = ArticlesFavoris.query.filter_by(id_of_user=user_id, id_of_article=article_id).first()
        if article_to_delete:
            db.session.delete(article_to_delete)
            db.session.commit()
    # flash(f"L'article a été supprimé de vos favoris;success")
    return redirect(url_for('VoirFavoris'))

############# CETTE ROUTE PERMET AUX UTILISATEURS DE RECHERCHER DES ARTICLES ###########

@app.route('/searchFor', methods=['GET', 'POST'])
def SearchFor():
    categories_with_icons = get_categories_with_icons()
    articles_trouve = []
    item_recherche = request.args.get('saisie')
    print("item_recherche",item_recherche)
    if item_recherche:
        articles_trouve = Articles.query.filter(Articles.name.ilike(f"%{item_recherche}%")).all()
        print("articles_trouve", articles_trouve)
    return render_template('searchFor.html', articles_trouve=articles_trouve, item_recherche=item_recherche, categories_with_icons=categories_with_icons)
    


@app.route('/payement/<int:article_id>', methods=['GET', 'POST'])
@flask_login.login_required
def payement(article_id):
    session = stripe.checkout.Session(
    payment_method_types=['card'],
    line_items=[{
        'price': 'price_1OwrzII0GTnWYq6mYNVfWQe4',
        'quantity': 1
    }],
    mode = 'payment',
    success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
    cancel_url=url_for('index', _external=True),
    )    

    return render_template('payement.html', 
    checkout_session_id = session['id'], 
    checkout_public_key=app.config['STRIPE_PUBLIC_KEY'])










@app.route('/articles_details/<int:article_id>', methods=['GET', 'POST'])
def ArticlesDetails(article_id):
    cart_item = []
    comments = []
    if article_id:
        article = Articles.query.get(article_id) 
        article.nombre_de_vues += 1
        db.session.commit()
        category = Category.query.get(article.category_id)
        comments = db.session.query(Commentaires, Articles).join(Articles).filter(Commentaires.article_id == article_id, Articles.id == article_id).all()
        articles = Articles.query.all()

        for items in articles:
            items.image = '/'.join('/'.join(items.image.split('/')[1:]).split('\\'))
            items.image = items.image.split('/')[-1]  

            if not current_user.is_authenticated:
                pass
            else:
                cart_item = Panier.query.filter_by(user_id = current_user.id).all()
    return render_template('articles_details.html',comments=comments, articles=articles, article = article, category=category, cart_item=cart_item)




@app.route('/favoris/<int:id_of_user>/<int:id_of_article>')
def AjouterAuxFavoris(id_of_user, id_of_article):
    user = UsersData.query.get(id_of_user)
    article = Articles.query.get(id_of_article)

    if user and article:
        favoris = ArticlesFavoris.query.filter_by(id_of_user=id_of_user, id_of_article=id_of_article).first()

        if favoris:
            flash(f"L'article a été ajouté  à vos favoris;success")
        else:
            favoris = ArticlesFavoris(id_of_user=id_of_user, id_of_article=id_of_article)
            db.session.add(favoris)
            db.session.commit()
            flash(f"L'article a été ajouté  à vos favoris;success")
        return redirect(url_for('home'))
    return render_template('Favoris.html')



@app.route('/VoirFavoris', methods=['GET','POST'])
def VoirFavoris():
    user_id = current_user.id
    cart_item = Panier.query.filter_by(user_id = current_user.id).all()
    favoris_utilisateur = db.session.query(ArticlesFavoris, Articles).filter(ArticlesFavoris.id_of_user == user_id, ArticlesFavoris.id_of_article == Articles.id).all()
    return render_template('Favoris.html', favoris_utilisateur=favoris_utilisateur,cart_item=cart_item)




# @app.route('/send', methods=['GET', 'POST'])
# def send_reset_password_email():
#         email = request.form.get('email')

#         msg = Message('envoi d\'email',
#                     recipients=['luckpegan@gmail.com'])
#         msg.body = "Corps du message"
#         msg.html = "Corps du message, html, JE SUIS TTROOP CONTENT CA MARCHE"

#         mail.send(msg)
#         return "Message envoye"





# @app.route('/forgot_password', methods=['GET', 'POST'])
# def forgot_password():
#     form = ResetPasswordRequestForm()
#     if form.validate_on_submit():
#         email = form.email.data

#         users_data = UsersData(
#             email=email
#         )
#         db.session.add(users_data)
#         db.session.commit()
    
#     return render_template('forgot_password.html', form=form)



from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        email = form.email.data

        # Générer et envoyer le token de réinitialisation de mot de passe
        token = generate_reset_token(email)
        send_reset_password_email(email, token)
        flash('Un email de réinitialisation de mot de passe a été envoyé.', 'success')
     
    return render_template('forgot_password.html', form=form)

def generate_reset_token(email):
    secret_key = app.config['SECRET_KEY']
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(email, salt='reset-password-salt')

def send_reset_password_email(email, token):
    # Construire le lien de réinitialisation de mot de passe
    reset_link = url_for('change_password', token=token, _external=True)

    # Créer le contenu de l'email
    subject = "Réinitialisation de mot de passe"
    body = f"Pour réinitialiser votre mot de passe, veuillez cliquer sur le lien suivant : {reset_link}"
    recipients = [email]

    # Envoyer l'email
    message = Message(subject=subject, body=body, recipients=recipients)
    mail.send(message)






@app.route('/change_password/<token>', methods=['GET', 'POST'])
def change_password(token):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='reset-password-salt', max_age=3600)  # Vérifie si le token est valide pendant 1 heure
    except:
        flash('Ce lien de réinitialisation de mot de passe est invalide ou expiré.', 'error')
        return redirect(url_for('forgot_password'))

    user = UsersData.query.filter_by(email=email).first()
    if not user:
        flash('Cet email n\'est pas associé à un compte.', 'error')
        return redirect(url_for('forgot_password'))

    form = change_passwordForm()
    if form.validate_on_submit():
        Password = form.Password.data
        confirm_Password = form.confirm_Password.data
         
        if Password == confirm_Password:
        # Sauvegarder le nouveau mot de passe dans la base de données
            user.Password = bcrypt.generate_password_hash(Password).decode('utf8')
        db.session.commit()
        flash('Votre mot de passe a été réinitialisé avec succès.', 'success')
        return redirect(url_for('Login'))

    return render_template('change_password.html', form=form)


