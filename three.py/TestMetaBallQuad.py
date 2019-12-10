from core import *
from cameras import *
from geometry import *
from material import *
from helpers import *
from random import randint
from math import sin, cos

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
        self.gridGeo = MetaBallQuadGeometryBeta(xRes=50,yRes=50)
        self.gridGeo.fill_sector(2,3)
        self.gridGeo.fill_sector(2,4)
        self.gridGeo.remove_sector(2,3)
        #self.gridGeo.fill_all_sectors()
        #self.gridGeo.remove_all_sectors()
        material = SurfaceBasicMaterial()
        self.gridGeoMesh = Mesh(self.gridGeo,material)
        self.scene.add(self.gridGeoMesh)

        self.frameCounter = 0
        self.circleList = []
        self.circle = MetaCircle(25,12,5)
        self.circleList.append(self.circle)
        self.circleList.append(MetaCircle(25,7,6))
        print(self.circleList)

        self.time = 0
        

    def testMetaQuadEfficiency(self):
        remove = randint(0,1)
        x = randint(0,24)
        y = randint(0,24)
        
        if remove:
            self.gridGeo.remove_sector(x,y)
        else:
            self.gridGeo.fill_sector(x,y)
            
        
    def update(self):

        self.cameraControls.update()
        self.frameCounter += 1
        self.time += (1/60)
        ax = int(sin(self.time)*20 + 25)
        self.circle.set_position(ax, 12)

        #clear the list
        self.gridGeo.remove_all_sectors()

        for x in range(self.gridGeo.xRes):
            for y in range(self.gridGeo.yRes):
                point_sum = 0
                for circle in self.circleList:
                    point_sum += circle.get_value_of_point(x,y)
                    #if(circle.inside_circle(x,y)):
                    #    self.gridGeo.fill_sector(x,y,False)
                if(point_sum > 1):
                    self.gridGeo.fill_sector(x,y,False,False)
        self.gridGeo.updateAttributes()
            

        if self.frameCounter > 0:
            self.frameCounter = 0
            #self.testMetaQuadEfficiency()

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])
            
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestQuadGridGeometry().run()

