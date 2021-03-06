import bpy

mat_name = bpy.context.active_object.active_material.name
mat = (bpy.data.materials.get(mat_name) or bpy.data.materials.new(mat_name))
mat.use_nodes = True

nt = mat.node_tree
nodes = nt.nodes
links = nt.links

image_path = "C:\\Users\\lori-laptop\\Desktop\\PBRTest Folder\\example_Col1.png"
image_path2 = "C:\\Users\\lori-laptop\\Desktop\\PBRTest Folder\\example_nrm.png"
image_path3 = "C:\\Users\\lori-laptop\\Desktop\\PBRTest Folder\\example_spec.png"


#clear all nodes
while (nodes): nodes.remove(nodes[0])

#Map node names
albedoMap = nodes.new("ShaderNodeTexImage")
normalMap = nodes.new("ShaderNodeTexImage")
roughMap = nodes.new("ShaderNodeTexImage")#.color_space = 'NONE'

#Utility node names
output = nodes.new("ShaderNodeOutputMaterial")
principled = nodes.new ("ShaderNodeBsdfPrincipled")
mapping = nodes.new("ShaderNodeMapping")
texCoord = nodes.new("ShaderNodeTexCoord")

mainTexCoord = [ node for node in mat.node_tree.nodes if node.bl_idname=="ShaderNodeTexCoord"]
# python list comprehension filters the list of nodes down to the ones that match the right bl_idname
texCoordinateNode = mainTexCoord[0]

#Image Texture Node Image
albedoMap.image = bpy.data.images.load(image_path)
normalMap.image = bpy.data.images.load(image_path2)
roughMap.image = bpy.data.images.load(image_path2)

#Sort node tree for Texture Images
image_texture_nodes = [n for n in nt.nodes if n.type == "TEX_IMAGE"]
# Extract the name of the node and place in list
image_texture_names = [n.name for n in image_texture_nodes]
#Filter out image textures
node_types = [n for n in nt.nodes if n.type != "TEX_IMAGE"]
# Extract string name and place in new node
#Reversed so it orders them correctly
node_names = [n.name for n in reversed(node_types)]
#insert image_texture_names at the correct index 
for i in image_texture_names:
    node_names.insert(2,i)

def makeLink(var1, var2, var3, var4):
    """
    Creates a link between a Material Node's output,
    and another Material Node's input.
    args follow the order: Output Node Name, Socket Name, Input Node Name, Socket Name
    """
    links.new(var1.inputs[var2], var3.outputs[var4])

def defaultLinks():
    makeLink(output, 'Surface', principled, 'BSDF')
    makeLink(mapping, 'Vector', texCoordinateNode, 'UV')

def makeAlbedo():
    makeLink(principled, 'Base Color', albedoMap, 'Color')
    makeLink(albedoMap, 'Vector', mapping, 'Vector')
    

def makeNormal():
    makeLink(principled, 'Normal', normalMap, 'Color')
    makeLink(normalMap, 'Vector', mapping, 'Vector')
    
def makeSpec():
    makeLink(principled, "Metallic", roughMap, 'Color')
    makeLink(roughMap, 'Vector', mapping, 'Vector')

#Set node X & Y Locations
def setLocation():

    startlocx = 0
    startlocy = 0
    
    locx = startlocx
    locy = startlocy
    
    nodes[node_names[0]].location.x = locx
    nodes[node_names[0]].location.y = locy
    for i, node in enumerate(node_names[1:]):
        lastnode = node_names[i]
        if nodes[lastnode].type == "TEX_IMAGE" and nodes[node].type == "TEX_IMAGE":
            locy += nodes[lastnode].height + 200
        else:
            locy = startlocy
            locx += nodes[lastnode].width + 50
        nodes[node].location.x = locx 
        nodes[node].location.y = locy 
        
#Run the functions
defaultLinks()
makePrincipled
makeNormal()
makeSpec()
setLocation()
