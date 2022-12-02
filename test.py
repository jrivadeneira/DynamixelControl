from dynafacade import ServoController
from IKSolver import getThetas
import math

def mapit(theta, maximum, sweepSize):
    maximum /= 2
    motorpos = theta / (sweepSize)
    motorpos = (motorpos * maximum) + maximum
    return motorpos

ctrl = ServoController('COM3')

ctrl.create_servo(1,"Ax18A.conf")
ctrl.create_servo(2,"2xl430w250t.conf")
ctrl.create_servo(3,"2xl430w250t.conf")

ds = ctrl.get_servo(1)
es = ctrl.get_servo(2)
fs = ctrl.get_servo(3)

length0 = 24
length1 = 70
length2 = 182

thetas = getThetas(120, 0, 120, length0, length1, length2, True)
q = [((x/math.pi) * 180) for x in thetas]


servoPositions = [mapit(-x,1024,5 * math.pi / 6) for x in thetas]
mid_servo_position = mapit(-thetas[1],4096,math.pi)
last_servo_position = mapit(thetas[-1],1024,5 * math.pi / 6)
print(mid_servo_position)
print(last_servo_position)

ds.RAM['Torque Enable'].set_value(1)
es.RAM['Torque Enable'].set_value(1)

es.RAM['Goal Position'].set_value(int(mid_servo_position))
ds.RAM['Goal Position'].set_value(int(last_servo_position))

input('say anything: ')
es.RAM['Torque Enable'].set_value(0)
ds.RAM['Torque Enable'].set_value(0)

# print(es.RAM['Hardware Error Status'].get_value())


present_load_packet = es.RAM['Present Load'].get_value()
present_load = present_load_packet[0]
if(present_load >> 15):
    present_load -= (1<<16)
present_load /= 10
print("Present Load:", present_load,'% ::', present_load_packet)

present_input_voltage_packet = es.RAM['Present Input Voltage'].get_value()
present_input_voltage = present_input_voltage_packet[0]/10
print("Present Input Voltage:", present_input_voltage,'V ::', present_input_voltage_packet)

temperature_limit_packet = es.EEPROM['Temperature Limit'].get_value()
temperature_limit = temperature_limit_packet[0]

present_temperature_packet = es.RAM['Present Temperature'].get_value()
present_temperature = present_temperature_packet[0]
print("Present Temperature:", present_temperature, 'C', '/', temperature_limit, 'C ::', present_temperature_packet)


temperature_limit_packet = es.EEPROM['Temperature Limit'].get_value()
temperature_limit = temperature_limit_packet[0]

# print(es.EEPROM['Max Voltage Limit'].get_value())
# print(es.EEPROM['Min Voltage Limit'].get_value())

# print(es.EEPROM['Shutdown'].get_value())


ctrl.disconnect()