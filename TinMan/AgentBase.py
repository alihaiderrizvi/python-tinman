import sys,math
from Log import Log

class AgentBase:
    def __init__(self, body):
        if body == None:
            raise(BaseException('body'))
        self.body = body
        
        self.log = Log.create()
        self.is_alive = True
        self.think_completed = None
        self.shutting_down = None
        self._context = None
    
    def _context_measures(self):
        return self._context.measures
    measures = property(_context_measures)

    def _body_getter(self):
        return self.body

    Iagent_body = property(_body_getter)

    def __Iagent_context_getter__(self):
        if self._context == None:
            raise(BaseException('The context property cannot be accessed before the first call to think.'))
        return self._context
    def __Iagent_context_setter__(self,value):
        if value == None:
            raise(BaseException('value'))
        if self._context != None:
            raise(BaseException('Context has already been set.'))
        self._context = value
    
    

    Iagent_context = property(__Iagent_context_getter__, __Iagent_context_setter__)

    context = Iagent_context

    def Iagent_think(self, state):
        self.think(state)
        evt = self.think_completed
        if evt != None:
            evt()
    
    def Iagent_on_shutting_down(self):
        self.on_shutdown()
        evt = self.shutting_down
        if evt != None:
            evt()
    
    def stop_simulation(self):
        self.log.info('Agent requested that the simulation stops')
        self.is_alive = False

    def on_initialise(self):
        pass
        





