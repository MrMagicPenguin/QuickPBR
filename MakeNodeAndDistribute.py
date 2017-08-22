import bpy

mat_name = "Material"
mat = (bpy.data.materials.get(mat_name) or bpy.data.materials.new(mat_name))
mat.use_nodes = True

nt = mat.node_tree
nodes = nt.nodes
links = nt.links

image_path = "E:\\PBRTest Folder\\example_Col1.png"
image_path2 = "E:\\PBRTest Folder\\example_nrm.png"
image_path3 = "E:\\PBRTest Folder\\example_spec.png"


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


#Node Name, Socket Name, Node Name, Socket Name

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


imageNodeDict = [ node for node in mat.node_tree.nodes if node.bl_idname=="ShaderNodeTexImage"]
# python list comprehension filters the list of nodes down to the ones that match the right bl_idname

#distribute nodes along the x axis
def distribute():
    nodes = bpy.data.materials['Material'].node_tree.nodes
    nodeValues = nodes.values()
    nodeKeys = nodes.keys()
    # I don't want to node lists such as atomicNodes and imageTextures in order to cycle through. I don't want to hardcode things.
    #Using the list comprehension shown above as the argument above, you are returned strings
    #the for loop throws a type error, stating:
    # "invalid key, must be a string or int"
    # not ShaderNodeTexImage
    # So it seems to be returning a dictionary, not a list. How can we format a dictionary to return what we want? We just want the 'Value' of the set,
    #I don't know how much we care for the key, in our output anyway.
    atomicNodes = nodeKeys
    imageTextures = ['Image Texture', 'Image Texture.001', 'Image Texture.002']
    
    locx = 0
    locy = 0
    for i in atomicNodes:
        nodes[i].location.x = locx
        locx += nodes[i].width + 50
        nodes[i].location.y = 0
    for i in imageTextures:
        imageNodeDict[i].location.y = locy
        locy += imageNodeDict[i].height + 200
        imageNodeDict[i].location.x = nodes[1].location.x

#Run the functions
defaultLinks()
makeAlbedo()
makeNormal()
makeSpec()
distribute()
print(imageNodeDict)
#print(mainTexCoord)
#print(texCoordinateNode)
