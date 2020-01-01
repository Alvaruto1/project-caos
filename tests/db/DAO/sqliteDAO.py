import os,sqlite3, datetime
from flask import current_app
import FlaskBootMDL.src.db.DAO.DAO as DAO
from sqlite3 import Error
from FlaskBootMDL.src.webapp.models.user import User

class SqliteDAOUser(DAO.UserDAO):

    table = "User"
    columns = ['']
    
    def __init__(self,connection):
        self.connection=connection 
    
    def create(self,user):       

        try:
            birthDate = datetime.datetime.strptime(user.birthDate, '%d/%m/%y')
        except (ValueError, AttributeError) as e:
            print('Error: {}'.format(e))
            return False

        try:
            if user.name == '' or user.lastName == '' or user.email == '':
                raise Error('empty fields')
                #print('Error: empty fields')
                return False
        except Error as e:
            print('Error: {}'.format(e))
            raise Exception('error')
            
        cursor = self.connection.cursor()        
        dataUser = (user.name, user.lastName, birthDate, user.email)
        sql = """ INSERT INTO {} (name, lastName, birthDate, email) VALUES(?,?,?,?);""".format(self.table)    
        
        try: 
            cursor.execute(sql, dataUser)
        except Error as e:
            print('Error: {}'.format(e))
            return False

        #self.connection.commit()
        return True
    
    def delete(self,idUser):
        
        cursor = self.connection.cursor()
        sql = """ DELETE FROM {} WHERE id = '{}';""".format(self.table, idUser)
        
        try:
            cursor.execute(sql)
            if cursor.rowcount == 0:
                raise Error('no found row, no deleted')
                #print('Error: no found row, no deleted')    
                return False    
        except Error as e:
            print('Error: {}'.format(e))
            return False
        
        #self.connection.commit()
        return True
    
    def update(self,user):

        try:
            birthDate = datetime.datetime.strptime(user.birthDate, '%d/%m/%y')
        except (ValueError, AttributeError) as e:
            print('Error: {}'.format(e))
            return False

        try:
            if user.name == '' or user.lastName == '' or user.email == '':
                raise Error('empty fields')
                #print('Error: empty fields')
                return False
        except Error as e:
            print('Error: {}'.format(e))
            return False        
        
        cursor = self.connection.cursor()
        dataUser = (user.name, user.lastName, birthDate, user.email, user.id)
        sql = """ UPDATE {} SET name=?, lastName=?, birthDate=?, email=? WHERE id=?;""".format(self.table)

        try:
            cursor.execute(sql,dataUser)
            if cursor.rowcount == 0:
                raise Error(' no found row, no updated3')
                #print('Error: no found row, no updated')    
                return False 
        except Error as e:
            print('Error: {}'.format(e))
            return False               

        return True
    
    
    def getOne(self,idUser):
        
        cursor = self.connection.cursor()
        sql = """ SELECT * FROM {} WHERE id = '{}';""".format(self.table, idUser)
        
        try:
            cursor.execute(sql)
        except Error as e:
            print('Error: {}'.format(e))            
            return False

        user = None
        query = cursor.fetchone()        

        if query:
            user = self.queryToObject(query)
        else:
            print('Error: no found user')
        
        return user
    
    
    def getAll(self):
        
        cursor = self.connection.cursor()
        sql = """ SELECT * FROM {};""".format(self.table)
        
        try:
            cursor.execute(sql)
        except Error as e:
            print('Error: {}'.format(e))            
            return False

        rows = cursor.fetchall()
        users = []
        for row in rows:
            user = self.queryToObject(row)
            users.append(user)
        
        return users

    
    def queryToObject(self,query):
        
        idUser = query[0]
        name = query[1]
        lastName = query[2]
        birthDate = query[3]
        email = query[4]
        user = User(name,lastName,birthDate,email)
        user.id = idUser

        return user 


    
    

class DAOManagerSqlite(DAO.DAOManager):
    """
    DAOManagerSqlite :class manager DAO to sqlite    
    """
    daos = None
    conecction = None

    def __init__(self):
        
        self.daos = {
            0:
                [
                    {
                        'create':super().create,
                        'update':super().update,
                        'delete':super().delete,
                        'getOne':super().getOne,
                        'getAll':super().getAll
                    }
                    ,super().userDAO,SqliteDAOUser
                ],
        }

        try:            
            self.conecction = sqlite3.connect('dataBase.db')            
            print("Conexion con exito")            
        except sqlite3.DatabaseError as error:
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

        sql = """BEGIN TRANSACTION;"""
        cursor = self.conecction.cursor()
        cursor.execute(sql)
        
    
    def endTransaction(self,state):
        cursor = self.conecction.cursor()
        try:           
            if not state:
                raise Error('problem query')
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

   
    



        

    

    
