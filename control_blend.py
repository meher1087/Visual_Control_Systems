import bpy
import numpy as np
from random import randint
import mathutils
from numpy import linalg as LA
import math
import bpy
import sys
import os

'''
@param self

import os
import sys
dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir )

del sys.modules['control_blend']

create_collection('states')
create_material(Blue,(r,g,b,I))
arrow_between(x1, y1, z1, x2, y2, z2,color) 
    - arrow size depends on distance between points
    - color will be name of color defined using create_material
add_axis(origin, point on axis, radius of cylinder,length of axis,color)

add_color(ob,color) - apply defined color to object
                    - ob = bpy.context.object
add_shapes(name, verts, faces, edges=None, col_name)
                    - name 'some_shape'
                    - verts [(0,0,0),(1,1,1),(2,2,2)] - coords
                    - edges [(0,1),(1,2),(2,0)] - pairs of points
                    - faces [have to figure out]    
transform(A,collection=None,obj=None,simulate = False)
simulate(frame_number,A,collection='states')

def add_points(color,scale=1,locations=None,collection=None,Random=False,number=None):

def name_object(Name,object=None,collection=None):

'''
# initally remove all materials

for material in bpy.data.materials:
    material.user_clear()
    bpy.data.materials.remove(material)
# remove collections
context = bpy.context
scene = context.scene
for c in scene.collection.children:
    scene.collection.children.unlink(c)

# create new collection called states
#myCol = bpy.data.collections.new("states")
#bpy.context.scene.collection.children.link(myCol)

def create_collection(name):
    myCol = bpy.data.collections.new("states")
    bpy.context.scene.collection.children.link(myCol)
    

# create basic materials

def create_material(Name,color):
    mat = bpy.data.materials.new(Name)
    mat.diffuse_color=color

def create_basic_materials():
    create_material('Blue',(0,0,1,1))
    create_material('Red',(1,0,0,1))
    create_material('Green',(0,1,0,1))
    create_material('Yellow',(1,1,0,1))
    create_material('Magenta',(1,0,1,1))
    create_material('Cyan',(0,1,1,1))

def create_random_materials(number):
    for i in range(number):
        create_material('Mat'+str(i),(randint(0,255),randint(0,255),randint(0,255),1))

def arrow_between(x1, y1, z1, x2, y2, z2,color):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1    
    dist = math.sqrt(dx**2 + dy**2 + dz**2)
    r = 0.1*dist
    bpy.ops.mesh.primitive_cone_add(depth=dist, location = (dx/2 + x1, dy/2 + y1, dz/2 + z1), radius1=r, radius2=0.0)
    #bpy.ops.mesh.primitive_cylinder_add(radius = r, depth = dist,location = (dx/2 + x1, dy/2 + y1, dz/2 + z1))
    
    # Assign available material
    ob = bpy.context.object
    add_color(ob,color)

    
    #set orientation
    phi= math.atan2(dy, dx) 
    theta= math.acos(dz/dist) 
    bpy.context.object.rotation_euler[1] = theta 
    bpy.context.object.rotation_euler[2] = phi 


def add_axis(origin, point, r,d,color):
    x1 = origin[0]
    y1 = origin[1]
    z1 = origin[2]
    
    x2 = point[0]
    y2 = point[1]
    z2 = point[2]
    
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1    
    dist = math.sqrt(dx**2 + dy**2 + dz**2)
    bpy.ops.mesh.primitive_cylinder_add(radius = r, depth = d,location = (dx/2 + x1, dy/2 + y1, dz/2 + z1))
    # Assign available material
    ob = bpy.context.object
    add_color(ob,color)
    
    phi= math.atan2(dy, dx) 
    theta= math.acos(dz/dist) 

    bpy.context.object.rotation_euler[1] = theta 
    bpy.context.object.rotation_euler[2] = phi 

def add_color(color,object=None):
    if object is None:
        ob = bpy.context.active_object
    else:
        ob = bpy.data.objects[object]
    me = ob.data
    mat = bpy.data.materials[color]
    me.materials.append(mat)

def add_shapes(name, verts, faces, col_name,edges=None ):    
    if edges is None:
        edges = []
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(mesh.name, mesh)
    col = bpy.data.collections.get(col_name)
    col.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    mesh.from_pydata(verts, edges, faces)

# simulate
def transform(A,collection=None,object=None,simulate=False):
    x_dot = []
    if collection:
        for name,cube in bpy.data.collections[collection].objects.items():
            #cube = bpy.data.objects["cube" +str(i)]
            
            # one blender unit in x-direction
            #inv = cube.matrix_world.copy()
            #inv.invert()
            loc = cube.location
            x_dot = np.dot(A,loc)
            #print(loc)
            #print(x_dot)
            cube.location = mathutils.Vector(x_dot) + loc 
            if simulate:
                cube.keyframe_insert(data_path = 'location')
                print('key_Frame_inserted '+ name)
    if object:
        obj = bpy.data.objects[object]
        loc = obj.location
        x_dot = np.dot(A,loc)
        #print(loc)
        #print(x_dot)
        obj.location = mathutils.Vector(x_dot) + loc 
        if simulate:
            obj.keyframe_insert(data_path = 'location')

def simulate(end,A,collection=None,object=None,start=0,frame_gap=1):
    for i in range(start, end, frame_gap):
        bpy.data.scenes["Scene"].frame_set(i)
        print('frame_set ',i)
        transform(A,collection=collection,object=object,simulate=True)
    
def add_points(color,scale=1,locations=None,collection=None,Random=False,number=None,Grid=10):
    if collection:
        c = bpy.data.collections.find(collection)
        if c != 1:
            create_collection(collection)
    
    if Random:
        locations=[]
        for i in range(number):
            G = Grid
            locations.append([randint(-G,G),randint(-G,G),randint(-G,G)])
    
    for i in range(len(locations)):    
        bpy.ops.mesh.primitive_uv_sphere_add(location=locations[i])  
        bpy.ops.transform.resize(value=(scale, scale, scale))
        ob = bpy.context.active_object
        add_color(color)
        
        if collection:
            # Remove object from all collections not used in a scene
            bpy.ops.collection.objects_remove_all()
            # add it to our specific collection
            bpy.data.collections[collection].objects.link(ob)

def name_object(Name,object=None,collection=None):
    if collection:
        if object:
            obj = bpy.data.collections[collection].objects[object]
        else:
            obj = bpy.context.active_object
        obj.name = Name
        obj.show_name = True
    else:
        obj.name = Name
        obj.show_name = True


# CALUCULATET EIGS AND DISPLAY EIG FRAME
def add_eig_vectors(A,origin=None,rad = 1, len=50,colors=['Red','Green','Blue']):
    try:
        eig_val,eig_vect = LA.eig(A)
        if len(eig_val)>len(colors):
            raise TypeError('please enter colors in list')
        if origin is None:
            origin = np.zeros([1,len(eig_val)])
        for i in range(len(eig_val)):
            add_axis(origin,eig_vect[:,i],rad,len,colors[i])
    except:
        print('Cant find eig values')

def add_ref_frame(A,origin=None,rad = 0.1, len=50,colors=['Red','Green','Blue']):
    try:
        col,row = np.shape(A)
        if col>len(colors):
            raise TypeError('please enter colors in list')
        if origin is None:
            origin = np.zeros([1,row])
        for i in range(col):
            add_axis(origin,A[:,i],rad,len,colors[i])
    except:
        print('Cant find eig values')

def sample_transform():
    A = [[0.1,0.2,0.5],[-0.3,0.4,0.8],[-0.9,0.4,0.3]]
    return A

