import os
import sqlite3
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# TODO - Migrar mysql a sqlite
class Database:
    def __init__(self) -> None:
        self.connection = self.newConnection()
        self.cursor = self.connection.cursor()

    def newConnection(self) -> mysql.connector:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_DATABASE'),
            auth_plugin='mysql_native_password'
        )

        return connection

    def commit(self) -> None:
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()


@app.route("/")
def users():
    database = Database()
    cursor = database.cursor
    cursor.execute("SELECT * FROM User;")
    return render_template('users.html', users=cursor.fetchall())


@app.route("/upload")
def upload_view():
    return render_template('upload_view.html')


@app.route("/uploader", methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':
        f = request.files['avatar']
        relative_path = f"uploads/{secure_filename(f.filename)}"
        data = {
            'nombre': request.form['nombre'],
            'email': request.form['email'],
            'avatar': relative_path
        }
        f.save("app/static/" + relative_path)

        database = Database()
        cursor = database.cursor
        cursor.execute(
            f"INSERT INTO User(nombre, correo, url_avatar) VALUES ('{data['nombre']}', '{data['email']}', '{data['avatar']}');")
        database.commit()
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
