from leg import Leg
from dynafacade import ServoController
import time
import math

ctrl = ServoController('COM4')
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

def gait_prepare():
    pass

def gait_complete():
    n = 24
    group1 = [leg, leg5, leg2]
    group2 = [leg3, leg6, leg4]
    for eachLeg in legs:
        eachLeg.current_path = eachLeg.get_path_to_home(n, True)
    for i in range(n):
        for eachLeg in group1:
            eachLeg.move_to(eachLeg.current_path[i])
    for i in range(n):
        for eachLeg in group2:
            eachLeg.move_to(eachLeg.current_path[i])

def prepare_bi_gait_paths(steps = 24, time_on_ground = .35, theta = 0):
    bi_legs = [leg, leg4, leg2, leg6, leg3, leg5]
    for index, eachLeg in enumerate(bi_legs):
        eachLeg.current_path = eachLeg.get_walk_paths(steps, time_on_ground, theta)
        offset = (index//2) * (steps//3)
        eachLeg.current_path = eachLeg.current_path[-offset:] + eachLeg.current_path[:-offset]

def prepare_ripple_gait_paths(steps = 24, time_on_ground = 5/6, theta = 0):
    for index, eachLeg in enumerate(legs):
        # calculate offset for each leg
        eachLeg.current_path = eachLeg.get_walk_paths(steps, time_on_ground, theta)
        offset = (index * (steps//4)) % steps
        eachLeg.current_path = eachLeg.current_path[-offset:] + eachLeg.current_path[:-offset]

def prepare_wave_gait_paths(steps=24, time_on_ground=.85, theta=0):
    for i,eachLeg in enumerate(legs):
        eachLeg.current_path = eachLeg.get_walk_paths(steps, time_on_ground, theta)
        # set the offset here
        offset = (steps//6) * i
        eachLeg.current_path = eachLeg.current_path[-offset:] + eachLeg.current_path[:-offset]

def prepare_tri_gait_paths(steps = 24, time_on_ground=.75, theta=0):
    for eachLeg in legs:
        eachLeg.walk_path = eachLeg.get_walk_paths(steps, time_on_ground, theta)
    # divide the legs into two groups
    group1 = [leg, leg5, leg2]
    group2 = [leg3, leg6, leg4]
    n = len(leg.walk_path)
    # offset by 50% of the path
    offset = n//2
    for eachLeg in group1:
        eachLeg.current_path = eachLeg.walk_path
    for eachLeg in group2:
        eachLeg.current_path = eachLeg.walk_path[-offset:] + eachLeg.walk_path[:-offset]
    
def start_motion(theta = 0, time_on_ground=0.55, steps = 12):
    group1 = [leg, leg5, leg2]
    group2 = [leg3, leg6, leg4]
    # generate halfstep paths
    for eachLeg in group1:
        eachLeg.to_path_start = eachLeg.calculate_to_current_path_start(steps, True)
    for eachLeg in group2:
        eachLeg.to_path_start = eachLeg.calculate_to_current_path_start(steps, False)
    for i in range(steps):
        for eachLeg in legs:
            eachLeg.move_to(eachLeg.to_path_start[i])

def move_legs(theta = 0):
    n = len(legs[0].current_path)
    # Run each leg through it's paths. 
    for i in range(n):
        for eachLeg in legs:
            eachLeg.move_to(eachLeg.current_path[i])
        
def rotate_body(left=False):
    # Divide legs into two groups
    group2 = [leg3, leg6, leg4]
    # move group 1 to raised position
    time_on_ground = .55
    n = 24
    offset = n//2
    for eachleg in legs:
        eachleg.current_path = eachleg.get_turn_paths(n, time_on_ground, left)
    for eachleg in group2:
        eachleg.current_path = eachleg.current_path[-offset:] + eachleg.current_path[:-offset]

def walk_forwards(x=5):
    start_motion()
    for i in range(x):
        move_legs()
    gait_complete()

def walk_backwards(x=5):
    start_motion(theta=math.pi)
    for i in range(x):
        move_legs(theta=math.pi)
    gait_complete()

def strafe_left(x=5):
    start_motion(theta=math.pi/2)
    for i in range(x):
        move_legs(theta=math.pi/2)
    gait_complete()

def strafe_right(x=5):
    start_motion(theta=-math.pi/2)
    for i in range(x):
        move_legs(theta=-math.pi/2)
    gait_complete()

n = 16
for eachLeg in legs:
    eachLeg.current_path = eachLeg.get_path_to_home(n, True)

for i in range(n):
    for eachLeg in legs:
        eachLeg.move_to(eachLeg.current_path[i])
time.sleep(1)
# Experiment zone

# prepare_tri_gait_paths()
# start_tri_gait(theta=math.pi)
# # time.sleep(1)

# for i in range(4):
#     tri_gait(theta=math.pi)
# gait_complete()
# walk_forwards()
# strafe_right()
# strafe_left()
# rotate_body()
# prepare_tri_gait_paths()
prepare_bi_gait_paths()
start_motion()
for i in range(3):
    move_legs()
gait_complete()

# Cleanup zone
time.sleep(1)
# Get the raise path for each leg
for eachLeg in legs:
    eachLeg.current_path = eachLeg.calculate_to_rest_path(n)

for i in range(n):
    for eachLeg in legs:
        eachLeg.move_to(eachLeg.current_path[i])

for eachServo in servos:
    eachServo.RAM['Torque Enable'].set_value(0)
