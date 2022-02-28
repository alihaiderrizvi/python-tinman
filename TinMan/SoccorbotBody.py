from Hinge import Hinge
from Geometry.angles import Angle

class SoccerbotBody:
    rsg_path = "rsg/agent/soccerbot058/soccerbot.rsg"
    def __init__(self):
        self.hj1 = Hinge('hj1', 'he1',  Angle.from_degree(-120),Angle.from_degree(120))
        self.hj2 = Hinge('hj2', 'he2',  Angle.from_degree(-45),Angle.from_degree(45))

        self.laj1 = Hinge('laj1', 'lae1',  Angle.from_degree(-90),Angle.from_degree(180))
        self.laj2 = Hinge('laj2', 'lae2',  Angle.from_degree(-10),Angle.from_degree(180))
        self.laj3 = Hinge('laj3', 'lae3',  Angle.from_degree(-135),Angle.from_degree(135))
        self.laj4 = Hinge('laj4', 'lae4',  Angle.from_degree(-10),Angle.from_degree(130))

        self.raj1 = Hinge('raj1', 'rae1',  Angle.from_degree(-90),Angle.from_degree(180))
        self.raj2 = Hinge('raj2', 'rae2',  Angle.from_degree(-180),Angle.from_degree(10))
        self.raj3 = Hinge('raj3', 'rae3',  Angle.from_degree(-135),Angle.from_degree(135))
        self.raj4 = Hinge('raj4', 'rae4',  Angle.from_degree(-10),Angle.from_degree(130))

        self.llj1 = Hinge('llj1', 'lle1',  Angle.from_degree(-60),Angle.from_degree(90))
        self.llj2 = Hinge('llj2', 'lle2',  Angle.from_degree(-45),Angle.from_degree(120))
        self.llj3 = Hinge('llj3', 'lle3',  Angle.from_degree(-45),Angle.from_degree(75))
        self.llj4 = Hinge('llj4', 'lle4',  Angle.from_degree(-160),Angle.from_degree(10)) 
        self.llj5 = Hinge('llj5', 'lle5',  Angle.from_degree(-90),Angle.from_degree(905))
        self.llj6 = Hinge('llj6', 'lle6',  Angle.from_degree(-45),Angle.from_degree(45))
        

        self.rlj1 = Hinge('rlj1', 'rle1',  Angle.from_degree(-90),Angle.from_degree(60))
        self.rlj2 = Hinge('rlj2', 'rle2',  Angle.from_degree(-45),Angle.from_degree(120))
        self.rlj3 = Hinge('rlj3', 'rle3',  Angle.from_degree(-75),Angle.from_degree(45))
        self.rlj4 = Hinge('rlj4', 'rle4',  Angle.from_degree(-160),Angle.from_degree(10))
        self.rlj5 = Hinge('rlj5', 'rle5',  Angle.from_degree(-90),Angle.from_degree(90))
        self.rlj6 = Hinge('rlj6', 'rle6',  Angle.from_degree(-45),Angle.from_degree(45))

        self.all_hinges = [
            self.hj1, self.hj2,
            self.raj1, self.raj2, self.raj3, self.raj4,
            self.laj1, self.laj2, self.laj3, self.laj4,
            self.rlj1, self.rlj2, self.rlj3, self.rlj4, self.rlj5, self.rlj6,
            self.llj1, self.llj2, self.llj3, self.llj4, self.llj5, self.llj6
        ] 
        
    def get_hinge_for_effector_label(self, effector_label):
        return [i for i in self.all_hinges if i.effector_label == effector_label][0]
    
    def convert_camera_polar_to_local_vector(self, camera_view):
        return camera_view.to_vector3()

               