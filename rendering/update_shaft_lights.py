"""Add/check 16 inspection-light pairs per shaft in the existing Blender scene.

    blender -b --factory-startup --python-exit-code 1 --python rendering/update_shaft_lights.py
    blender -b --factory-startup --python-exit-code 1 --python rendering/update_shaft_lights.py -- --check-only

Reuses the hub fixture mesh/materials. All shaft lamps share a copy of the hub
light data, with a wider inspection beam and independent brightness control.
"""

import json
import math
from pathlib import Path
import sys

import bpy
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

TAG = "shaft_inspection_light_generator"
COLLECTION = "Elevator inspection lights"
SOURCE = "Shaft inspection light source"
PAIRS = 16
AXIAL_OFFSET = 6.0


def rebuild(geo, drawing, count, pitch, origin):
    col = bpy.data.collections.get(COLLECTION)
    pairs = int(col.get("Pairs per shaft", PAIRS)) if col else PAIRS
    if pairs < 1:
        raise ValueError("Pairs per shaft must be positive")
    for ob in list(bpy.data.objects):
        if ob.get(TAG):
            bpy.data.objects.remove(ob, do_unlink=True)
    if col is None:
        col = bpy.data.collections.new(COLLECTION)
        bpy.data.collections["Habitat stack"].children.link(col)
    source = bpy.data.collections.get(SOURCE) or bpy.data.collections.new(SOURCE)
    # Keep the source outside the scene hierarchy: only its instances render.
    light = bpy.data.objects["Hub light"]
    fixture = bpy.data.objects["Hub light fixture"]
    data = bpy.data.lights.get("Shaft inspection lights - shared power and colour")
    if data is None:
        data = light.data.copy()
        data.name = "Shaft inspection lights - shared power and colour"
        data.spot_size = math.radians(150)
    lamp = bpy.data.objects.new("Shaft inspection light - shared source", data)
    lamp[TAG] = True
    source.objects.link(lamp)
    housing = fixture.copy()
    housing.name = "Shaft inspection light - hub fitting"
    housing[TAG] = True
    housing.parent = None
    housing.matrix_world = light.matrix_world.inverted() @ fixture.matrix_world
    source.objects.link(housing)
    col["Pairs per shaft"] = pairs
    col["Axial offset (m)"] = AXIAL_OFFSET
    col["Power control"] = data.name
    col["Scope"] = "Rendering layout; beam coverage and electrical ratings not engineered"
    col["Regenerate"] = "Run rendering/update_shaft_lights.py after changing pair count"
    inner, outer = geo["hub_radius"], drawing["shafts"]["main_top"]
    for k in range(count):
        for q in range(drawing["shafts"]["count"]):
            angle = k * drawing["shafts"]["stagger"] + q * math.pi / 2
            turn = Matrix.Rotation(angle, 4, 'Z')
            for j in range(pairs):
                radius = inner + (j + 0.5) * (outer - inner) / pairs
                for side in (-1, 1):
                    ob = bpy.data.objects.new(
                        f"Shaft lamp T{k+1:02d} Q{q+1} pair {j+1:02d} {'+' if side > 0 else '-'}", None)
                    col.objects.link(ob)
                    ob.instance_type = 'COLLECTION'
                    ob.instance_collection = source
                    ob.parent = bpy.data.objects["Habitat - inertial attitude"]
                    local = Vector((radius, 0, side * AXIAL_OFFSET))
                    ob.location = turn.to_3x3() @ local + Vector((origin[0], origin[1], origin[2] + k * pitch))
                    # Local -Z is the beam. Aim 45 degrees along the shaft,
                    # back towards its plane, so neighbouring beams overlap.
                    direction = turn.to_3x3() @ Vector((1, 0, -side))
                    ob.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
                    ob[TAG] = True
                    ob["torus"], ob["quadrant"], ob["pair"], ob["side"] = k, q, j, side
    bpy.context.view_layer.update()
    return validate(geo, drawing, count, pitch, origin)


def validate(geo, drawing, count, pitch, origin):
    col = bpy.data.collections[COLLECTION]
    pairs = col["Pairs per shaft"]
    lamps = list(col.objects)
    shafts = count * drawing["shafts"]["count"]
    assert len(lamps) == shafts * pairs * 2
    source = bpy.data.collections[SOURCE]
    assert source not in list(bpy.context.scene.collection.children_recursive)
    assert len(source.objects) == 2
    template = next(o for o in source.objects if o.type == 'LIGHT')
    housing = next(o for o in source.objects if o.type == 'MESH')
    assert housing.data == bpy.data.objects["Hub light fixture"].data
    assert [s.material for s in housing.material_slots] == [s.material for s in bpy.data.objects["Hub light fixture"].material_slots]
    assert template.data != bpy.data.objects["Hub light"].data
    assert template.data.type == 'SPOT'
    inner, outer = geo["hub_radius"], drawing["shafts"]["main_top"]
    seen = set()
    for ob in lamps:
        assert ob.get(TAG) and ob.parent == bpy.data.objects["Habitat - inertial attitude"]
        assert ob.instance_collection == source
        k, q, j, side = ob["torus"], ob["quadrant"], ob["pair"], ob["side"]
        key = (k, q, j, side)
        assert key not in seen
        seen.add(key)
        angle = k * drawing["shafts"]["stagger"] + q * math.pi / 2
        turn = Matrix.Rotation(angle, 3, 'Z')
        position = turn.inverted() @ (ob.location - Vector((origin[0], origin[1], origin[2] + k * pitch)))
        radius = inner + (j + 0.5) * (outer - inner) / pairs
        assert abs(position.x - radius) < 0.002 and abs(position.y) < 0.002
        assert abs(position.z - side * AXIAL_OFFSET) < 0.002
        direction = ob.rotation_euler.to_matrix() @ Vector((0, 0, -1))
        expected = (turn @ Vector((1, 0, -side))).normalized()
        assert direction.dot(expected) > 0.99999
    return dict(shafts=shafts, pairs_per_shaft=pairs, lamps_per_shaft=2 * pairs,
                lamps_total=len(lamps), spacing_m=(outer - inner) / pairs,
                axial_offset_m=AXIAL_OFFSET, shared_source=template.data.name)


def original_state():
    s = bpy.context.scene
    return dict(objects={o.name:([list(r) for r in o.matrix_world],
                        o.data.name if o.data else None,
                        [m.material.name if m.material else None for m in o.material_slots])
                        for o in bpy.data.objects if not o.get(TAG)},
                render=[s.camera.name,s.render.resolution_x,s.render.resolution_y,
                        s.render.resolution_percentage,s.cycles.device,s.cycles.samples,s.view_settings.exposure],
                hub_light=[bpy.data.objects['Hub light'].data.energy,
                           list(bpy.data.objects['Hub light'].data.color),
                           bpy.data.objects['Hub light'].data.spot_size])


def main():
    from rendering.update_radiators import ASSETS, settings
    scene = ASSETS / "scene.blend"
    bpy.ops.wm.open_mainfile(filepath=str(scene))
    config = settings()
    if '--check-only' in sys.argv:
        print('SHAFT_LIGHTS_OK', json.dumps(validate(*config)))
        return
    before = original_state()
    report = rebuild(*config)
    assert original_state() == before, 'Original scene state changed'
    bpy.ops.wm.save_as_mainfile(filepath=str(scene), compress=False, relative_remap=True)
    bpy.ops.wm.open_mainfile(filepath=str(scene))
    assert original_state() == before, 'Original scene changed after reopening'
    validate(*settings())
    print('SHAFT_LIGHTS_OK', json.dumps(report))


if __name__ == '__main__':
    main()
