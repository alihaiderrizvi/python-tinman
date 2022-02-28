from AgentBase import AgentBase
from NaoBody import NaoBody
from Geometry.angles import Angle
from Geometry.AngularSpeed import AngularSpeed
import random
import math
class WavingAgent(AgentBase):
    
    def __init__(self):
        super(WavingAgent, self).__init__(NaoBody())
        print("""Waving agent is controlled via the keyboard. Press Keys '0' through '9' to set the angle directly, or press '?' to repeatedly set a random angle""") 

    def think(self, state):
        c= input('Press key and Enter')

        if not c:
            return
        
        if c >= "0" and c <= "9":
            angle = int(c)*10
            self.body.laj1.move_to_with_gain(Angle.from_degree(angle), 1)
        
        elif c == '?':
            self.body.laj1.set_control_function(self.fun)
        
    def fun(self, hinge, context, perceptorstate):
        if (perceptorstate.simulation_time.microseconds/1000) %250 ==0:
            return AngularSpeed.from_degrees_per_second(random.randint(-100,100))
        return AngularSpeed(math.nan)