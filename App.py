from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysql_connector import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Rodrigo1'
app.config['MYSQL_DB'] = 'instalaciones'
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
        querry='select * from instalaciones.Cargas'
    else:
        querry=f'select * from instalaciones.Cargas where id ={id}'
    cur = mysql.connection.cursor()
    cur.execute(querry)
    data = cur.fetchall()
    return data

def sum(val_1,val_2):
    return val_1, val_2, val_1+val_2
EXAMPLE_SQL = 'select * from instalaciones.Cargas'

@app.route('/')
def Index():
    data = get_mysql_data() 

    return render_template('index.html', cargas=data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname, use, powerW, powerS = get_form_data()
        mysql_QUERRY(f'INSERT INTO instalaciones.Cargas (Nombre, Tipo, PotenciaW, PotenciaS) VALUES("{fullname}", "{use}", "{powerW}", "{powerS}")')
        # cur = mysql.connection.cursor()
        # cur.execute('INSERT INTO instalaciones.Cargas (fullname, use, powerW) VALUES(%s, %s, %s)',
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
        cur = mysql.connection.cursor()
        cur.execute(f'update instalaciones.Cargas set fullname="{str(fullname)}", use="{str(use)}", powerW="{str(powerW)}" powerS="{str(powerS)}" where id = {id}')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute(f'delete from instalaciones.Cargas where id = {id}')
    mysql.connection.commit()
    flash('Contact succesfully removed')
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(port=3000, debug=True)