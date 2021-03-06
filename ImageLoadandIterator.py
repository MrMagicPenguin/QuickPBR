import bpy, os, re

mat_name = "Material"
mat = (bpy.data.materials.get(mat_name) or bpy.data.materials.new(mat_name))  
mat.use_nodes = True
nt = mat.node_tree
nodes = nt.nodes
links = nt.links

ob = bpy.context.active_object
path_name = "E:\PBRTest Folder"

diffCheck = r"Col1"
nrmCheck = r"nrm"
dispCheck = r"disp"
specCheck = r"spec"

def path_iterator(path_name):
   for fp in os.listdir(path_name):
       if fp.endswith( tuple( bpy.path.extensions_image ) ):
           yield fp

for file_name in path_iterator(path_name):
    print(os.path.join(path_name, file_name))
    if re.search(diffCheck, file_name):
        print("Diffuse Found!")
        makeLink()
    elif re.search(nrmCheck, file_name):
        print ("Normal Found!")
    elif re.search(dispCheck, file_name):
        print ("Displace Found!")
    elif re.search(specCheck, file_name):
        print ("Specular found!")
    else:
        print ("no match")
        