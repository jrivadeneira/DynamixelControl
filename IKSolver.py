import math

def mapit(theta, maximum, sweepSize):
    maximum /= 2
    motorpos = theta / (sweepSize)
    motorpos = (motorpos * maximum) + maximum
    return int(motorpos)

# inverse kinematics solver for a 3DOF robotic leg where the first joint is parallel to the ground and the other two joints are perpendicular to the ground
def getThetas(x, y, z, length0, length1, length2, y_negate, theta1_offset = 0):
    if(y_negate):
        y *= -1
    theta1 = math.atan2(y, x) + theta1_offset
    # calculate the distance from the origin to the point (x, y, z)
    d = math.sqrt(x**2 + y**2 + z**2)
    # calculate the angle between the line from the origin to the point (x, y, z) and the line from the origin to the point (x, y, 0)
    alpha = math.acos(z/d)
    # calculate the angle between the line from the origin to the point (x, y, 0) and the line from the origin to the point (x, y, length0)
    beta = math.acos(length0/d)
    # calculate the angle between the line from the origin to the point (x, y, length0) and the line from the origin to the point (x, y, length0 + length1)
    gamma = math.acos((length1**2 + d**2 - length2**2)/(2 * length1 * d))
    # calculate the angle between the line from the origin to the point (x, y, length0) and the line from the origin to the point (x, y, length0 + length2)
    delta = math.acos((length2**2 + d**2 - length1**2)/(2 * length2 * d))
    # calculate the angle between the line from the origin to the point (x, y, length0) and the line from the origin to the point (x, y, length0 + length1 + length2)
    epsilon = math.acos((length1**2 + length2**2 - d**2)/(2 * length1 * length2))
    # calculate the angle between the line from the origin to the point (x, y, length0) and the line from the origin to the point (x, y, length0 + length1 + length2)
    theta2 = math.pi - alpha - beta - gamma
    theta3 = math.pi - epsilon
    return [theta1, theta2, theta3]
    
def calculate_line_points(start, end, steps):
    points = []
    for i in range(steps):
        t = i / steps
        x = (1-t) * start[0] + t * end[0]
        y = (1-t) * start[1] + t * end[1]
        z = (1-t) * start[2] + t * end[2]
        points.append((x,y,z))
    return points

# calculate Quadratic bezier curve points between start, middle and end
def calculate_bezier_points(start, middle , end, steps):
    points = []
    for i in range(steps):
        t = i / steps
        x = (1-t)**2 * start[0] + 2 * (1-t) * t * middle[0] + t**2 * end[0]
        y = (1-t)**2 * start[1] + 2 * (1-t) * t * middle[1] + t**2 * end[1]
        z = (1-t)**2 * start[2] + 2 * (1-t) * t * middle[2] + t**2 * end[2]
        points.append((x,y,z))
    return points