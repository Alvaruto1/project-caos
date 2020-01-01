from flask import jsonify,request, flash
from tests.core.web import app, render_view
from tests.db.DAO.mysqlDAO import DAOManagerMysql
from tests.utils.temp_toke import PerpetualTimer

perpetualT = PerpetualTimer()

@app.route('/edit')
def edit():
    mysqlDM = DAOManagerMysql()   
    # verficia si el toquen que se tiene en las cookies esta registrado en la bd y devulve el usuario corresponidente
    user = mysqlDM.do(mysqlDM.USER,mysqlDM.EXIST_TOKEN,request.cookies.get('token'))
    
    if user:            
        return render_view('edit.html',user=user)
    perpetualT.cancel()
    return render_view('sign_in.html')

@app.route('/edited', methods=('POST','GET'))
def edited():
    mysqlDM = DAOManagerMysql()   
    # verficia si el toquen que se tiene en las cookies esta registrado en la bd y devulve el usuario corresponidente
    user = mysqlDM.do(mysqlDM.USER,mysqlDM.EXIST_TOKEN,request.cookies.get('token'))
    

    if user:
        emailB = user.email
        passwordB = user.password
        if request.method == 'POST':
            
            email = request.form['username']
            password = request.form['password']
            user.email = email
            user.password = password
            state = mysqlDM.do(mysqlDM.USER, mysqlDM.UPDATE,user)
            print(state)
            print('arto'*8)
            if state:
                mysqlDM.commit()
                return render_view('home.html',user=user)
            flash('Error al editar usuario')
            return render_view('edit.html',user=user)
        user.email = emailB
        user.password = passwordB
        return render_view('home.html',user=user)
    perpetualT.cancel()
    return render_view('sign_in.html')