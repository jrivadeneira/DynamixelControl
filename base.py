from dynafacade import ServoController
from leg import Leg
ctrl = ServoController('COM3')
# Base for a six-legged robot

# Create servos 1 through 18
def create_servos():
    ctrl.create_servo(1,"Ax18A.conf")
    ctrl.create_servo(2,"2xl430w250t.conf")
    ctrl.create_servo(3,"2xl430w250t.conf")
    ctrl.create_servo(4,"Ax18A.conf")
    ctrl.create_servo(5,"2xl430w250t.conf")
    ctrl.create_servo(6,"2xl430w250t.conf")
    ctrl.create_servo(7,"Ax18A.conf")
    ctrl.create_servo(8,"2xl430w250t.conf")
    ctrl.create_servo(9,"2xl430w250t.conf")
    ctrl.create_servo(10,"Ax18A.conf")
    ctrl.create_servo(11,"2xl430w250t.conf")
    ctrl.create_servo(12,"2xl430w250t.conf")
    ctrl.create_servo(13,"Ax18A.conf")
    ctrl.create_servo(14,"2xl430w250t.conf")
    ctrl.create_servo(15,"2xl430w250t.conf")
    ctrl.create_servo(16,"Ax18A.conf")
    ctrl.create_servo(17,"2xl430w250t.conf")
    ctrl.create_servo(18,"2xl430w250t.conf")

# Create 6 legs
def create_legs():
    leg1 = Leg(ctrl=ctrl, id1=1, id2=2, id3=3, length0=24, length1=70, length2=182, y_negate=False)
    leg2 = Leg(ctrl=ctrl, id1=4, id2=5, id3=6, length0=24, length1=70, length2=182, y_negate=False)
    leg3 = Leg(ctrl=ctrl, id1=7, id2=8, id3=9, length0=24, length1=70, length2=182, y_negate=False)
    leg4 = Leg(ctrl=ctrl, id1=10, id2=11, id3=12, length0=24, length1=70, length2=182, y_negate=True)
    leg5 = Leg(ctrl=ctrl, id1=13, id2=14, id3=15, length0=24, length1=70, length2=182, y_negate=True)
    leg6 = Leg(ctrl=ctrl, id1=16, id2=17, id3=18, length0=24, length1=70, length2=182, y_negate=True)
    legs = [leg1, leg2, leg3, leg4, leg5, leg6]
    return legs
create_servos()
legs = create_legs()


def main():
    for leg in legs:
        leg.move(50, 0, 50)

def home_position():
    # move all legs to home position
    # leg 1, 3, 5 move up and home (x, y, z) = (50, 0, 100)
    for leg in legs[::2]:
        leg.move(50, 0, 100)
    # leg 1, 3, 5 move down (x, y, z) = (50, 0, 50)
    for leg in legs[::2]:
        leg.move(50, 0, 50)
    # leg 2, 4, 6 move up and home (x, y, z) = (50, 0, 100)
    for leg in legs[1::2]:
        leg.move(50, 0, 100)
    # leg 2, 4, 6 move down (x, y, z) = (50, 0, 50)
    for leg in legs[1::2]:
        leg.move(50, 0, 50)

def walk():
    # tripod gait for 6 legs
    # leg 1, 3, 5 move up and forward at the same time (x, y, z) = (50, 50, 100)
    for leg in legs[::2]:
        leg.move(50, 50, 100)
    # leg 2, 4, 6 move forward (x, y, z) = (50, -50, 50)
    for leg in legs[1::2]:
        leg.move(50, -50, 50)
    # leg 1, 3, 5 move down (x, y, z) = (50, 50, 50)
    for leg in legs[::2]:
        leg.move(50, 50, 50)
    # leg 2, 4, 6 move up and forward at the same time (x, y, z) = (50, 50, 100)
    for leg in legs[1::2]:
        leg.move(50, 50, 100)
    # leg 1, 3, 5 move forward (x, y, z) = (50, -50, 50)
    for leg in legs[::2]:
        leg.move(50, -50, 50)
    # leg 2, 4, 6 move down (x, y, z) = (50, 50, 50)
    for leg in legs[1::2]:
        leg.move(50, 50, 50)
    

