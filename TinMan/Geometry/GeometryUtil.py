

class GeometryUtil:
    def calculate_distance_along_line_that_is_closest_to_point(origin, direction, point):
        v = direction.normalize()
        s = v.cross(vector3(0,0,1))
        u = ((s.x/s.y)*(origin.y-point.y) + (point.x - origin.x))/(v.x-(s.x/s.y)*v.y)
        return (orgin + v*u -point).length        
