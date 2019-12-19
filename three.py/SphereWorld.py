from core import *
from cameras import *
from geometry import *
from material import *
from helpers import *

class SphereWorld(Base):
    
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
        #self.cameraControls = FirstPersonController(self.input, self.camera)

        ## setup a parent object for the camera to rotate around
        self.cameraController = Object3D()

        ## setup original position of the camera, so we have a reference and our matrix mults later do not edit this.
        self.originalCameraMatrix = MatrixFactory.makeCopy(self.camera.transform.matrix)

        ## initialize the surface for the sphere world
        sphere_texture= OpenGLUtils.initializeTexture('images/earth.jpg')
        self.sphere = Mesh(SphereGeometry(),SurfaceBasicMaterial(texture=sphere_texture))
        self.scene.add(self.sphere)
        
        self.cameraController.add(self.camera)

        
        floorMesh = GridHelper(size=10, divisions=10, gridColor=[0,0,0], centerColor=[1,0,0])
        floorMesh.transform.rotateX(-3.14/2, Matrix.LOCAL)
        ## self.scene.add(floorMesh)
        self.x_speed = 0.01
        self.y_speed = 0.01
        
    def update(self):

        #self.cameraControls.update()

        if self.input.isKeyPressed(pygame.K_w):
            print('w is pressed')
            self.cameraController.transform.rotateX(-self.x_speed, type=Matrix.LOCAL)
        if self.input.isKeyPressed(pygame.K_a):
            print('a is pressed')
            self.cameraController.transform.rotateY(-self.y_speed, type=Matrix.LOCAL)
        if self.input.isKeyPressed(pygame.K_s):
            print('s is pressed')
            self.cameraController.transform.rotateX(self.x_speed, type=Matrix.LOCAL)
        if self.input.isKeyPressed(pygame.K_d):
            print('d is pressed')
            self.cameraController.transform.rotateY(self.y_speed, type=Matrix.LOCAL)

        ## Custom parent child multiplication. This makes the camera move relative to the camera controllers position,
        ## based on the original position, because using the current position causes previous transformations to overlap
        ## rather than stop when they are done.
        self.camera.transform.matrix = self.cameraController.transform.matrix @ self.originalCameraMatrix
            

        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio( size["width"]/size["height"] )
            self.renderer.setViewportSize(size["width"], size["height"])
            
        self.renderer.render(self.scene, self.camera)
                    
# instantiate and run the program
SphereWorld().run()

