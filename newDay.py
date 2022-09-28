from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysql_connector import MySQL
from databases import LocalHost
import datetime
Host=LocalHost
db_name=Host['db_name']


app = Flask(__name__)
app.config['MYSQL_HOST'] = Host['host']
app.config['MYSQL_USER'] = Host['user']
app.config['MYSQL_PASSWORD'] = Host['password']
app.config['MYSQL_DB'] = f'{db_name}'
app.secret_key = 'mysecretkey'
mysql = MySQL(app)
print(mysql)
## Creamos un nuevo día..
day=datetime.date.today()

def _getDNI(mysql,db_name):
    with app.app_context():
        querry=f'select DNIAlumnos from  {db_name}.alumnos'
        cur = mysql.connection.cursor()
        cur.execute(querry)
        data = cur.fetchall()
    return data

def createDay(mysql):
    with app.app_context():
        day=str(datetime.date.today()).replace('-','')
        querry=f'create table DAY{day} (DNIAlumno INT NOT NULL PRIMARY KEY, Asistence BIT)'
        cur = mysql.connection.cursor()
        cur.execute(querry)

createDay(mysql)