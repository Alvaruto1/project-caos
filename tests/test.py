import unittest, datetime
from flask import json
from functools import reduce
from tests.db.DAO.mysqlDAO import DAOManagerMysql
from tests.db.DAO.DAO import DAOManager
from tests.webapp.models.user import User
from tests.webapp.models.token import Token
from tests.db.db import create_tables
from tests.core.web import app, render_view
from tests.webapp.controllers import *
from tests.utils.temp_toke import PerpetualTimer


class ViewsTestCase(unittest.TestCase):

    def setUp(self):        
        
        app.testing = True
        app.secret_key = 'testing_key'
        self.app = app.test_client(use_cookies=True)

        p = PerpetualTimer()
        p.setTime(10)          
        self.daoManager = DAOManagerMysql()
        self.daoManager.init()
        

        create_tables(self.daoManager.conecction.cursor(),'tests/db/schemas/db_login.sql')
        self.daoManager.commit() 
              
        

    def test_register_view(self):        
        
        # no inico de sesion
        res = self.app.get('/register',follow_redirects=True)
        self.assertEqual(res.status_code,200)
        self.assertIn('Registrarse',str(res.data))
        

        # register user
        data = {
            'username':'userRegisterTest',
            'password':'pas124'
        }
        res = self.app.post('/register',follow_redirects=True,data=data)
        self.assertEqual(res.status_code,200)
        self.assertIn('<td>userRegisterTest</td>',str(res.data))
    


    def test_sign_in_view(self):        
        
        # no inico de sesion
        res = self.app.get('/sign_in',follow_redirects=True)
        self.assertEqual(res.status_code,200)
        self.assertIn('<h4 class="col s12 center-align">Inicio Sesi',str(res.data))


        # register user
        data = {
            'username':'alvaruto18@gmail.com',
            'password':'123456'
        }        
        res = self.app.post('/sign_in',follow_redirects=True,data=data)
        self.assertEqual(res.status_code,200)
        self.assertIn('<td>alvaruto18@gmail.com</td>',str(res.data))



    def test_edit_view(self):        
        
        # no inico de sesion
        res = self.app.get('/edit',follow_redirects=True)
        self.assertEqual(res.status_code,200)
        self.assertIn('<h4 class="col s12 center-align">Inicio Sesi',str(res.data))


        # edit views
        self.app.set_cookie('127.0.0.1','token','7688377309094510949')
        
        res = self.app.get('/edit',follow_redirects=True)
        self.assertEqual(res.status_code,200)
        self.assertIn('<h4 class="offset-s3 col s6 center-align">Edit user</h4>',str(res.data))



    def test_edited_view(self):        
        
        # no inico de sesion
        res = self.app.get('/edited',follow_redirects=True)
        self.assertEqual(res.status_code,200)
        self.assertIn('<h4 class="col s12 center-align">Inicio Sesi',str(res.data))

        # edit user
        self.app.set_cookie('127.0.0.1','token','7688377309094510949')
        data = {
            'username':'alvaruto5@gmail.com',
            'password':'abcd'
        } 
        res = self.app.post('/edited',follow_redirects=True,data=data)
        self.assertEqual(res.status_code,200)
        self.assertIn('<td>alvaruto5@gmail.com</td>',str(res.data)) 



    def test_search_view(self):        
        
        # no inico de sesion
        res = self.app.get('/search',follow_redirects=True)
        self.assertEqual(res.status_code,200)
        self.assertIn('<h4 class="col s12 center-align">Inicio Sesi',str(res.data))

        # search
        self.app.set_cookie('127.0.0.1','token','7688377309094510949')
        search = 'gmail'
        data = {
            'search':search,
        } 
        res = self.app.get('/search',follow_redirects=True,query_string=data)
        
        data = json.loads(res.data)        
        self.assertEqual(res.status_code,200)

        for u in data:
           self.assertIn(search,u['email'])

          

    
    def tearDown(self):

        self.daoManager.conecction.close()

