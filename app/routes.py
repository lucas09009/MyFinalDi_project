########## MES-IMPORTATIONS ##########
from flask import render_template, redirect, url_for, request, flash, session, make_response, json
from app import app, bcrypt, db, login_manager
from .models import Promotions, Articles, UsersData, Panier, Payement, Category, ArticlesFavoris, Commentaires
from .forms import LoginForm, SignupForm, PublierArticles,EditProfileForm, PromotionsForm,DeleteArticleForm, EditArticleForm, CommentaireForm, PayementForm, AjouterCategorieForm
from flask_login import login_user, logout_user, current_user
import flask_login
import os, random
from datetime import datetime
from werkzeug.utils import secure_filename
from functools import wraps
from .utils import ChoixDeCategories, get_categories_with_icons, choixDePromo
from flask_mail import Message
import stripe

#######CETTE ROUTE RENVOIE LES IMAGES ET LES ARTICLES A LA PAGE D'ACCEUIL ###########
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
    pagination = Articles.query.order_by(Articles.date_arrive).paginate(page=page, per_page=8, error_out=False)
    
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
        
        return redirect(url_for('home'))
    return view_decorate    


######### CETTE ROUTE RETURNE LE TEMPLATE home.html UNE FOIS QU'ON ACCEDE A L'URL '/ADMIN' 
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


####### CETTE ROUTE PERMET DE CHARGER D'UN UTILISATEUR DEPUIS LA DATABASE UsersData A PARTIR DE SON ID #########
@login_manager.user_loader
def load_user(user_id):
    return UsersData.query.get(int(user_id))

############# CETTE ROUTarticles_en_promoX ADMINS DE MODIFIER DES ARTICLES ###########

@app.route('/Make_A_Promo/<int:article_id>', methods = ['GET', 'POST'])
def make_new_promo(article_id):
    article = Articles.query.get(article_id)
    liste = choixDePromo()
    return render_template('adminPromotionsPage.html', article=article, liste=liste)



@app.route('/PromotionsArticles/<int:promo_id>/<int:article_id>', methods = ['GET', 'POST'])
def promotionsArticles(promo_id, article_id):
    article = Articles.query.get(article_id)
    article.promotion_id = promo_id
    print(article.promotion_id)
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

                # uploaded_file = form.Image.data
                # filename = secure_filename(uploaded_file.filename)
                # image_path = os.path.join(app.config['UPLOAD_PATH'], filename)
                # uploaded_file.save(image_path)
                # new_path = filename
                # image = image_path
                # path_list = image.split('/')[1:]
                # new_path = '/'.join(path_list)
                # new_path = new_path.replace('\\', '/')

                user.Image = new_path
                # articles_of_user = Articles.query.filter_by(user_id=current_user.id)
                # if articles_of_user:
                #     for article in articles_of_user:
                #         article.user_image = current_user.Image
                db.session.commit()
                flash('Les modifications ont été enregistrées')
                return redirect(url_for('userProfile', user_id=user.id))
            # db.session.commit()
            # return redirect(url_for('home'))
        return render_template('editprofile.html', form=form, user=user, cart_item=cart_item)
    return "User non trouvé"



@app.route('/userProfile/<int:user_id>', methods = ['GET', 'POST'])
def userProfile(user_id):
    cart_item = Panier.query.filter_by(user_id = current_user.id).all()
    user = UsersData.query.get_or_404(user_id)
    form = EditProfileForm(obj=user)
    if user:
        return render_template('userProfile.html', form=form, user=user, cart_item=cart_item)

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
                flash("Identifiants ou mot de passe incorrect. Veuillez réessayer;error")
                return redirect(url_for('Login'))
                        
                        
        flash("Veuillez d'abord créer un compte;error")
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


@app.route('/ajouterCategorie/Promo', methods=['GET', 'POST'])
def ajouterCategoriePromo():
    form = PromotionsForm()
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
        db.session.add(new_category)
        db.session.commit()
        flash("La catégorie a été ajoutée avec succès")
        return redirect(url_for('ajouterCategoriePromo')) 

    return render_template('ajouterCategoriePromo.html', form=form)

