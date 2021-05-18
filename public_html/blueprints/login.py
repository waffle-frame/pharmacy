from models import *
from flask import Blueprint, render_template, request, redirect, session


bp = Blueprint('login', __name__ )


@bp.route('/', methods=['GET'])
def Get():
    msg = request.args.get('msg', None)
    return render_template('login/login.html', msg = msg)
    
    
@bp.route('/', methods=['POST'])
def Check():
    _username =  request.form['username']
    _password = request.form['password']
    
    user = Users.get_or_none(_username == Users.username)
    
    if user == None:
        return redirect('/login/?msg=Такой пользователь остуствует')
        
    if _password != user.password:
        return redirect('/login/?msg=Неправильный пароль')
    
    
    session['userid'] = user.id
    session['role'] = user.role
    session['networkid'] = user.network.id


    if user.role == 'admin':
        return redirect('/admin/')
    else:
        employee = Employees.get(Employees.userID == user)

        print(employee)

        session['pharmacy'] = int(str(employee.pharmacy))
        session['department'] = int(str(employee.department))

        return redirect('/selller/sale')