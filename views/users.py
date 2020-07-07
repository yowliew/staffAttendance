from flask import Blueprint, request, session, url_for, render_template, redirect, flash, current_app
from models.users import UserModel

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/', methods=['GET'])  # get /users/login
def the_login():
    return redirect(url_for('users.login_user'))


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            UserModel.is_user_valid(username=username, password=password)
            session['username'] = username
            return redirect(url_for('users.the_base'))
        except Exception as e:
            flash(f"Error {e}", category="warning")
            return render_template("users/login.html", org_name=current_app.config["ORG_NAME"]) # error
    return render_template("users/login.html", org_name=current_app.config["ORG_NAME"])  # GET method


@user_blueprint.route('/register', methods=['GET'])  # get /users/register
def register_user():
    if request.method == 'GET':
        return render_template("users/register.html")  # This is for Get method


@user_blueprint.route('/attendance', methods=['GET'])  # render the landing page
def the_base():
    return render_template("base.html", org_name=current_app.config["ORG_NAME"])
