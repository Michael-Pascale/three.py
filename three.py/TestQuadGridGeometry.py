from core import *
from cameras import *
from geometry import *
from material import *
from helpers import *

class TestQuadGridGeometry(Base):
    
    def initialize(self):

        self.setWindowTitle('Test')
        self.setWindowSize(800,800)

        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25, 0.25, 0.25)
        
        self.scene = Scene()

        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 1, 5)
        self.camera.transform.lookAt(0, 0, 0)
        self.cameraControls = FirstPersonController(self.input, self.camera)

        
        floorMesh = GridHelper(size=10, divisions=10, gridColor=[0,0,0], centerColor=[1,0,0])
        floorMesh.transform.rotateX(-3.14/2, Matrix.LOCAL)
        self.scene.add(floorMesh)

        ## generate a QuadGridGeometry
        self.gridGeo = QuadGridGeometry(xRes=2,yRes=2,sectors={
            Pair(0,0):[1,2,4],
            Pair(1,1):[4,3,2],
            Pair(1,0):[1,2,3],
            Pair(0,1):[1,3,4]})
        material = SurfaceBasicMaterial()
        self.gridGeoMesh = Mesh(self.gridGeo,material)
        self.scene.add(self.gridGeoMesh)
        
    def update(self):

        self.cameraControls.update()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])
            
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestQuadGridGeometry().run()

