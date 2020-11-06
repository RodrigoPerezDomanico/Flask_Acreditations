from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysql_connector import MySQL
from databases import LocalHost, WebHost

Host=WebHost
db_name=Host['db_name']


def get_form_data():
    fullname=request.form['fullname']
    use=request.form['use']
    powerW=request.form['powerW']
    powerS=request.form['powerS']
    return fullname, use, powerW, powerS
    
def mysql_QUERRY(querry,mysql,requires_data=False):
    cur = mysql.connection.cursor()
    try:
        cur.execute(querry)

        if requires_data:
            return cur.fetchall()
        else:
            mysql.connection.commit()
    except:
        return []

def get_mysql_data(mysql,id=""):
    if id == "":
        querry=f'select * from  {db_name}.cargas'
    else:
        querry=f'select * from {db_name}.cargas where id ={id}'
    cur = mysql.connection.cursor()
    cur.execute(querry)
    data = cur.fetchall()
    return data


def get_login_data():
    user_name=request.form['UserName']
    user_password=request.form['Password']
    return [user_name,user_password]



def validate_login(login_data,mysql):
    
    user_data=get_user_data(login_data,mysql)
    print(user_data)
    if user_data != []:
        is_valid_user=True
        print(is_valid_user)
        return is_valid_user
    else:
        is_valid_user=False
        print(is_valid_user)
        return is_valid_user
    
def get_user_data(login_data,mysql):

    if len(login_data)==2:
        print('Querry1')
        querry =f'select * from {db_name}.usuarios where NombreUsuario="{str(login_data[0])}" and ContraseñaUsuario="{str(login_data[1])}"'
    else:
        print('Querry2')
        querry =f'select * from {db_name}.usuarios where NombreUsuario="{str(login_data)}"'
    user_data = mysql_QUERRY(querry,mysql,requires_data=True)
    return user_data