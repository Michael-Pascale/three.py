from core import *
from cameras import *
from geometry import *
from material import *
from helpers import *
from components import *
from lights import *
from physics import *
import random
import numpy as np
import math

#The following demo does not use the Light materials from three py, but
#a much more simple shader just to show the specular lighting in action
#in python
class TestSpecularSimple(Base):
	def initialize(self):
		
		self.setWindowTitle('Specular Light Demo')
		self.setWindowSize(720,480)
		
		self.renderer = Renderer()
		self.renderer.setViewportSize(720,480)
		self.renderer.setClearColor(0.25,0.25,0.25)
		self.renderer.shadowMapEnabled = True
		
		self.scene = Scene()
		
		#add a point light to the screen
		self.light = PointLight(position = [3,2,0], color=[1,1,1])
		#self.light = DirectionalLight(color=[1,1,1], position = [3,2,0],direction=[-1,-1,-1],isSpecular=1)
		#self.scene.add(self.light)
		self.scene.add(PointLightHelper(self.light, radius=0.1))
		
		ambience = AmbientLight(color=[1,1,1],strength=0.05)
		self.scene.add(ambience)
		
		directionalLight = DirectionalLight(color=[1,1,1], position=[2,2,0], direction=[-2,-1,0])
		directionalLight.enableShadows(strength=0.5)
		directionalLight.shadowCamera.setViewRegion(left=-2,right=2,top=2,bottom=-5,near=10,far=3)
		#pointLight = PointLight(color=[1,1,1], position = [3,2,0])
		#self.scene.add(pointLight)
		self.scene.add(directionalLight)
		
		self.camera = PerspectiveCamera()
		self.camera.transform.setPosition(0,1,6)
		self.camera.transform.lookAt(0,0,0)
		self.camera.transform.setPosition(0,1,5)
		self.cameraControls = FirstPersonController(self.input,self.camera)
		
		#widthResolution = 16, heightResolution = 16
		#problem with normals in BoxGeometry?
		geometry = SphereGeometry()
		#geometry = OBJGeometry('models/fireflower.obj')
		shinyTexture=OpenGLUtils.initializeTexture("models/fireflower.png")
		discoTexture= OpenGLUtils.initializeTexture('images/color-grid.png')
		material = PascaleSurfacePhongMaterial(objColor=[1,1,1], objTexture=discoTexture, usesFog = 1, fog_Color=[1,1,1])
		self.mesh = Mesh(geometry,material)
		self.mesh.setCastShadow(True)
		
		self.scene.add(self.mesh)
		
		#self.mesh.transform.scaleUniform(0.0005)
		self.mesh.transform.translate(y=-1)
		
		#add a floor to the scene
		floor_geometry = QuadGeometry(width=10,height=10)
		#floor_geometry = BoxGeometry()
		floor_texture = OpenGLUtils.initializeTexture('images/color-grid.png')
		floor_material = PascaleSurfaceBasicMaterial(texture=floor_texture)
		floor = Mesh(floor_geometry, floor_material)
		floor.transform.rotateX(-1.57,Matrix.GLOBAL)
		#floor.transform.scaleUniform(10)
		floor.transform.translate(y=-2)
		floor.setReceiveShadow(True)
		self.scene.add(floor)
		
		
		#light position uniform
		#self.lightPos = (0.0,3.0,4.0)
		self.time = 0
		self.dt = 1/60.0
		
	def update(self):
		self.cameraControls.update()
		
		
		self.time += self.dt
		#update position of the light
		#self.lightPos = (3*math.cos(self.time*1),0.25,3*math.sin(self.time*1))
		self.light.transform.rotateY(0.013, Matrix.GLOBAL)
		self.mesh.material.setUniform('vec3','viewPos',self.camera.transform.getPosition())
		#self.mesh.material.setUniform('vec3','lightPosition',np.asarray(self.lightPos))
		
		
		#get the cameras relative forward
		rotationMat = self.camera.transform.getRotationMatrix()
		globalForward = (0.0,0.0,1.0)
		cameraRelForward = rotationMat.dot(globalForward)
		self.mesh.material.setUniform('vec3','viewDir',cameraRelForward)
		#print(cameraRelForward)
		
		if self.input.resize():
			size = self.input.getWindowSize()
			self.camera.setAspectRatio(size["width"]/size["height"])
			self.renderer.setViewportSize(size["width"],size["height"])
		
		self.renderer.render(self.scene,self.camera)
	
TestSpecularSimple().run()
	
	