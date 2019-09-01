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

#This demo demonstrates the use of the new basic material, with speculaer flags activated
class TestReflectivePlane(Base):
	def initialize(self):
		
		self.setWindowTitle('Specular Light Demo')
		self.setWindowSize(720,480)
		
		self.renderer = Renderer()
		self.renderer.setViewportSize(720,480)
		self.renderer.setClearColor(0.25,0.25,0.25)
		self.renderer.shadowMapEnabled = True
		
		self.scene = Scene()
		
		
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
		discoTexture= OpenGLUtils.initializeTexture('images/mirror.jpg')
		material = PascaleSurfacePhongMaterial(objColor=[1,1,1], objTexture=discoTexture, usesFog = 1, fog_Color=[1,1,1])
		self.mesh = Mesh(geometry,material)
		#self.mesh.setCastShadow(True)
		
		self.scene.add(self.mesh)
		
		#add a floor to the scene
		floor_geometry = QuadGeometry(width=10,height=10)
		floor_texture = OpenGLUtils.initializeTexture('images/color-grid.png')
		floor_material = PascaleSurfaceBasicMaterial(color=[0,0,1])
		floor = Mesh(floor_geometry, floor_material)
		floor.transform.rotateX(-1.57,Matrix.GLOBAL)
		floor.transform.translate(y=-2)
		#floor.setReceiveShadow(True)
		self.scene.add(floor)
		
		#add something under the floor
		spheremesh = Mesh(geometry, PascaleSurfaceLambertMaterial())
		self.scene.add(spheremesh)
		spheremesh.transform.translate(y=0, x=-4, z=2)
		
		
		#add a mirror
		self.gui_render_target = RenderTarget.RenderTarget()
		self.gui_mesh = Mesh(QuadGeometry(width=2,height=2),ReflectiveMaterial(texture=self.gui_render_target.textureID))
		self.gui_mesh.transform.translate(x=-3)
		self.mirror_cam = PerspectiveCamera()
		gui_mesh_pos = self.gui_mesh.transform.getPosition()
		self.mirror_cam.transform.setPosition(gui_mesh_pos[0],gui_mesh_pos[1],gui_mesh_pos[2] + 0.25)
		self.camera_pos = self.camera.transform.getPosition()
		self.mirror_cam.transform.lookAt(self.camera_pos[0],self.camera_pos[1],self.camera_pos[2])
		#hard coded normal for now.
		self.normal = [0,0,1]
		self.distance_vec = np.subtract(self.camera_pos, self.mirror_cam.transform.getPosition())
		self.reflection = self.distance_vec - np.multiply(np.multiply((np.dot(self.distance_vec,self.normal)),2),self.normal)
		self.mirror_cam.transform.lookAt(self.reflection[0],self.reflection[1],self.reflection[2])
		self.scene.add(self.gui_mesh)
		
	def update(self):
		self.cameraControls.update()
		self.mesh.material.setUniform('vec3','viewPos',self.camera.transform.getPosition())
		
		#update mirror camera position
		
		self.camera_pos = self.camera.transform.getPosition()
		self.distance_vec = np.subtract(self.camera_pos, self.mirror_cam.transform.getPosition())
		mirror_cam_pos = self.mirror_cam.transform.getPosition()
		self.reflection = self.distance_vec - np.multiply(np.multiply((np.dot(self.distance_vec,self.normal)),2),self.normal)
		self.reflection = self.reflection * 2
		self.mirror_cam.transform.lookAt(-self.reflection[0],-self.reflection[1],-self.reflection[2])
		
		
		#get the cameras relative forward
		#This code is necssary for the shader to work, so it may be worthwhile to get this out of the main render loop somehow
		rotationMat = self.camera.transform.getRotationMatrix()
		globalForward = (0.0,0.0,1.0)
		cameraRelForward = rotationMat.dot(globalForward)
		self.mesh.material.setUniform('vec3','viewDir',cameraRelForward)
		
		if self.input.resize():
			size = self.input.getWindowSize()
			self.camera.setAspectRatio(size["width"]/size["height"])
			self.renderer.setViewportSize(size["width"],size["height"])
		
		#move camera to behind the mirror for the first rendering pass
		#distance = abs(self.camera.transform.getPosition()[2] -  self.gui_mesh.transform.getPosition()[2])
		#self.camera.transform.translate(z=-2*distance)
		#gui_mesh_pos = self.gui_mesh.transform.getPosition()
		#get old rotation matrix for resetting camera position
		#M = self.camera.transform.getRotationMatrix()
		#self.camera.transform.lookAt(gui_mesh_pos[0],gui_mesh_pos[1],gui_mesh_pos[2])
		self.renderer.render(self.scene,self.mirror_cam,self.gui_render_target)
		
		#move the camera back
		#self.camera.transform.translate(z=2*distance)
		#self.camera.transform.setRotationSubmatrix(M)
		self.renderer.render(self.scene,self.camera)
		#self.renderer.render(self.gui_mesh, self.camera, clearColor=False)
		#self.renderer.render(self.gui_mesh,self.camera)
	
TestReflectivePlane().run()
	
	