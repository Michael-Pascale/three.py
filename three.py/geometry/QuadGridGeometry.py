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
    def __init__(self, points):
        super().__init__()
        self.points = points

        ## points is a list of points labeled 1,2,3,4 which correspond to corners
        ## on a quad. Based on the points given, different triangles can be formed.
        ## There must be at least 3 points and no more than 4 points
        ## NOTE: while this does generate UV data, it is not very meaningful,
        ## this geometry is not intended for texture data
        vertexPositionData = []
        vertexUVData = []
        vertexNormalData = []
        if(len(points) == 4):
            #4 points means to form a square spanning the entire geometry
            vertexPositionData.extend([self.point_to_vertex[1],self.point_to_vertex[2],
                                       self.point_to_vertex[3]])
            vertexPositionData.extend([self.point_to_vertex[1],self.point_to_vertex[3],
                                       self.point_to_vertex[4]])
            vertexUVData.extend([self.point_to_uv[1],self.point_to_uv[2],
                                 self.point_to_uv[3]])
            vertexUVData.extend([self.point_to_uv[1],self.point_to_uv[3],
                                 self.point_to_uv[4]])
        else:
            for point in points:
                vertexPositionData.append(self.point_to_vertex[point])
                vertexUVData.append(self.point_to_uv[point])


        ## parse through the vertexPositionData and generate normals
        count = int(len(vertexPositionData) / 3)
        print(count)
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
                
            

        """vertexPositionData = self.attributeData["vertexPosition"]["value"]
        vertexUVData = self.attributeData["vertexUV"]["value"]
        vertexNormalData = self.attributeData["vertexNormal"]["value"]
        
        if circleTop:        
            angle = radians(360) / radialSegments
            posCenter = [0, height/2, 0]
            uvCenter = [0.5,0.5]
            normal = [0,1,0]
            for i in range(radialSegments):
                posA = [ radiusTop*cos(i*angle), height/2, radiusTop*sin(i*angle) ]
                posB = [ radiusTop*cos((i+1)*angle), height/2, radiusTop*sin((i+1)*angle) ]
                vertexPositionData.extend( [posCenter, posA, posB] )
                
                uvA = [ cos(i*angle)*0.5 + 0.5, sin(i*angle)*0.5 + 0.5 ]
                uvB = [ cos((i+1)*angle)*0.5 + 0.5, sin((i+1)*angle)*0.5 + 0.5 ]
                vertexUVData.extend( [uvCenter, uvA, uvB] )
                
                vertexNormalData.extend( [normal,normal,normal] )
                
        if circleBottom:        
            angle = radians(360) / radialSegments
            posCenter = [0, -height/2, 0]
            uvCenter = [0.5,0.5]
            normal = [0,-1,0]
            for i in range(radialSegments):
                posA = [ radiusBottom*cos(i*angle), -height/2, radiusBottom*sin(i*angle) ]
                posB = [ radiusBottom*cos((i+1)*angle), -height/2, radiusBottom*sin((i+1)*angle) ]
                vertexPositionData.extend( [posCenter, posA, posB] )
                
                uvA = [ cos(i*angle)*0.5 + 0.5, sin(i*angle)*0.5 + 0.5 ]
                uvB = [ cos((i+1)*angle)*0.5 + 0.5, sin((i+1)*angle)*0.5 + 0.5 ]
                vertexUVData.extend( [uvCenter, uvA, uvB] )
                
                vertexNormalData.extend( [normal,normal,normal] )"""
                
        self.vertexCount = len( vertexPositionData )
        
        self.setAttribute("vec3", "vertexPosition", vertexPositionData)
        self.setAttribute("vec2", "vertexUV", vertexUVData)
        self.setAttribute("vec3", "vertexNormal", vertexNormalData)
        

