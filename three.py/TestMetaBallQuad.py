from core import *
from cameras import *
from geometry import *
from material import *
from helpers import *
from random import randint

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
        self.gridGeo = MetaBallQuadGeometryBeta(xRes=250,yRes=250)
        self.gridGeo.fill_sector(2,3)
        self.gridGeo.fill_sector(2,4)
        self.gridGeo.remove_sector(2,3)
        #self.gridGeo.fill_all_sectors()
        #self.gridGeo.remove_all_sectors()
        material = SurfaceBasicMaterial()
        self.gridGeoMesh = Mesh(self.gridGeo,material)
        self.scene.add(self.gridGeoMesh)

        self.frameCounter = 0

    def testMetaQuadEfficiency(self):
        remove = randint(0,1)
        x = randint(0,249)
        y = randint(0,249)
        
        if remove:
            self.gridGeo.remove_sector(x,y)
        else:
            pass
            #self.gridGeo.fill_sector(x,y)
            
        
    def update(self):

        self.cameraControls.update()
        self.frameCounter += 1

        if self.frameCounter > 1:
            self.frameCounter = 0
            self.testMetaQuadEfficiency()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])
            
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestQuadGridGeometry().run()

