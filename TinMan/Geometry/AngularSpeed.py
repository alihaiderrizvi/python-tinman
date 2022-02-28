import math
from Geometry import angles

class AngularSpeed:
    epsilon = 0.0001

    #Factory methods and constructur

    def from_radians_per_second(radians_per_second):
        return AngularSpeed(radians_per_second)
    
    def from_degrees_per_second(degrees_per_second):
        return AngularSpeed(angles.Angle.degrees_to_radians(degrees_per_second))

    #constructor
    def __init__(self,radians_per_second):
        self.radians_per_second = radians_per_second

    #End region

    #Properties
    def _degrees_per_second(self):
        return angles.Angle.radians_to_degrees(self.radians_per_second)
    
    def _is_nan(self):
        return math.isnan(self.radians_per_second)
    
    def _abs(self):
        return AngularSpeed(abs(self.radians_per_second))

    degrees_per_second = property(_degrees_per_second)
    is_nan  = property(_is_nan)
    abs = property(_abs)

    #end Region

    def limit(lower_limit, upper_limit):
        if lower_limit > upper_limit:
            raise BaseException("The lower limit must be less than upper limit")
        if self < lower_limit:
            return lower_limit
        if self > upper_limit:
            return upper_limit
        return self
    
    #Operators, equality and hashing

    def equals(self, obj):
        return type(obj) == AngularSpeed and self.equals2(obj)
    
    def equals2(self,obj):
        return abs(obj.radians_per_second - self.radians_per_second) < AngularSpeed.epsilon

    def get_hash_code(self):
        return self.radians_per_second

    def __add__(a,b):
        return AngularSpeed(a.radians_per_second + b.radians_per_second)
    
    def __sub__(a,b):
        return AngularSpeed(a.radians_per_second - b.radians_per_second)

    def __mul__(a,scale):
        if type(scale) == TimeSpan: #Need to be updated after time class
            return angles.Angle.from_radians(a.radians_per_second*scale)
        return AngularSpeed(a.radians_per_second*scale)
    
    def __truediv__(a,quotient):
        return AngularSpeed(a.radians_per_second/quotient)

    def __gt__(a,b):
        return a.radians_per_second > b.radians_per_second

    def __lt__(a,b):
        return a.radians_per_second < b.radians_per_second
    
    def __ge__(a,b):
        return a.radians_per_second >= b.radians_per_second
    
    def __le__(a,b):
        return a.radians_per_second <= b.radians_per_second
    
    def __eq__(a,b):
        return a.equals(b)
    
    def __ne__(a,b):
        return not a.equals(b)

    #End Region

    def __str__(self):
        return str(round(self.degrees_per_second,2)) + ' degrees per second'