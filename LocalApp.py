from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from flask_mysql_connector import MySQL
import flask_login as flog
from databases import LocalHost
from utils import get_form_data, get_login_data, get_mysql_data, mysql_QUERRY, validate_login, get_user_data

Host=LocalHost
db_name=Host['db_name']

validate_login
#Configuracion de la app
app = Flask(__name__)
app.config['MYSQL_HOST'] = Host['host']
app.config['MYSQL_USER'] = Host['user']
app.config['MYSQL_PASSWORD'] = Host['password']
app.config['MYSQL_DB'] = f'{db_name}'
app.secret_key = 'mysecretkey'
mysql = MySQL(app)

EXAMPLE_SQL = f'select * from {db_name}.cargas'

@app.route('/')
def main():
    login_name=request.cookies.get('LoginName')
    if login_name==None:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('Cargas'))
    


@app.route('/login')
def login():
    login_name=request.cookies.get('LoginName')
    if login_name!=None:
        return redirect(url_for('Cargas'))
    return render_template('login.html')


@app.route('/check_user', methods=['POST','GET'])
def check_user():
    login_data=get_login_data()
    is_valid_user=validate_login(login_data,mysql,db_name)
    
    if is_valid_user:
        response=make_response(redirect(url_for('Cargas')))
        response.set_cookie('LoginName',login_data[0])
        return response
    else:
        flash('Usuario o Contraseña inválida')
        return redirect(url_for('login'))
        


@app.route('/cargas', methods=['POST','GET'])
def Cargas():
    
    login_name=request.cookies.get('LoginName')
    if login_name==None:
        return redirect(url_for('login'))
    print(login_name)
    user_name=get_user_data(login_name,mysql,db_name)[0][1]
    print(user_name)
    if login_name==user_name:
        data = get_mysql_data(mysql,db_name) 

        return render_template('cargas.html', cargas=data)
    else:
        return redirect(url_for('login'))

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname, use, powerW, powerS = get_form_data()
        mysql_QUERRY(f'INSERT INTO {db_name}.cargas (Nombre, Tipo, PotenciaW, PotenciaS) VALUES("{fullname}", "{use}", "{powerW}", "{powerS}")',mysql)
        flash('Carga Agregada Satisfactoriamente')
        return redirect(url_for('Cargas'))

@app.route('/edit/<string:id>')
def get_contact(id):
    data = get_mysql_data(mysql,db_name,id)   
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<string:id>',methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname, use, powerW, powerS = get_form_data()
        querry=f'update {db_name}.cargas set Nombre="{str(fullname)}", Tipo="{str(use)}", PotenciaW="{str(powerW)}", PotenciaS="{str(powerS)}" where id = {id}'
        mysql_QUERRY(querry,mysql)
        return redirect(url_for('Cargas'))

@app.route('/delete/<string:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute(f'delete from {db_name}.cargas where id = {id}')
    mysql.connection.commit()
    flash('Contact succesfully removed')
    return redirect(url_for('Cargas'))

if __name__ == "__main__":
    app.run(port=3000, debug=True)