"""Build the valley torus in Blender, with editable Screw/Solidify/Boolean modifiers.

Open this file in Blender's Scripting workspace using Text > Open, then Text > Run Script.
Change RADIUS_M below and run again to rebuild this script's collection only.
Keep this file in the repository's blender/ directory. NumPy is bundled with Blender.

Dimensions and steel sizing are imported from the surrounding repository checkout.
Only the tube layers are drawn: hull, nominal rock jacket, outer cell wall, crawl
space and bumper. The solver uses the model's default 1 g, side anchors, vaulted
ceiling, 144 circumferential and four radial section elements. Frames, cell walls,
stiffeners, cables, fill, buildings and the floor's shield credit are not drawn.

Dimension convention: the model locates zero-thickness skin reference surfaces at
a and a+jacket. Keep the rock exactly between these surfaces; put finite hull
steel inward and outer-wall steel outward to avoid intersecting layers. The clear
air radius is therefore a minus hull thickness. The crawl space is measured from
the finished outer wall, and the bumper adds its own thickness beyond it. These
millimetre-scale envelope corrections are explicit, not thickness exaggerations.
Section-element steel thicknesses are averaged onto neighbouring profile vertices.
Solidify interpolates these samples, so this is a modelling surface, not a
fabrication drawing or an exact finite-element volume/mass reconstruction.
"""

# ------------------------- Main parameter ----------------------------------
RADIUS_M = 900.0             # Model floor / outer-rim reference radius, metres.

# ------------------------- Display options ---------------------------------
CUTAWAY = True              # Remove the +X,+Y quarter using live Booleans.
SHOW_BUMPER = False         # Hide the thin outer bumper initially to expose hull.
RING_STEPS = 256            # Around the habitat; increase for close views.
RENDER_STEPS = 512
ANCHORS = "sides"           # Model choices: sides, crest, fan.
CEILING = "vaulted"         # Model choices: vaulted, hung.

import math
import sys
from pathlib import Path

COLLECTION_NAME = "Habitat - generated layers"
GENERATOR_ID = "vinc.space-habitat.blender.layers.v1"
MODEL_SOURCE = "habitat_model + structure_model/tube_section.py in this checkout"


def repository_root():
    script = Path(__file__).resolve()
    for root in (script.parent, script.parent.parent):
        if (root / "habitat_model" / "geometry.py").is_file() and \
                (root / "structure_model" / "tube_section.py").is_file():
            return root
    raise RuntimeError("Keep build_habitat.py in the repository's blender/ directory")


def calculate(radius_m):
    """Recalculate both geometry and steel sizing for the requested radius."""
    import numpy as np

    if isinstance(radius_m, bool) or not isinstance(radius_m, (int, float)):
        raise ValueError("RADIUS_M must be a number in metres")
    if not math.isfinite(radius_m) or not 200 <= radius_m <= 2500:
        raise ValueError("RADIUS_M must be between 200 and 2500 m (explorer domain)")
    root = repository_root()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from habitat_model.assumptions import load, params
    from habitat_model.design import Design
    from habitat_model import geometry, mass
    from structure_model import tube_section

    # Avoid silently importing another checkout that was opened in this session.
    for module in (geometry, mass, tube_section):
        if not Path(module.__file__).resolve().is_relative_to(root):
            raise RuntimeError("Another model checkout is already imported; restart Blender")
    p = params(load())
    d = Design(radius_m=float(radius_m), n_tori=1)
    geo = geometry.compute(p, d)
    model_mass = mass.compute(p, d, geo)
    inp = tube_section.inputs(p, d, geo, model_mass)
    sized = tube_section.Model(inp, ANCHORS, CEILING, n_radial=4, n_around=144).size()
    if not sized["sized"]:
        raise RuntimeError("Section sizing failed its allowable-stress check; scene left untouched")
    # Solver thicknesses live at edges; average adjacent edges onto profile nodes.
    profiles = {
        key: (sized[key] + np.roll(sized[key], 1)) / 2
        for key in ("t_hull", "t_outer")
    }
    return p, geo, sized, profiles


def material(bpy, name, rgba, metallic=0.0, roughness=0.7):
    name = "Habitat / " + name
    mat = next((m for m in bpy.data.materials
                if m.name == name and m.get("generator") == GENERATOR_ID), None)
    if mat is None:
        mat = bpy.data.materials.new(name)
        mat["generator"] = GENERATOR_ID
    mat.diffuse_color = rgba
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get("Principled BSDF")
    if shader:
        shader.inputs["Base Color"].default_value = rgba
        shader.inputs["Metallic"].default_value = metallic
        shader.inputs["Roughness"].default_value = roughness
    return mat


def fresh_collection(bpy):
    # Remove only objects explicitly tagged as this generator's previous output.
    old = next((c for c in bpy.data.collections
                if c.get("generator") == GENERATOR_ID), None)
    if old:
        for obj in list(old.objects):
            if obj.get("generator") == GENERATOR_ID:
                data = obj.data
                bpy.data.objects.remove(obj, do_unlink=True)
                if isinstance(data, bpy.types.Mesh) and data.users == 0:
                    bpy.data.meshes.remove(data)
        if not old.objects and not old.children:
            bpy.data.collections.remove(old)
    collection = bpy.data.collections.new(COLLECTION_NAME)
    collection["generator"] = GENERATOR_ID
    bpy.context.scene.collection.children.link(collection)
    return collection


