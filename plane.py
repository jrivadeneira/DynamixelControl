class Plane:
    normal_vector = [0, 0, 1]
    origin_vector = [0, 0, 0]
    def __init__(self, normal, origin=None) -> None:
        self.normal_vector = normal
    
    def get_z(self, x, y):
        return self.normal_vector[0] * x + self.normal_vector[1] * y + self.normal_vector[2]
    