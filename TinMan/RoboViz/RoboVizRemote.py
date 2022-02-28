import sys

from RoboViz import Shape

class RoboVizOptions:
    default_udp_port = 32769
    default_host_name = 'localhost'

    def __init__(self):
        use_default_prefix  = True
        port = RoboVizOptions.default_udp_port
        host_name = RoboVizOptions.default_host_name

class RoboVizRemote:

    def __init__(self, *args):
        if len(args) == 1:
            self.agent = args[0]
            self.options = RoboVizOptions()
        elif len(args) == 2:
            self.agent = args[0]
            self.options = args[1]
        
        self._path = str()
        self._sets = []
        self._agent_text = str()
        self._agent_text_color = str()
        self._use_default_prefix = self.options.use_default_prefix
        self._simulation_context = self.agent.context

        self.agent.think_completed += RoboVizRemote.on_think_completed
        self.agent.shutting_down += RoboVizRemote.on_shut_down

        self._udp_client = UdpClient()
        self._udp_client.connect(options.host_name, options.port)

        self._is_agent_text_dirty = False
        self._agent_text = None
        self._agent_text_color = Color.light_sky_blue

    def add(shape_set):
        if not shape_set:
            raise(BaseException)
        else:
            self._sets.append(shape_set)
            shape_set.set_parent(self)
        
    def _path_getter(self):
        if not self._path:
            if not self._use_default_prefix:
                return self._path
            else:
                if  not(self._simulation_context.uniform_number.has_value) or self._simulation_context.team_side == FieldSide.unknown:
                    raise BaseException('"Cannot determine default prefix for RoboViz shape set path as the agent's uniform number and team side have not been reported yet.  Make sure you initialise your instance of RoboVizRemote in your overridden IAgent.OnInitialise to avoid this error."')
                    self._path = str(self._simulation_context.team_side)[0] + '.A' + self._simulation_context.uniform_number.value
        return self._path
    
    path = property(self._path_getter)

    def _agent_text_setter(self, value):
        if self._agent_text == value:
            return
        self._agent_text = value
        self._is_agent_text_dirty = True

    agent_text = property(self._agent_text, self._agent_text_setter)

    def _agent_text_color_setter(self, value):
        if self._agent_text_color == value:
            return
        self._agent_text_color = value
        self._is_agent_text_dirty = True

    agent_text_color = property(self._agent_text_color, self._agent_text_color_setter)
        
    def on_think_completed(self):
        self.queue = list(self._sets)
        self.dirty_nodes = list()

        while self.queue:
            set = self.queue.pop(0)
            if set.is_dirty():
                self.dirty_nodes.append(set)
            else:
                for subset in set.subsets:
                    self.queue.append()
        
        for set in self.dirty_nodes():
            set.flush_messages(self._udp_client)
            self.swap_buffer(set, self._udp_client)

        if self._is_agent_text_dirty:
            if not self._agent_text or not self._agent_text.strip():
                buf = [2,2, self.get_agent_btye()]
                self._udp_client.send(buf, len(buf))
            else:
                text_bytes = bytes(self._agent_text, 'ascii')
                buf = [None for i in range(7 + len(text_bytes))]
                buf[0],buf[1],buf[2] = 2,1,self.get_agent_btye()
                Shape.WriteColor(buf,3 self.agent_text_color, False)
                for i in range(len(text_bytes)):
                    buf[6+i] = text_bytes[i]
                self._udp_client.send(buf, len(buf))
            self._is_agent_text_dirty = False

    def get_agent_btye(self):
        if self._simulation_context.team_side == FieldSide.unknown:
            raise(BaseException("Team side is unknown"))
        if self._simulation_context.uniform_number == None:
            raise(BaseException('Unifrom Number is unknown'))
        if self._simulation_context.uniform_number.value < 1 or self._simulation_context.uniform_number.value > 128:
            raise(BaseException('Uniform number is invalid'))
        val = 0 if self._simulation_context.team_side == FieldSide.left else 128
        return bytes((val + self._simulation_context.uniform_number - 1))
    
    def swap_buffer(set, udp_client):
        path_bytes = set.path_bytes
        num_bytes = 3 + len(path_bytes)
        buf = [None for i in range(num_bytes)]
        for i in range(len(path_bytes)):
            buf[2+i] = path_bytes[i]
        udp_client.send(buf, len(buf))

    def on_shut_down(self):
        self._udp_client([bytes(0) for i in range(3)], 3)
        self._udp_client.close()

        




