import math

class Plane:
    normal_vector = [0, 0, 1]
    origin_vector = [0, 0, 0]
    def __init__(self, normal, origin=None) -> None:
        self.normal_vector = normal
        if(origin != None):
            self.origin_vector = origin
    
    def get_normal(self):
        return self.normal_vector
    
    def get_z(self, x, y):
        return (self.normal_vector[0] * (x - self.origin_vector[0]) + self.normal_vector[1] * (y - self.origin_vector[1]) + self.origin_vector[2]) / self.normal_vector[2]
    
    def rotate_plane(self, theta, phi):
        self.normal_vector = self.rotate_vector(self.normal_vector, theta, phi)

    def rotate_vector(self, vector, theta, phi):
        x = vector[0]
        y = vector[1]
        z = vector[2]
        x1 = x * math.cos(theta) - y * math.sin(theta)
        y1 = x * math.sin(theta) + y * math.cos(theta)
        z1 = z
        y2 = y1 * math.cos(phi) - z1 * math.sin(phi)
        z2 = x1 * math.sin(phi) + z1 * math.cos(phi)
        return [x1, y2, z2]
    
    def roll_plane(self, theta):
        self.normal_vector = self.rotate_vector(self.normal_vector, theta, 0)

    def pitch_plane(self, phi):
        self.normal_vector = self.rotate_vector(self.normal_vector, 0, phi)