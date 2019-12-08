from geometry import *
from math import pi, sin, cos, radians
from mathutils import Surface
import numpy as np

class QuadGridGeometry(Geometry):
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
    def __init__(self, sectors, xRes=1, yRes=1):
        super().__init__()
        self.sectors = sectors
        ## This Grid Geometry requires the use of the pair object within the helpers folder
        
        self.xRes = xRes
        self.yRes = yRes

        ## points is a dict of list of points labeled (x,y): 1,2,3,4 which correspond to
        ## on a quad, specified by x and y. Based on the points given, different triangles can be formed.
        ## There must be at least 3 points and no more than 4 points per specified quad
        ## NOTE: while this does generate UV data, it is not very meaningful,
        ## this geometry is not intended for texture data
        vertexPositionData = []
        vertexUVData = []
        vertexNormalData = []

        ## store width and height of each sector
        width = 1.0/xRes
        height = 1.0/yRes
        displacement = np.array([width, height, 0])
        for i,sector in enumerate(sectors):
            print(sector.toList())
            print(displacement)
            if(len(sectors[sector]) == 4):
                #4 points means to form a square spanning the entire sector
                A = list(np.array(self.point_to_vertex[1]) + np.array(sector.toList())*displacement)
                B = list(np.array(self.point_to_vertex[2]) + np.array(sector.toList())*displacement)
                C = list(np.array(self.point_to_vertex[3]) + np.array(sector.toList())*displacement)
                D = list(np.array(self.point_to_vertex[4]) + np.array(sector.toList())*displacement)
                vertexPositionData.extend([ A , B, C])
                vertexPositionData.extend([A,C,D])
                
                vertexUVData.extend([self.point_to_uv[1],self.point_to_uv[2],
                                     self.point_to_uv[3]])
                vertexUVData.extend([self.point_to_uv[1],self.point_to_uv[3],
                                     self.point_to_uv[4]])
            else:
                points = sectors[sector]
                for point in points:
                    vertexPositionData.append(list((np.array(self.point_to_vertex[point]) + np.array(sector.toList()))*displacement))
                    vertexUVData.append(self.point_to_uv[point])


            ## parse through the vertexPositionData and generate normals
            count = int(len(vertexPositionData) / 3)
            for i in range(count):
                A = np.array(vertexPositionData[i*3])
                B = np.array(vertexPositionData[i*3 + 1])
                C = np.array(vertexPositionData[i*3 + 2])
                v1 = B - A
                v2 = C - A

                normal = np.cross(v1,v2)
                normal = normal / np.linalg.norm(normal)
                normal = list(normal)
                vertexNormalData.extend([normal,normal,normal])
                
        self.vertexCount = len( vertexPositionData )
        
        self.setAttribute("vec3", "vertexPosition", vertexPositionData)
        self.setAttribute("vec2", "vertexUV", vertexUVData)
        self.setAttribute("vec3", "vertexNormal", vertexNormalData)
        

