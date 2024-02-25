import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from unwrap import app, db, bcrypt
from unwrap.forms import RegistrationForm, LoginForm, UpdateAccountForm, ListPropertyForm
from unwrap.models import User, Property, Location
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func, update


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    print('------form', form.validate_on_submit())
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            lastname=form.lastname.data,
            firstname=form.firstname.data,
            email=form.email.data,
            password=hashed_password
            )
        
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.lastname = form.lastname.data
        current_user.firstname = form.firstname.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.lastname.data = current_user.lastname
        form.firstname.data = current_user.firstname
        form.email.data = current_user.email
    return render_template('account.html', title='Account',
                           form=form)

@app.route("/search")
def search():
    return render_template("search.html", title='The project')


@app.route("/list_property", methods=['GET', 'POST'])
def list_property():
    form = ListPropertyForm()
    if form.validate_on_submit():
        loc = Location.query.filter_by(country=form.country.data, city=form.city.data).first()
        
        if not loc:
            loc = Location(
                country = form.country.data,
                city = form.city.data
            )

        prop = Property(
            price = form.price.data,
            title = form.title.data,
            description = form.description.data,
            location_id = loc.id,
            location = loc,
        )
        
        db.session.add(prop)
        db.session.commit()
        flash('Property listed successfully!', 'success')
        return redirect(url_for('property_attachments'))
    
    return render_template("list_property.html", title='List your property', form=form)
