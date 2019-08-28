from core import *
from cameras import *
from geometry import *
from material import *
from helpers import *
from components import *
from lights import *
from physics import *
import random
#NOTE: this test was for internal testing, for a more detailed explanation of what is going on
#look at TestCollisionDetection
class TestPhong(Base):
    
    def initialize(self):

        self.setWindowTitle('Phong Lighting')
        self.setWindowSize(800,800)

        self.renderer = Renderer()
        self.renderer.setViewportSize(800,800)
        self.renderer.setClearColor(0.25, 0.25, 0.25)

        
        self.scene = Scene()

        self.light = PointLight(position = [0,3,0],strength = 0.5)
        self.scene.add(self.light)
        ambient = AmbientLight(color = [0.5,0.3,0.6],strength = 0.25)
        self.scene.add(ambient)

        self.camera = PerspectiveCamera()
        self.camera.transform.setPosition(0, 1, 6)
        self.camera.transform.lookAt(0, 0, 0)
        self.camera.transform.setPosition(0,1,5)
        self.cameraControls = FirstPersonController(self.input, self.camera)
        
        geometry = SphereGeometry()
        material = SurfacePhongMaterial()
        self.Mesh1 = ComponentMesh(geometry,material)
        sphere = Sphere(radius=1,center=self.Mesh1.transform.getPosition())
        self.Mesh1.addComponent("Sphere",sphere)
        self.scene.add(self.Mesh1)

        #create a plane, not attached to any object/mesh, just floating in space
        #self.plane = Plane(normal = (-1,0,0), offset = 3)

       

        
        floorMesh = GridHelper(size=10, divisions=10, gridColor=[0,0,0], centerColor=[1,0,0])
        floorMesh.transform.rotateX(-3.14/2, Matrix.LOCAL)
        self.scene.add(floorMesh)
        self.time = 0

        self.pause = False
        
    def update(self):

        self.cameraControls.update()
        

        if not self.pause:
            self.time = self.time + 1/60.0
            #self.light.position = [math.cos(self.time)*3, math.sin(self.time)*3,0.0]
            self.light.transform.setPosition(0.0, math.sin(self.time)*10,math.cos(self.time)*10)
            
        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])

        if self.input.isMousePressed():
            self.pause = not self.pause
            
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
TestPhong().run()

