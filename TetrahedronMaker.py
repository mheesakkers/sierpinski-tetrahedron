"""
Name: 'Creation of a sierpinski tetrahedron'
Blender: 2.73a
Author: 'Misha Heesakkers'
"""

import bpy
import math

class Tetrahedron:
    
    objectName = 'Tetrahedron'
        
    location = (0.0, 0.0, 0.0)
    scale = 4
    vertices =[]
    edges = []
    faces = [[0, 1, 2], [0, 1, 3], [1, 2, 3], [2, 3, 0]]
    
    def initializeObject(self):
        self.mesh = bpy.data.meshes.new('TetrahedronMesh')
        self.object = bpy.data.objects.new(self.objectName, self.mesh)
        
    def linkObjectToScene(self):
        scene = bpy.context.scene
        scene.objects.link(self.object)
        scene.objects.active = self.object
         
    def updateLocation(self):
        self.object.select = True
        self.object.location = self.location
        
    def updateMesh(self):
        self.vertices = self.calculateVertices(self.scale)
        self.mesh.from_pydata(self.vertices, [], self.faces)
        self.mesh.update()
        
    def calculateVertices(self, scale):
        array = [
            (0 * scale, -1 / math.sqrt(3) * scale, 0 * scale),
            (0.5 * scale, 1 / (2 * math.sqrt(3)) * scale, 0 * scale),
            (-0.5 * scale, 1 / (2 * math.sqrt(3)) * scale, 0 * scale),
            (0 * scale, 0 * scale, math.sqrt(2 / 3) * scale)
        ]
        return array
    
    def getMidpoints(self):
        midpoints = []
        for vertex in self.object.data.vertices:
            coordinate = (
                (vertex.co[0] * 0.5) + self.location[0],
                (vertex.co[1] * 0.5) + self.location[1],
                (vertex.co[2] * 0.5) + self.location[2]
            )
            midpoints.append(coordinate)
        return midpoints
    
    def removeObject(self):
        bpy.context.scene.objects.unlink(self.object) 
        self.object.user_clear()
        bpy.data.objects.remove(self.object)
    
    def __init__(self):
        self.initializeObject()

if __name__ == "__main__":
    initialTetrahedron = Tetrahedron()
    initialTetrahedron.linkObjectToScene()
    initialTetrahedron.updateLocation()
    initialTetrahedron.updateMesh()

    objects = [];
    objects.append(initialTetrahedron)
    
    def generate():
        newObjects = []
        
        for tetrahedron in objects:
            for point in tetrahedron.getMidpoints():
                temp = Tetrahedron()
                temp.scale = tetrahedron.scale / 2
                temp.location = point
                temp.linkObjectToScene()
                temp.updateLocation()
                temp.updateMesh()
                newObjects.append(temp)
            
            #Remove parent tetrahedron
            tetrahedron.removeObject()
            
        return newObjects
    
    # Re calling the generate() function
    # for making new generations on new generations
    for i in range(0, 3):
        objects = generate()