from dynafacade import ServoController
ctrl = ServoController('COM4')

ctrl.create_servo(1,"Ax18A.conf")
ctrl.create_servo(2,"2xl430w250t.conf")
ctrl.create_servo(3,"2xl430w250t.conf")

ds = ctrl.get_servo(1)
es = ctrl.get_servo(2)
fs = ctrl.get_servo(3)

ds.RAM['Torque Enable'].set_value(1)
ds.RAM['Goal Position'].set_value(512+256 + 128)
input('say anything: ')
ds.RAM['Torque Enable'].set_value(0)

es.RAM['Torque Enable'].set_value(1)
es.RAM['Goal Position'].set_value(2048 + 512)
input('say anything: ')
es.RAM['Torque Enable'].set_value(0)

fs.RAM['Torque Enable'].set_value(1)
fs.RAM['Goal Position'].set_value(2048)
input('say anything: ')
fs.RAM['Torque Enable'].set_value(0)

ctrl.disconnect()