class UserTestCase(unittest.TestCase):

    def setUp(self):
              
        self.daoManager = DAOManagerMysql()
        self.daoManager.init()        
        create_tables(self.daoManager.conecction.cursor(),'tests/db/schemas/db_login.sql')
        self.daoManager.commit()        
        

    def test_user_creation(self):        
        
        # is nice 
        token = Token('token3',datetime.datetime.now(),'0')
        user = User('al@gmail.com','12345',token,'0')
        res = self.daoManager.do(DAOManager.USER, DAOManager.CREATE,user)
        self.daoManager.commit()
        self.assertTrue(res)

        # no empty fields 
        token = Token('token2',datetime.datetime.now(),'0')
        user = User('','',token,'0')
        res = self.daoManager.do(DAOManager.USER, DAOManager.CREATE,user)
        self.daoManager.commit()
        self.assertFalse(res)

        # user equal None 
        user = None
        res = self.daoManager.do(DAOManager.USER, DAOManager.CREATE,user)
        self.daoManager.commit()
        self.assertFalse(res)

    
    def test_user_deletion(self):
        
        # is nice
        res = self.daoManager.do(DAOManager.USER,DAOManager.DELETE,9)        
        self.daoManager.commit()
        self.assertTrue(res)

        # delete a row where id out range
        res = self.daoManager.do(DAOManager.USER,DAOManager.DELETE,2000)
        self.daoManager.commit()
        self.assertFalse(res)        

        # delete a row where id is not correctly
        res = self.daoManager.do(DAOManager.USER,DAOManager.DELETE,'borrar')
        self.daoManager.commit()
        self.assertFalse(res)

    def test_user_update(self):       

        # is nice 
        token = Token('token2Update',datetime.datetime.now(),58)
        userUpdate = User('andres','pas23',token,58)        
        res = self.daoManager.do(DAOManager.USER, DAOManager.UPDATE,userUpdate)
        self.daoManager.commit()
        self.assertTrue(res)

        # no empty fields 
        token = Token('token2Update',datetime.datetime.now(),58)
        userUpdate = User('','',token,58)        
        res = self.daoManager.do(DAOManager.USER, DAOManager.UPDATE,userUpdate)
        self.daoManager.commit()
        self.assertFalse(res)

        # user equal None 
        userUpdate = None        
        res = self.daoManager.do(DAOManager.USER, DAOManager.UPDATE,userUpdate)
        self.daoManager.commit()
        self.assertFalse(res)

        # update a row where id out range
        token = Token('token2Update',datetime.datetime.now(),70)
        userUpdate = User('lizeth','pas123',token,70)
        res = self.daoManager.do(DAOManager.USER, DAOManager.UPDATE,userUpdate)
        self.daoManager.commit()
        self.assertFalse(res)

        # update a row where id is not correctly
        token = Token('token2Update',datetime.datetime.now(),'no')
        userUpdate = User('','',token,'no')
        res = self.daoManager.do(DAOManager.USER, DAOManager.UPDATE,userUpdate)
        self.daoManager.commit()
        self.assertFalse(res)


    def test_user_get_one(self):

        # is nice
        email = 'liz@gmasil.com'
        userGet = self.daoManager.do(DAOManager.USER, DAOManager.GET_ONE,email)
        self.assertIsInstance(userGet, User)

        # id no found
        idUser = 2000
        userGet = self.daoManager.do(DAOManager.USER, DAOManager.GET_ONE,idUser)
        self.assertIsNone(userGet, User)        

        idUser = 'no'
        userGet = self.daoManager.do(DAOManager.USER, DAOManager.GET_ONE,idUser)
        self.assertIsNone(userGet, User)
    
    
    def test_user_get_all(self):        
           
        usersGet = self.daoManager.do(DAOManager.USER, DAOManager.GET_ALL)
        self.assertIsInstance(usersGet, list)

        # number users should be equal 18
        usersGet = self.daoManager.do(DAOManager.USER, DAOManager.GET_ALL)
        self.assertEqual(len(usersGet),18)

    
    def test_user_get_filter(self):        
        
        filt='gmail'
        usersGet = self.daoManager.do(DAOManager.USER, DAOManager.GET_ALL,filt)        
        self.assertNotEqual(len(usersGet),0)
        self.assertIsInstance(usersGet, list)

        # no user found with this filter
        filt='gmailcolombia'
        usersGet = self.daoManager.do(DAOManager.USER, DAOManager.GET_ALL,filt)        
        self.assertEqual(len(usersGet),0)
        

    
    def test_user_transaction(self):
        
        # is nice
        self.daoManager.beginTransaction()
        
        token = Token('token3',datetime.datetime.now(),'0')
        user = User('al@gmail.com','12345',token,'0')
        res = self.daoManager.do(DAOManager.USER, DAOManager.CREATE,user)
        
        res1 = self.daoManager.endTransaction(res)

        self.assertTrue(res1)

        # user empty
        self.daoManager.beginTransaction()
        
        token = Token('token3',datetime.datetime.now(),'0')
        user = User('','',token,'0')
        res = self.daoManager.do(DAOManager.USER, DAOManager.CREATE,user)
        
        res1 = self.daoManager.endTransaction(res)

        self.assertFalse(res1)

        # token empty incomplete
        self.daoManager.beginTransaction()
        
        token = Token('',datetime.datetime.now(),'0')
        user = User('','',token,'0')
        res = self.daoManager.do(DAOManager.USER, DAOManager.CREATE,user)
        
        res1 = self.daoManager.endTransaction(res)

        self.assertFalse(res1)
        

        
    def tearDown(self):

        self.daoManager.conecction.close()

if __name__ == "__main__":
    unittest.main()
    