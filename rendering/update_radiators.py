"""Update the saved scene's elevator shafts and radiator wings with Blender 5.2+.

Run from the repository root:
    blender -b --factory-startup --python-exit-code 1 --python rendering/update_radiators.py

Only this script's tagged objects/meshes are replaced. Existing structural meshes,
materials, cameras, lighting, planting and render settings are preserved. The scene
is saved uncompressed; the new meshes join the existing habitat mesh library.
"""

import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from habitat_model import geometry, layout, wing_geometry
from habitat_model.assumptions import load, params
from habitat_model.design import Design

ASSETS = ROOT / "rendering/assets"
TAG = "radiator_shaft_generator"
COLLECTION = "Elevators and radiator wings"
PREFIX = "Elevator and radiator / "


def mesh(name, vertices, faces):
    data = bpy.data.meshes.new(PREFIX + name)
    data.from_pydata(vertices, [], faces)
    data.update()
    data.use_fake_user = True
    data[TAG] = True
    data.materials.append(None)  # editable, object-linked material in scene.blend
    return data


def beam(vertices, faces, start, end, width):
    """A square member, with no operators or temporary scene objects."""
    a, b = Vector(start), Vector(end)
    axis = (b - a).normalized()
    u = axis.cross(Vector((0, 0, 1)))
    if u.length < 0.1:
        u = axis.cross(Vector((0, 1, 0)))
    u.normalize()
    v = axis.cross(u)
    i = len(vertices)
    for p in (a, b):
        vertices.extend(tuple(p + width / 2 * (s * u + t * v))
                        for s, t in ((-1, -1), (1, -1), (1, 1), (-1, 1)))
    faces.extend(tuple(i + k for k in f) for f in
                 ((3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4),
                  (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)))


def shaft_mesh(geo, drawing):
    vertices, faces = [], []
    width = drawing["shafts"]["width"]
    # The 8 m envelope, 0.9 m rails, 0.22 m braces and 12 m bays are
    # illustration dimensions, not a structural sizing of the shafts.
    corner = (width - 0.9) / 2
    corners = [(-corner, -corner), (corner, -corner),
               (corner, corner), (-corner, corner)]
    inner = math.sqrt(geo["hub_radius"] ** 2 - corner ** 2) - 0.5
    outer = drawing["shafts"]["main_top"]
    for y, z in corners:
        beam(vertices, faces, (inner, y, z), (outer, y, z), 0.9)
    stations = [inner + (outer - inner) * i / math.ceil((outer - inner) / 12)
                for i in range(math.ceil((outer - inner) / 12) + 1)]
    for x in stations:
        for j, (y, z) in enumerate(corners):
            yy, zz = corners[(j + 1) % 4]
            beam(vertices, faces, (x, y, z), (x, yy, zz), 0.22)
    for i, (x, nx) in enumerate(zip(stations, stations[1:])):
        for j in range(4):
            a, b = corners[j], corners[(j + 1) % 4]
            if i % 2:
                a, b = b, a
            beam(vertices, faces, (x, *a), (nx, *b), 0.22)
    # Short brackets cross the 1 m shaft/panel clearance. They illustrate
    # attachment, without changing the panel footprint used by the thermal model.
    r0, r1 = drawing["wings"]["main"]["band"]
    for x in stations:
        if r0 + 1 < x < r1 - 1:
            for side in (-1, 1):
                beam(vertices, faces, (x, side * (width / 2 - 0.2), 0),
                     (x, side * (drawing["wings"]["edge"] + 0.4), 0), 0.18)
    return mesh("8 m shaft truss", vertices, faces)


def guide_mesh(drawing):
    """Open guide around the last 5 m, without a rigid radial end plate."""
    vertices, faces = [], []
    top = drawing["shafts"]["main_top"]
    c = drawing["shafts"]["width"] / 2 + 0.35
    corners = [(-c, -c), (c, -c), (c, c), (-c, c)]
    for x in (top - 5, top):
        for j, (y, z) in enumerate(corners):
            yy, zz = corners[(j + 1) % 4]
            beam(vertices, faces, (x, y, z), (x, yy, zz), 0.35)
    for y, z in corners:
        beam(vertices, faces, (top - 5, y, z), (top, y, z), 0.35)
    return mesh("5 m sliding rim guide", vertices, faces)


