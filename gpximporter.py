import os
import bpy
import xml.etree.ElementTree as ET
import bmesh


# Use Bmesh to create a mesh from from datapoints
def points_to_mesh(vertices,create_edges):
    
    # generate empty edges
    edges = []
    
    # generate edge indices if user specifies to do so
    if create_edges:
        for index, edge in enumerate(vertices):
            if index+1 < len(vertices):
                edges.append((index,index+1))
    
    # generate empty faces list
    faces = []

    # generate mesh
    gpx_mesh = bpy.data.meshes.new('gpx_mesh')

    # fill mesh from data
    gpx_mesh.from_pydata(vertices, edges, faces)
    gpx_mesh.update()

    # generate object
    gpx_object = bpy.data.objects.new('gpx', gpx_mesh)

    # generaate new collection to add the object to
    gpx_collection = bpy.data.collections.new('gpx_collection')
    bpy.context.scene.collection.children.link(gpx_collection)

    # add the new meshyy
    gpx_collection.objects.link(gpx_object)


def read_xml_data(context, filepath, use_some_setting):
    
    print(filepath)    
    tree = ET.parse(filepath)
    root = tree.getroot()
    
    # TODO: Remove the "is_original" check and always just iterate over the contents of <trkseg></trkseg> instead of the naiive root[1][1] children

    is_original = False
    # Original Apple Health GPX files have additional data
    if root[0].tag == "{http://www.topografix.com/GPX/1/1}metadata":
        is_original = True
        print("This is a original Apple File")
    
    try:
        print("running read_gpx... printing *.gpx metadata")
        global waypoints
        waypoints = []
        
        if is_original:
            for child in root[1][1]:
                waypoint = list(map(float,child.attrib.values()))
                waypoint.append(0)
                waypoints.append(waypoint)   
        else:
            # This is just tested for one other GPX type
            for child in root[0][0]:
                waypoint = list(map(float,child.attrib.values()))
                waypoint.append(0)
                waypoints.append(waypoint)
        
        vertices = [tuple(item) for item in waypoints]
       
        points_to_mesh(vertices,use_some_setting)
    except:
        print("import failed")

    return {'FINISHED'}


# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, CollectionProperty
from bpy.types import Operator


class ImportGPXData(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "import_test.gpx_data"  # important since its how bpy.ops.import_test.gpx_data is constructed
    bl_label = "Import Some Data"

    # ImportHelper mixin class uses this
    filename_ext = ".gpx"

    filter_glob: StringProperty(
        default="*.gpx",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting: BoolProperty(
        name="Create Edges",
        description="Creates connecting edges from each datapoint to the next",
        default=True,
    )

    ###########################################
    # necessary to support multi-file import
    files: CollectionProperty(
        type=bpy.types.OperatorFileListElement,
        options={'HIDDEN', 'SKIP_SAVE'},
    )

    directory: StringProperty(
        subtype='DIR_PATH',
    )
    ###########################################

    def execute(self, context):
        for current_file in self.files:
            filepath = os.path.join(self.directory, current_file.name)
            read_xml_data(context, filepath, self.use_setting)
        return {'FINISHED'}


# Only needed if you want to add into a dynamic menu.
def menu_func_import(self, context):
    self.layout.operator(ImportGPXData.bl_idname, text="Text Import Operator")


# Register and add to the "file selector" menu (required to use F3 search "Text Import Operator" for quick access).
def register():
    bpy.utils.register_class(ImportGPXData)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.utils.unregister_class(ImportGPXData)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.import_test.gpx_data('INVOKE_DEFAULT')
