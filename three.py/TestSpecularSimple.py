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
		
		self.scene = Scene()
		
		#add a point light to the screen
		self.light = PointLight(position = [3,2,0], color=[1,1,1])
		#self.light = DirectionalLight(color=[1,1,1], position = [3,2,0],direction=[-1,-1,-1],isSpecular=1)
		self.scene.add(self.light)
		self.scene.add(PointLightHelper(self.light, radius=0.1))
		
		ambience = AmbientLight(color=[1,1,1],strength=0.05)
		self.scene.add(ambience)
		
		directionalLight = DirectionalLight(color=[1,1,1], position = [3,2,0],direction=[-1,-1,-1])
		#pointLight = PointLight(color=[1,1,1], position = [3,2,0])
		#self.scene.add(pointLight)
		#self.scene.add(directionalLight)
		
		self.camera = PerspectiveCamera()
		self.camera.transform.setPosition(0,1,6)
		self.camera.transform.lookAt(0,0,0)
		self.camera.transform.setPosition(0,1,5)
		self.cameraControls = FirstPersonController(self.input,self.camera)
		
		#widthResolution = 16, heightResolution = 16
		#problem with normals in BoxGeometry?
		geometry = OBJGeometry('models/fireflower.obj')
		shinyTexture=OpenGLUtils.initializeTexture("models/fireflower.png")
		material = SpecularMaterial(color=[1,1,1], texture=shinyTexture, isSpecular=1, useFog = 1, fogColor=[1,1,1])
		self.mesh = Mesh(geometry,material)
		
		self.scene.add(self.mesh)
		
		self.mesh.transform.scaleUniform(0.0005)
		self.mesh.transform.translate(y=-1)
		
		
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
	
	