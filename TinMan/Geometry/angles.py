import math
import random

class Angle:
    epsilon = 0.0001
    '''
    zero = Angle(0)
    two_pi = Angle(math.pi*2)
    half_pi = Angle(math.pi/2)
    pi = Angle(math.pi)
    nan = Angle(math.nan)
    '''
    
    #Region Factory Methods
    
    def random():
        return Angle((random.randint(0,200)/100)*math.pi)

    def from_radians(radians):
        return Angle(radians)

    def from_degree(degrees):
        return Angle(Angle.degrees_to_radians(degrees))

    def a_cos(d):
        return Angle.from_radians(math.acos(d))

    def a_tan(d):
        return Angle.from_radians(math.atan(d))

    def a_tan2(x,y):
        return Angle.from_radians(math.atan2(x,y))

    def __init__(self,radians = 0):
        self.radians = radians
        

    #end region



    #Region Utility Methods

    def degrees_to_radians(degrees):
        factor = math.pi/180
        return degrees*factor

    def radians_to_degrees(radians):
        factor = 180/math.pi
        return radians*factor

    #end region

    #Properties 

    def __get_degrees(self):
        return Angle.radians_to_degrees(self.radians)
    
    def __get_cos(self):
        return math.cos(self.radians)

    def __get_sin(self):
        return math.sin(self.radians)

    def __get_tan(self):
        return math.tan(self.radians)
    
    def __get_is_nan(self):
        return math.isnan(self.radians)
    
    def __get_abs(self):
        return Angle(abs(self.radians))


    degrees = property(__get_degrees)
    cos = property(__get_cos)
    sin = property(__get_sin)
    tan = property(__get_tan)
    is_nan = property(__get_is_nan)
    abs = property(__get_abs)

    #end properties

    def normalise_balanced(self):
        new = self.radians

        while new < -math.pi:
            new += math.pi*2
        while new >= math.pi:
            new -= math.pi*2
        return Angle.from_radians(new)

    def limit(self, lowerlimit, upperlimit):
        if lowerlimit > upperlimit:
            raise BaseException('The Lower limit must be less than upper limit')
        if self < lowerlimit:
            return lowerlimit
        if self > upperlimit:
            return upperlimit
        return self



    #region operators, equality, hashing

    def equals(self,obj):
        return type(obj) == type(self) and self.equals_2(obj)

    def equals_2(self,other):
        return (self.is_nan() and other.is_nan()) or abs(other.radians-self.radians) < self.epsilon

    def get_hash_code(self):
        return hash(self.radians)

    def __add__(a,b):
        return Angle.from_radians((a.radians + b.radians))

    def __mul__(a,scale):
        return Angle.from_radians((a.radians * scale))

    def __sub__(a,b):
        return Angle.from_radians((a.radians - b.radians))


    def __truediv__(a,quotient):
        # if type(b) != Angle:
        #     return Angle.from_radians(a.radians/b) #Code to be added after time class
        return Angle.from_radians(a.radians/quotient)

    def __gt__(a,b):
        return a.radians > b.radians

    def __lt__(a,b):
        return a.radians < b.radians

    def __ge__(a,b):
        return a.radians >= b.radians

    def __le__(a,b):
        return a.radians <= b.radians

    def __eq__(a,b):
        return a.equals(b)

    def __ne__(a,b):
        return not a.equals(b)

    def __str__(self):
        return str(round(Angle.radians_to_degrees(self.radians),2))+ ' Degrees'





    
    
