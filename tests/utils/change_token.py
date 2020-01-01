import datetime
from tests.utils.generate_token import generateToken
from tests.webapp.models.token import Token
from tests.db.DAO.mysqlDAO import DAOManagerMysql

def changeToken(idtoken):  
    print('cambia')  
    mysqlDM = DAOManagerMysql()   
    tokenValue = generateToken()
    t = Token(tokenValue,datetime.datetime.now(),idtoken)
    #actualiza el valro del token en la bd
    mysqlDM.do(mysqlDM.TOKEN, mysqlDM.UPDATE, t)
    mysqlDM.commit()