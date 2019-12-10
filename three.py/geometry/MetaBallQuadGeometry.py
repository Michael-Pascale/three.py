from geometry import *
from math import pi, sin, cos, radians
from mathutils import Surface
import numpy as np

class MetaBallQuadGeometryBeta(Geometry):
    point_to_vertex = {
        1: [-0.5,-0.5,0],
        2: [0.5,-0.5,0],
        3: [0.5,0.5,0],
        4: [-0.5,0.5,0]
        }
    point_to_uv = {
        1: [0.0,0.0],
        2: [1.0,0.0],
        3: [1.0,1.0],
        4: [0.0,1.0]
        }
    def __init__(self, xRes=1, yRes=1, xSize=1, ySize=1):
        super().__init__()
        self.xRes = xRes
        self.yRes = yRes
        self.xSize = xSize
        self.ySize = ySize

        self.width = self.xSize / self.xRes
        self.height = self.ySize / self.yRes

        self.vertexPositionData = []
        self.vertexUVData = []
        self.vertexNormalData = []

        self.vertexCount = len( self.vertexPositionData )
        
        self.setAttribute("vec3", "vertexPosition", self.vertexPositionData)
        self.setAttribute("vec2", "vertexUV", self.vertexUVData)
        self.setAttribute("vec3", "vertexNormal", self.vertexNormalData)

        self.filledSectors = {}
        self.numSectors = 0

    def fill_sector(self, x, y, update=True, search=True):
        if search:
            if([x,y] in self.filledSectors.values()):
                return
        
        A = [x*self.width-self.width/2,
             y*self.height - self.height/2,
             0]
        B = [x*self.width+self.width/2,
             y*self.height - self.height/2,
             0]
        C = [x*self.width+self.width/2,
             y*self.height + self.height/2,
             0]
        D = [x*self.width-self.width/2,
             y*self.height + self.height/2,
             0]

        self.vertexPositionData.extend([A,B,C])
        self.vertexPositionData.extend([A,C,D])
        
        self.vertexUVData.extend([self.point_to_uv[1],self.point_to_uv[2],
                                         self.point_to_uv[3]])
        self.vertexUVData.extend([self.point_to_uv[1],self.point_to_uv[3],
                                         self.point_to_uv[4]])

        A = np.array(A)
        B = np.array(B)
        C = np.array(C)
        D = np.array(D)
        v1 = B-A
        v2 = C-A
        normal = np.cross(v1,v2)
        normal = normal / np.linalg.norm(normal)
        normal = list(normal)
        self.vertexNormalData.extend([normal,normal,normal])
        v1 = C-A
        v2 = D-A
        normal = np.cross(v1,v2)
        normal = normal / np.linalg.norm(normal)
        normal = list(normal)
        self.vertexNormalData.extend([normal,normal,normal])

        self.filledSectors[self.numSectors] = [x,y]
        self.numSectors += 1
        if update:
            self.updateAttributes()

    def remove_sector(self, x, y, update=True):
        if([x,y] not in self.filledSectors.values()):
            return False
        the_key = -1
        for key, value in self.filledSectors.items():
            if([x,y] == value):
                the_key = key
        

        if(the_key == -1):
            return False

        

        index = the_key*6
        
        del self.vertexPositionData[index:index+6]
        del self.vertexUVData[index:index+6]
        del self.vertexNormalData[index:index+6]
        

        self.filledSectors.pop(the_key, None)
        self.numSectors -= 1

        new_dict = {}
        for key, value in self.filledSectors.items():
            if(key < the_key):
                new_dict[key] = value
            else:
                new_dict[key-1] = value

        self.filledSectors = new_dict
        if update:
            self.updateAttributes()

    def updateAttributes(self):
        self.vertexCount = len( self.vertexPositionData )

        self.updateAttribute("vertexPosition", self.vertexPositionData)
        self.updateAttribute("vertexUV", self.vertexUVData)
        self.updateAttribute("vertexNormal", self.vertexNormalData)

    def fill_all_sectors(self):
        ## re write to not update attributes
        for x in range(self.xRes):
            for y in range(self.yRes):
                self.fill_sector(x,y,False)
        self.updateAttributes()

    def remove_all_sectors(self):
        ##rewrite to just delete all the data and then update attributes 
        self.vertexPositionData = []
        self.vertexUVData = []
        self.vertexNormalData = []

        self.filledSectors = {}
        self.numSectors = 0

        self.updateAttributes()
        
        

