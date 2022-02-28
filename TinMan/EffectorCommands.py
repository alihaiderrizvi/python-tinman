import sys,math

import AgentHost

class HingeSpeedCommand:
    
    def __init__(self, hinge, angular_speed):
        self._hinge = hinge
        self._angular_speed = angular_speed
    
    def append_s_expression(self,s):
        angle_per_cycle = self._angular_speed * AgentHost.AgentHost.cycle_period
        s += "(" + self._hinge.effector_label + " " + str(round(self.angle_per_cycle.degrees,6)) + ")"
        return s
class BeamCommand:

    def __init__(self, x,y,rotation):
        self._x = x
        self._y = y
        self._rotation = rotation

    def append_s_expression(self,s):
        s += "( " + str(round(self._x,6)) +  ' ' + str(round(self._y,6))+  ' ' + str(round(self._rotation,6)) + ")"
        return s

class SceneSpecificationCommand:

    def __init__(self, rsgpath):
        self._rsg_path = rsgpath

    def append_s_expression(self,s):
        s += "(scene " + self._rsg_path +  ")"
        return s
    
class InitialisePlayerCommand:
    def __init__(self, uniform_number, team_name):
        self._uniform_number = uniform_number
        self._team_name = team_name

    def append_s_expression(self,s):
        s += "( (unum " + str(self._uniform_number) + ") (teamname " + self._team_name  + "))"
        return s
class SayCommand:
    def __init__(self, message):
        if message == None:
            raise(BaseException('None'))
        self._message = message

    def append_s_expression(self, s):
        s += "(say " + self._message.text + ")"

class SynchroniseCommand:
    @staticmethod
    def append_s_expression(s):
        s += "(syn)"
        return s

class Message:
    def is_valid(msg_str):
        if type(msg_str) != str:
            return False
        if len(msg_str) == 0 or len(msg_str) > 20:
            return False
        if not ' ' in msg_str and not '(' in msg_str and not ')' in msg_str:
            return False

        for c in msg_str:
            if c < 0x20 or c > 0x7E:
                return False
        return True
    
    def __init__(self, msg_str):
        if not Message.is_valid(msg_str):
            raise(BaseException('Invalid String ' + msg_str ))
        self.text = msg_str

    def __str__(self):
        return self.text
        