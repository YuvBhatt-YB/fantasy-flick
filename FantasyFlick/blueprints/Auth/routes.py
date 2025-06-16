from flask import Flask,render_template,Blueprint,request,redirect,url_for,flash
from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email
from FantasyFlick.app import db,bcrypt
from FantasyFlick.blueprints.Auth.models import User
from flask_login import login_user,logout_user


Auth = Blueprint("Auth",__name__,template_folder="templates")

class SignUpForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    email = EmailField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    signup = SubmitField("Sign Up")

class LogInForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    login = SubmitField("Log In")

@Auth.route("/signup",methods=["GET","POST"])
def signup():
    username = None
    email = None
    password = None
    signup_form = SignUpForm()
    if signup_form.validate_on_submit():
        username = signup_form.username.data
        email = signup_form.email.data
        password = signup_form.password.data
        signup_form.username.data = ""
        signup_form.email.data = ""
        signup_form.password.data = ""
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists.","warning")
            return redirect(url_for("Auth.signup"))
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(username=username,email=email,password=hashed_password,role="user")
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("HomePage.index"))

    return render_template("Auth/signup.html",signup_form=signup_form)



@Auth.route("/login",methods=["GET","POST"])
def login():
    username = None
    password = None
    login_form = LogInForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        login_form.username.data = ""
        login_form.password.data = ""
        
        user = User.query.filter(User.username == username).first()
        if user is None:
            flash("Username not found","error")
            return redirect(url_for("Auth.login"))
        if bcrypt.check_password_hash(user.password,password):
            login_user(user)
            return redirect(url_for("UserDashboard.index"))
        else:
            flash("Invalid Username or Password","error")
            return redirect(url_for("Auth.login"))
            
    return render_template("Auth/login.html",login_form = login_form)

@Auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('HomePage.index'))