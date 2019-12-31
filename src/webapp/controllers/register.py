from flask import flash, request, make_response, session
import datetime

from src.core.web import app, render_view
from src.utils.generate_token import generateToken
from src.utils.temp_toke import PerpetualTimer
from src.db.DAO.mysqlDAO import DAOManagerMysql
from src.db.DAO.DAO import DAOManager
from src.webapp.models.user import User
from src.webapp.models.token import Token
from src.utils.change_token import changeToken

@app.route('/register', methods=('GET', 'POST'))
def register():
    
    mysqlDM = DAOManagerMysql()
    user = mysqlDM.do(mysqlDM.USER,mysqlDM.EXIST_TOKEN,request.cookies.get('token'))
    perpetualT = PerpetualTimer() 

    if user:
              
        perpetualT.setFunction(changeToken, user.token.id)
        perpetualT.start()

        return render_view('home.html',user=user)

    if request.method == 'POST':  
        
        # generacion de token
        tokenValue = generateToken()
        t = Token(tokenValue,datetime.datetime.now(),0)
        # creacion de usario
        user = User(request.form['username'],request.form['password'],t,'0')              
        #if m.create(user):
        mysqlDM.beginTransaction()
        state = mysqlDM.do(mysqlDM.USER, mysqlDM.CREATE,user)        
        mysqlDM.endTransaction(state)

        if state:            
            user = mysqlDM.do(mysqlDM.USER, mysqlDM.GET_ONE, user.email)
            session['user'] = user.id
            response = make_response(render_view('home.html',user=user))
            # expiracion de cookie (no es posble ponerl una espiracion menor a 0.3 dias)
            expireDate = t.date + datetime.timedelta(days=0.3)
            response.set_cookie("token",tokenValue, expires=expireDate)            
            perpetualT.setFunction(changeToken,user.token.id)
            perpetualT.start()
                    #return 'Email: {} \nPassword: {}'.format(user.email,user.password)
            return response

        perpetualT.cancel()  
        flash('Email ya creado')
        
    perpetualT.cancel()  
    return render_view('register.html')