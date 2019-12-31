import os,datetime, mysql.connector
from flask import current_app
import src.db.DAO.DAO as DAO
from mysql.connector import Error
from src.webapp.models.user import User
from src.webapp.models.token import Token

class MysqlDAOUser(DAO.UserDAO):

    table = "users"
    
    def __init__(self,connection):
        self.connection=connection 
    
    def create(self,user): 

        # generate token
        try:
            mT = DAOManagerMysql()
            if not mT.do(mT.TOKEN, mT.CREATE, user.token):
                raise Error('no create token')
                return False
            
            #mT.create(user.token)
            idToken = mT.do(mT.TOKEN, mT.LAST_ID_TOKEN)     
            
        except Error as e:
            print('Error DAOUser create 1: {}'.format(e)) 
            return False     
        

        try:
            if user.email == '' or user.password == '':
                raise Error('empty fields')
                #print('Error: empty fields')
                return False

        except Error as e:
            print('Error DAOUser create 2: {}'.format(e))            
            return False
            
        cursor = self.connection.cursor()        
        dataUser = (user.email, user.password, idToken,)
        sql = """ INSERT INTO {} (email, password, idtoken) VALUES(%s,%s,%s);""".format(self.table)    
        
        try: 
            cursor.execute(sql, dataUser)
        except Error as e:
            print('Error DAOUser create 3: {}'.format(e))
            return False

        #self.connection.commit()
        return True
    
    def delete(self,idUser):
        
        cursor = self.connection.cursor()
        sql = """ DELETE FROM {} WHERE idusers = '{}';""".format(self.table, idUser)
        
        try:
            cursor.execute(sql)
            if cursor.rowcount == 0:
                raise Error('no found row, no deleted')
                #print('Error: no found row, no deleted')    
                return False    
        except Error as e:
            print('Error DAOUser delete: {}'.format(e))
            return False
        
        #self.connection.commit()
        return True
    
    def update(self,user):        

        try:
            if user.email == '' or user.password == '':
                raise Error('empty fields')
                #print('Error: empty fields')
                return False
        except Error as e:
            print('Error DAOUser update: {}'.format(e))
            return False        
        
        cursor = self.connection.cursor()
        dataUser = (user.email, user.password, user.token.id,user.id)
        sql = """ UPDATE {} SET email=%s, password=%s, idtoken=%s WHERE idusers=%s;""".format(self.table)

        try:
            cursor.execute(sql,dataUser)
            if cursor.rowcount == 0:
                raise Error(' no found row, no updated')
                #print('Error: no found row, no updated')    
                return False 
        except Error as e:
            print('Error DAOUser update: {}'.format(e))
            return False               

        return True
    
    
    def getOne(self,idUser):
        
        cursor = self.connection.cursor()
        sql = """ SELECT * FROM {} WHERE email = '{}';""".format(self.table, idUser)
        
        try:            
            cursor.execute(sql)
        except Error as e:
            print('Error DAOUser getOne: {}'.format(e))            
            return False

        user = None
        query = cursor.fetchone()        

        if query:
            user = self.queryToObject(query)
        else:
            print('Error DAOUser getOne: no found user')
        
        return user
    
    
    def getAll(self,filter = None):
        
        cursor = self.connection.cursor()

        filterWhere = '' if filter is None else "WHERE email LIKE '%{}%'".format(filter)

        sql = """ SELECT * FROM {} {};""".format(self.table,filterWhere)
        
        try:
            cursor.execute(sql)
        except Error as e:
            print('Error DAOUser getAll: {}'.format(e))            
            return False

        rows = cursor.fetchall()
        users = []
        for row in rows:
            user = self.queryToObject(row)
            users.append(user)
        
        return users

    
    def _getOneByToken(self, idToken):

        cursor = self.connection.cursor()
        sql = "SELECT * FROM users WHERE idtoken='{}'".format(idToken)
        cursor.execute(sql)
        query = cursor.fetchone()

        if query == None:            
            return None

        return self.queryToObject(query)


    def existToken(self, token):

        cursor = self.connection.cursor()
        sql = "SELECT * FROM tokens WHERE value = '{}'".format(token)
        cursor.execute(sql)
        query = cursor.fetchone()

        if query == None:
            return None
        
        user = self._getOneByToken(query[0])
        return user

    
    def queryToObject(self,query):
             
        idUser = query[0]
        email = query[1]
        password = query[2]
        idtoken = query[3]
        mT = DAOManagerMysql()
        token = mT.do(mT.TOKEN, mT.GET_ONE, idtoken)
               
        user = User(email, password, token, idUser)        

        return user 


