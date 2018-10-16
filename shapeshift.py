
#the intuitive method...

print("")
print("NEW RUN")
print("")

#HEADERS FOR ALGORITHM
import numpy as np  
import math as mm
import random
#HEADERS FOR BLENDER
import bpy 
from bpy import context

#CLEARS SCREEN
obj = bpy.context.active_object
if (context.active_object.mode == 'EDIT'):
    bpy.ops.object.mode_set(mode ='OBJECT', toggle=False)
for item in bpy.context.selectable_objects:
    item.select = True
object = bpy.context.scene.objects.active
bpy.ops.object.delete() 

#FUNCTIONS
#The generate function uses 'B', the array bounds, which contains the 
#boundries of the points that are to be optimized, and generates 
#random values to start the process.
def generate(B):
    g = []
    for i in range(1, number_of_variables_total+1):
        j = number_of_variables
        LB = B[i-1][j-2]
        UB = B[i-1][j-1]
        u = random.uniform(LB, UB)
        g.append(u)
    return g

#The tweak function accepts 'h', the array that contains the values 
#to be tweaked and 'B', the bounds for the same. It tweaks the values 
#by adding a number in the range of (-0.05,0.05)
def tweak(v):
    r = random.uniform(0, 10)
    t = random.uniform(-r, r)
    for i in range(1, number_of_variables_total+1):
        j = number_of_variables
        LB = bounds[i-1][j-2]
        UB = bounds[i-1][j-1]
        v[i-1] = v[i-1] + t
        if(v[i-1]>UB or v[i-1]<LB):
            v[i-1] = random.uniform(LB, UB)
    return v

#The purpose of the the function pointify is to arrange the array of 
#the optimized values into point form. For example, if the values 
#array has elements [1,2,3,4,5,6], performing the function pointify 
#will return [[1,2],[3,4],[5,6]]. This function requires v, the intial 
#array for which you want to perform the pointify operation and p, the 
#result array.
def pointify(v,p):
    p=[]
    p.insert(0,[])
    '''
    for i in range(0,number_of_points_optimize):
        k = positions_of_points_optimize[i] - 1
        p.insert(k,[])
        #p[k].insert(0,(v[(2*i)-2]))
        #p[k].insert(1,(v[(2*i)-1]))
        #p[k].insert(0,(v[(2*i)]))
        #p[k].insert(1,(v[(2*i)+1]))
    '''    
    p[0].insert(0,(v[0]))
    p[0].insert(1,(v[1]))
    return p

def distance(p,q):
    total = 0
    #total += (abs(p[0][0]-q[r][0])) + (abs(p[0][1]-q[r][1]))
    for i in range(0, len(p), 1):
        #total = total + (((p[i][0]-q[i][0])**2) + ((p[i][1]-q[i][1])**2))**.5
        total = total + (abs(p[i][0]-q[i][0])) + (abs(p[i][1]-q[i][1]))
    return total

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

def add_control_point(B,pos):  
    g = [] 
    for k in range(0,number_of_variables):
        new_cp = random.uniform(B[k][0],B[k][1])
        g.append(new_cp)
    return g

def make_change(vals):
    g = []
    for k in range(0,number_of_variables):
        g.append(vals[k])
    return g

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

#The area function accepts p, a 2D array of points and computes the area 
#of the figure made of those points by using the 1/2*|x1*y2-x2*y1 + .... | 
#formula for consecutive points on the figure. 
def area(p):
    products = 0.0
    for i in range(0, len(p), 1):
        if (i < (len(p)-1)):
            q = i+1
            products += (p[i][0]*p[q][1]) - (p[i][1]*p[q][0])        
        elif (i == (len(p)-1)):
            products += ((p[i][0]*p[0][1]) - (p[i][1]*p[0][0]))
        products = products
    AR = 0.5 * abs(products)
    return AR

#The perimeter function accepts p, a 2D array of points and computes the perimeter 
#of the figure made of those points by using the coordinate formula
#for consecutive points on the figure. 
def perimeter(p):
    sum = 0.0
    for i in range(0, len(p), 1):
        if (i < (len(p)-1)):
            q = i+1
            sum += (p[i][0]-p[q][0])**2 + (p[i][1]-p[q][1])**2        
        elif (i == (len(p)-1)):
            sum += (p[i][0]-p[0][0])**2 + (p[i][1]-p[0][0])**2
        sum = sum
    perim = sum**.5
    return perim

#This is the fitness function, which returns the perimeter of the shape
def fitness(a,b):
    fit = a
    return fit

