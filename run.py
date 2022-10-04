import os
import sys

import bpy
sys.path.append(os.getcwd())
import urllib.request
import urllib

sys.path.append(os.getcwd())

# check if the file exists at ./addons/VRM_Addon_for_Blender-release.zip
# if not, download it from github
def check_vrm_addon():
    addon_path = os.path.join(os.getcwd(), 'addons', 'VRM_Addon_for_Blender-release.zip')
    if not os.path.exists(addon_path):
        print('VRM addon not found, downloading...')
        url = 'https://github.com/saturday06/VRM_Addon_for_Blender/raw/release-archive/VRM_Addon_for_Blender-release.zip'
        urllib.request.urlretrieve(url, addon_path)
        print('VRM addon downloaded')

check_vrm_addon()

bpy.ops.preferences.addon_install(overwrite=True,filepath='./addons/cats-blender-plugin-master.zip') 
bpy.ops.preferences.addon_enable(module='cats-blender-plugin-master')

bpy.ops.preferences.addon_install(overwrite=True,filepath='./addons/VRM_Addon_for_Blender-release.zip') 
bpy.ops.preferences.addon_enable(module='VRM_Addon_for_Blender-release')

bpy.ops.wm.save_userpref()

# get the glb name from the first arg passed to the command line
glb_path = sys.argv[4] + '.glb'
print('glb name is', glb_path)

# open blend file
bpy.ops.wm.open_mainfile(filepath=os.path.abspath("./headless.blend"))

# import glb at glb_path
bpy.ops.import_scene.gltf(filepath=glb_path)

print('Scene contents:')
for obj in bpy.data.objects:
    print(obj.name)

vrm_out_file = glb_path.replace('glb', 'vrm')

bpy.ops.vrm.load_human_bone_mappings(filepath="./bonemap.json")
print('Loaded bone map')

# Set the target of the armature modifier on all meshes in the scene to the "Armature" object
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        for mod in obj.modifiers:
            if mod.type == 'ARMATURE':
                mod.object = bpy.data.objects['Armature']

# reparent the mesh to the target armature
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        # set the object parent to objects['Armature']
        obj.parent = bpy.data.objects['Armature']

# Delete any armatures that are not the "Armature" object
for obj in bpy.data.objects:
    if obj.type == 'ARMATURE' and obj.name != 'Armature':
        obj.select_set(True)
    else:
        obj.select_set(False)
bpy.ops.object.delete()

print('Exporting objects')
for obj in bpy.data.objects:
    print(obj.name)

# select armature
bpy.data.objects['Armature'].select_set(True)

# Export VRM
bpy.ops.export_scene.vrm(filepath=vrm_out_file, export_invisibles=False, export_only_selections=False, enable_advanced_preferences=False, export_fb_ngon_encoding=False)
print('Exported', vrm_out_file)