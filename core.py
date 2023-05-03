from leg import Leg
from dynafacade import ServoController
import time
import math

ctrl = ServoController('/dev/cu.usbserial-1410')
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

servo10 = ctrl.create_servo(10,"Ax18A.conf")
servo11 = ctrl.create_servo(11,"2xl430w250t.conf")
servo12 = ctrl.create_servo(12,"2xl430w250t.conf")

servo13 = ctrl.create_servo(13,"Ax18A.conf")
servo14 = ctrl.create_servo(15,"2xl430w250t.conf")
servo15 = ctrl.create_servo(14,"2xl430w250t.conf")

servo16 = ctrl.create_servo(16,"Ax18A.conf")
servo17 = ctrl.create_servo(17,"2xl430w250t.conf")
servo18 = ctrl.create_servo(18,"2xl430w250t.conf")

servos = [servo1, servo2, servo3, servo4, servo5, servo6, servo7, servo8, servo9, servo10, servo11, servo12, servo13, servo14, servo15, servo16, servo17, servo18]
servos_2xl430w250t = [servo2, servo3, servo5, servo6, servo8, servo9, servo11, servo12, servo14, servo15, servo17, servo18]

# for each in servos:
    # print(each.RAM['Present Position'].get_value())

# get hardware error status for 2xl430w250t servos
for each in servos_2xl430w250t:
    print(each.RAM['Hardware Error Status'].get_value())
    if(each.RAM['Hardware Error Status'].get_value()[2] in [128, 33]):
        each.reboot(ctrl.port_handler)


# create lengths for legs
length0 = 24
length1 = 70
length2 = 137

# create leg parameters
leg_params = [False, math.pi/6]
leg2_params = [False, 0]
leg3_params = [False, -math.pi/6]
leg4_params = [True, math.pi/6]
leg5_params = [True, 0]
leg6_params = [True, -math.pi/6]

# Create legs
leg = Leg(servo3, servo2, servo1, length0, length1, length2, leg_params[0], leg_params[1])
leg2 = Leg(servo6, servo5, servo4, length0, length1, length2, leg6_params[0], leg6_params[1])
leg3 = Leg(servo9, servo8, servo7, length0, length1, length2, leg5_params[0], leg5_params[1])
leg4 = Leg(servo12, servo11, servo10, length0, length1, length2, leg4_params[0], leg4_params[1])
leg5 = Leg(servo15, servo14, servo13, length0, length1, length2, leg3_params[0], leg3_params[1])
leg6 = Leg(servo18, servo17, servo16, length0, length1, length2, leg2_params[0], leg2_params[1])

legs = [leg, leg6, leg5, leg4, leg2, leg3]

def move_group(group, position):
    for eachLeg in group:
        eachLeg.move_to(position)

# create a path for the legs to follow
for eachLeg in legs:
    eachLeg.move_to_home()
time.sleep(1)
n = 100
for eachLeg in legs:
    eachLeg.walk_path = eachLeg.get_walk_paths(n)

def wave_gait():
    # wave gait
    # time on ground
    time_on_ground = .8
    n = 36
    # calculate paths for each leg using time on ground
    for eachLeg in legs:
        eachLeg.walk_path = eachLeg.get_walk_paths(n, time_on_ground)
    # do not divide the legs into groups 
    n=len(leg.walk_path)
    for i in range(n):
        for index, eachLeg in enumerate(legs):
            # calculate offset for each leg
            offset = index * (n//6)
            print((i + offset)%n,' / ', len(eachLeg.walk_path))
            eachLeg.move_to(eachLeg.walk_path[(i + offset)%n])

def ripple_gait():
    # ripple gait
    # time on ground
    time_on_ground = .5
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

def bi_gait():
    # tri gait
    # time on ground
    time_on_ground = .35

    n = 24
    # calculate paths for each leg using time on ground
    for eachLeg in legs:
        eachLeg.walk_path = eachLeg.get_walk_paths(n, time_on_ground)
    # divide the legs on diagonal groups
    group1 = [leg, leg4]
    group2 = [leg2, leg6]
    group3 = [leg3, leg5]
    n=len(leg.walk_path)
    # offset by 50% of the path
    for i in range(n):
        for index, eachLeg in enumerate(group1):
            # calculate offset for each leg
            offset = 0
            eachLeg.move_to(eachLeg.walk_path[(i + offset)%n])
        for index, eachLeg in enumerate(group2):
            # calculate offset for each leg
            offset = 0
            eachLeg.move_to(eachLeg.walk_path[(i + offset + (n//3))%n])
        for index, eachLeg in enumerate(group3):
            # calculate offset for each leg
            offset = 0
            eachLeg.move_to(eachLeg.walk_path[(i + offset + ((n//3)*2))%n])
        print(i)

def tri_gait(theta = 0):
    # time on ground 75%
    time_on_ground = .60
    n = 24
    # calculate paths for each leg using time on ground
    for eachLeg in legs:
        eachLeg.walk_path = eachLeg.get_walk_paths(n, time_on_ground, theta)
    # divide the legs into two groups
    group1 = [leg, leg5, leg2]
    group2 = [leg3, leg6, leg4]
    n = len(leg.walk_path)
    # offset by 50% of the path
    for i in range(n):
        for index, eachLeg in enumerate(group1):
            # calculate offset for each leg
            offset = 0
            eachLeg.move_to(eachLeg.walk_path[(i + offset)%n])
        for index, eachLeg in enumerate(group2):
            # calculate offset for each leg
            offset = n//2
            eachLeg.move_to(eachLeg.walk_path[(i + offset)%n])

def rotate_body():
    # Divide legs into two groups
    group1 = [leg, leg5, leg2]
    group2 = [leg3, leg6, leg4]
    # move group 1 to raised position
    time_on_ground = .52
    n = 48
    for eachleg in legs:
        eachleg.turn_path = eachleg.get_turn_paths(n, time_on_ground, True)
    
    for i in range(n):
        for index, eachLeg in enumerate(group1):
            # calculate offset for each leg
            offset = 0
            eachLeg.move_to(eachLeg.turn_path[(i + offset)%n])
        for index, eachLeg in enumerate(group2):
            # calculate offset for each leg
            offset = n//2
            eachLeg.move_to(eachLeg.turn_path[(i + offset)%n])




# for i in range(3):
    # tri_gait()

# for i in range(1):
    # rotate_body()

# Move leg 1 in a circle
# leg.move_to(leg.get_raised_position())
# path = leg.get_walk_paths(100, .5, math.pi)
# for eachPoint in path:
    # leg.move_to(eachPoint)
    # print(eachPoint)
    # time.sleep(.01)

# for i in range (2):
    # tri_gait(0)
# 

for i in range(2):
    tri_gait(math.pi/2)

for eachLeg in legs:
    eachLeg.move_to_home()
# aleg= leg3
# aleg.move_to(aleg.get_raised_position())



print('say anything to exit')
cmd = input()
if(cmd == 'exit'):
    for eachServo in servos:
        eachServo.RAM['Torque Enable'].set_value(0)