class MysqlDAOToken(DAO.TokenDAO):

    table = "tokens"    
    
    def __init__(self,connection):
        self.connection=connection 
    
    def create(self,token):  

        try:
            if token.value == '' or token.date is None:
                raise Error('empty fields')
                #print('Error: empty fields')
                return False
        except Error as e:
            print('Error DAOToken create: {}'.format(e))
            return False
            
        self.cursor = self.connection.cursor()        
        datatoken = (token.value, token.date)
        sql = """ INSERT INTO {} (value, date) VALUES(%s,%s);""".format(self.table)    
        
        try: 
            self.cursor.execute(sql, datatoken)
        except Error as e:
            print('Error DAOToken create: {}'.format(e))
            return False

        #self.connection.commit()
        return True
    
    def delete(self,idtoken):
        
        cursor = self.connection.cursor()
        sql = """ DELETE FROM {} WHERE idtokens = '{}';""".format(self.table, idtoken)
        
        try:
            cursor.execute(sql)
            if cursor.rowcount == 0:
                raise Error('no found row, no deleted')
                #print('Error: no found row, no deleted')    
                return False    
        except Error as e:
            print('Error DAOToken delete: {}'.format(e))
            return False
        
        #self.connection.commit()
        return True
    
    def update(self,token):        

        try:
            if token.value == '' or token.date is None:
                raise Error('empty fields')
                #print('Error: empty fields')
                return False
        except Error as e:
            print('Error DAOToken update: {}'.format(e))
            return False        
        
        cursor = self.connection.cursor() 
            
        datatoken = (token.value, token.date)
        sql = """ UPDATE {} SET value=%s, date=%s WHERE idtokens='{}';""".format(self.table,token.id)
        
        try:
            cursor.execute(sql,datatoken)
            if cursor.rowcount == 0:
                raise Error('no found row, no updated3')
                #print('Error: no found row, no updated')    
                return False 
        except Error as e:
            print('Error DAOToken update: {}'.format(e))
            return False               

        return True
    
    
    def getOne(self,idtoken):
        
        cursor = self.connection.cursor()
        sql = """ SELECT * FROM {} WHERE idtokens = '{}';""".format(self.table, idtoken)
        
        try:
            cursor.execute(sql)
        except Error as e:
            print('Error DAOToken getOne: {}'.format(e))            
            return False

        token = None
        query = cursor.fetchone()        

        if query:
            token = self.queryToObject(query)
        else:
            print('Error DAOToken getOne: no found token')
        
        return token
    
    
    def getAll(self,filter):
        
        cursor = self.connection.cursor()
        
        filterWhere = '' if filter == None else 'WHERE {}' 
        
        sql = """ SELECT * FROM {} {};""".format(self.table,filterWhere)
        
        try:
            cursor.execute(sql)
        except Error as e:
            print('Error DAOToken getAll: {}'.format(e))            
            return False

        rows = cursor.fetchall()
        tokens = []
        for row in rows:
            token = self.queryToObject(row)
            tokens.append(token)
        
        return tokens    

    def getLastIdToken(self):
        return self.cursor.lastrowid

    
    def queryToObject(self,query):
        
        idtoken = query[0]
        value = query[1]
        date = query[2]        
        token = Token(value,date,idtoken)       

        return token
    
    

class DAOManagerMysql(DAO.DAOManager):
    """
    DAOManagerSqlite :class manager DAO to sqlite    
    """
    
    __instance = None

    def __new__(cls):
        if DAOManagerMysql.__instance is None:            
            DAOManagerMysql.__instance = object.__new__(cls)            
        return DAOManagerMysql.__instance
    
    daos = None
    conecction = None

    def init(self):
        
        self.daos = {
            0:
                [
                    {
                        'create':super().create,
                        'update':super().update,
                        'delete':super().delete,
                        'getOne':super().getOne,
                        'getAll':super().getAll,
                        'existToken': super().existToken,
                    }
                    ,super().userDAO,MysqlDAOUser
                ],
            1:
                [
                    {
                        'create':super().create,
                        'update':super().update,
                        'delete':super().delete,
                        'getOne':super().getOne,
                        'getAll':super().getAll,                        
                        'lastIdToken': super().getLastIdToken
                    }
                    ,super().tokenDAO,MysqlDAOToken
                ],
        }

        try: 
            config = {
                'host' :'localhost',
                'user' :'root',
                'password' : 'rootmysql2019',
                'database' : 'db_login',
                'port' : "3306"
            }           
            self.conecction = mysql.connector.connect(**config)         
            print("Conexion con exito")            
        except mysql.connector.DatabaseError as error:
            print("Error: No se puede hacer la conexion",error)       
    
    def do(self,daoInt,doThing,objectPrimary=None,*args):
        """
        do :it use a Dao's method
        
        Arguments:
            daoInt {Int} -- identifier dao
                USER = 0               
                
            doThing {String} -- action identifier dao's method
                CREATE = 'create'
                UPDATE = 'update'
                DELETE = 'delete'
                GET_ONE = 'getOne'
                GET_ALL = 'getAll'                
        
        Keyword Arguments:
            objectPrimary {String} -- item as parameter of dao's method (default: {None})
        """  

        if self.daos[daoInt][1] == None:
            self.daos[daoInt][1] = self.daos[daoInt][2](self.conecction)
        
        return self.daos[daoInt][0][doThing](self.daos[daoInt][1],objectPrimary,args)
    
    
    def beginTransaction(self):

        sql = """START TRANSACTION;"""
        cursor = self.conecction.cursor()
        cursor.execute(sql)
        
    
    def endTransaction(self,state):
        cursor = self.conecction.cursor()
        try:     
            if not state:
                raise Error('failled transaction')
            sql = """COMMIT;""" 
            cursor.execute(sql)
            return True
        except Error as e:
            print('Error: {}'.format(e))
            sql = """ROLLBACK;"""            
            cursor.execute(sql)
            return False

        
    
    def commit(self):

        self.conecction.commit()

   
    



        

    

    
