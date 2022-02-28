import sys,math
from PerceptorParsing import switch_case, Parser,Scanner,PerceptorState
from NetworkUtil import NetworkUtil
from Log import Log
import SimulationContext
from datetime import timedelta
import socket
from EffectorCommands import *
import PlayMode as PlayMode
from pprint import pprint

class AgentHost:
    default_tcp_port = 3200
    default_host_name = 'localhost'
    cycle_period_seconds = 0.02
    cycle_period = timedelta(cycle_period_seconds)
    _log = Log.create()

    def __init__(self, uniform_number = None):
        self._host_name = AgentHost.default_host_name
        self._port_number = AgentHost.default_tcp_port
        self._team_name = 'TinManBots'
        self._context = SimulationContext.SimulationContext(self)
        self.context = self._context
        self.has_run = None
        self._stop_requested = False
        self._desired_uniform_number = uniform_number

    def _team_name_setter(self,value):
        if self.has_run != None:
            raise(BaseException('TeamName cannot be set after AgentHost.run has been called.'))
        if value == None:
            raise(BaseException('value'))
        self._team_name = value

    def _team_name_getter(self):
        return self._team_name

    team_name = property(_team_name_getter, _team_name_setter)

    def _desired_uniform_number_setter(self, value):
        if self.has_run != None:
            raise(BaseException('Desired_Uniform_number cannot be set after AgentHost.run has been called.'))
        if value < 0:
            raise(BaseException('Value '+ str(value)+ ' The desired uniform number must be zero or a positive integer'))
        self._desired_uniform_number = value

    def _desired_uniform_number_getter(self):
        return self._desired_uniform_number

    desired_uniform_number = property(_desired_uniform_number_getter, _desired_uniform_number_setter)


    def _host_name_setter(self,value):
        if self.has_run != None:
            raise(BaseException('HostName cannot be set after AgentHost.run has been called.'))
        if value == None:
            raise(BaseException('value'))
        if len(value.strip()) == 0:
            raise(BaseException('HostName cannot be blank ' + value))
        self._host_name = value

    def _host_name_getter(self):
        return self._host_name

    host_name = property(_host_name_getter, _host_name_setter)


    def _port_name_setter(self,value):
        if self.has_run != None:
            raise(BaseException('PortNumber cannot be set after AgentHost.run has been called.'))
        if value <= 0:
            raise(BaseException('value ' + str(value)+ ' PortNumber must be greater than zero' ))
        self._port_number = value

    def _port_name_getter(self):
        return self._port_number

    port_name = property(_port_name_getter, _port_name_setter)

    def run(self, agent):
        if agent == None:
            raise(BaseException('agent'))

        if self.has_run != None:
            raise(BaseException('Run can only be called once, and has already been called'))
        
        AgentHost._log.info('Connecting via TCP to ' + self.host_name + ":" + str(self._port_name_getter()))

        try:
            client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            client.connect((self.host_name, self.port_name))
        except:
            AgentHost._log.Error('Unable to connect to '+ self.host_name+ " : "+ self.port_number)
            raise(BaseException())
        
        AgentHost._log.info('Connected.')
        self.has_run = True
        AgentHost._log.info('Initializing agent')
       
        agent.context = self.context
        agent.on_initialise()

        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as client:
            client.connect((self.host_name, self.port_name))
            self._log.info('Sending initialisation messages')
            AgentHost.send_commands(client, [SceneSpecificationCommand(agent.body.rsg_path)])
            client.settimeout(0.5)
            print('payload')
            NetworkUtil.read_response_string(client, 0.5)
            AgentHost.send_commands(client, [InitialisePlayerCommand(self.desired_uniform_number, self.team_name)])
            print('payload')
            NetworkUtil.read_response_string(client, 0.5)
            commands = list()

            while not self._stop_requested and agent.is_alive:
                
                data = NetworkUtil.read_response_string(client, 0.1)
            
                if not data or data == None:
                    continue
                print('data')
                print(data)
                scanned = Scanner.Scanner(Scanner.StringBuffer(data))
                parser = Parser.Parser(scanned)
                parser.parse()
                perceptor_state = parser.state
                errors = parser.errors
            
                if errors.has_error:
                    AgentHost._log.error('Parse Error: ' + Parser.Errors.error_messages() + '\nData:' + data)

                for hinge in agent.body.all_hinges:
                    angle = perceptor_state.try_get_hinge_angle(hinge)
                    if angle != False:
                        hinge.angle = angle

                if perceptor_state.team_side !=  PerceptorState.FieldSide.unknown:
                    self.context.team_side = perceptor_state.team_side

                if perceptor_state.play_mode != PlayMode.PlayMode.unknown and perceptor_state.play_mode != self.context.play_mode:
                    self.context.play_mode = perceptor_state.play_mode

            
                if perceptor_state.uniform_number:
                    assert perceptor_state.uniform_number > 0
                    self.context.uniform_number = perceptor_state.uniform_number

                agent.think(perceptor_state)

                for hinge in agent.body.all_hinges:
                    hinge.compute_control_function(self.context, perceptor_state)
                
                self._context.flush_commands(commands)
                

                commands += [i.get_command() for i in agent.body.all_hinges if i.is_desired_speed_changed]
                
                commands.append(SynchroniseCommand())

                AgentHost.send_commands(client, commands)
                

                commands = []

            agent.on_shutting_down()

    
    def stop(self):
        self._stop_requested = True

    def send_commands(client, commands):
        command_str = AgentHost.concat_command_strings(commands)
        NetworkUtil.write_string_with_32_bit_length_prefix(client, command_str)

    def concat_command_strings(commands):
        sb = ''
        
        for command in commands:
           sb = command.append_s_expression(sb)
        return sb

                



    
