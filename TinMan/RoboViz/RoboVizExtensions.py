import sys


from RoboViz import Shape

class RoboVizExtensions:
    def transform(transformation_matrix, line):
        return Shape.Line(transformation_matrix.transform(line.end1),transformation_matrix.transform(line.end2),line.pixel_thickness,line.color)
        