def wing_mesh(drawing, side):
    wing = drawing["wings"]["main"]
    r0, r1 = wing["band"]
    edge, beta = drawing["wings"]["edge"], wing["angle"]
    start = max(r0, edge / math.sin(beta))
    vertices, faces = [], []
    nr, na = 128, 8
    for i in range(nr + 1):
        rho = start + (r1 - start) * i / nr
        phi0 = math.asin(edge / rho)
        for j in range(na + 1):
            phi = phi0 + (beta - phi0) * j / na
            vertices.append((rho * math.cos(phi), side * rho * math.sin(phi), 0))
    for i in range(nr):
        for j in range(na):
            a = i * (na + 1) + j
            face = (a, a + na + 1, a + na + 2, a + 1)
            faces.append(face if side > 0 else tuple(reversed(face)))
    data = mesh("radiator wing " + ("left" if side > 0 else "right"), vertices, faces)
    data["coverage_per_torus"] = wing["coverage"]
    data["one_face_area_m2"] = wing_geometry.area(beta, r0, r1, edge) / 8
    return data


def settings():
    """Read the actual saved assembly, including its slightly larger skin pitch."""
    array_obj = bpy.data.objects["Tori - Array count and spacing"]
    array = array_obj.modifiers["Torus count and spacing"]
    if (not array.use_constant_offset or array.use_relative_offset
            or array.use_object_offset or any(abs(v) > 1e-6 for v in array.constant_offset_displace[:2])):
        raise ValueError("Expected the existing axial, constant-pitch torus Array")
    hull = bpy.data.objects["Pressure hull"].data
    radius = max(math.hypot(v.co.x, v.co.y) for v in hull.vertices)
    p = params(load())
    d = Design(radius_m=round(radius, 3), n_tori=array.count, tiers_lit=0, site="Eros")
    geo = geometry.compute(p, d)
    drawing = layout.compute(p, d, geo)
    # The saved bumper includes steel thickness outside the model's ideal
    # envelope. Clear its actual inner face by 1 cm, retaining the model's
    # total panel area through a tiny increase in wing angle.
    main = drawing["wings"]["main"]
    model_band = tuple(main["band"])
    bumper = bpy.data.objects["Bumper"].data
    surface = BVHTree.FromPolygons([v.co for v in bumper.vertices],
                                  [list(f.vertices) for f in bumper.polygons])
    # Use the faces, not just their vertices: the polygonal circumference
    # reaches a few centimetres farther inward between vertices.
    bumper_inner = surface.find_nearest(Vector((0, 0, 0)))[3]
    safe_outer = math.sqrt((bumper_inner - 0.01) ** 2 - 0.03 ** 2)
    r0, r1 = model_band[0], min(model_band[1], safe_outer)
    main["model_band"] = model_band
    main["band"] = (r0, r1)
    adjusted_cover = main["area_per_torus"] / (math.pi * (r1 ** 2 - r0 ** 2))
    main["angle"] = layout.wing_angle(adjusted_cover, r0, r1, drawing["wings"]["edge"])
    origin = array_obj.location + array_obj.data.vertices[0].co
    return geo, drawing, array.count, array.constant_offset_displace.z, tuple(origin)


def material(name, color, metallic, roughness):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    m.diffuse_color = (*color, 1)
    return m


def validate(geo, drawing, count, pitch, origin):
    objects = [o for o in bpy.data.objects if o.get(TAG)]
    assert len(objects) == count * 4 * 4
    expected_area = drawing["wings"]["main"]["area_per_torus"]
    area = 0
    for ob in objects:
        assert ob.parent == bpy.data.objects["Habitat - inertial attitude"]
        k, q = ob["torus"], ob["quadrant"]
        assert abs(ob.location.z - origin[2] - k * pitch) < 1e-4
        assert abs(ob.rotation_euler.z - (k * drawing["shafts"]["stagger"] + q * math.pi / 2)) < 1e-6
        assert ob.data.library.filepath == "//habitat.blend"
        if ob.get("part") == "wing":
            r0, r1 = drawing["wings"]["main"]["band"]
            for v in ob.data.vertices:
                assert r0 - 1e-3 <= math.hypot(v.co.x, v.co.y) <= r1 + 1e-3
                assert abs(v.co.y) >= drawing["wings"]["edge"] - 1e-4
                assert abs(math.atan2(v.co.y, v.co.x)) <= drawing["wings"]["main"]["angle"] + 1e-7
                assert abs(v.co.z) < 1e-6
            area += sum(f.area for f in ob.data.polygons)
    assert abs(area / (count * expected_area) - 1) < 1e-4
    assert {lib.filepath for lib in bpy.data.libraries} == {"//habitat.blend", "//vegetation.blend", "//eros.blend"}
    assert all(Path(bpy.path.abspath(lib.filepath)).is_file() for lib in bpy.data.libraries)
    return dict(tori=count, shafts=count * 4, wings=count * 8,
                band_m=list(drawing["wings"]["main"]["band"]),
                one_face_area_per_torus_m2=area / count,
                half_angle_deg=math.degrees(drawing["wings"]["main"]["angle"]),
                stagger_deg=math.degrees(drawing["shafts"]["stagger"]), pitch_m=pitch)


