# from dbm import error
from Geometry import angles, Polar, Vector3
from PerceptorParsing import Scanner, PerceptorState
import PlayMode
from EffectorCommands import *

from datetime import timedelta
import math

class Parser:
    _EOF = 0
    _double = 1
    _ident = 2
    max_t = 50

    min_err_dist = 2
    set = [
		[True,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False],
		[False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,False, False,False,False,True, True,True,True,True, True,True,True,True, False,False,False,False, False,False,False,False],
		[False,True,True,True, True,False,True,True, True,True,True,True, True,True,True,True, True,True,True,True, True,True,True,True, True,True,True,True, True,True,True,True, True,True,True,True, True,True,True,True, True,True,True,True, True,True,True,True, True,True,True,False],
		[False,False,False,False, False,False,True,False, False,True,False,False, False,False,False,False, True,False,False,True, False,True,False,True, False,False,True,False, True,False,False,True, False,False,True,False, False,False,False,False, False,False,False,False, False,False,False,False, True,False,False,False]

    ]

    def as_double(self,s):
        if s == 'nan':
            return math.nan
        else:
            d = float()
            try:
                d = float(s)
            except ValueError:
                self.error.sem_err("Unable to convert \ " + s + " \ to a float")
            return d
        
    def see_landmark(self, pos, landmark):
        self.landmark_positiions.append(PerceptorState.LandMarkPosition.LandmarkPosition(landmark, pos))

    def __init__(self, scanner):
        self.scanner = scanner
        self.errors = Errors()
        self.t = Scanner.Token()
        self.la = Scanner.Token()
        self.err_dist = int()
        self.team_name = str()
        self.simulation_time = timedelta()
        self.game_time = timedelta()
        self.play_mode = PlayMode.PlayMode.unknown #needs to rewatch
        self.team_side = PerceptorState.FieldSide.unknown
        self.player_id = int()
        self.agent_temperature = float()
        self.agent_battery = float()
        self.gyro_states = list()
        self.accelerometer_states = list()
        self.hinge_states = list()
        self.univsersal_joints_states = list()
        self.touch_states = list()
        self.force_states = list()
        self.landmark_positiions = list()
        self.visible_lines = list()
        self.team_mate_positions = list()
        self.opposition_positions = list()
        self.ball_position = Polar.Polar()
        self.messages = list()
        self.agent_position = Vector3.Vector3()

    def syn_err(self,n):
        if self.err_dist >= Parser.min_err_dist:
            Errors.syn_err(self.la.line, self.la.col, n)
            self.err_dist = 0
    
    def sem_err(self, msg):
        if self.err_dist >= Parser.min_err_dist:
            self.errors.sem_err(self.t.line, self.t.col, msg)
            self.err_dist = 0
    
    def get(self):
        while True:
            self.t = self.la
            self.la = self.scanner.scan()
            if self.la.kind <= Parser.max_t:
                print('a')
                self.err_dist += 1
                break
        self.la = self.t
    
    def expect(self,n):
        if self.la.kind == n:
            self.get()
        else:
            self.syn_err(n)

    def start_of(self,s):
        return Parser.set[s][self.la.kind]
    
    def expect_weak(self,n, follow):
        if self.la.kind == n:
            self.get()
        else:
            self.syn_err(n)
            while not self.start_of(follow):
                self.get()
    
    def weak_seperator(self, n, syfol, repfol):
        kind = self.la.kind
        if kind == n:
            self.get()
            return True
        elif self.start_of(repfol):
            return False
        else:
            self.syn_err(n)
            while not( self.set[syfol][kind] or self.set[repfol][kind] or self.set[0][kind]):
                self.get()
                kind = self.la.kind
            return self.start_of(syfol)
        
    def double(self):
        if self.la.kind == 1:
            self.get()
        elif self.la.lind == 3:
            self.get()
        else:
            self.syn_err(51)
        return self.as_double(self.t.val)
    
    def angle_in_degrees(self):
        self.expect(1)
        return angles.Angle.from_degree(self.as_double(self.t.val))
    
    def ident(self):
        self.expect(2)
        return self.t.val
        
    def time_span(self):
        secs = self.double()
        return timedelta(secs=secs)

    def vector3(self):
        x,y,z = self.double(), self.double(),self.double()
        return Vector3.Vector3(x,y,z)
    
    def polar(self):
        distance, theta, phi = self.double(),self.double(),self.double()
        return Polar.Polar(distance, theta, phi)
    
    def int_flag(self):
        return self.double() != 0

    def polar_pos_expr(self):
        self.expect(4)
        pos = self.polar()
        self.expect(5)
    
    def time_expr(self):
        self.expect(6)
        self.expect(7)
        self.expect(8)
        time = self.time_span()
        self.expect(5)
        self.expect(5)
        return time

    def game_state_expr(self):
        self.expect(9)
        pm_str = str()
        player_id_dbl = float()
        player_id = None
        team_side = None
        if self.la.kind == 10:
            self.get()
            player_id_dlb = self.double()
            self.expect(5)
            player_id = int(player_id_dbl)

        if self.la.kind == 11:
            self.get()
            if self.la.kind == 12 or self.la.kind == 13:
                if self.la.kind == 12:
                    self.get()
                    team_side = PerceptorState.FieldSide.left
                else:
                    
                    self.get()
                    team_side = PerceptorState.FieldSide.right
            self.expect(5)
        
        self.expect(7)
        self.expect(14)
        time = self.time_span()
        self.expect(5)
        self.expect(7)
        self.expect(15)
        pm_str = self.ident()
        self.expect(5)
        if not self.play_mode.PlayModeUtil.try_parse(pm_str):
            self.sem_err('Unable to parse play mode ' + pm_str + ' .')
        else:
            self.play_mode = self.play_mode.PlayModeUtil.try_parse(pm_str)
        self.expect(5)

        return time, self.play_mode, player_id, team_side
    
    def gyro_state_expr(self):
        label = str()
        x,y,z = float(), float(), float()
        self.expect(16)
        self.expect(7)
        self.expect(17)
        label = self.ident()
        self.expect(5)
        self.expect(7)
        self.expect(18)
        x,y,z = self.double(), self.double(), self.double()
        self.expect(5)
        self.expect(5)
        return PerceptorState.GyroState(label, x,y,z)

    def accelerometer_state_expr(self):
        label = str()
        v = Vector3.Vector3()
        self.expect(19)
        self.expect(7)
        self.expect(17)
        label = self.ident()
        self.expect(5)
        self.expect(7)
        self.expect(20)
        v = self.vector3()
        self.expect(5)
        self.expect(5)
        return PerceptorState.AccelerometerState(label, v)

    def hinge_joint_expr(self):
        label = str()
        angle = angles.Angle()
        self.expect(21)
        self.expect(7)
        self.expect(17)
        label = self.ident()
        self.expect(5)
        self.expect(7)
        self.expect(22)
        angle = self.angle_in_degrees()
        self.expect(5)
        self.expect(5)
        return PerceptorState.HingeState(label,angle)

    def univseral_joint_expr(self):
        self.expect(23)
        self.expect(7)
        self.expect(17)
        label = self.ident()
        self.expect(5)
        self.expect(7)
        self.expect(24)
        angle1 = self.angle_in_degrees()
        self.expect(5)
        self.expect(7)
        self.expect(25)
        angle2 = self.angle_in_degrees()
        self.expect(5)
        self.expect(5)
        return PerceptorState.UniversalJointState(label, angle1, angle2)

    def touch_state_expr(self):
        self.expect(26)
        self.expect(17)
        label = self.ident()
        self.expect(27)
        is_touching = self.int_flag()
        self.expect(5)
        return PerceptorState.TouchState(label, is_touching)

    def force_state_expr(self):
        self.expect(28)
        self.expect(7)
        self.expect(17)
        label = self.ident()
        self.expect(5)
        self.expect(7)
        self.expect(29)
        point = self.vector3()
        self.expect(5)
        self.expect(7)
        self.expect(30)
        force = self.vector3()
        self.expect(5)
        self.expect(5)
        return PerceptorState.ForceState(label,point, force)

    def agent_state_expr(self):
        self.expect(31)
        self.expect(7)
        self.expect(32)
        temp = self.double()
        self.expect(5)
        self.expect(7)
        self.expect(33)
        battery = self.double()
        self.expect(5)
        self.expect(5)
        return temp, battery
    
    def see_expr(self):
        self.expect(34)
        while self.la.kind == 7:
            self.get()
            if self.start_of(1):
                self.visible_item_expr()
            elif self.la.kind == 44:
                self.player_expr()
            elif self.la.kind == 46:
                self.my_pos_expr()
            elif self.la.kind == 47:
                self.line_expr()
            else:
                self.syn_err(52)
            self.expect(5)
        self.expect(5)

    def visible_item_expr(self):
        label = self.la.val
        if self.la.kind == 35 or self.la.kind == 36 or self.la.kind == 37 or self.la.kind == 38 or self.la.kind == 39 or self.la.kind == 40 or self.la.kind == 41 or self.la.kind == 42 or self.la.kind ==43:
            self.get()
        else:
            self.syn_err(53)
        pos = self.polar_pos_expr() 
        if label == 'F1L':
            self.see_landmark(pos, PerceptorState.Landmark.FlagLeftTop)
        elif self.la.kind == 'F2L':
            self.see_landmark(pos, PerceptorState.Landmark.FlagLeftBottom)
        elif self.la.kind == 'F1R':
            self.see_landmark(pos, PerceptorState.Landmark.FlagRightTop)
        elif self.la.kind == 'F2R':
            self.see_landmark(pos, PerceptorState.Landmark.FlagRightBottom)
        elif self.la.kind == 'G1L':
            self.see_landmark(pos, PerceptorState.Landmark.GoalLeftTop)
        elif self.la.kind == 'G2L':
            self.see_landmark(pos, PerceptorState.Landmark.GoalLeftBottom)
        elif self.la.kind == 'G1R':
            self.see_landmark(pos, PerceptorState.Landmark.GoalRightTop)
        elif self.la.kind == 'G2R':
            self.see_landmark(pos, PerceptorState.Landmark.GoalRightBottom)
        elif self.la.kind == 'B':
            self.ball_position = pos
        else:
            self.sem_err('Unable to parse visible item type string ' + label + ' .' )
        
    def player_expr(self):
        team_name = str()
        parts= list()
        
        self.expect(44)
        self.expect(11)

        while self.start_of(2):
            self.get()
            team_name += self.t.val
        
        self.expect(5)
        self.expect(45)

        player_id = self.double()

        self.expect(5)

        while self.la.kind == 7:
            self.get()
            part_label = self.ident()
            pos = self.polar_pos_expr()
            self.expect(5)
            parts.append(PerceptorState.BodyPartPosition(part_label, pos))

        is_team_mate = team_name == self.team_name
        player = PerceptorState.PlayerPosition(is_team_mate, int(player_id),parts)

        if is_team_mate:
            self.team_mate_positions.append(player)
        else:
            self.opposition_positions.append(player)

    def my_pos_expr(self):
        self.expect(46)
        agent_position = self.vector3()
        self.agent_position = agent_position

    def line_expr(self):
        self.expect(47)
        end1 = self.polar_pos_expr()
        end2 = self.polar_pos_expr()
        self.visible_lines.append(PerceptorState.VisibleLine(end1,end2))
    
    def hear_expr(self):
        time = timedelta()
        angle = angles.Angle(math.nan)
        message_text = str()
        self.expect(48)
        time = self.time_span()

        if self.la.kind == 49:
            self.get()
        elif self.la.kind == 1:
            direction = self.angle_in_degrees()
        else:
            self.syn_err(54)

        while self.start_of(2):
            self.get()
            message_text += self.t.val
        
        self.expect(5)
        return PerceptorState.HeardMessage(time,direction,Message(message_text))

    def perceptors(self):
        while self.start_of(3):
            if self.la.kind == 6:
                t = self.time_expr()
                self.simulation_time = t
            elif self.la.kind == 9:
                t, pm, id, side = self.game_state_expr()
                self.game_time = t
                self.play_mode = pm
                self.player_id = id
                if side.has_value:
                    self.team_side = side.value
            elif self.la.kind == 31:
                t,b = self.agent_state_expr()
                self.agent_temperature = t
                self.agent_battery = b
            
            elif self.la.kind == 16:
                gyro_state = self.gyro_state_expr
                self.gyro_states.append(gyro_state)
            
            elif self.la.kind == 19:
                acc_state = self.accelerometer_state_expr()
                self.accelerometer_states.append(acc_state)

            elif self.la.kind == 21:
                hj_state = self.hinge_joint_expr()
                self.hinge_states.append(hj_state)

            elif self.la.kind == 23:
                uj_state = self.univseral_joint_expr()
                self.univsersal_joints_states.append(uj_state)
            
            elif self.la.kind == 26:
                t_state = self.touch_state_expr()
                self.touch_states(t_state)

            elif self.la.kind == 28:
                f_state = self.force_state_expr()
                self.force_states.append(f_state)
            
            elif self.la.kind == 34:
                self.see_expr()
            
            elif self.la.kind == 48:
                message = self.hear_expr()
                self.messages.append(message)
        self.state = PerceptorState.PerceptorState(self.simulation_time, self.game_time, self.play_mode, self.team_side,
        self.player_id, self.gyro_states, self.hinge_states, self.univsersal_joints_states, self.touch_states, self.force_states, self.accelerometer_states,
        self.landmark_positiions, self.visible_lines, self.team_mate_positions, self.opposition_positions, self.ball_position, self.agent_battery, self.agent_temperature,
        self.messages, self.agent_position)

    def parse(self):
        self.la = Scanner.Token()
        self.la.val = ''
        self.get()
        self.perceptors()
        self.expect(0)


