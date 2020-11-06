from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from flask_mysql_connector import MySQL
from databases import WebHost
from utils import get_form_data, get_login_data, get_mysql_data, mysql_QUERRY, validate_login, get_user_data

Host=WebHost
db_name=Host['db_name']


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
        # querry =f'select * from {db_name}.usuarios where NombreUsuario="{str(login_data[0])}" and ContraseñaUsuario="{str(login_data[1])}"'
        # user.is_authenticated = login_data[1]==mysql_QUERRY(querry,mysql,requires_data=True)[0][2]
        
        return response
    else:
        flash('Usuario o Contraseña inválida')
        return redirect(url_for('login'))
        


@app.route('/index', methods=['POST','GET'])
def Index():
    
    login_name=request.cookies.get('LoginName')
    if login_name==None:
        return redirect(url_for('login'))
    
    user_name=get_user_data(login_name,mysql)[0][1]
    
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

    
# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_mysql_connector import MySQL
# db_name='heroku_4176df70e24c00b'
# app = Flask(__name__)
# app.config['MYSQL_HOST'] = 'us-cdbr-east-02.cleardb.com'
# app.config['MYSQL_USER'] = 'bfe72865c42656'
# app.config['MYSQL_PASSWORD'] = '14b76e1c'
# app.config['MYSQL_DB'] = 'heroku_4176df70e24c00b'
# mysql = MySQL(app)

# # Settings
# app.secret_key = 'mysecretkey'

# def get_form_data():
#     fullname=request.form['fullname']
#     use=request.form['use']
#     powerW=request.form['powerW']
#     powerS=request.form['powerS']
#     return fullname, use, powerW, powerS
# def mysql_QUERRY(querry):
#     cur = mysql.connection.cursor()
#     cur.execute(querry)
#     mysql.connection.commit()
# def get_mysql_data(id=""):
#     if id == "":
#         querry='select * from heroku_4176df70e24c00b.cargas'
#     else:
#         querry=f'select * from heroku_4176df70e24c00b.cargas where id ={id}'
#     cur = mysql.connection.cursor()
#     cur.execute(querry)
#     data = cur.fetchall()
#     return data


# EXAMPLE_SQL = 'select * from heroku_4176df70e24c00b.cargas'
# # @app.route('/login')
# # def Login():
    
# @app.route('/')
# def Index():
#     data = get_mysql_data() 

#     return render_template('index.html', cargas=data)

# @app.route('/add_contact', methods=['POST'])
# def add_contact():
#     if request.method == 'POST':
#         fullname, use, powerW, powerS = get_form_data()
#         mysql_QUERRY(f'INSERT INTO heroku_4176df70e24c00b.cargas (Nombre, Tipo, PotenciaW, PotenciaS) VALUES("{fullname}", "{use}", "{powerW}", "{powerS}")')
#         # cur = mysql.connection.cursor()
#         # cur.execute('INSERT INTO heroku_4176df70e24c00b.Cargas (fullname, use, powerW) VALUES(%s, %s, %s)',
#         # (fullname, use, powerW))
#         # mysql.connection.commit()
#         flash('Carga Agregada Satisfactoriamente')
#         return redirect(url_for('Index'))

# @app.route('/edit/<string:id>')
# def get_contact(id):
#     data = get_mysql_data(id)   
#     return render_template('edit-contact.html', contact = data[0])

# @app.route('/update/<string:id>',methods=['POST'])
# def update_contact(id):
#     if request.method == 'POST':
#         fullname, use, powerW, powerS = get_form_data()
#         querry=f'update {db_name}.cargas set Nombre="{str(fullname)}", Tipo="{str(use)}", PotenciaW="{str(powerW)}", PotenciaS="{str(powerS)}" where id = {id}'
#         mysql_QUERRY(querry)
#         return redirect(url_for('Index'))

# @app.route('/delete/<string:id>')
# def delete(id):
#     cur = mysql.connection.cursor()
#     cur.execute(f'delete from heroku_4176df70e24c00b.cargas where id = {id}')
#     mysql.connection.commit()
#     flash('Contact succesfully removed')
#     return redirect(url_for('Index'))

# if __name__ == "__main__":
#     app.run(port=3000, debug=True)