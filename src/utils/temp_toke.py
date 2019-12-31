from threading import Timer,Thread,Event


# clase que ejecuta una funcion cada cierto tiempo
class PerpetualTimer(object):

    __instance = None
    thread = None
    params = None    

    def __new__(cls):
        if PerpetualTimer.__instance is None:            
            PerpetualTimer.__instance = object.__new__(cls)            
        return PerpetualTimer.__instance

    def init(self):
        self.thread = Timer(self.t,self._handleFunction)
        print('inica'*8)
        
    def setTime(self, time):
        self.t= time

    # anexar funcion qeu sera ejecutada
    def setFunction(self, hFunction, *params):               
        self.hFunction = hFunction 
        self.params = params
           
        
    # ciclo infinito de hilo de ejecucio
    def _handleFunction(self):            
        self.hFunction(*self.params)
        self.thread = Timer(self.t,self._handleFunction)
        self.thread.start() 

    # inicio de ciclo
    def start(self):        
        self.init()                  
        self.thread.start()

    def cancel(self):
        self.thread.cancel()
