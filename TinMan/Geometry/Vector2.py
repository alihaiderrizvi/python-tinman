from Geometry import angles
import math

class Vector2:
    epsilon = 0.0001

    def __init__(self,x,y): #constructor
        self.x = x
        self.y = y
    
    #Static Utility Mehtods

    def get_dot_product(a,b):
        return a.x*b.x + a.y*b.y
    
    #End

    #Properties

    def __get_is_zero(self):
        return abs(self.x -0 < Vector2.epsilon and self.y - 0 < Vector2.epsilon)

    def __get_is_nan(self):
        return math.isnan(self.x) and math.isnan(self.y)

    def __get_length(self):
        return math.sqrt(self.x**2 + self.y**2)
    is_zero = property(__get_is_zero)
    is_nan = property(__get_is_nan)
    length = property(__get_length)
    
    #end region

    def Normalize(self):
        if self.length != 0:
            return Vector2(self.x/self.length, self.y/self.length)
        else:
            return self
    
    def dot(self, vector2):
        return Vector2.get_dot_product(self, vector2)
    

    def with_x(self,newx):
        return Vector2(newx,self.y)
    
    def with_y(self,newy):
        return Vector2(self.x,newy)

    def abs(self):
        return Vector2(abs(self.x),abs(self.y))

    #Operator Overloads

    def __sub__(a,b):
        return Vector2(a.x-b.x,a.y-b.y)
    
    def __add__(a,b):
        return Vector2(a.x+b.x,a.y+b.y)

    def __mul__(a,scale):
        return Vector2(a.x*scale,a.y*scale)

    def __truediv__(a,quotient):
        if quotient == 0:
            raise ZeroDivisionError
        else:
            return Vector2(a.x/quotient,a.y/quotient)

    def __eq__(a,b):
        return a.equals(b)

    def __ne__(a,b):
        return not a.equals(b)

    #end region

    def __str__(self):
        return str(round(self.x,2)) +'i ' + str(round(self.y,2))+ 'j'

    def equals(self,a):
        return type(a) == Vector2 and self.equals2(a)
    
    def equals2(self,a):
        return (math.isnan(self.x) and math.isnan(self.y) and math.isnan(a.x) and math.isnan(a.y)) or (abs(self.x - a.x) < Vector2.epsilon and abs(self.y - a.y) < Vector2.epsilon)

    def get_hash_code(self):
        return int(self.x) + int(self.y*5)

    def angle_to(self,v):
        dot =Vector2.get_dot_product(self,v)
        if dot < -1:
            dot = -1
        if dot > 1:
            dot = 1
        return angles.Angle.from_radians(math.acos(dot)) 