############# CETTE ROUTE PERMET AUX Utilisateurs DE PUBLIER DES ARTICLES ###########
@admin_required
@app.route('/publierArticles', methods=['GET', 'POST'])
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
            # user_image = current_user.Image
        )
        db.session.add(new_article)
        db.session.commit()
        flash("L'article a été ajouté avec succès")
        return redirect(url_for('viewsForAdmin')) 
        # else:
        #     print('connecte')
        #     next = request.args.get('next')
        #     return redirect(next or url_for('home'))
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
        items.image = '/'.join(''.join(items.image.split('/')[1:]).split('\\'))

    if current_user.is_authenticated:
        cart_item = Panier.query.filter_by(user_id = current_user.id).all()
    else:
        pass
    return render_template('promotions.html',promotion=promotion,cart_item=cart_item, categories_with_icons=categories_with_icons, liste_des_articles=liste_des_articles, articles_en_promo=articles_en_promo, liste=liste)


############# CETTE ROUTE PERMET AUX ADMINS DE SUPPRIMER DES ARTICLES ###########
@app.route('/deleteArticle', methods=['GET', 'POST']) 
def deleteArticle():
    article_id = request.args.get('article_id')
    article_to_delete =  Articles.query.get(article_id)
    form = DeleteArticleForm()
    if  form.validate_on_submit():
        name = form.name.data
        if article_to_delete and (article_to_delete.name == name):
            db.session.delete(article_to_delete)
            db.session.commit()
            flash(f"L'article a été supprimé avec succès")
            return redirect(url_for('viewsForAdmin'))
        else:
            flash("Erreur: L'article avec cet ID ou ce nom n'a pas été trouvé ou les informations ne correspondent pas.", "alert-error")
    return render_template('delete_article.html', form=form, article=article_to_delete)


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


@flask_login.login_required
@app.route('/Mes_articles')
def MesArticles():
    mes_articles = Articles.query.filter_by(user_id=current_user.id).all()
    cart_item = Panier.query.filter_by(user_id = current_user.id).all()

    print('MES ARTICLES',mes_articles)
    return render_template('mes_articles.html', mes_articles=mes_articles, cart_item=cart_item)


@app.route('/add_to_cart/without_login/<int:article_id>', methods=['GET', 'POST'])
def add_to_cart_without_login(article_id):
    article = Articles.query.get(article_id)
    if request.method == 'POST':
        if 'panier' not in session:
            print('notoanier')
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

@app.route('/panier/Users/NotConnected', methods=['GET', 'POST'])
def panierForUserNonConnecte():
    articles = Articles.query.all()
    for items in articles:
        items.image = '/'.join(''.join(items.image.split('/')[1:]).split('\\'))
    return render_template('mon_panier.html', articles=articles)


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


@app.route('/incrementer-quantite/<int:user_id>/<int:article_id>', methods=['GET','POST'])
def incrementer_quantite(user_id, article_id):
    user = UsersData.query.get(user_id)
    article = Articles.query.get(article_id)

    if user and article:
            cart_item = Panier.query.filter_by(user_id=user_id, article_id=article_id).first()

            if cart_item:
                if cart_item.quantite < article.quantity:
                    cart_item.quantite += 1
            else:
                cart_item = Panier(user_id=user_id, article_id=article_id, quantite=1)
                db.session.add(cart_item)

            db.session.commit()
            flash(f"L'article a été ajouté avec succès,success")
            return redirect(url_for('add_to_cart',user_id=user_id, article_id=article_id ))
    return render_template('mon_panier.html')


@app.route('/decrementer-quantite/<int:user_id>/<int:article_id>', methods=['GET','POST'])
def decrementer_quantite(user_id, article_id):
    
    user = UsersData.query.get(user_id)
    article = Articles.query.get(article_id)

    if user and article:
            cart_item = Panier.query.filter_by(user_id=user_id, article_id=article_id).first()

            if cart_item:
                if cart_item.quantite >= 1:
                    cart_item.quantite =- 1
                    if cart_item.quantite == 0:
                        db.session.delete(cart_item)

            db.session.commit()
            flash(f"L'article a été ajouté avec succès,success")
            return redirect(url_for('add_to_cart',user_id=user_id, article_id=article_id ))
    return render_template('mon_panier.html')

@app.route('/panier', methods=['GET','POST'])
def panier():
    user_id = current_user.id
    articles = Articles.query.all()
    random.shuffle(articles)

    cart_item = Panier.query.filter_by(user_id = current_user.id).all()
    panier_utilisateur = db.session.query(Panier, Articles).filter(Panier.user_id == user_id, Panier.article_id == Articles.id).all()
    return render_template('mon_panier.html', articles=articles, panier_utilisateur=panier_utilisateur, cart_item=cart_item)