def new_mesh(bpy, collection, name, vertices, edges=(), faces=()):
    mesh = bpy.data.meshes.new(name + " profile")
    mesh.from_pydata(vertices, edges, faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    obj["generator"] = GENERATOR_ID
    collection.objects.link(obj)
    return obj


def outward_normals(bpy, obj, screw, centre):
    """Check evaluated normals, rather than assuming Screw's orientation."""
    depsgraph = bpy.context.evaluated_depsgraph_get()
    depsgraph.update()
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    try:
        face = mesh.polygons[0]
        c = face.center
        r = math.hypot(c.x, c.y)
        direction = ((r - centre) * c.x / r, (r - centre) * c.y / r, c.z)
        if sum(a * b for a, b in zip(face.normal, direction)) < 0:
            screw.use_normal_flip = not screw.use_normal_flip
    finally:
        evaluated.to_mesh_clear()


def layer(bpy, collection, name, centre, radii, thicknesses, offset, mat, cutter):
    count = len(radii)
    vertices = []
    for i, radius in enumerate(radii):
        phi = math.tau * i / count  # 0 = floor side, pi = hub-facing crest.
        vertices.append((centre + float(radius) * math.cos(phi), 0.0,
                         float(radius) * math.sin(phi)))
    edges = [(i, (i + 1) % count) for i in range(count)]
    obj = new_mesh(bpy, collection, name, vertices, edges)
    obj.data.materials.append(mat)

    maximum = max(float(t) for t in thicknesses)
    group = obj.vertex_groups.new(name="Model thickness / maximum")
    for i, t in enumerate(thicknesses):
        group.add([i], float(t) / maximum, "REPLACE")

    screw = obj.modifiers.new("01 Revolve profile around habitat axis", "SCREW")
    screw.axis = "Z"
    screw.angle = math.tau
    screw.screw_offset = 0.0
    screw.iterations = 1
    screw.steps = RING_STEPS
    screw.render_steps = RENDER_STEPS
    screw.use_merge_vertices = True
    screw.merge_threshold = 0.00001
    screw.use_smooth_shade = True
    screw.use_normal_calculate = True
    outward_normals(bpy, obj, screw, centre)

    solid = obj.modifiers.new("02 Material thickness (metres)", "SOLIDIFY")
    solid.thickness = maximum
    solid.offset = offset
    solid.use_even_offset = True
    solid.use_quality_normals = True
    solid.use_rim = True
    solid.vertex_group = group.name
    solid.thickness_vertex_group = 0.0
    if cutter is not None:
        cut = obj.modifiers.new("03 Quarter cutaway - disable to restore full ring", "BOOLEAN")
        cut.operation = "DIFFERENCE"
        cut.solver = "EXACT"
        cut.object = cutter
    obj["minimum_thickness_m"] = min(float(t) for t in thicknesses)
    obj["maximum_thickness_m"] = maximum
    obj["thickness_note"] = "Solidify Thickness is maximum; vertex group scales it around tube"
    obj["model_source"] = MODEL_SOURCE
    return obj


def quarter_cutter(bpy, collection, reach):
    # A closed box removes +X,+Y. Tiny asymmetric offset avoids faces coincident
    # with ring seams while being negligible at habitat scale.
    lo = -0.001
    vertices = [(x, y, z) for z in (-reach, reach)
                for y in (lo, reach) for x in (lo, reach)]
    faces = [(0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4),
             (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5)]
    obj = new_mesh(bpy, collection, "Cutaway tool (hidden)", vertices, faces=faces)
    obj.display_type = "WIRE"
    obj.hide_render = True
    obj.hide_set(True)
    return obj


def viewport(bpy, reach):
    from mathutils import Vector

    # Set every open 3D view, including the Layout workspace, without shortcuts.
    eye = Vector((1.2, 1.4, 1.1))
    rotation = (-eye).to_track_quat("-Z", "Y")
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type != "VIEW_3D":
                continue
            space = area.spaces.active
            space.clip_start = 0.05
            space.clip_end = max(10000.0, reach * 20)
            space.shading.type = "SOLID"
            space.shading.color_type = "MATERIAL"
            space.overlay.show_floor = False
            space.overlay.show_axis_x = False
            space.overlay.show_axis_y = False
            if space.region_3d:
                space.region_3d.view_location = (0.0, 0.0, 0.0)
                space.region_3d.view_distance = reach * 3.1
                space.region_3d.view_rotation = rotation
                space.region_3d.view_perspective = "PERSP"


def main():
    import bpy
    import numpy as np

    if not (isinstance(RING_STEPS, int) and 32 <= RING_STEPS <= 4096):
        raise ValueError("RING_STEPS must be an integer from 32 to 4096")
    if not (isinstance(RENDER_STEPS, int) and 32 <= RENDER_STEPS <= 4096):
        raise ValueError("RENDER_STEPS must be an integer from 32 to 4096")
    print("Habitat: calculating geometry and steel sizing...", flush=True)
    p, geo, section, profiles = calculate(RADIUS_M)
    if bpy.context.object and bpy.context.object.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    collection = fresh_collection(bpy)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene.unit_settings.length_unit = "METERS"

    steel = material(bpy, "Pressure hull", (0.52, 0.63, 0.72, 1), 0.75, 0.35)
    wall = material(bpy, "Outer jacket wall", (0.28, 0.39, 0.47, 1), 0.75, 0.4)
    rock = material(bpy, "Compacted rock", (0.34, 0.23, 0.14, 1), 0, 0.95)
    bumper_mat = material(bpy, "Bumper", (0.65, 0.68, 0.70, 1), 0.65, 0.4)
    a = geo["tube_radius"]
    centre = geo["radius"] - a
    count = len(profiles["t_hull"])
    uniform = lambda x: np.full(count, x)
    reach = geo["envelope_outer"] + float(profiles["t_outer"].max()) + p.bumper_m
    cutter = quarter_cutter(bpy, collection, reach * 1.3) if CUTAWAY else None
    hull = layer(bpy, collection, "01 Steel - pressure hull", centre, uniform(a),
                 profiles["t_hull"], -1.0, steel, cutter)
    jacket = layer(bpy, collection, "02 Rock - nominal jacket", centre, uniform(a),
                   uniform(geo["jacket"]), 1.0, rock, cutter)
    outer = layer(bpy, collection, "03 Steel - outer jacket wall", centre,
                  uniform(a + geo["jacket"]), profiles["t_outer"], 1.0, wall, cutter)
    bumper = layer(bpy, collection, "04 Steel - bumper (outside crawl space)", centre,
                   uniform(a + geo["jacket"] + p.crawl_space_m) + profiles["t_outer"],
                   uniform(p.bumper_m), 1.0, bumper_mat, cutter)
    bumper.hide_set(not SHOW_BUMPER)
    bumper.hide_render = not SHOW_BUMPER
    for obj in (hull, jacket, outer, bumper):
        obj["floor_reference_radius_m"] = geo["radius"]
        obj["tube_centreline_radius_m"] = centre
        obj["nominal_tube_diameter_m"] = geo["width"]
        obj["nominal_jacket_thickness_m"] = geo["jacket"]
        obj["crawl_clearance_m"] = p.crawl_space_m
    collection["radius_m"] = float(RADIUS_M)
    collection["model_source"] = MODEL_SOURCE
    collection["section_converged"] = bool(section["converged"])
    collection["section_utilisation"] = float(section["utilisation"])
    for obj in bpy.context.selected_objects:
        obj.select_set(False)
    hull.select_set(True)
    bpy.context.view_layer.objects.active = hull
    viewport(bpy, reach)
    report = f"""Habitat layers - source {MODEL_SOURCE}

Main parameter RADIUS_M = {RADIUS_M:g} m (model floor reference).
Tube centreline radius = {centre:.6f} m.
Nominal tube diameter = {2*a:.6f} m.
Nominal rock jacket = {geo['jacket']:.6f} m (before floor fill credit).
Pressure hull = {section['t_hull'].min()*1000:.4f} to {section['t_hull'].max()*1000:.4f} mm.
Outer jacket wall = {section['t_outer'].min()*1000:.4f} to {section['t_outer'].max()*1000:.4f} mm.
Crawl clearance = {p.crawl_space_m:g} m outside finished outer wall.
Bumper = {p.bumper_m*1000:g} mm; hidden initially = {not SHOW_BUMPER}.
Section: anchors={ANCHORS}, ceiling={CEILING}, converged={section['converged']}.
Steel thickness samples are averaged from section elements to profile vertices.

Each layer has live Screw > Solidify > Boolean modifiers.
Solidify Thickness shows the maximum, with its vertex group distributing the thickness.
Disable the Boolean monitor icon on every layer to remove the quarter cutaway,
or set CUTAWAY=False and rerun. Show the bumper using the Outliner's eye icon.
Change RADIUS_M at the top of the script and run again to recompute all layers.
Only tagged generator objects are replaced. Save your scene using File > Save As.

The thin-shell model's interfaces are kept at a and a+jacket. Steel is added to
opposite sides of the nominal rock jacket: pressure hull inward, cell wall outward.
Air space is smaller than the nominal tube by the hull's thickness on each side.
The outer wall and bumper add millimetres to the model's nominal outer envelope.
The rock is the nominal jacket; thinning credited to floor fill is not drawn.
No frames, cell walls, stiffeners, anchors, spokes, internal fill or buildings.
Their absence means the visible shells alone do not represent all structural steel.
"""
    text_name = "Habitat layers - dimensions and notes"
    notes = next((t for t in bpy.data.texts if t.name == text_name
                  and t.get("generator") == GENERATOR_ID), None)
    if notes is None:
        notes = bpy.data.texts.new(text_name)
        notes["generator"] = GENERATOR_ID
    notes.clear()
    notes.write(report)
    print(report, flush=True)


if __name__ == "__main__":
    main()
