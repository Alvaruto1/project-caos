from flask import flash, request, make_response
import datetime

from src.core.web import app, render_view
from src.utils.generate_token import generateToken
from src.utils.temp_toke import PerpetualTimer
from src.db.DAO.mysqlDAO import DAOManagerMysql
from src.db.DAO.DAO import DAOManager
from src.webapp.models.user import User
from src.webapp.models.token import Token

@app.route('/register', methods=('GET', 'POST'))
def register():
    
    mysqlDM = DAOManagerMysql()
    if request.method == 'POST':  
        
        # generacion de token
        tokenValue = generateToken()
        t = Token(tokenValue,datetime.datetime.now(),0)
        # creacion de usario
        user = User(request.form['username'],request.form['password'],t,'0')              
        #if m.create(user):
        mysqlDM.beginTransaction()
        state = mysqlDM.do(mysqlDM.USER, mysqlDM.CREATE,user)
        print(state,'estadp'*8)
        mysqlDM.endTransaction()
        
        if state:            
            
            session['user'] = user.id
            response = make_response(render_view('home.html',user=user))
            # expiracion de cookie (no es posble ponerl una espiracion menor a 0.3 dias)
            expireDate = t.date + datetime.timedelta(days=0.3)
            response.set_cookie("token",tokenValue, expires=expireDate)
            
            # cambio de token de usario cada 
            @copy_current_request_context
            def verificate():
                #mT = MySQLToken()
                tokenValue = generateToken()
                t = Token(tokenValue,datetime.datetime.now(),user.token)
                #actualiza el valro del token en la bd
                mysqlDM.do(mysqlDM.TOKEN, mysqlDM.UPDATE, t)
                mysqlDM.commit()
                                          
                    
            perpetualT = PerpetualTimer()
            perpetualT.setFunction(verificate)
            perpetualT.start()
                    #return 'Email: {} \nPassword: {}'.format(user.email,user.password)
            return response
        mysqlDM.endTransaction()
        flash('Email ya creado')
        

    return render_view('register.html')