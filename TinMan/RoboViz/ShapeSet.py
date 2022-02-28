import sys,math

from Geometry import Vector3

class ShapeSet:
    def __init__(self, name):
        if name == None:
            raise(BaseException("Name"))
        if not name.strip():
            raise(BaseException('Must Be non-blank, name'))
        if name.index('.') != -1:
            raise(BaseException('Cannot contain the "." character. If you wish to represesnt hierarchy, use nested ShapeSet objects.'))
        self._name = name

        self._shapes = []
        self._subsets = []
        self._parent_set = None
        self._parent_root = None
        self._path = None
        self._path_bytes = None
    
    subsets = property(self._subsets)

    def _path_getter_(self):
        if self._path == None:
            if self._parent_set != None:
                self._path = self._parent_set.path + '.' + self._name
            elif self._parent_root != None:
                self._path = self._parent_root.path + '.'  + self._name if len(self._parent_root.path) == 0 else self._name
            else:
                raise(BaseException('Cannot determine path for a shapeset that does not have a RoboVizRemote at the root of its hierarchy'))
            return self._path

    path = property(self._path_getter_)

    def add(self, shape):
        if type(shape) == Shape:
            if shape == None:
                raise(BaseException('shape'))
            self._shapes.append(shape)
            shape.set_shape_set(self)
            self.is_dirty = True
        elif type(shape) == ShapeSet:
            if shape == None:
                raise(BaseException('shapes2'))
            self._subsets.append(shape)
            shape.set_parent(self)

    def add_range(self, shapes):
        if shapes == None:
            raise(BaseException('shapes'))
        for shape in shapes:
            self.add(shape)

    def clear(self):
        del self._shapes
        self._shapes = list()
        self.is_dirty = True

    def translate(self, offset):
        if offset == Vector3.Vector3():
            return
        for shape in self._shapes:
            shape.translate(offset)
        for subset in self._subsets:
            subset.translate(offset)
    
    def remove(self, shape):
        if shape == None:
            raise(BaseException('shape'))
        if shape in self._shapes:
            self._shapes.remove(shape)
        else:
            raise(BaseException('Cannot remove the shape as it is not contained in this shapeset'))
        
        shape.clear_set_shape_set()
        self.is_dirty = True

    def _path_bytes_getter(self):
        if self._path_bytes == None:
            self._path_bytes = bytes(self.path, 'ascii')

    path_bytes = property(_path_bytes_getter)
    
    def set_parent(self, parent):
        
        if parent == None:
            raise(BaseException('Parent'))
        if self._parent_set != None or self._parent_root != None:
            raise(BaseException('Parent has already been set'))
        if type(parent) == ShapeSet:
            self._parent_set = parent
        elif type(parent) == RoboVizRemote:
            self._parent_root = parent

    def flush_messages(self, udp_client):
        for shape in self._shapes:
            if shape.is_visible:
                shape.send_message(udp_client)
        for set in self._subsets:
            set.flush_messages(udp_client)
        self.is_dirty  = False
    
