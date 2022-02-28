import Log
from Geometry import Vector3
from configparser import ConfigParser
from PerceptorParsing import PerceptorState
import random
class Measures:
    _log = Log.Log.create()

    def __init__(self):
        self.ball_mass_kilograms = Measures.get_value('ball_mass_kilograms', 0.026)
        self.ball_radius_metres = Measures.get_value('ball_radius_metres', 0.04)
        self.field_y_length = Measures.get_value('field_y_length', 14)
        self.field_x_length = Measures.get_value('field_x_length', 21)
        self.field_z_length = Measures.get_value('field_z_length', 40)
        self.goal_y_length = Measures.get_value('goal_y_length', 2.1)
        self.goal_z_length = Measures.get_value('goal_z_length', 0.8)
        self.goal_x_length = Measures.get_value('goal_x_length', 0.6)
        self.penalty_area_x_length = Measures.get_value('penalty_area_x_length', 1.8)
        self.penalty_area_y_length = Measures.get_value('penalty_area_y_length', 3.9)
        self.free_kick_distance = Measures.get_value('free_kick_distance', 1.3)
        self.free_kick_move_distance = Measures.get_value('free_kick_move_distance', 1.5)
        self.goal_kick_distance = Measures.get_value('goal_kick_distance', 1.0)

        self.field_x_left = -self.field_x_length/2
        self.field_x_right = self.field_x_length/2
        self.field_y_top = self.field_x_length/2
        self.field_y_bottom = -self.field_y_length/2

        self.flag_height = 0
        self.goal_post_x = self.field_x_length/2

        self.flag_left_top_position = Vector3.Vector3(-self.field_x_length/2, self.field_y_length/2, self.flag_height)
        self.flag_right_top_position = Vector3.Vector3(self.field_x_length/2, self.field_y_length/2, self.flag_height)
        self.flag_left_bottom_position = Vector3.Vector3(-self.field_x_length/2, -self.field_y_length/2, self.flag_height)
        self.flag_right_bottom_position = Vector3.Vector3(+self.field_x_length/2, -self.field_y_length/2, self.flag_height)
        self.goal_left_top_position = Vector3.Vector3(-self.goal_post_x, self.goal_y_length/2, self.goal_z_length)
        self.goal_right_top_position = Vector3.Vector3(self.goal_post_x, self.goal_y_length/2, self.goal_z_length)
        self.goal_left_bottom_position = Vector3.Vector3(-self.goal_post_x, -self.goal_y_length/2, self.goal_z_length)
        self.goal_right_bottom_position = Vector3.Vector3(+self.goal_post_x, -self.goal_y_length/2, self.goal_z_length)

    def get_value(key_suffix, default_value):
        config = ConfigParser()
        key = 'TinMan.Measures.' + key_suffix
        config.read('TinMan/app.config')
        value_string = config.get('configuration', key)
        if value_string == None:
            return default_value
        try:
            return float(value_string)
        except ValueError:
            Measures._log.warn('Unable to parse config key ' + value_string + ' as a dobule. Using default value of ' +str(default_value) + ' instead.')
            return default_value

    def get_land_point_global(self,landmark):
        
        if landmark == PerceptorState.Landmark.flag_left_top:
            return self.flag_left_top_position
        elif landmark == PerceptorState.Landmark.flag_left_bottom:
            return self.flag_left_bottom_position
        elif landmark == PerceptorState.Landmark.flag_right_top:
            return self.flag_right_top_position
        elif landmark == PerceptorState.Landmark.flag_right_bottom:
            return self.flag_right_bottom_position
        elif landmark == PerceptorState.Landmark.goal_left_top:
            return self.goal_left_top_position
        elif landmark == PerceptorState.Landmark.goal_left_bottom:
            return self.goal_left_bottom_position
        elif landmark == PerceptorState.Landmark.goal_right_top:
            return self.goal_right_top_position
        elif landmark == PerceptorState.Landmark.goal_right_bottom:
            return self.goal_right_bottom_position
        else:
            raise(BaseException('Unexpected landmark enum value '+ landmark))

    def is_in_field(self,vector):
        return vector.x >= -self.field_x_length/2 and vector.x <= self.field_x_length/2 and vector.y > -self.field_y_length/2 and vector.y < self.field_y_length/2
    
    def get_random_position(self, side):
        x1 = -self.field_x_length/2
        x2 = self.field_x_length/2

        if side == PerceptorState.FieldSide.left:
            x2 = 0
        
        elif side == PerceptorState.FieldSide.right:
            x1 = 0
        
        z = (random.randint(0, 10000)/10000)*self.field_z_length
        y = ((random.randint(0, 10000)/10000)*self.field_y_length) - self.field_y_length/2
        x = ((random.randint(0, 10000)/10000)*(x2-x1)) + x1

        return Vector3.Vector3(x,y,z)
        