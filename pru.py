from src.utils.temp_toke import PerpetualTimer
import time

def suma(a,b,c):
    print(a+b+c)

def prueba(*alvaro):
    print(alvaro)
    suma(*alvaro)
#prueba(1,3,4)

p = PerpetualTimer()

p.setTime(2)
p.init()
p.setFunction(prueba,1,3,4)
p.start()
time.sleep(3)
p.setFunction(prueba,1,8,4)
p.start()

