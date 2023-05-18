import json
import os

from flask import Flask, render_template, request, jsonify, redirect, flash, url_for

from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user


from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    # Check if user is in paid_user table
    user = User.query.get(int(user_id))
    if user:
        return user


    # If user is not in either table, return None
    return None

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
with app.app_context():
    class User(UserMixin, db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        phone = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(100))
        name = db.Column(db.String(1000))
    db.create_all()
class MyModelView(ModelView):
    def is_accessible(self):



            return True
admin = Admin(app)
admin.add_view(MyModelView(User, db.session))
@app.route('/')
def index():

    return "database created "
@app.route("/register",methods=["GET","POST"])
def re():
    if request.method=="POST":
        name=request.form.get("name")

        phone=request.form.get("phone")
        password_hashed=generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new=User(
            name=name,password=password_hashed,phone=phone
        )
        db.session.add(new)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        name = request.form.get("name")
        password = request.form.get("password")
        user=User.query.all()
        for  i  in user :
            if name ==i.name :
                if check_password_hash(i.password, password) :
                            return "welcome"
        return redirect("/register")
    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)