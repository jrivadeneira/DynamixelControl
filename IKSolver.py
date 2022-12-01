import math

def getThetas(x, y, z, length0, length1, length2, y_negate):
    if(y_negate):
        y *= -1

    theta0 = 0
    theta1 = 0
    theta2 = 0


    theta0 += math.atan2(y, x)
    x -= length0*math.cos(theta0)
    if(not y_negate):
        y -= length0*math.sin(theta0)
    else:
        y += length0*math.sin(theta0)

    r1 = length1 * math.cos(theta0)
    r2 = length2 * math.cos(theta0)

        # theta zero is entirely dependent on the unit vector of x and y. Mostly y because it is the only dof that can control it.
        # given an x and y, find a unit vector and scale

    r1Squared = r1**2
    r2Squared = r2**2
    xzMag = (x**2+z**2)**(1/2)
    xzMagSquared = xzMag**2

    # calculate stuff
    theta2 = math.acos((xzMagSquared-(r1Squared+r2Squared))/(2*r1*r2))
    numerator = r2*math.sin(theta2)
    denominator = r2*math.cos(theta2) + r1
    alpha = math.atan2(numerator, denominator)
    beta = math.atan2(z, x)
    theta1 = beta-alpha
        
    return theta0, theta1, theta2
