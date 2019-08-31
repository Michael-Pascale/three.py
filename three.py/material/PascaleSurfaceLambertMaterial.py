from OpenGL.GL import *
from core import OpenGLUtils
from material import PascaleSurfaceBasicMaterial

#This material demonstrates specular lighting
#tutorial found online courtesy (https://learnopengl.com/Lighting/Basic-Lighting)
class PascaleSurfaceLambertMaterial(PascaleSurfaceBasicMaterial):
	def __init__(self, objColor=[1,1,1], objAlpha=1,objTexture=None,usesFog=0,fogStartDistance=5,fogEndDistance=15,fog_Color=[1,1,1]):
		super().__init__(objColor,objAlpha,objTexture,0,usesFog,fogEndDistance,fogEndDistance,fog_Color,1)