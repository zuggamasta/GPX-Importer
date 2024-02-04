# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "GPS Exchange Format (.gpx)",
    "author" : "zuggamasta",
    "description" : "",
    "blender" : (4, 0, 2),
    "version" : (0, 1, 1),
    "location" : "",
    "doc_url": "{BLENDER_MANUAL_URL}/addons/import_export/scene_gltf2.html",
    "tracker_url": "https://github.com/KhronosGroup/glTF-Blender-IO/issues/",
    "warning" : "",
    "category" : "Import-Export"
}

import os
import bpy
from xml.dom.minidom import parse
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


def read_xml_data(context, filepath, use_create_edges, plot_elevation):
    
    print(filepath)    
    xml = parse(filepath)
    trkpts = xml.getElementsByTagName("trkpt")

    try:
        print("running read_gpx... printing *.gpx metadata")
        global waypoints
        waypoints = []

        for trkpt in trkpts:
            elevation = 0
            if plot_elevation:
                elevation = float(trkpt.getElementsByTagName("ele")[0].firstChild.nodeValue)
                        
            waypoint = (float(trkpt.attributes["lon"].value), float(trkpt.attributes["lat"].value), elevation)
            waypoints.append(waypoint)
     
        print(waypoints)
        points_to_mesh(waypoints,use_create_edges)

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
    create_edges: BoolProperty(
        name="Create Edges",
        description="Creates connecting edges from each data point to the next",
        default=True,
    )

    plot_elevation: BoolProperty(
        name="Plot Elevation",
        description="Uses the elevation data point as Z-axis",
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
            read_xml_data(context, filepath, self.create_edges, self.plot_elevation)
        return {'FINISHED'}


# Only needed if you want to add into a dynamic menu.
def menu_func_import(self, context):
    self.layout.operator(ImportGPXData.bl_idname, text="GPS Exchange Format (.gpx)")


# Register and add to the "file selector" menu (required to use F3 search "GPS Exchange Format (.gpx)" for quick access).
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
