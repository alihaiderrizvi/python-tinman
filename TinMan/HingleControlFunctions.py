import sys,math
from TinMan.Geometry import AngularSpeed


class HingeControlFunctions:

    def move_to_with_gain(hinge, desired_angle, gain):
        if hinge == None:
            raise(BaseException('hinge'))
        
        def func(h,c,state):
            print(desired_angle, h.angle)
            angle_diff = desired_angle - h.angle

            if angle_diff.abs.degrees < 1:
                return AngularSpeed.AngularSpeed(0)
            speed = angle_diff.degrees*gain

            return AngularSpeed.AngularSpeed.from_degrees_per_second(speed)

        hinge.set_control_function(func)