@app.route('/supprimer_article_panier/<int:article_id>', methods=['GET', 'POST'])
def supprimer_article_panier(article_id):
    if article_id:
        if current_user.is_authenticated:
            print('nom',current_user.Username)
            article_to_delete = Panier.query.filter_by(user_id=current_user.id, article_id=article_id).first()
            if article_to_delete:
                db.session.delete(article_to_delete)
                db.session.commit()
            return redirect(url_for('panier'))
        else:
            for item in session['panier']:
                if item['id'] == article_id:
                    article_to_delete = item
                    session['panier'].remove(article_to_delete)
                    session.modified = True
        return redirect(url_for('panierForUserNonConnecte'))
    return render_template('mon_panier.html')



@app.route('/supprimer_article_favoris/<int:article_id>', methods=['GET', 'POST'])
def supprimer_article_favoris(article_id):
    user_id = current_user.id
    if article_id:
        article_to_delete = ArticlesFavoris.query.filter_by(id_of_user=user_id, id_of_article=article_id).first()
        if article_to_delete:
            db.session.delete(article_to_delete)
            db.session.commit()
    return redirect(url_for('VoirFavoris'))


@app.route('/searchFor', methods=['GET', 'POST'])
def SearchFor():
    categories_with_icons = get_categories_with_icons()
    if request.method == 'POST':
        item_recherche = request.form.get('saisie')
        if item_recherche:
            articles_trouvé = Articles.query.filter(Articles.name.ilike(f"%{item_recherche}%")).all()
    return render_template('searchFor.html', articles_trouvé=articles_trouvé, item_recherche=item_recherche, categories_with_icons=categories_with_icons)
    


@app.route('/payement/<int:article_id>', methods=['GET', 'POST'])
@flask_login.login_required
def payement(article_id):
    article = Articles.query.get(article_id)
    name = current_user.Username
    Montant_Total = article.price

    form = PayementForm(name=name,  prix_total=Montant_Total)
    payement = Payement(name=name, prix_total=Montant_Total)
    db.session.add(payement)
    db.session.commit()
    flash(f"Votre demande est en cours de traitement, vous serez contactez dans un instant ")
    return render_template('payement.html', form=form, article=article)










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
        print(comments)
        for items in articles :
            items.image = '/'.join(''.join(items.image.split('/')[1:]).split('\\'))

            if not current_user.is_authenticated:
                pass
            else:
                cart_item = Panier.query.filter_by(user_id = current_user.id).all()
    return render_template('articles_details.html',comments=comments, articles=articles, article = article, category=category, cart_item=cart_item)


@app.route('/commentaires', methods=['GET', 'POST'])
def Make_A_Comment():
    article_id = request.args.get('article_id')
    form = CommentaireForm()
    if form.validate_on_submit():
        commentaires = form.commentaires.data

        new_comments = Commentaires(commentaires=commentaires, user_id=current_user.id, article_id=article_id, user_name=current_user.Username, image=current_user.image)
        db.session.add(new_comments)            
        db.session.commit()
        return redirect(url_for('ArticlesDetails', article_id=article_id))
    return render_template('commentaires.html', form = form)

@app.route('/vider_panier', methods=['POST'])
def vider_panier():
    session.clear()
    flash("Le panier a été vidé", 'info')
    return redirect(url_for('MonPanier'))


@app.route('/favoris/<int:id_of_user>/<int:id_of_article>')
def AjouterAuxFavoris(id_of_user, id_of_article):
    user = UsersData.query.get(id_of_user)
    article = Articles.query.get(id_of_article)

    if user and article:
        favoris = ArticlesFavoris.query.filter_by(id_of_user=id_of_user, id_of_article=id_of_article).first()

        if favoris:
            flash('Vous ne pouvez ajouter cet article une seule fois')
        else:
            favoris = ArticlesFavoris(id_of_user=id_of_user, id_of_article=id_of_article)
            db.session.add(favoris)

        db.session.commit()
        flash(f"L'article a été ajouté avec succès,success")
        return redirect(url_for('home'))

    return render_template('Favoris.html')



@app.route('/VoirFavoris', methods=['GET','POST'])
def VoirFavoris():
    user_id = current_user.id
    cart_item = Panier.query.filter_by(user_id = current_user.id).all()
    favoris_utilisateur = db.session.query(ArticlesFavoris, Articles).filter(ArticlesFavoris.id_of_user == user_id, ArticlesFavoris.id_of_article == Articles.id).all()
    # favoris_utilisateur = ArticlesFavoris.query.filter_by(id_of_user = user_id).all()
    # print('favoris_utilisateur',favoris_utilisateur)
    # print('favoris_utilisateur',type(favoris_utilisateur))
    return render_template('Favoris.html', favoris_utilisateur=favoris_utilisateur,cart_item=cart_item)



