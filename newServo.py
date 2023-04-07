from dynafacade import ServoController
import time

ctrl = ServoController('COM3')
ctrl.port_handler.setBaudRate(1000000)

# ctrl.create_servo(1,"Ax18A.conf")
# show baud rate
# print(ctrl.get_servo(1).EEPROM['Baud Rate'].get_value())
# set baud rate to 1 (1Mbps)
# ctrl.get_servo(1).EEPROM['Baud Rate'].set_value(1)
# set id to 7
# ctrl.get_servo(1).EEPROM['ID'].set_value(10)

# print(ctrl.get_servo(2).EEPROM['Baud Rate'].get_value())
# ctrl.create_servo(7,"Ax18A.conf")
# ctrl.create_servo(8,"2xl430w250t.conf")
# ctrl.create_servo(9,"2xl430w250t.conf")
n1,n2,n3 = 16,17,18
ctrl.create_servo(n1,"Ax18A.conf")
ctrl.create_servo(n2,"2xl430w250t.conf")
ctrl.create_servo(n3,"2xl430w250t.conf")

# set id's to 7 8 and 9

# show baud rates
print(ctrl.get_servo(n1).EEPROM['Baud Rate'].get_value())
print(ctrl.get_servo(n2).EEPROM['Baud Rate'].get_value())
print(ctrl.get_servo(n3).EEPROM['Baud Rate'].get_value())


# show hardware error status
print(ctrl.get_servo(n2).RAM['Hardware Error Status'].get_value())
print(ctrl.get_servo(n3).RAM['Hardware Error Status'].get_value())
# reboot those servos
ctrl.get_servo(n2).reboot(ctrl.port_handler)
ctrl.get_servo(n3).reboot(ctrl.port_handler)
time.sleep(1)
print(ctrl.get_servo(n2).RAM['Hardware Error Status'].get_value())
print(ctrl.get_servo(n3).RAM['Hardware Error Status'].get_value())
# set ids to 16 17 and 18
# ctrl.get_servo(n1).EEPROM['ID'].set_value(16)
# ctrl.get_servo(n2).EEPROM['ID'].set_value(17)
# ctrl.get_servo(n3).EEPROM['ID'].set_value(18)
# # set baud rate to 3 (1Mbps)
# ctrl.get_servo(n1).EEPROM['Baud Rate'].set_value(1)
# ctrl.get_servo(n2).EEPROM['Baud Rate'].set_value(3)
# ctrl.get_servo(n3).EEPROM['Baud Rate'].set_value(3)
# show baud rates
# print(ctrl.get_servo(1).EEPROM['Baud Rate'].get_value())
# print(ctrl.get_servo(5).EEPROM['Baud Rate'].get_value())
# print(ctrl.get_servo(6).EEPROM['Baud Rate'].get_value())
# # set port handler baud rate to 1Mbps
# ctrl.port_handler.setBaudRate(1000000)
# # reboot servos
# ctrl.get_servo(1).reboot(ctrl.port_handler)
# ctrl.get_servo(2).reboot(ctrl.port_handler)
# time.sleep(1)
# # set id's to 8 and 9
# ctrl.get_servo(11).EEPROM['ID'].set_value(1)
# ctrl.get_servo(12).EEPROM['ID'].set_value(2)
# get servo status
# print(ctrl.get_servo(1).RAM['Hardware Error Status'].get_value())
# print(ctrl.get_servo(2).RAM['Hardware Error Status'].get_value())
# ctrl.create_servo(1,"2xl430w250t.conf")
# ctrl.create_servo(2,"2xl430w250t.conf")
# set the servo ids to 8 and 9
# ctrl.get_servo(1).EEPROM['ID'].set_value(11)
# ctrl.get_servo(2).EEPROM['ID'].set_value(12)