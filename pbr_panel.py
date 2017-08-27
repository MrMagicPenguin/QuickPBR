import bpy


class HelloWorldPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Quick Layout Options"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_category = 'Quick PBR'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Create a new node layout")

        row = layout.row()
        row.label(text="Options.....")
        row = layout.row()

        row = layout.row()
        #This does not run yet, quick_layout() is not being registered.
        row.operator("bpy.ops.rug.quick_layout")


def register():
    bpy.utils.register_class(HelloWorldPanel)


def unregister():
    bpy.utils.unregister_class(HelloWorldPanel)


if __name__ == "__main__":
    register()
