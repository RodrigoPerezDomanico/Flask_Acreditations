from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysql_connector import MySQL
from databases import LocalHost, WebHost

# Host=WebHost
# db_name=Host['db_name']


def get_form_data():
    fullname=request.form['fullname']
    idNumber=request.form['idNumber']
    return fullname,idNumber
    
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

def get_mysql_data(mysql,db_name,id="",reg=None):
    print(reg)
    
    if id == "":
        querry=f'select * from  {db_name}.alumnos'
    else:
        if reg=='nombreAlumnos':
            querry=f'select * from {db_name}.alumnos where nombreAlumnos="{str(id)}"'
        else:
            querry=f'select * from {db_name}.alumnos where DNIAlumnos={id}'

    cur = mysql.connection.cursor()
    cur.execute(querry)
    data = cur.fetchall()
    print(data)
    return data


def get_login_data():
    user_name=request.form['UserName']
    user_password=request.form['Password']
    return [user_name,user_password]



def validate_login(login_data,mysql,db_name):
    
    user_data=get_user_data(login_data,mysql,db_name)
    
    if user_data != []:
        is_valid_user=True
        return is_valid_user
    else:
        is_valid_user=False
        return is_valid_user
    
def get_user_data(login_data,mysql,db_name):

    if len(login_data)==2:
        querry =f'select * from {db_name}.usuarios where NombreUsuario="{str(login_data[0])}" and ContraseñaUsuario="{str(login_data[1])}"'
    else:
        querry =f'select * from {db_name}.usuarios where NombreUsuario="{str(login_data)}"'
    user_data = mysql_QUERRY(querry,mysql,requires_data=True)
    return user_data