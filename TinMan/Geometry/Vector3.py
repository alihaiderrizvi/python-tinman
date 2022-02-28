from Geometry import angles
import math

class Vector3:
    epsilon = 0.0001

    def __init__(self,x=0,y=0,z=0): #constructor
        self.x = x
        self.y = y
        self.z = z
    
    #Static Utility Mehtods

    def get_cross_product(a,b):
        return Vector3((a.y*b.z)-(a.z*b.y),(a.z*b.x)-(a.x*b.z),(a.x*b.y)-(a.y*b.x))

    def get_dot_product(a,b):
        return a.x*b.x + a.y*b.y + a.z*b.z
    
    #End

    #Properties

    def __get_is_zero(self):
        return abs(self.x -0 < Vector3.epsilon and self.y - 0 < Vector3.epsilon and self.z - 0 <Vector3.epsilon)

    def __get_is_nan(self):
        return math.isnan(self.x) and math.isnan(self.y) and math.isnan(self.z)

    def __get_length(self):
        return math.sqrt(self.x**2 + self.y**2 +self.z**2)
    is_zero = property(__get_is_zero)
    is_nan = property(__get_is_nan)
    length = property(__get_length)
    
    #end region

    def Normalize(self):
        if self.length != 0:
            return Vector3(self.x/self.length, self.y/self.length, self.z/self.length)
        else:
            return self
    
    def dot(self, vector):
        return Vector3.get_dot_product(self, vector)

    def cross(self, vector):
        return Vector3.get_cross_product(self,vector)
    

    def with_x(self,newx):
        return Vector3(newx,self.y,self.z)
    
    def with_y(self,newy):
        return Vector3(self.x,newy,self.z)

    def with_z(self,newz):
        return Vector3(self.x,self.y,newz)

    def abs(self):
        return Vector3(abs(self.x),abs(self.y),abs(self.z))

    #Operator Overloads

    def __sub__(a,b):
        return Vector3(a.x-b.x,a.y-b.y,a.z-b.z)
    
    def __add__(a,b):
        return Vector3(a.x+b.x,a.y+b.y,a.z+b.z)

    def __mul__(a,scale):
        return Vector3(a.x*scale,a.y*scale,a.z*scale)

    def __truediv__(a,quotient):
        if quotient == 0:
            raise ZeroDivisionError
        else:
            return Vector3(a.x/quotient,a.y/quotient,a.z/quotient)

    def __eq__(a,b):
        return a.equals(b)

    def __ne__(a,b):
        return not a.equals(b)

    #end region

    def __str__(self):
        return str(round(self.x,2)) +'i ' + str(round(self.y,2))+ 'j ' + str(round(self.z,2))

    def equals(self,a):
        return type(a) == Vector3 and self.equals2(a)
    
    def equals2(self,a):
        return (math.isnan(self.x) and math.isnan(self.y) and math.isnan(self.z) and math.isnan(a.x) and math.isnan(a.y) and math.isnan(a.z)) or (abs(self.x - a.x) < Vector3.epsilon and abs(self.y - a.y) < Vector3.epsilon and abs(self.z - a.z) < Vector3.epsilon)

    def get_hash_code(self):
        return int(self.x) + int(self.y*5) + int(self.z*13)

    def angle_to(self,v):
        dot = Vector3.get_dot_product(self,v)
        if dot < -1:
            dot = -1
        if dot > 1:
            dot = 1
        return angles.Angle.from_radians(math.acos(dot)) 

