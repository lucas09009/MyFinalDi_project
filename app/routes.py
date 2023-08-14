from flask import render_template, redirect, url_for, request, flash
from app import app, bcrypt, db, login_manager
from .models import ImageDefilante, Articles, UsersData
from .forms import LoginForm, SignupForm
from flask_login import login_user, current_user

@login_manager.user_loader
def load_user(user_id):
    return UsersData.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def home():
    images = ImageDefilante.query.all()
    return render_template('home.html', images=images)

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
                print('abalo')
                next = request.args.get('next')
                if user.is_admin:
                    return redirect(next or url_for('viewsForAdmin'))
                else:
                    return redirect(next or url_for('home'))
            else:
                flash("Identifiants ou mot de passe incorrect. Veuillez réessayer.", 'error')
                return redirect(url_for('Login'))
    return render_template('login.html', form=form)


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