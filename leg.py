from IKSolver import getThetas, mapit, calculate_line_points, calculate_bezier_points
import math
class Leg:

    def __init__(self, servo1, servo2, servo3, length0, length1, length2, y_negate, theta1_offset = 0):
        self.servo1 = servo1
        self.servo2 = servo2
        self.servo3 = servo3
        self.length0 = length0
        self.length1 = length1
        self.length2 = length2
        self.y_negate = y_negate
        self.walk_paths = None
        self.turn_paths = None
        self.theta1_offset = theta1_offset 
        self.servo1.RAM['Torque Enable'].set_value(1)
        self.servo2.RAM['Torque Enable'].set_value(1)
        self.servo3.RAM['Torque Enable'].set_value(1)
        
    '''
    first_servo_position = mapit(thetas[0],4096,math.pi)
    mid_servo_position = mapit(-thetas[1],4096,math.pi)
    last_servo_position = mapit(thetas[-1],1024,5 * math.pi / 6)
    '''
    def move(self, x, y, z):
        thetas = getThetas(x, y, z, self.length0, self.length1, self.length2, self.y_negate, self.theta1_offset)
        # convert thetas to servo positions
        servo1_pos = mapit(thetas[0],4096, math.pi)
        servo2_pos = mapit(-thetas[1],4096, math.pi)
        servo3_pos = mapit(thetas[-1],1024, math.radians(150))
        # set the servo positions
        self.servo3.RAM['Goal Position'].set_value(servo3_pos)
        self.servo2.RAM['Goal Position'].set_value(servo2_pos)
        self.servo1.RAM['Goal Position'].set_value(servo1_pos)
        self.current_pos = (x, y, z)
        
    def move_to(self, xyz):
        self.move(xyz[0], xyz[1], xyz[2])

    def moveBy(self, x, y, z):
        self.move(self.current_pos[0] + x, self.current_pos[1] + y, self.current_pos[2] + z)

    def stop(self):
        self.servo1.RAM['Torque Enable'].set_value(0)
        self.servo2.RAM['Torque Enable'].set_value(0)
        self.servo3.RAM['Torque Enable'].set_value(0)

    def start(self):
        self.servo1.RAM['Torque Enable'].set_value(1)
        self.servo2.RAM['Torque Enable'].set_value(1)
        self.servo3.RAM['Torque Enable'].set_value(1)

    def setSpeed(self, speed):
        self.servo1.RAM['Moving Speed'].set_value(speed)
        self.servo2.RAM['Moving Speed'].set_value(speed)
        self.servo3.RAM['Moving Speed'].set_value(speed)
    
    def move_to_home(self):
        xyz = (100, 0, 100)
        if(self.y_negate):
            xyz = self.rotate(xyz, self.theta1_offset)
        else:
            xyz = self.rotate(xyz, -self.theta1_offset)
        self.move(xyz[0], xyz[1], xyz[2])

    def get_home_position(self):
        xyz = (100, 0, 100)
        if(self.y_negate):
            xyz = self.rotate(xyz, self.theta1_offset)
        else:
            xyz = self.rotate(xyz, -self.theta1_offset)
        return xyz
    
    def get_raised_position(self):
        xyz = self.get_home_position()
        return (xyz[0], xyz[1], xyz[2] - 200)
    
    def get_forward_position(self):
        xyz = self.get_home_position()
        return (xyz[0], xyz[1] + 45, xyz[2])
    
    def get_backward_position(self):
        xyz = self.get_home_position()
        return (xyz[0], xyz[1] - 45, xyz[2])

    def rotate(self, xyz, theta):
        x = xyz[0] * math.cos(theta) - xyz[1] * math.sin(theta)
        y = xyz[0] * math.sin(theta) + xyz[1] * math.cos(theta)
        z = xyz[2]
        return (x, y, z)

    def rotate_about(self, xyz, ijk,theta):
        # Subtract ijk from xyz
        xyz = (xyz[0] - ijk[0], xyz[1] - ijk[1], xyz[2] - ijk[2])
        # Rotate xyz
        xyz = self.rotate(xyz, theta)
        # Add ijk to xyz
        xyz = (xyz[0] + ijk[0], xyz[1] + ijk[1], xyz[2] + ijk[2])
        return xyz
    
    def get_walk_paths(self, steps = 100, time_on_ground = 0.5, theta = 0):
        if(self.y_negate):
            theta = -theta
        forward = self.rotate_about(self.get_forward_position(), self.get_home_position(), theta)
        backward = self.rotate_about(self.get_backward_position(), self.get_home_position(), theta)
        raised = self.get_raised_position()
        paths = calculate_line_points(backward, forward, math.ceil(steps * time_on_ground)) + calculate_bezier_points(forward, raised, backward, math.floor(steps*(1-time_on_ground)))
        return paths
    
    def get_turn_paths(self, steps=100, time_on_ground = 0.5, reverse = False):
        forward = self.get_forward_position()
        backward = self.get_backward_position()
        if(reverse):
            forward,backward = backward,forward
        if(self.y_negate):
            forward,backward = backward,forward
        raised = self.get_raised_position()
        paths = calculate_line_points(backward, forward, math.ceil(steps * time_on_ground)) + calculate_bezier_points(forward, raised, backward, math.floor(steps*(1-time_on_ground)))
        return paths