#Target Object
stop_coords = [[0,0,1],[10,10,1],[50,20,1],[25,75,1],[50,150,1],[75,75,1],[50,20,1],[90,10,1],[100,0,1]]
form_object(stop_coords)
obj = bpy.context.object
obj = bpy.ops.object.convert(target='MESH', keep_original=False)
objs = bpy.context.object
stop_v = get_vertices(objs)
#stop_area = area(stop_v)
#tarea = stop_area
#print("The area of the stop object is :  " , stop_area)
bpy.ops.object.mode_set(mode = 'OBJECT')
obj = bpy.context.scene.objects.active
bpy.ops.object.delete()

start_coords = [[0,0,1],[100,0,1]]

#SPECIFICS
#IMPORTANT NOTE: EVERY TIME YOU MODIFY ANY SPECIFICS PLEASE CHANGE THE ARRAY p IN FUNCTION pointify APPROPRIATELY!!!

number_of_iterations = 30 #30
sample_size = 50 #50

number_of_points_total = len(stop_coords)-len(start_coords)
number_of_points_optimize = 1
number_of_variables = 2
number_of_variables_total = number_of_variables * number_of_points_optimize

positions_of_points_optimize = [2]

bounds=[]
for i in range(0,number_of_variables_total):
    bounds.append([0,10])

final = []
opt_vals = []
p = []

times=0
while(times<number_of_points_total):
    now_coords = [[0,0,1],[10,10,1],[50,20,1],[25,75,1],[50,150,1],[75,75,1],[50,20,1],[90,10,1],[100,0,1]]
    if(times>=1):
        opt_vals.append(final)

        integer = positions_of_points_optimize[0]
        dummy = []
        for t in range(len(positions_of_points_optimize)):
            dummy.append(positions_of_points_optimize[t])

        positions_of_points_optimize = []
        while (integer in dummy or integer==0 or integer==(len(stop_coords)-1)):
            integer = random.randint(1,(len(stop_coords)-1))
        positions_of_points_optimize = [integer] + dummy
    
    val = generate(bounds)
    #best = pointify(val,p)
    val.append(1)
    best = val
    now_coords[positions_of_points_optimize[0]] = best

    for p in range(0,len(opt_vals)):
        now_coords[positions_of_points_optimize[p+1]] = opt_vals[len(opt_vals)-p-1]
        
    print(now_coords)
    form_object(now_coords)
    obj = bpy.context.object
    obj = bpy.ops.object.convert(target='MESH', keep_original=False)
    objs = bpy.context.object
    cur_v = get_vertices(objs)
    #cur_area = area(stop_v)
    #carea = cur_area
    bpy.ops.object.mode_set(mode = 'OBJECT')
    obj = bpy.context.scene.objects.active
    bpy.ops.object.delete()

    best_value = distance(cur_v,stop_v)
    #best_value = distance(now_coords,stop_coords)

    times+=1
    
    for j in range(30):
        n=1
        while(n<50):
            n+=1
            count=0
            notBest=True
            while(notBest):
                count+=1
                xi=tweak(val)
                x=xi
                now_coords[positions_of_points_optimize[0]] = x

                print(now_coords)
                
                form_object(now_coords)
                obj = bpy.context.object
                obj = bpy.ops.object.convert(target='MESH', keep_original=False)
                objs = bpy.context.object
                gen_v = get_vertices(objs)
                #gen_area = area(stop_v) 
                #garea = gen_area
                bpy.ops.object.mode_set(mode = 'OBJECT')
                obj = bpy.context.scene.objects.active
                bpy.ops.object.delete()
                
                y=distance(gen_v,stop_v)
                #y=distance(now_coords,stop_coords)
                notBest = False
                if((y<1  and y>(-1)) or count>200):
                    notBest=False
            if(y<best_value):
                final=[]
                for i in x:
                    final.append(i)
                best = x
                best_value = y
        print("The seed is ", j, " and the value of x is ", final, " and the best value is ", best_value)
    print(3)
    print("pos: ", positions_of_points_optimize)
    if(times==number_of_points_total):
        opt_vals.append(final)
    print("final: ", final)
    print("FINAL I HOPE: ", opt_vals)
    

#print("pos: ", positions_of_points_optimize)

now_coords = [[0,0,1],[10,10,1],[50,20,1],[25,75,1],[50,150,1],[75,75,1],[50,20,1],[90,10,1],[100,0,1]]
for p in range(0,len(positions_of_points_optimize)):
    now_coords[positions_of_points_optimize[p]] = opt_vals[len(opt_vals)-p-1]

print("last now: ", now_coords)
#CLEARS SCREEN
obj = bpy.context.scene.objects.active
bpy.ops.object.delete()

#DISPLAY TARGET AND GENERATED OBJECTS 
form_object(now_coords)
form_object(stop_coords)
