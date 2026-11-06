"""Render an inspection image without saving preview changes to the Blender scene.

    blender -b --factory-startup --python-exit-code 1 --python rendering/render_radiators_preview.py

Blue panels and orange shafts identify the additions. Studio fill and omitted
interior geometry aid inspection; this is not the saved scene's lighting/materials.
"""

from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(ROOT / "assets/scene.blend"))
for name in ("Grass", "Trees", "Soil surface", "Diffuser ceiling", "Light-box reflector",
             "Light pipes", "Ceiling frames"):
    bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)
bpy.data.objects["Eros"].hide_render = True

orange = bpy.data.materials.new("Inspection / orange shafts")
orange.diffuse_color = (0.65, 0.23, 0.035, 1)
orange.use_nodes = True
orange.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = orange.diffuse_color
for ob in bpy.data.objects:
    if ob.get("part") == "shaft":
        ob.material_slots[0].material = orange
panel = bpy.data.materials["Radiators - matte two-sided panels"]
panel.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value = (0.08, 0.32, 0.6, 1)

scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 32
scene.cycles.use_denoising = True
scene.render.threads_mode = 'FIXED'
scene.render.threads = 4
scene.render.resolution_x = scene.render.resolution_y = 800
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.use_compositing = False
scene.view_settings.view_transform = 'Standard'
scene.view_settings.exposure = -4

world = scene.world = bpy.data.worlds.new("Inspection studio")
world.use_nodes = True
nodes, links = world.node_tree.nodes, world.node_tree.links
fill = nodes.get("Background")
fill.inputs["Color"].default_value = (0.32, 0.38, 0.48, 1)
fill.inputs["Strength"].default_value = 20
camera_bg = nodes.new('ShaderNodeBackground')
camera_bg.inputs["Color"].default_value = (0.01, 0.015, 0.025, 1)
path = nodes.new('ShaderNodeLightPath')
mix = nodes.new('ShaderNodeMixShader')
links.new(path.outputs["Is Camera Ray"], mix.inputs[0])
links.new(fill.outputs[0], mix.inputs[1])
links.new(camera_bg.outputs[0], mix.inputs[2])
links.new(mix.outputs[0], nodes.get("World Output").inputs["Surface"])

array = bpy.data.objects["Tori - Array count and spacing"]
pitch = array.modifiers["Torus count and spacing"].constant_offset_displace.z
count = array.modifiers["Torus count and spacing"].count
centre = pitch * (count - 1) / 2
attitude = bpy.data.objects["Habitat - inertial attitude"].matrix_world
camera = scene.camera = bpy.data.objects["Camera - bottom"]
camera.location = attitude @ Vector((0, -1500, -3400))
target = attitude @ Vector((0, 0, centre))
camera.rotation_euler = (target - camera.location).to_track_quat('-Z', 'Y').to_euler()
camera.data.type = 'ORTHO'
camera.data.ortho_scale = 2250
scene.render.filepath = str(ROOT / "radiators-preview.png")
bpy.ops.render.render(write_still=True)
