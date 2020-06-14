# Visual_Control_Systems

Project is to prepare visual explanation for all basic concepts of Linear Algebra and Modren Control Systems.

CURRENT PROGRESS:
- Python files added to plot S plane in 3D and gradient plot in 2-D for given transfer function
- Python files added to plot gradient of a function
- Python module developed to use blender for working with vectror agebra. Following methods are available in it



*create_collection('states')
* create_material(Blue,(r,g,b,I))
* arrow_between(x1, y1, z1, x2, y2, z2,color) 
    - arrow size depends on distance between points
    - color will be name of color defined using create_material
* add_axis(origin, point on axis, radius of cylinder,length of axis,color)

* add_color(ob,color) - apply defined color to object
                    - ob = bpy.context.object
* add_shapes(name, verts, faces, edges=None, col_name)
                    - name 'some_shape'
                    - verts [(0,0,0),(1,1,1),(2,2,2)] - coords
                    - edges [(0,1),(1,2),(2,0)] - pairs of points
                    - faces [have to figure out]    
* transform(A,collection=None,obj=None,simulate = False)
* simulate(frame_number,A,collection='states')

* add_points(color,scale=1,locations=None,collection=None,Random=False,number=None):

* name_object(Name,object=None,collection=None):

To use it place the module in blender/version/modules/ and then import it in blender as
from control_blend import *

To use it from local folder try this
import os
import sys
dir = os.path.dirname(bpy.data.filepath)
sys.path.append(dir )

To delete the import use this
del sys.modules['control_blend']

