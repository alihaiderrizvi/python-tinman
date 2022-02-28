
import math

class TransformationMatrix:
    epsilon = 0.0001
    def __init__(self,*args):
        if len(args) == 1:
            args = tuple(args[0])
        if len(args) == 16:
            self._m00 = args[0]
            self._m01 = args[1]
            self._m02 = args[2]
            self._m03 = args[3]
            self._m10 = args[4]
            self._m11 = args[5]
            self._m12 = args[6]
            self._m13 = args[7]
            self._m20 = args[8]
            self._m21 = args[9]
            self._m22 = args[10]
            self._m23 = args[11]
            self._m30 = args[12]
            self._m31 = args[13]
            self._m32 = args[14]
            self._m33 = args[15]

    #properties

    def _get_identity(self):
        return TransformationMatrix(1,0,0,0,
                                    0,1,0,0,
                                    0,0,1,0,
                                    0,0,0,1)
    def _get_nan(self):
        return TransformationMatrix([math.nan for i in range(16)])

    identity = property(_get_identity)
    nan = property(_get_nan)

    #End region

    def translation(x,y,z):
        return TransformationMatrix(1,0,0,x,
                                    0,1,0,y,
                                    0,0,1,y,
                                    0,0,0,1)
    

    def get_transform_for_coordinate_axes(x_axis, y_axis, z_axis):
        return TransformationMatrix(x_axis.x, y_axis.x,z_axis.x,0,
                                    x_axis.y, y_axis.y,z_axis.y,0,
                                    x_axis.z, y_axis.z,z_axis.z,0,
                                    0,0,0,1)

    def translate(self,*args):
        if len(args) == 3:
            x,y,z = args[0],args[1],args[2]
            return Translation(x,y,z).multiply(self)
        if len(args) == 1:
            vector = args[0]
            return self.translate(vector.x,vector.y,vector.z)


    def rotate_x(self,angle):
        c = angle.cos
        s = angle.sin
        return TransformationMatrix(1,0,0,0,
                                    0,c,-s,0,
                                    0,s,c,0,
                                    0,0.0,1).multiply(self)

    def rotate_y(self,angle):
        c = angle.cos
        s = angle.sin
        return TransformationMatrix(c,0,s,0,
                                    0,1,0,0,
                                    -s,0,c,0,
                                    0,0,0,1).multiply(self)

    def rotate_z(self,angle):
        c = angle.cos
        s = angle.sin
        return TransformationMatrix(c,-s,0,0,
                                    s,c,0,0,
                                    0,0,1,0,
                                    0,0,0,1).multiply(self)

    
        

            
