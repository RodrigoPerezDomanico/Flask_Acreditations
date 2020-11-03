from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysql_connector import MySQL
from databases import LocalHost
db_name=LocalHost['db_name']
app = Flask(__name__)
app.config['MYSQL_HOST'] = LocalHost['host']
app.config['MYSQL_USER'] = LocalHost['user']
app.config['MYSQL_PASSWORD'] = LocalHost['password']
app.config['MYSQL_DB'] = '{db_name}'
mysql = MySQL(app)

# Settings
app.secret_key = 'mysecretkey'

def get_form_data():
    fullname=request.form['fullname']
    use=request.form['use']
    powerW=request.form['powerW']
    powerS=request.form['powerS']
    return fullname, use, powerW, powerS
def mysql_QUERRY(querry):
    cur = mysql.connection.cursor()
    cur.execute(querry)
    mysql.connection.commit()
def get_mysql_data(id=""):
    if id == "":
        querry=f'select * from  {db_name}.cargas'
    else:
        querry=f'select * from {db_name}.cargas where id ={id}'
    cur = mysql.connection.cursor()
    cur.execute(querry)
    data = cur.fetchall()
    return data


EXAMPLE_SQL = 'select * from {db_name}.cargas'

@app.route('/')
def Index():
    data = get_mysql_data() 

    return render_template('index.html', cargas=data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname, use, powerW, powerS = get_form_data()
        mysql_QUERRY(f'INSERT INTO {db_name}.cargas (Nombre, Tipo, PotenciaW, PotenciaS) VALUES("{fullname}", "{use}", "{powerW}", "{powerS}")')
        # cur = mysql.connection.cursor()
        # cur.execute('INSERT INTO {db_name}.Cargas (fullname, use, powerW) VALUES(%s, %s, %s)',
        # (fullname, use, powerW))
        # mysql.connection.commit()
        flash('Carga Agregada Satisfactoriamente')
        return redirect(url_for('Index'))

@app.route('/edit/<string:id>')
def get_contact(id):
    data = get_mysql_data(id)   
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<string:id>',methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname, use, powerW, powerS = get_form_data()
        querry=f'update {db_name}.cargas set Nombre="{str(fullname)}", Tipo="{str(use)}", PotenciaW="{str(powerW)}", PotenciaS="{str(powerS)}" where id = {id}'
        mysql_QUERRY(querry)
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