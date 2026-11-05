import bpy,json,hashlib
from pathlib import Path
import numpy as np

root=Path(__file__).resolve().parent
source=root/'space-habitat-900m.blend'
source_bytes=source.read_bytes()
assert hashlib.sha1(b'blob '+str(len(source_bytes)).encode()+b'\0'+source_bytes).hexdigest()=='f09d8281a47a8f0efef3b20ff1f86e3edcb9b1f6'
bpy.ops.wm.open_mainfile(filepath=str(source))
assert bpy.app.version==(5,2,3)
for image in bpy.data.images:
 if image.source=='FILE':image.filepath='//assets/sky.exr'

def geometry(mesh):
 h=hashlib.sha256()
 for coll,prop,size,dt in [(mesh.vertices,'co',3,np.float32),(mesh.edges,'vertices',2,np.int32),(mesh.loops,'vertex_index',1,np.int32),(mesh.polygons,'loop_start',1,np.int32),(mesh.polygons,'loop_total',1,np.int32),(mesh.polygons,'material_index',1,np.int32)]:
  a=np.empty(len(coll)*size,dtype=dt);coll.foreach_get(prop,a);h.update(a.tobytes())
 return {'counts':[len(mesh.vertices),len(mesh.edges),len(mesh.loops),len(mesh.polygons)],'sha256':h.hexdigest()}

def snapshot():
 s=bpy.context.scene
 objects={}
 for ob in bpy.data.objects:
  objects[ob.name]={'type':ob.type,'data':ob.data.name if ob.data else None,'matrix':[list(row) for row in ob.matrix_world],'parent':ob.parent.name if ob.parent else None,'materials':[slot.material.name if slot.material else None for slot in ob.material_slots],'modifiers':[(m.name,m.type,m.show_viewport,m.show_render,m.node_group.name if m.type=='NODES' and m.node_group else None) for m in ob.modifiers]}
 return {'objects':objects,'meshes':{m.name:geometry(m) for m in bpy.data.meshes if m.users},'scene_count':len(bpy.data.scenes),'camera':s.camera.name,'render':[s.render.resolution_x,s.render.resolution_y,s.render.resolution_percentage,s.cycles.device,s.cycles.samples],'cameras':{c.name:[c.lens,c.clip_start,c.clip_end] for c in bpy.data.cameras},'materials':{m.name:[len(m.node_tree.nodes),len(m.node_tree.links)] if m.use_nodes else None for m in bpy.data.materials},'node_groups':{g.name:[len(g.nodes),len(g.links)] for g in bpy.data.node_groups}}

before=snapshot()
assert before['render']==[1600,1200,100,'GPU',4096],before['render']
local=[m for m in bpy.data.meshes if m.library is None]
vegetation=[m for m in local if m.name.startswith('Broadleaf ') or m.name.startswith('Grass tuft ')]
habitat=[m for m in local if m not in vegetation]
assert len(vegetation)==12,(len(vegetation),[m.name for m in vegetation])
original_names={m:m.name for m in local}
objects_materials={ob.name:[slot.material for slot in ob.material_slots] for ob in bpy.data.objects if ob.type=='MESH' and ob.data in local}
for filename,meshes in [('habitat.blend',habitat),('vegetation.blend',vegetation)]:
 copies=[]
 for m in meshes:
  name=original_names[m];m.name='__split_source__'+name
  clone=m.copy();clone.name=name
  # Keep polygon material indices and the slot count, but retain editable materials in scene.blend.
  for i in range(len(clone.materials)):clone.materials[i]=None
  copies.append(clone)
 bpy.data.libraries.write(str(root/'assets'/filename),set(copies),path_remap='RELATIVE',fake_user=True,compress=True)
 names=[m.name for m in copies]
 for m in copies:bpy.data.meshes.remove(m)
 with bpy.data.libraries.load(str(root/'assets'/filename),link=True,relative=True) as (available,loaded):
  assert set(names)<=set(available.meshes)
  loaded.meshes=names
 linked={m.name:m for m in loaded.meshes}
 for old in meshes:
  old.user_remap(linked[original_names[old]])
 for old in meshes:
  assert old.users==0,(old.name,old.users)
  bpy.data.meshes.remove(old)
for name,materials in objects_materials.items():
 ob=bpy.data.objects[name]
 assert len(ob.material_slots)==len(materials),(name,len(ob.material_slots),len(materials))
 for i,material in enumerate(materials):
  ob.material_slots[i].link='OBJECT';ob.material_slots[i].material=material

assert all(m.library for m in bpy.data.meshes)
after=snapshot()
assert before==after,'Scene state changed during splitting'
bpy.ops.wm.save_as_mainfile(filepath=str(root/'assets/scene.blend'),compress=True,relative_remap=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'assets/scene.blend'))
assert snapshot()==before,'Reopened scene differs from source'
assert {lib.filepath for lib in bpy.data.libraries}=={'//habitat.blend','//vegetation.blend','//eros.blend'}
assert all(Path(bpy.path.abspath(lib.filepath)).is_file() for lib in bpy.data.libraries)
assert [i.filepath for i in bpy.data.images if i.source=='FILE']==['//sky.exr']
print('SPLIT_OK',json.dumps({'Blender':bpy.app.version_string,'habitat_meshes':len(habitat),'vegetation_meshes':len(vegetation),'files':{p.name:p.stat().st_size for p in (root/'assets').glob('*.blend')}}),flush=True)
