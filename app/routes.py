from flask import render_template, redirect, url_for, request, flash
from app import app, bcrypt, db, login_manager
from .models import ImageDefilante, Articles, UsersData
from .forms import LoginForm, SignupForm, PublierArticles,EditProfileForm
from flask_login import login_user, logout_user, current_user
import flask_login
import os, random
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

@login_manager.user_loader
def load_user(user_id):
    return UsersData.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def home():
    form = EditProfileForm()
    image_uploaded = True  
    images = Articles.query.all()
    random.shuffle(images)

    return render_template('home.html', images=images, form=form)

@flask_login.login_required
@app.route('/editProfile/<int:user_id>', methods=['GET', 'POST'])
def editProfile(user_id):
    user = UsersData.query.get_or_404(user_id)
    form = EditProfileForm(obj=user)

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
            flash('Les modifications ont été enregistrées')
            return redirect(url_for('editProfile', user_id=user.id))
        db.session.commit()
        flash('Les modifications ont été enregistrées')

    return render_template('userProfile.html', form=form)
    #     Username = form.Username.data
    #     Biographie = form.Biographie.data
    #     Image = form.Image.data

    #     uploaded_file = form.Image.data
    #     filename = secure_filename(uploaded_file.filename)
    #     image_path = os.path.join(app.config['UPLOAD_PATH'], filename)
    #     uploaded_file.save(image_path)
    #     image = image_path
    #     path_list = image.split('/')[1:]
    #     new_path = '/'.join(path_list)

    #     user_new_infos = UsersData(Username=Username , Image = new_path, Biographie=Biographie)
    #     db.session.add(user_new_infos)
    #     db.session.commit()
    #     return redirect(url_for('edit_profile', user_id=user.id))
    # return render_template('userProfile.html', form=form)





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
                print('USERCONNECTED',current_user.is_authenticated)
                if user.is_admin:
                    return redirect(next or url_for('viewsForAdmin'))   
                else:
                    return redirect(next or url_for('home'))
            else:
                flash("Identifiants ou mot de passe incorrect. Veuillez réessayer.", 'error')
                return redirect(url_for('Login'))
    return render_template('login.html', form=form)

@app.route('/Logout')
def Logout():
    logout_user()
    return redirect(url_for('home'))


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
                            image=new_path)  
            db.session.add(new_articles)
            db.session.commit()
            
            flash(f"L'article            a été ajouté avec succes")
            return redirect(url_for('home'))
    return render_template('publierArticles.html', form=form)

