from Geometry import Vector3

class Polar: #Immutable Data type
    def __init__(self,distance =0,theta = 0,phi=0):
        '''
        Theta = Angle in horizontal plane, 0 means pointing towards opponent goal
        Phi = Lattiduninal angle. 0 = Horizontal, -ve = pointing downward '''

        if distance < 0:
            raise BaseException("Distance", distance, "must not be negative")
        self.distance = distance
        self.theta = theta
        self.phi = phi

    def to_vector3(self):
        t = Distance * self.phi.cos
        x = t * self.theta.cos
        y = t * self.theta.sin
        z = Distance*self.phi.sin

        return Vector3.Vector3(x,y,z) #need addition

    def is_zero(self):
        return self.distance == 0 and self.theta == Angle(0) and self.phi == Angle(0)

    def __str__(self):
        return "Distance: " + str(round(self.distance,2)) + ", Theta: " + str(round(self.theta,2)) + ", Phi: " +str(round(self.degrees,2)) 
    
