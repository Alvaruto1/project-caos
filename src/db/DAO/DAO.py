import abc

class DAO(metaclass= abc.ABCMeta):

    @abc.abstractmethod
    def create(self,object):
        pass
    
    @abc.abstractmethod
    def delete(self,idObject):
        pass
    
    @abc.abstractmethod
    def update(self,object):
        pass
    
    @abc.abstractmethod
    def getOne(self,idObject):
        pass
    
    @abc.abstractmethod
    def getAll(self):
        pass

    @abc.abstractmethod
    def queryToObject(self,query):
        pass

class UserDAO(DAO, metaclass=abc.ABCMeta):
    pass

class TokenDAO(DAO, metaclass=abc.ABCMeta):
    pass

class DAOManager():

    USER = 0   
    TOKEN = 1 

    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'
    GET_ONE = 'getOne'
    GET_ALL = 'getAll'

    userDAO = None
    tokenDAO = None

    def create(self,dao,objectPrimary,*args):
        return dao.create(objectPrimary)
    
    def update(self,dao,objectPrimary,*args):
        return dao.update(objectPrimary)

    def delete(self,dao,objectPrimary,*args):
        return dao.delete(objectPrimary)
    
    def getOne(self,dao,objectPrimary,*args):
        return dao.getOne(objectPrimary)
    
    def getAll(self,dao,objectPrimary=None,*args):
        return dao.getAll()