class ParseError:

    def __init__(self,line,col,code,msg):
        self.line_number = line
        self.column_number = col
        self.error_code = code
        self.message = msg

    def to_string(self):
        m = self.message
        has_info = self.line_number != -1 or self.column_number != -1 or self.error_code != -1
        info_yet = False

        if has_info:
            m += ' ('
        if self.line_number != -1:
            m += "line " + str(self.line_number)
            info_yet = True

        if self.column_number != -1:
            if info_yet:
                m += ", "
            m += 'Col ' + str(self.column_number) 
        
        if self.error_code != -1:
            if info_yet:
                m += ', '
            m += 'Code ' + str(self.error_code)
        
        if has_info:
            m += ')'
        
        return m

class Errors:
    items = []
    
    
    
    def getter(self):
        return bool(Errors.items)

    
    has_error = property(getter)

    

    def error_messages():
        if not Errors.items:
            return str(Errors.items)
        s = str()
        for var in Errors.items:
            s += var + '\n'
        return s
    
    
    def syn_err(line, col, n):
        if n == 0:
            s = 'EOF expoected'
        elif n == 1:
            s = 'Double expected'
        elif n == 2:
            s = 'ident expected'
        elif n == 3:
            s = '"nan" expected'
        elif n == 4:
            s = '"pol" expected'
        elif n == 5:
            s = '")" expected'
        elif n == 6:
            s = '"(time" expected'
        elif n == 7:
            s = '"(" expected'
        elif n == 8:
            s = '"now" expected'
        elif n == 9:
            s = '"(GS" expected'
        elif n == 10:
            s = '"(unum expected'
        elif n == 11:
            s = ' "(team expected'
        elif n == 12:
            s = "'left' expected"
        elif n == 13:
            s = "'right' expected"
        elif n == 14:
            s = " 't' expected"
        elif n == 15:
            s = "'pm' expected"
        elif n == 16:
            s = "'(GYR' expected"
        elif n == 17:
            s = "'n' expected"
        elif n == 18:
            s = "'rt' expected"
        elif n == 19:
            s = "'(ACC' expected"
        elif n == 20:
            s = "'a' expected"
        elif n == 21:
            s = "'(HJ' expected"
        elif n == 22:
            s = "'ax' expected"
        elif n == 23:
            s = "'(UJ' expected"
        elif n == 24:
            s = "'ax1' expected"
        elif n == 25:
            s = "'ax2' expected"
        elif n == 26:
            s = "'(TCH' expected"
        elif n == 27:
            s = "'val' expected"
        elif n == 28:
            s = "'(FRP' expected"
        elif n == 29:
            s = "'c' expected"
        elif n == 30:
            s = "'f' expected"
        elif n == 31:
            s = "'(AgentState' expected"
        elif n == 32:
            s = "'Temp' expected"
        elif n == 33:
            s = "'Battery' expected"
        elif n == 34:
            s = "'(See' expected"
        elif n == 35:
            s = "'F1L' expected"
        elif n == 36:
            s = "'F2L' expected"
        elif n == 37:
            s = "'F1R' expected"
        elif n == 38:
            s = "'F2R' expected"
        elif n == 39:
            s = "'G1L' expected"
        elif n == 40:
            s = "'G2L' expected"
        elif n == 41:
            s = "'G1R' expected"
        elif n == 42:
            s = "'G2R' expected"
        elif n == 43:
            s = "'B' expected"
        elif n == 44:
            s = "'P' expected"
        elif n == 45:
            s = "'(id' expected"
        elif n == 46:
            s = "'mypos' expected"
        elif n == 47:
            s = "'L' expected"
        elif n == 48:
            s = "'(hear' expected"
        elif n == 49:
            s = "'self' expected"
        elif n == 50:
            s = "'???? expected"
        elif n == 51:
            s = "invalid double"
        elif n == 52:
            s = "invalid see_expr"
        elif n == 53:
            s = "Invalid visible_item_expr"
        elif n == 54:
            s = "Invalid hear_exper"
        else:
            s = 'error code' + str(n)
        
        Errors.add_error(line,col, n, s)
    

    def add_error(line, col, code,msg):
        Errors.items.append(ParseError(line, col, code,msg))
    

    
    def sem_err(*args):
        if len(args) == 3:
            Errors.add_error(args[0], args[1], -1, args[2])
        else:
            Errors.add_error(-1,-1,-1,args[0])
    def warning(*args):
        if len(args) == 3:
            Errors.add_error(args[0], args[1], -1, args[2])
        else:
            Errors.add_error(-1,-1,-1,args[0])
    
class FatalError(Exception):
    def __init__(self, m):
        super(m)