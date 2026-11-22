"""Run with freecadcmd from the Dune_Weaver repo root, DW_OUT=<parts.json>.
Tessellates the table and mechanism into coloured meshes for scripts/models/pack_glb.py.

  cd ~/UbuntuProjects/Dune_Weaver && DW_OUT=/tmp/dw.json QT_QPA_PLATFORM=offscreen \\
    freecadcmd -c "exec(open('<site>/scripts/models/dune_weaver_export.py').read())"
  python3 <site>/scripts/models/pack_glb.py /tmp/dw.json <site>/assets/models/dune-weaver.glb
"""
import json, os
from pathlib import Path
import FreeCAD as App
import MeshPart
OUT = Path(os.environ['DW_OUT'])
STAND_INS = ('mechanism envelope', 'mechanism proxy', 'magnet cup', 'coupling magnet', 'magnet pad')
table_rep = json.loads(Path('reports/table_mount.validate.json').read_text())
datum = float(table_rep['stack']['datum_z'])
yaw = float(json.loads(Path('parameters/table_mount.json').read_text())['mechanism_yaw_deg']['value'])
mapping = App.Placement(App.Vector(), App.Rotation(App.Vector(0, 0, 1), -yaw)).multiply(
    App.Placement(App.Vector(0, 0, -datum), App.Rotation()))
parts = []


def add(name, role, shape, color):
    if role == 'cable reference':
        # Swept cable tubes tessellate into ~1.4M triangles; a coarse angle keeps them to a few sides.
        pts, tris = MeshPart.meshFromShape(Shape=shape, LinearDeflection=3.0, AngularDeflection=1.2,
                                           Relative=False).Topology
    else:
        bb = shape.BoundBox
        tol = max(0.4, min(3.0, bb.DiagonalLength * 0.005))
        pts, tris = shape.tessellate(tol)
    parts.append(dict(name=name, role=role, color=color,
                      v=[[round(p.x, 2), round(p.y, 2), round(p.z, 2)] for p in pts],
                      f=[list(t) for t in tris]))


t = App.openDocument(str(Path('cad/TableMount.FCStd').resolve()))
for o in t.Objects:
    if 'MountRole' not in o.PropertiesList or not hasattr(o, 'Shape') or o.Shape.isNull():
        continue
    if o.MountRole in STAND_INS:
        continue
    s = o.Shape.copy()
    s.Placement = mapping.multiply(s.Placement)
    add(o.Name, o.MountRole, s, None)
m = App.openDocument(str(Path('cad/DuneWeaver_Pulley_Draft.FCStd').resolve()))
for o in m.Objects:
    if 'ComponentRole' not in o.PropertiesList or o.Shape.isNull():
        continue
    s = o.Shape.copy()
    for parent in o.InList:
        if parent.TypeId == 'App::Part':
            s.Placement = parent.getGlobalPlacement().multiply(s.Placement)
            break
    add(o.Name, o.ComponentRole, s, getattr(o, 'DisplayColor', None))
OUT.write_text(json.dumps(parts))
print('parts', len(parts), 'tris', sum(len(p['f']) for p in parts))
