from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from flask_mysql_connector import MySQL
import flask_login as flog
from databases import LocalHost
from utils import get_form_data, get_login_data, get_mysql_data, mysql_QUERRY, validate_login, get_user_data

Host=LocalHost
db_name=Host['db_name']


#Configuracion de la app
app = Flask(__name__)
app.config['MYSQL_HOST'] = Host['host']
app.config['MYSQL_USER'] = Host['user']
app.config['MYSQL_PASSWORD'] = Host['password']
app.config['MYSQL_DB'] = f'{db_name}'
app.secret_key = 'mysecretkey'
mysql = MySQL(app)


# Configuración del Login
login_manager =flog.LoginManager()
login_manager.init_app(app)
class User(flog.UserMixin):
    pass

@login_manager.user_loader
def user_loader():
    login_data=get_login_data()
    is_valid_user=validate_login(login_data,mysql)
    if not is_valid_user:
        return
    user=User()
    user.id=login_data[0]
    print(user.id)
    user.is_authenticated=True




    


EXAMPLE_SQL = f'select * from {db_name}.cargas'

@app.route('/')
def login():
    login_name=request.cookies.get('LoginName')
    if login_name!=None:
        return redirect(url_for('Index'))
    return render_template('login.html')


@app.route('/check_user', methods=['POST','GET'])
def check_user():
    login_data=get_login_data()
    is_valid_user=validate_login(login_data,mysql)
    
    if is_valid_user:
        response=make_response(redirect(url_for('Index')))
        response.set_cookie('LoginName',login_data[0])

        # user=User()
        # user.id=login_data[0]
        # print(user.id)
        # querry =f'select * from {db_name}.usuarios where NombreUsuario="{str(login_data[0])}" and ContraseñaUsuario="{str(login_data[1])}"'
        # print(login_data[1],mysql_QUERRY(querry,mysql,requires_data=True)[0][2], login_data[1]==mysql_QUERRY(querry,mysql,requires_data=True)[0][2])
        # user.is_authenticated = login_data[1]==mysql_QUERRY(querry,mysql,requires_data=True)[0][2]
        
        return response
    else:
        print('Usuario No encontrado')
        flash('Usuario o Contraseña inválida')
        return redirect(url_for('login'))
        


@app.route('/index', methods=['POST','GET'])
def Index():
    
    login_name=request.cookies.get('LoginName')
    if login_name==None:
        return redirect(url_for('login'))
    print(login_name)
    user_name=get_user_data(login_name,mysql)[0][1]
    print(user_name)
    if login_name==user_name:
        data = get_mysql_data(mysql) 

        return render_template('index.html', cargas=data)
    else:
        return redirect(url_for('login'))

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname, use, powerW, powerS = get_form_data()
        mysql_QUERRY(f'INSERT INTO {db_name}.cargas (Nombre, Tipo, PotenciaW, PotenciaS) VALUES("{fullname}", "{use}", "{powerW}", "{powerS}")',mysql)
        # cur = mysql.connection.cursor()
        # cur.execute('INSERT INTO {db_name}.Cargas (fullname, use, powerW) VALUES(%s, %s, %s)',
        # (fullname, use, powerW))
        # mysql.connection.commit()
        flash('Carga Agregada Satisfactoriamente')
        return redirect(url_for('Index'))

@app.route('/edit/<string:id>')
def get_contact(id):
    data = get_mysql_data(mysql,id)   
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<string:id>',methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname, use, powerW, powerS = get_form_data()
        querry=f'update {db_name}.cargas set Nombre="{str(fullname)}", Tipo="{str(use)}", PotenciaW="{str(powerW)}", PotenciaS="{str(powerS)}" where id = {id}'
        mysql_QUERRY(querry,mysql)
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute(f'delete from {db_name}.cargas where id = {id}')
    mysql.connection.commit()
    flash('Contact succesfully removed')
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(port=3000, debug=True)