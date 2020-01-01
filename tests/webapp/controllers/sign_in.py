from flask import flash, request, make_response, session,redirect, url_for
import datetime

from tests.core.web import app, render_view
from tests.db.DAO.mysqlDAO import DAOManagerMysql
from tests.db.DAO.DAO import DAOManager
from tests.utils.generate_token import generateToken
from tests.utils.temp_toke import PerpetualTimer
from tests.utils.change_token import changeToken
from tests.webapp.models.user import User
from tests.webapp.models.token import Token

@app.route('/sign_in', methods=('GET', 'POST'))
def signIn():

    mysqlDM = DAOManagerMysql()   
    # verficia si el toquen que se tiene en las cookies esta registrado en la bd y devulve el usuario corresponidente
    user = mysqlDM.do(mysqlDM.USER,mysqlDM.EXIST_TOKEN,request.cookies.get('token'))
    perpetualT = PerpetualTimer() 
    if user:

        # inicio de ciclo infinito cambio de token             
        perpetualT.setFunction(changeToken, user.token.id)
        perpetualT.start()

        return render_view('home.html',user=user)
        

    if request.method == 'POST':
        
        # generacion de token
        tokenValue = generateToken()
        t = Token(tokenValue,datetime.datetime.now(),0)
        email = request.form['username']
        # busqueda de usario por gmail (ingresado anteriormente)       
        user = mysqlDM.do(mysqlDM.USER, mysqlDM.GET_ONE,email)
        
        if user != None:
            
            # verificacion de password
            if user.password == request.form['password']:
                
                t.id=user.token.id
                mysqlDM.do(mysqlDM.TOKEN, mysqlDM.UPDATE, t)
                mysqlDM.commit()
                session['user'] = user.id                
                response = make_response(render_view('home.html',user=user))
                # expiracion de cookie (no es posble ponerl una espiracion menor a 0.3 dias)
                expireDate = t.date + datetime.timedelta(days=0.3)
                response.set_cookie("token",tokenValue,expires = expireDate) 
                               
                perpetualT.setFunction(changeToken, user.token.id)                
                perpetualT.start()                                            
                
                return response        
        flash('Datos ingresados incorrectos')
        perpetualT.cancel()        
        return render_view('sign_in.html')        

    perpetualT.cancel()
    return render_view('sign_in.html')
