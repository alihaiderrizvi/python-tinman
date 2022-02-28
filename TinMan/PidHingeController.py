from datetime import timedelta
from AgentHost import AgentHost
from Geometry.AngularSpeed import AngularSpeed

class PidHingeController:
    def __init__(self, hinge):
        if hinge == None:
            raise(BaseException('hinge'))
        self.hinge = hinge
        self.proportional_gain = 20
        self.integral_gain = 0.1
        self.derivative_gain = 1000
        self._last_time = timedelta()

def _target_angle_setter_(self,value):
    self._target_angle = value
    self.hinge.set_control_function(self.control_function)
    target_angle = property(self._target_angle, self._target_angle_setter_)

def control_function(self, hinge, context, perceptor_state):
    if self._last_time == timedelta() or self._last_time < perceptor_state.simulation_time - AgentHost.cycle_period:
        previous_error = 0
        integral = 0
    self._last_time = perceptor_state.simulation_time
    dt = AgentHost.cycle_period_seconds
    error = self.target_angle.radians - hinge.angle.radians
    integral += error*dt
    derivative = (error-previous_error)*dt

    return AngularSpeed.from_radians_per_second(self.proportional_gain * error + self.integral_gain * integral + self.derivative_gain * derivative)

def __str__(self):
    return "<PID hinge = " + self.hinge.perceptor_label + " " + str(self.proportional_gain) + " " + str(self.integral_gain) + " " + str(self.derivative_gain) + ">"
    