from leg import Leg
from dynafacade import ServoController
import time
import math

ctrl = ServoController('COM3')
ctrl.port_handler.setBaudRate(1000000)

# create servos for first three legs
servo1 = ctrl.create_servo(1,"Ax18A.conf")
servo2 = ctrl.create_servo(2,"2xl430w250t.conf")
servo3 = ctrl.create_servo(3,"2xl430w250t.conf")

servo4 = ctrl.create_servo(4,"Ax18A.conf")
servo5 = ctrl.create_servo(5,"2xl430w250t.conf")
servo6 = ctrl.create_servo(6,"2xl430w250t.conf")

servo7 = ctrl.create_servo(7,"Ax18A.conf")
servo8 = ctrl.create_servo(8,"2xl430w250t.conf")
servo9 = ctrl.create_servo(9,"2xl430w250t.conf")

servo16 = ctrl.create_servo(16,"Ax18A.conf")
servo17 = ctrl.create_servo(17,"2xl430w250t.conf")
servo18 = ctrl.create_servo(18,"2xl430w250t.conf")




servos = [servo1, servo2, servo3, servo4, servo5, servo6, servo7, servo8, servo9, servo16, servo17, servo18]

servos_2xl430w250t = [servo2, servo3, servo5, servo6, servo8, servo9, servo17, servo18]

# check servo error status
for each in servos:
    print(each.RAM['Present Position'].get_value())

# get hardware error status for 2xl430w250t servos
for each in servos_2xl430w250t:
    print(each.RAM['Hardware Error Status'].get_value())
    if(each.RAM['Hardware Error Status'].get_value()[2] == 128):
        each.reboot(ctrl.port_handler)


# create lengths for legs
length0 = 24
length1 = 70
length2 = 137


# Create legs
leg = Leg(servo3, servo2, servo1, length0, length1, length2, True, -math.pi/6)
leg2 = Leg(servo6, servo5, servo4, length0, length1, length2, False, -math.pi/6)
leg3 = Leg(servo9, servo8, servo7, length0, length1, length2, True, math.pi/6)
leg6 = Leg(servo18, servo17, servo16, length0, length1, length2, False, math.pi/6)

legs = [leg, leg2, leg3, leg6]
    
def move_group(group, position):
    for eachLeg in group:
        eachLeg.move_to(position)

# create a path for the legs to follow
for eachLeg in legs:
    eachLeg.move_to_home()
time.sleep(1)
n = 96
for eachLeg in legs:
    eachLeg.walk_path = eachLeg.get_walk_paths(n)

# cut the legs into two groups
group1 = [leg, leg3]
group2 = [leg2, leg6]

def take_step():
    for i in range(n):
        for eachLeg in group1:
            eachLeg.move_to(eachLeg.walk_path[i])
        # offset the other group by half of the path
        for eachLeg in group2:
            eachLeg.move_to(eachLeg.walk_path[(i+(n//2))%n])
        # time.sleep(0.0001)
# for i in range(1):
    # take_step()

def wave_gait():
    # wave gait
    # time on ground
    time_on_ground = 0.75
    n = 96
    # calculate paths for each leg using time on ground
    for eachLeg in legs:
        eachLeg.walk_path = eachLeg.get_walk_paths(n, time_on_ground)
    # do not divide the legs into groups 
    for i in range(n):
        for index, eachLeg in enumerate(legs):
            # calculate offset for each leg
            offset = index * (n//4)
            eachLeg.move_to(eachLeg.walk_path[(i + offset)%n])
        
for i in range(10):
    wave_gait()

time.sleep(5)
for eachServo in servos:
    eachServo.RAM['Torque Enable'].set_value(0)

