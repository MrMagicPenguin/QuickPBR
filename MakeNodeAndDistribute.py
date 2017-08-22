import bpy

mat_name = "Material"
mat = (bpy.data.materials.get(mat_name) or bpy.data.materials.new(mat_name))
mat.use_nodes = True

nt = mat.node_tree
nodes = nt.nodes
links = nt.links

image_path = "C:\\Users\\lori-laptop\\Desktop\\PBRTest Folder\\example_Col1.png"
image_path2 = "C:\\Users\\lori-laptop\\Desktop\\PBRTest Folder\\example_nrm.png"


#clear all nodes
while (nodes): nodes.remove(nodes[0])

#Shader node convenience variable names - SCV
#Map node names
albedoMap = nodes.new("ShaderNodeTexImage")
normalMap = nodes.new("ShaderNodeTexImage")
#Utility node names
output = nodes.new("ShaderNodeOutputMaterial")
diffuse = nodes.new ("ShaderNodeBsdfDiffuse") # change to Principled later
mapping = nodes.new("ShaderNodeMapping")
texCoord = nodes.new("ShaderNodeTexCoord")

mainTexCoord = [ node for node in mat.node_tree.nodes if node.bl_idname=="ShaderNodeTexCoord"]
# python list comprehension filters the list of nodes down to the ones that match the right bl_idname
texCoordinateNode = mainTexCoord[0]

albedoMap.image = bpy.data.images.load(image_path)
normalMap.image = bpy.data.images.load(image_path2)

#SCV name, SCV input node, SCV name, SCV output node
"""
Creates a link between a Material Node's output, and another Material Node's input
"""
def makeLink(var1, var2, var3, var4):
    links.new(var1.inputs[var2], var3.outputs[var4])

    
def makeAlbedo():
    makeLink(output, 'Surface', diffuse, 'BSDF')
    makeLink(diffuse, 'Color', albedoMap, 'Color')
    makeLink(albedoMap, 'Vector', mapping, 'Vector')
    makeLink(mapping, 'Vector', texCoordinateNode, 'UV')

def makeNormal():
    makeLink(output, 'Surface', diffuse, 'BSDF')
    makeLink(diffuse, 'Normal', normalMap, 'Color')
    makeLink(normalMap, 'Vector', mapping, 'Vector')
    makeLink(mapping, 'Vector', texCoordinateNode, 'UV')


imageTextureList = [ node for node in mat.node_tree.nodes if node.bl_idname=="ShaderNodeTexImage"]
# python list comprehension filters the list of nodes down to the ones that match the right bl_idname
imageTextureListLength = len(imageTextureList)
print(imageTextureListLength)

#distribute nodes along the x axis
def distribute():
    nodes = bpy.data.materials['Material'].node_tree.nodes
    atomicNodes = ['Texture Coordinate', 'Mapping', 'Image Texture','Diffuse BSDF', 'Material Output']
    
    loc = 0
    for i in atomicNodes:
        nodes[i].location.x = loc
        loc += nodes[i].width + 50
        nodes[i].location.y = 0
        for img in imageTextureList:
            imageTextureIndex[img].location.y = loc
            loc += imageTextures.height + 50

        
#Run the functions
makeAlbedo()
makeNormal()
distribute()
print(imageTextureList)
print(imageTextureIndex)