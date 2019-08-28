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
		
		self.camera = PerspectiveCamera()
		self.camera.transform.setPosition(0,1,6)
		self.camera.transform.lookAt(0,0,0)
		self.camera.transform.setPosition(0,1,5)
		self.cameraControls = FirstPersonController(self.input,self.camera)
		
		#widthResolution = 16, heightResolution = 16
		#problem with normals in BoxGeometry?
		geometry = BoxGeometry(widthResolution = 16, heightResolution = 16)
		material = SpecularMaterial()
		self.mesh = Mesh(geometry,material)
		
		self.scene.add(self.mesh)
		
	def update(self):
		self.cameraControls.update()
		self.mesh.material.setUniform('vec3','viewPos',self.camera.transform.getPosition())
		
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
	
	