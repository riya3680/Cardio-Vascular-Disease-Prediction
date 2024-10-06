import numpy as np
from flask import Flask, request, jsonify, render_template, current_app, session , redirect , url_for, flash
import pickle
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
import bcrypt
from src.pipeline.predict_pipeline import customdata,predictpipeline


#create flask app

app =Flask(__name__)
with app.app_context():
    current_app.name

#db connection

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mydatabase'
app.secret_key='thisissecretkey'

mysql = MySQL(app)


# db = SQLAlchemy()
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SECRET_KEY'] = 'thisisasecretkey'
#
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False)
#     password = db.Column(db.String(80), nullable=False)

class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(), Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Login")


#load pickle model
model=pickle.load(open("model.pkl", 'rb'))


@app.route("/")
def Home():
    return render_template("base.html")
@app.route("/base.html")
def base():
    return render_template("base.html")
@app.route("/about.html")
def about():
    return render_template("about.html")
@app.route("/cvd.html")
def cvd():
    return render_template("cvd.html")
@app.route("/moreinfo.html")
def moreinfo():
    return render_template("moreinfo.html")
@app.route("/contact.html")
def contact():
    return render_template("contact.html")

#registration
@app.route("/register.html", methods=['GET','POST'])
def register():
    # msg = ''
    # if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form:
    #     name = request.form['name']
    #     email = request.form['email']
    #     password = request.form['password']
    #     print(name)
    #
    #     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #     cursor.execute('SELECT * FROM users  WHERE name = % s', (name,))
    #     account = cursor.fetchone()
    #     if account:
    #         msg = 'Account already exists !'
    #     elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
    #         msg = 'Invalid email address !'
    #     elif not re.match(r'[A-Za-z0-9]+', name):
    #         msg = 'Username must contain only characters and numbers !'
    #     elif not name or not password or not email:
    #         msg = 'Please fill out the form !'
    #     else:
    #         cursor.execute('INSERT INTO users VALUES (NULL, % s, % s, % s)', (name, email, password))
    #         mysql.connection.commit()
    #         msg = 'You have successfully registered !'
    # elif request.method == 'POST':
    #     msg = 'Please fill out the form !'
    # return render_template('register.html', msg=msg)


    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

        cursor = mysql.connection.cursor()

        cursor.execute("INSERT INTO users (name,email,password) VALUES (%s,%s,%s)", (name, email, hashed_password))
        mysql.connection.commit()
        flash("You have successfully registered !")

        return redirect(url_for('/'))

    return render_template('register.html', form=form)

@app.errorhandler(404)
def internal_error(error):
    return redirect(url_for('login'))


@app.route("/login.html")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['user_id'] = user[0]
            return redirect(url_for('index'))
        else:
            flash("Login failed. Please check your email and password")
            return redirect(url_for('login'))

    return render_template("index.html")
    return render_template('login.html', form=form)



    #return render_template("index.html")

    #return render_template("login.html")


@app.route("/analysis.html")
def analysis():
    return render_template("analysis.html")


#after logged in

@app.route("/predict.html", methods=["GET", "POST"])
def predict():
    # if request.method == 'POST':
    #     age = request.form.get('age'),
    #     sex = request.form.get('sex'),
    #     cp = request.form.get('cp'),
    #     trestbps = request.form.get('trestbps'),
    #     chol = request.form.get('chol'),
    #     fbs = request.form.get('fbs'),
    #     restecg = request.form.get('restecg'),
    #     thalach = request.form.get('thalach'),
    #     exang = request.form.get('exang'),
    #     oldpeak = (request.form.get('oldpeak')),
    #     slope = request.form.get('slope'),
    #     ca = request.form.get('ca'),
    #     thal = request.form.get('thal')
    #
    #
    #
    #     final=[np.array(int_features)]
    #     prediction = model.predict_proba(final)
    #     return render_template("index.html", result=result[0])
    # return render_template("predict.html")


    if request.method == 'GET':
        return render_template("predict.html")
    else:
        gender = request.form.get("gender")
        data = customdata(
            age=request.form.get('age'),
            sex=1 if gender == "male"  else 0 ,
            cp=request.form.get('cp'),
            trestbps=request.form.get('trestbps'),
            chol=request.form.get('chol'),
            fbs=request.form.get('fbs'),
            restecg=request.form.get('restecg'),
            thalach=request.form.get('thalach'),
            exang=request.form.get('exang'),
            oldpeak=(request.form.get('oldpeak')),
            slope=request.form.get('slope'),
            ca=request.form.get('ca'),
            thal=request.form.get('thal'),
        )
        pred_df = data.get_data_as_data_frame()
        print(pred_df)

        predict_pipeline= predictpipeline()
        result = predict_pipeline.predict(pred_df)
        pred=result
        print(f"This is the result : {result}")
        result1 = "The person has heart disease" if result[0] == 1 else "The person is safe"
        print(result1)
        print(pred)
        return render_template("analysis.html", data=pred)

        if result[0] == 1:
            return render_template("analysis.html", result='THE PREDICTED RESULT IS SAFE')
        else:
            return render_template("analysis.html", result='YOU HAVE HEART DISEASE')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
