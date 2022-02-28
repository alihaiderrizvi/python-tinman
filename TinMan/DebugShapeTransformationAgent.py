import TinMan
from TinMan.Geometry import Vector3,angles,TransformationMatrix
from TinMan import NaoBody,AgentBase
from TinMan.RoboViz import RoboVizRemote, Shape, ShapeSet

class DebugShapeTransformationAgent(AgentBase.AgentBase):

    def __init__(self):
        super(DebugShapeTransformationAgent, self).__init__(NaoBody.NaoBody())
        line = Shape.Line
        Vector3 = Vector3.Vector3
        self._lines = [line(Vector3(0,0,0), Vector3(0,1,0)),
        line(Vector3(0,1,0), Vector3(1,1,0)),line(Vector3(1,1,0), Vector3(1,0,0)),
        line(Vector3(1,0,0), Vector3(0,0,0)),line(Vector3(0,0,0), Vector3(0,0,1)),
        line(Vector3(0,0,1), Vector3(1,0,1)),line(Vector3(1,0,1), Vector3(1,0,0)),
        line(Vector3(1,0,0), Vector3(0,0,0)),line(Vector3(0,0,0), Vector3(0,0,1)),
        line(Vector3(0,0,1), Vector3(0,1,1)),line(Vector3(0,1,1), Vector3(0,1,0)),
        line(Vector3(0,1,0), Vector3(0,0,0)),line(Vector3(0,0,1), Vector3(0,1,1)),
        line(Vector3(0,1,1), Vector3(1,1,1)),line(Vector3(1,1,1), Vector3(1,0,1)),
        line(Vector3(1,0,1), Vector3(0,0,1)),line(Vector3(0,1,0), Vector3(0,1,1)),
        line(Vector3(0,1,1), Vector3(1,1,1)),line(Vector3(1,1,1), Vector3(1,1,0)),
        line(Vector3(1,1,0), Vector3(0,1,0)),line(Vector3(1,0,0), Vector3(1,0,1)),
        line(Vector3(1,0,1), Vector3(1,1,1)),line(Vector3(1,1,1), Vector3(1,1,0)),
        line(Vector3(1,1,0), Vector3(1,0,0))]

        self._shape_set = ShapeSet.ShapeSet('Cube')

    def on_initialise(self):
        self._debugger = RoboVizRemote.RoboVizRemote(self)
        self._debugger.add(self._shape_set)
        super(DebugShapeTransformationAgent, self).on_initialise()

    def think(self, state):
        time_angle = angles.Angle.from_radians(state.simulation_time.total_secs)
        transformation = TransformationMatrix.TransformationMatrix(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1).translate(Vector3.Vector3().with_z(1)).rotate_x(time_angle).rotate_y(time_angle).translate(Vector3.Vector3().with_x(1)).rotate_z(time_angle)

        self._shape_set.clear()

        for line in self._lines:
            self._shape_set.add(transformation.transform(line))

