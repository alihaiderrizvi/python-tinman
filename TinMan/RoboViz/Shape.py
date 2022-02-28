import sys,math

from Geometry import Vector3


class Shape:
    def __init__(self):
        self._is_visible = True
        self.shape_set = None
    
    def is_visible_setter(self,value):
        if value == self.is_visible:
            return
        else:
            self._is_visible = value
            self.set_dirty()

    is_visible = property(self._is_visible, self.is_visible_setter)

    def remove(self):
        if self.shape_set == None:
            raise(BaseException('This shape cannot be removed as it is not currently contained within a shapeset.'))
        self.shape_set.remove()

    def set_shape_set(self, shape_set): 
        if shape_set == None:
            raise(BaseException('shape_set'))
        if self.shape_set == None:
            raise(BaseException('Shape already belongs to Shapeset' + str(self.shape_set.path) + ' so cannot be added to ' + str(shape_set.path)))
        self.shape_set = shape_set

    def clear_set_shape_set(self):
        if self.shape_set == None:
            raise(BaseException('Shape doesnt belong to a shapeSet'))
        self.shape_set = None

    def set_dirty(self):
        if self.shape_set != None:
            self.shape_set.is_dirty = True

    def write_double(buf, offset, d):
        assert not math.isnan(d) , 'Float value may not be Nan'
        s = str(round(d,6))
        s = [0:min(len(s),6)]
        assert len(s) == 6, 'Formatting of float value ' + str(d) + ' should be 6 characters long but was ' + str(len(s))
        bytes_temp = bytes(s[0:6], 'ascii')
        bytes_count = len(bytes_temp)
        for i in range(len(bytes_temp)):
            buf[offset+i] = bytes_temp[i]
        assert bytes_count == 6, 'Should have 6 bytes but instead have' + str(bytes_count)
    
    def write_color(buf,offset,color, include_alpha):
        buf[offset+1] = color.R
        buf[offset+2] = color.G
        buf[offset+3] = color.B
        if include_alpha:
            buf[offset+4] = color.A
    
    def validate_double(value):
        if math.isnan(value):
            raise(BaseException('Value' + str(value) + 'Cannot be NaN')
        if math.isinf(value):
            raise(BaseException('value' + str(value) + 'cannot be infinite'))

class Dot(Shape):

    def __init__(self, pixel_size = 5, color = color.white, position = Vector3.Vector3()):
        self._pixel_size = pixel_size
        self._color = color
        self.position = position
        self._x = self.position.x
        self._y = self.position.y
        self._z = self.position.z
        super().__init__()

    def _pixel_size_setter_(self,value):
        super(Dot,Dot).validate_double(value)
        self._pixel_size = value
        self.set_dirty()

    pixel_size = property(self._pixel_size, self._pixel_size_setter_)

    def _color_setter_(self,value):
        self._color = value
        self.set_dirty()

    color = property(self._color, self._color_setter_)

    def _position_setter(self, value):
        self._x = value.x
        self._y = value.y
        self._z = value.z
    
    position = property(Vector3(self.x,self.y,self.z),self._position_setter)

    def _x_setter(self,value):
        super(Dot,Dot).validate_double(value)
        self._x = value
        self.set_dirty()

    def _y_setter(self,value):
        super(Dot,Dot).validate_double(value)
        self._y = value
        self.set_dirty()

    def _z_setter(self,value):
        super(Dot,Dot).validate_double(value)
        self._z = value
        self.set_dirty()

    x = property(self._x, self._x_setter)
    y = property(self._y, self._y_setter)
    z = property(self._z, self._z_setter)

    def translate(self,offset):
        self.position += offset
    
    def send_message(self, udp_client):
        path_bytes = self.shape_set.path_bytes
        num_bytes = 30 + len(path_bytes)
        buf = [None for i in range(num_bytes)]
        buf[0] = 1
        buf[1] = 2
        super(Dot,Dot).write_double(buf,2, self._x)
        super(Dot,Dot).write_double(buf,8, self._y)
        super(Dot,Dot).write_double(buf,14, self._z)
        super(Dot,Dot).write_double(buf,20, self.pixel_size)
        super(Dot,Dot).write_color(buf,26,color, False)
        for i in range(len(path_bytes)):
            buf[29+i] = path_bytes[i]
        bytes_sent_count = udp_client.send(buf, len(buf))
        assert bytes_sent_count == num_bytes


class Line(Shape):

    def __init__(self, end1 = Vector3.Vector3(), end2 = Vector3.Vector3(), pixel_thickness = 1, color = color.white):
        self._pixel_thickness = pixel_thickness 
        self._color = color
        self.end1 = end1
        self._x1 = end1.x
        self._y1 = end1.y
        self._z1 = end1.z 
        self.end2 = end2
        self._x2 = end2.x
        self._y2 = end2.y
        self._z3 = end2.z
        super().__init()

    def _end1_setter(self,value):
        self.x1 =  value.x
        self.y1 = value.y
        self.z1 = value.z

    end1 = property(Vector3.Vector3(self._x,self._y,self._z), self._end1_setter)

    def _end2_setter(self,value):
        self.x2 =  value.x
        self.y2 = value.y
        self.z2 = value.z

    end2 = property(Vector3.Vector3(self._x,self._y,self._z), self._end2_setter)

    def _x1_setter(self,value):
        super(Line,Line).validate_double(value)
        self._x1 = value
        self.set_dirty()

    x1 = property(self._x1, self._x1_setter)

    def _y1_setter(self,value):
        super(Line,Line).validate_double(value)
        self._y1 = value
        self.set_dirty()

    y1 = property(self._y1, self._y1_setter)

    def _z1_setter(self,value):
        super(Line,Line).validate_double(value)
        self._z1 = value
        self.set_dirty()

    z1 = property(self._z1, self._z1_setter)

    def _x2_setter(self,value):
        super(Line,Line).validate_double(value)
        self._x2 = value
        self.set_dirty()

    x2 = property(self._x2, self._x2_setter)

    def _y2_setter(self,value):
        super(Line,Line).validate_double(value)
        self._y2 = value
        self.set_dirty()

    y2 = property(self._y2, self._y2_setter)

    def _z2_setter(self,value):
        super(Line,Line).validate_double(value)
        self._z2 = value
        self.set_dirty()

    z2 = property(self._z2, self._z2_setter)

    def _pixel_thickness_setter(self, value):
        super(Line,Line).validate_double(value)
        self._pixel_thickness = value
        self.set_dirty()

    pixel_thickness = property(self._pixel_thickness, self._pixel_thickness_setter)

    def _color_setter(self, value):
        self._color = color
        self.set_dirty()

    color = property(self._color, self._color_setter)

    def translate(self,offset):
        self.end1 += offset
        self.end2 += offset

    def send_message(self, udp_client):
        path_bytes = self.shape_set.path_bytes
        num_bytes = 48 + len(path_bytes)
        buf = [i for i in range(num_bytes)]

        buf[0] = 1
        buf[1] = 1
        super(Line,Line).write_double(buf,2, self._x1)
        super(Line,Line).write_double(buf,8, self._y1)
        super(Line,Line).write_double(buf,14, self._z1)
        super(Line,Line).write_double(buf,20, self._x2)
        super(Line,Line).write_double(buf,26, self._y2)
        super(Line,Line).write_double(buf,32, self._z2)
        super(Line,Line).write_double(buf,38, self.pixel_thickness)
        super(Line,Line).write_color(buf, 44, color, False)
        for i in range(len(path_bytes)):
            buf[47+i] = path_bytes[i]
        bytes_sent_count = udp_client.sent(buf, len(buf))
        assert bytes_sent_count == num_bytes

        
class Polygon(Shape):

    def __init__(self, vertices = [], color = color.white):
        if len(vertices) > 255:
            raise(BaseException('Polygon may have no more than 255 vertices'))
        self._vertices = vertices
        self._color = color

    def _color_setter(self, value):
        self._color = value
        self.set_dirty()

    color = property(self._color, self._color_setter)

    def __getitem__(self,index):
        return self._vertices[index]
    
    def __setitem__(self,index, value):
        self._vertices.__setitem__(index, value)
        self.set_dirty()
    
    def add(self, vertex):
        self._vertices.append(vertex)
        self.set_dirty()

    def add_range(self,vertices):
        self._vertices.extend(vertices)
        self.set_dirty()

    def remove_at(self,index):
        del self._vertices[index]
        self.set_dirty()

    def insert_at(self, index, vertex):
        self._vertices.insert(index,vertex)
        self.set_dirty()

    def clear(self):
        del self._vertices
        self._vertices = []
        self.set_dirty()

    def translate(self, offset):
        if offset == Vector3.Vector3():
            return
        for var in range(0, len(self._vertices)):
            self._vertices += offset
        self.set_dirty()
    
    def send_message(self, udp_client):
        path_bytes = self.shape_set.path_bytes
        num_bytes = (18*len(self._vertices)) + 8 + len(path_bytes)
        buf = [None for i in range(num_bytes)]
        buf[0] = 1
        buf[1] = 4
        buf[2] = bytes(len(self._vertices))
        super(Polygon,Polygon).write_color(buf, 3, self.color, True)

        offset = 7

        for vertex in self._vertices:
            super(Polygon,Polygon).write_double(buf,offset,vertex.x)
            offset += 6
            super(Polygon,Polygon).write_double(buf,offset,vertex.y)
            offset += 6
            super(Polygon,Polygon).write_double(buf,offset,vertex.z)
            offset += 6

        for i in range(len(path_bytes)):
            buf[offset+i] = path_bytes[i]
        
        bytes_sent_count = udp_client.send(buf, len(buf))
        assert bytes_sent_count == num_bytes

class Circle(Shape):

    def __init__(self, x = 0, y = 0, radius_metre = 0.5, pixel_thickness = 5, color = color.white):
        self._center_x = x
        self._center_y = y
        self._radius_metres = radius_metre
        self._pixel_thickness = pixel_thickness
        self._color = color

    def _center_x_setter(self,value):
        super(Circle,Circle).validate_double(value)
        self._center_x = value
        self.set_dirty()

    center_x = property(self._center_x, self._center_x_setter)

    def _center_y_setter(self,value):
        super(Circle,Circle).validate_double(value)
        self._center_y = value
        self.set_dirty()

    center_y = property(self._center_y, self._center_y_setter)

    def _radius_metres_setter(self,value):
        super(Circle,Circle).validate_double(value)
        self.radius_metres = value
        self.set_dirty()

    radius_metres = property(self._radis_metres, self._radius_metres_setter)

    def _pixel_thickness_setter(self,value):
        super(Circle,Circle).validate_double(value)
        self._pixel_thickness = value
        self.set_dirty()

    pixel_thickness = property(self._pixel_thickness, self._pixel_thicnkess_setter)

    def _color_setter(self,value):
        self._color = value
        self.set_dirty()

    color = property(self._color, self._color_setter)

    def translate(self, offset):
        self._center_x += offset.x
        self._center_y += offset.y
        self.set_dirty()

    def send_message(self, udp_client):
        path_bytes = self.shape_set.path_bytes
        num_bytes = 30 + len(path_bytes)
        buf = [None for i in range(num_bytes)]

        buf[0] = 1
        super(Circle,Circle).write_double(buf,2, self.center_x)
        super(Circle,Circle).write_double(buf,8, self.center_y)
        super(Circle,Circle).write_double(buf,14, self.radius_metres)
        super(Circle,Circle).write_double(buf,20, self.pixel_thickness)
        super(Circle,Circle).write_color(buf,26, self.color, False)

        for i in range(len(path_bytes)):
            buf[i+29] = path_bytes[i]
        
        bytes_sent_count = udp_client.send(buf, len(buf))
        assert bytes_sent_count == num_bytes

class Sphere(Shape):

    def __init__(self, center = Vector3.Vector3(), radius_metres = 0.5, color = color.white):
        self._radius_metres = radius_metres
        self._center = center
        self._x = center.x
        self._y = center.y
        self._z = center.z
        self._color = color
    
    def _radius_metres_setter(self, value):
        super(Sphere,Sphere).validate_double(value)
        self._radius_metres = value
        self.set_dirty()

    radius_metres = property(self._radius_metres, self._radius_metres_setter)

    def _color_setter(self, value):
        self._color = value
        self.set_dirty()

    color = property(self._color, self._color_setter)

    def _center_setter(self, value):
        self.x = value.x
        self.y = value.y
        self.z = value.z
    
    center = property(Vector3.Vector3(self.x,self.y,self.z), self._center_setter)

    def _x_setter(self,value):
        super(Sphere,Sphere).validate_double(value)
        self._x = value
        self.set_dirty()

    x = property(self._x, self._x_setter)

    def _y_setter(self,value):
        super(Sphere,Sphere).validate_double(value)
        self._y = value
        self.set_dirty()

    y = property(self._y, self._y_setter)

    def _z_setter(self,value):
        super(Sphere,Sphere).validate_double(value)
        self._z = value
        self.set_dirty()

    z = property(self._z, self._z_setter)

    def translate(self, offset):
        self.center += offset

    def send_message(self,udp_client):
        path_bytes = self.shape_set.path_bytes
        num_bytes = 30 + len(path_bytes)
        buf = [None for i in range(num_bytes)]

        buf[0] = 1
        buf[1] = 3

        super(Sphere,Sphere).write_double(buf,2,self.center.x)
        super(Sphere,Sphere).write_double(buf,8,self.center.y)
        super(Sphere,Sphere).write_double(buf,14,self.center.z)
        super(Sphere,Sphere).write_double(buf,20,self.radius_metres)
        super(Sphere,Sphere).write_color(buf,26,self.color, False)

        for i in range(len(path_bytes)):
            buf[29+i] = path_bytes[i]

        bytes_sent_count = udp_client.send(buf, len(buf))
        assert bytes_sent_count == num_bytes

class FieldAnnotation(Shape):

    def __init__(self, position = Vector3.Vector3(), text = '', color = color.white):
        self._text = text
        self._text_bytes = None
        self._color = color
        self.position = position
        self._x = position.x
        self._y = position.y
        self._z = position.z

    def _color_setter(self, value):
        if self._color ==value:
            return
        else:
            self._color = value
            self.set_dirty()

    color = property(self._color, self._color_setter)

    def _position_setter(self, value):
        self.x = value.x
        self.y = value.y
        self.z = value.z

    position = property(Vector3.Vector3(self.x,self.y, self.z), self._position_setter)

    def _x_setter(self,value):
        super(FieldAnnotation,FieldAnnotation).validate_double(value)
        self._x = value
        self.set_dirty()

    x = property(self._x, self._x_setter)

    def _y_setter(self,value):
        super(FieldAnnotation,FieldAnnotation).validate_double(value)
        self._y = value
        self.set_dirty()

    y = property(self._y, self._y_setter)

    def _z_setter(self,value):
        super(FieldAnnotation,FieldAnnotation).validate_double(value)
        self._z = value
        self.set_dirty()

    z = property(self._z, self._z_setter)

    def _text_setter(self, value):
        if self._text == value:
            return
        self._text = value
        self._text_bytes = None
        self.set_dirty()

    text = property(self._text, self._text_setter)

    def _text_bytes_getter(self,value):
        if self._text_bytes != None:
            return self._text_bytes
        else:
            self._text_bytes = bytes(self.text)
            return self._text_bytes
    
    text_bytes = property(self._text_bytes_getter)

    def translate(self, offset):
        self.position += offset

    def send_message(self, udp_client):

        if len(self.text_bytes) == 0:
            return
        path_bytes = self.shape_set.path_bytes
        num_bytes = 25 + len(path_bytes) + len(self.text_bytes)
        buf = [None for i in range(num_bytes)]

        buf[0] = 2
        buf[1] = 0

        super(FieldAnnotation,FieldAnnotation).write_double(buf,2,self.x)
        super(FieldAnnotation,FieldAnnotation).write_double(buf,8,self.y)
        super(FieldAnnotation,FieldAnnotation).write_double(buf,14,self.z)
        super(FieldAnnotation,FieldAnnotation).write_color(buf,20,color, False)
        for i in range(len(self.text_bytes)):
            buf[i+23] = self.text_bytes[i]
        for i in range(len(path_bytes)):
            buf[24+ len(self.text_bytes)+ i] = path_bytes[i]

        bytes_sent_count = udp_client.send(buf, len(buf))
        assert bytes_sent_count == num_bytes

        







    