def main():
    if bpy.app.version < (5, 2, 0):
        raise RuntimeError("Use Blender 5.2 or newer for the saved scene")
    scene_path, habitat_path = ASSETS / "scene.blend", ASSETS / "habitat.blend"
    bpy.ops.wm.open_mainfile(filepath=str(scene_path))
    geo, drawing, count, pitch, origin = settings()
    if "--check-only" in sys.argv:
        print("RADIATORS_OK", json.dumps(validate(geo, drawing, count, pitch, origin)))
        return
    # Edit only the mesh library; none of the original mesh datablocks are touched.
    bpy.ops.wm.open_mainfile(filepath=str(habitat_path))
    for m in list(bpy.data.meshes):
        if m.get(TAG):
            bpy.data.meshes.remove(m)
    new_meshes = [shaft_mesh(geo, drawing), guide_mesh(drawing),
                  wing_mesh(drawing, 1), wing_mesh(drawing, -1)]
    names = [m.name for m in new_meshes]
    bpy.ops.wm.save_as_mainfile(filepath=str(habitat_path), compress=True)
    bpy.ops.wm.open_mainfile(filepath=str(scene_path))
    for ob in list(bpy.data.objects):
        if ob.get(TAG):
            bpy.data.objects.remove(ob, do_unlink=True)
    col = bpy.data.collections.get(COLLECTION)
    if col is None:
        col = bpy.data.collections.new(COLLECTION)
        bpy.data.collections["Habitat stack"].children.link(col)
    with bpy.data.libraries.load(str(habitat_path), link=True, relative=True) as (_, loaded):
        loaded.meshes = list(names)
    sources = {m.name: m for m in loaded.meshes}
    steel = bpy.data.materials["Hub - brushed stainless steel"]
    radiator = material("Radiators - matte two-sided panels", (0.12, 0.14, 0.16), 0.05, 0.8)
    guide = material("Elevators - sliding guide housing", (0.11, 0.12, 0.13), 0.65, 0.5)
    for k in range(count):
        for q in range(drawing["shafts"]["count"]):
            for name, part, mat in zip(names, ("shaft", "guide", "wing", "wing"),
                                       (steel, guide, radiator, radiator)):
                ob = bpy.data.objects.new(f"Torus {k + 1:02d} / quadrant {q + 1} / {name.removeprefix(PREFIX)}", sources[name])
                col.objects.link(ob)
                ob.parent = bpy.data.objects["Habitat - inertial attitude"]
                ob.location = (origin[0], origin[1], origin[2] + k * pitch)
                ob.rotation_euler.z = k * drawing["shafts"]["stagger"] + q * math.pi / 2
                ob[TAG], ob["part"], ob["torus"], ob["quadrant"] = True, part, k, q
                ob.material_slots[0].link = 'OBJECT'
                ob.material_slots[0].material = mat
                if part == "wing":
                    solid = ob.modifiers.new("Panel thickness - visual 60 mm", 'SOLIDIFY')
                    solid.thickness, solid.offset = 0.06, 0
    col["geometry_source"] = "habitat_model/layout.py and wing_geometry.py; main section, no farms"
    col["regenerate"] = "Run rendering/update_radiators.py after changing the torus Array count/pitch"
    col["shaft_scope"] = "8 m truss placeholder; 5 m sliding guide schematic; fittings and penetrations not engineered"
    col["panel_scope"] = "5% coverage; two-sided; 60 mm visual thickness; visible shader is not thermal emissivity"
    if bpy.data.collections.get("Elevator inspection lights"):
        from rendering.update_shaft_lights import rebuild
        rebuild(geo, drawing, count, pitch, origin)
    bpy.context.view_layer.update()
    validate(geo, drawing, count, pitch, origin)
    bpy.ops.wm.save_as_mainfile(filepath=str(scene_path), compress=False, relative_remap=True)
    bpy.ops.wm.open_mainfile(filepath=str(scene_path))
    print("RADIATORS_OK", json.dumps(validate(geo, drawing, count, pitch, origin)))


if __name__ == "__main__":
    main()
