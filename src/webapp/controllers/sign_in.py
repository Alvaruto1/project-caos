from flask import flash, request, make_response, session
import datetime

from src.core.web import app, render_view
from src.db.DAO.mysqlDAO import DAOManagerMysql
from src.db.DAO.DAO import DAOManager
from src.utils.generate_token import generateToken
from src.utils.temp_toke import PerpetualTimer
from src.utils.change_token import changeToken
from src.webapp.models.user import User
from src.webapp.models.token import Token

@app.route('/sign_in', methods=('GET', 'POST'))
def signIn():

    mysqlDM = DAOManagerMysql()
    #m = MySQLUser()
    #mT = MySQLToken()
    
    # verficia si el toquen que se tiene en las cookies esta registrado en la bd y devulve el usuario corresponidente
    #user = mT.existToken(request.cookies.get('token'))
    user = mysqlDM.do(mysqlDM.USER,mysqlDM.EXIST_TOKEN,request.cookies.get('token'))
    print(request.cookies.get('token'))

    if user:

        # cambio de token de usuario cada cierto tiempo
        
        """def verificate():
            #mT = MySQLToken()
            tokenValue = generateToken()
            t = Token(tokenValue,datetime.datetime.now(),user.token)
            #actualiza el valro del token en la bd
            mysqlDM.do(mysqlDM.TOKEN, mysqlDM.UPDATE, t)
            #mT.update(t) """

        # inicio de ciclo infinito cambio de token
        
        perpetualT = PerpetualTimer()
        
        print(user,'pio'*10)
        perpetualT.setFunction(changeToken, user.token.id)
        perpetualT.start()
        #g.user.setFunction(verificate) 
        #g.user.start()        

        return render_view('home.html',user=user)

    if request.method == 'POST':
        
        # generacion de token
        tokenValue = generateToken()

        t = Token(tokenValue,datetime.datetime.now(),0)
        email = request.form['username']

        # busqueda de usario por gmail (ingresado anteriormente)       
        user = mysqlDM.do(mysqlDM.USER, mysqlDM.GET_ONE,email)
        #user = m.getOne(email)
        
        if user != None:
            
            # verificacion de password
            if user.password == request.form['password']:
                
                t.id=user.token.id

                mysqlDM.do(mysqlDM.TOKEN, mysqlDM.UPDATE, t)
                mysqlDM.commit()
                #mT.update(t)
                session['user'] = user.id                
                response = make_response(render_view('home.html',user=user))

                # expiracion de cookie (no es posble ponerl una espiracion menor a 0.3 dias)
                expireDate = t.date + datetime.timedelta(days=0.3)
                response.set_cookie("token",tokenValue,expires = expireDate) 

                # cambio de token de usario cada 
                
                """def verificate():
                    #mT = MySQLToken()
                    tokenValue = generateToken()
                    t = Token(tokenValue,datetime.datetime.now(),user.token)
                    #actualiza el valro del token en la bd
                    mysqlDM.do(mysqlDM.TOKEN, mysqlDM.UPDATE, t)
                 """                         
                print('aquie si entra')
                perpetualT = PerpetualTimer()
                print(perpetualT)
                perpetualT.setFunction(changeToken, user.token.id)
                perpetualT.start()                                            
                
                
                return response        
        flash('Datos ingresados incorrectos')
        return render_view('sign_in.html')        

    return render_view('sign_in.html')
