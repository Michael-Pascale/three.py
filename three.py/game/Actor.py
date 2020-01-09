## actor class - contains a mesh containing player information
from geometry import BoxGeometry
from material import SurfaceBasicMaterial
class Actor(object):
    ## stage - pass the stage to add the player to
    def __init__(self, stage,geometry=BoxGeometry(),material=SurfaceBasicMaterial()):
        super().__init__()
        self.geometry=geometry
        self.material = material
        self.mesh = Mesh(geometry, material)
        ## initialize mesh
        self.stage = stage
        self.stage.add(self)
