
#HEADERS
import numpy as np  
import math as mm
import random

import bpy 
from bpy import context

import sys

#CLEARS SCREEN
obj = bpy.context.active_object
if (context.active_object.mode == 'EDIT'):
    bpy.ops.object.mode_set(mode ='OBJECT', toggle=False)

for item in bpy.context.selectable_objects:
    item.select = True
     
object = bpy.context.scene.objects.active
bpy.ops.object.delete() 

#FUNCTIONS
    
#The form_object function uses coords, a 2D array that has the coordiantes 
#of the object you wish to form, and forms the NURBS object 'myCurve', using 
#this data. 
def form_object(coords):
    # create the Curve Datablock
    curveData = bpy.data.curves.new('myNURBSobject', type = 'CURVE')
    curveData.dimensions = '3D'
    # curveData.resolution_u = 2
    # map coords to spline
    polyline = curveData.splines.new('NURBS')
    polyline.points.add(len(coords))
    for i, coord in enumerate(coords):
        x,y,z = coord
        polyline.points[i].co = (x, y, z, 1)
    # create Object
    curveOB = bpy.data.objects.new('myNURBSobject', curveData)
    # attach to scene and validate context
    scn = bpy.context.scene
    scn.objects.link(curveOB)
    scn.objects.active = curveOB
    curveOB.select = True

#The get_vertices function requires the BLENDER MESH OBJECT, for which 
#it obtains a set of points on the object and returns the tuple form of 
#the vertices. 
def get_vertices(object):
    from bpy import context
    bpy.ops.object.mode_set(mode = 'EDIT')
    verts = []
    verts = [vert.co for vert in object.data.vertices]
    plain_verts = [vert.to_tuple() for vert in verts]
    #print("VERTICES ARE :     ", plain_verts)
    return plain_verts
