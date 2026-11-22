"""Pack the tessellated Dune Weaver parts into one small GLB (stdlib only).

Positions are quantised to int16 (KHR_mesh_quantization), indices are uint16,
normals are left out so three.js shades the CAD flat. Small fasteners are dropped.
"""
import json, math, struct, sys
from collections import defaultdict

src, dst = sys.argv[1], sys.argv[2]
parts = json.load(open(src))

DROP = {'fastener envelope', 'purchased fastener envelope', 'purchased nut envelope',
        'cable reference'}  # cables are swept tubes, over 1M triangles
# name: (rgb hex, metallic, roughness, alpha, emissive hex or None)
MATS = {
    'glass':   ('#bad7df', 0.0, 0.05, 0.16, None),
    'sand':    ('#d9c49b', 0.0, 0.95, 1.0, None),
    'board':   ('#26242b', 0.0, 0.8, 1.0, None),
    'print':   ('#2d2c36', 0.0, 0.6, 1.0, None),
    'wood':    ('#8a5a34', 0.0, 0.75, 1.0, None),
    'led':     ('#35d6ea', 0.0, 0.5, 1.0, '#35d6ea'),
    'steel':   ('#3b3b40', 0.6, 0.45, 1.0, None),
    'pcb':     ('#1f5f3a', 0.1, 0.6, 1.0, None),
    'electro': ('#536a85', 0.0, 0.6, 1.0, None),
    'ball':    ('#d7dbe0', 1.0, 0.18, 1.0, None),
}
ROLE = {
    'glass': 'glass', 'eva': 'sand', 'base board': 'board', 'side trim': 'wood', 'led strip': 'led',
    'table leg proxy': 'steel', 'ikea cross': 'steel', 'metal top ring reference': 'steel', 'electronics proxy': 'pcb',
    'base disc': 'electro', 'electronics deck': 'electro', 'electronics cover': 'electro',
    'electronics hanger': 'electro',
}


def mat_for(p):
    if p['color']:
        key = 'mech:' + p['color']
        if key not in MATS:
            metal = 'purchased' in p['role'] and 'motor' not in p['role'] and 'sensor' not in p['role']
            MATS[key] = (p['color'], 0.5 if metal else 0.0, 0.5, 1.0, None)
        return key
    return ROLE.get(p['role'], 'print')


def sphere(cx, cy, cz, r, seg=20, rings=14):
    v, f = [], []
    for i in range(rings + 1):
        th = math.pi * i / rings
        for j in range(seg):
            ph = 2 * math.pi * j / seg
            v.append([cx + r * math.sin(th) * math.cos(ph), cy + r * math.sin(th) * math.sin(ph), cz + r * math.cos(th)])
    for i in range(rings):
        for j in range(seg):
            a, b = i * seg + j, i * seg + (j + 1) % seg
            c, d = a + seg, b + seg
            f += [[a, c, b], [b, c, d]]
    return v, f


eva_top = max(v[2] for p in parts if p['role'] == 'eva' for v in p['v'])
bv, bf = sphere(200.0, 0.0, eva_top + 5.0, 5.0)  # 10 mm steel ball at rho 200 on the arm axis
parts.append(dict(name='Ball', role='ball', color=None, v=bv, f=bf))
ROLE['ball'] = 'ball'

groups = defaultdict(list)
for p in parts:
    if p['role'] in DROP or not p['f']:
        continue
    groups[mat_for(p)].append(p)

allv = [v for ps in groups.values() for p in ps for v in p['v']]
lo = [min(v[i] for v in allv) for i in range(3)]
hi = [max(v[i] for v in allv) for i in range(3)]
ctr = [(a + b) / 2 for a, b in zip(lo, hi)]
half = max((b - a) / 2 for a, b in zip(lo, hi))
q = half / 32000.0

buf = bytearray()
views, accessors, prims_by_mat, materials = [], [], defaultdict(list), []


def add_view(data, target, stride=None):
    while len(buf) % 4:
        buf.append(0)
    off = len(buf)
    buf.extend(data)
    vw = dict(buffer=0, byteOffset=off, byteLength=len(data), target=target)
    if stride:
        vw['byteStride'] = stride
    views.append(vw)
    return len(views) - 1


for mkey, ps in groups.items():
    # chunk parts so each primitive stays under 65535 vertices
    chunks, cur, n = [], [], 0
    for p in ps:
        if n + len(p['v']) > 65000 and cur:
            chunks.append(cur); cur, n = [], 0
        cur.append(p); n += len(p['v'])
    if cur:
        chunks.append(cur)
    for ch in chunks:
        pos, idx, base = bytearray(), bytearray(), 0
        qmin, qmax = [32767] * 3, [-32768] * 3
        for p in ch:
            for v in p['v']:
                qv = [int(round((v[i] - ctr[i]) / q)) for i in range(3)]
                for i in range(3):
                    qmin[i] = min(qmin[i], qv[i]); qmax[i] = max(qmax[i], qv[i])
                pos += struct.pack('<hhhh', *qv, 0)
            for t in p['f']:
                idx += struct.pack('<HHH', *(base + k for k in t))
            base += len(p['v'])
        pv = add_view(bytes(pos), 34962, 8)
        accessors.append(dict(bufferView=pv, componentType=5122, count=base, type='VEC3', min=qmin, max=qmax))
        pa = len(accessors) - 1
        iv = add_view(bytes(idx), 34963)
        accessors.append(dict(bufferView=iv, componentType=5123, count=len(idx) // 2, type='SCALAR'))
        prims_by_mat[mkey].append((pa, len(accessors) - 1))


def rgb(h):
    h = h.lstrip('#')
    lin = lambda c: (c / 255) ** 2.2
    return [lin(int(h[i:i + 2], 16)) for i in (0, 2, 4)]


meshes = []
for mkey, prims in prims_by_mat.items():
    col, metal, rough, alpha, emis = MATS[mkey]
    m = dict(name=mkey, pbrMetallicRoughness=dict(baseColorFactor=rgb(col) + [alpha], metallicFactor=metal,
                                                  roughnessFactor=rough), doubleSided=True)
    if alpha < 1:
        m['alphaMode'] = 'BLEND'
    if emis:
        m['emissiveFactor'] = rgb(emis)
    materials.append(m)
    mi = len(materials) - 1
    meshes.append(dict(name=mkey, primitives=[dict(attributes=dict(POSITION=pa), indices=ia, material=mi)
                                               for pa, ia in prims]))

s = q / 1000.0  # mm -> m
nodes = [dict(name='DuneWeaver', rotation=[-math.sqrt(0.5), 0, 0, math.sqrt(0.5)], children=[1])]
nodes.append(dict(name='parts', translation=[c / 1000.0 for c in ctr], scale=[s, s, s],
                  children=list(range(2, 2 + len(meshes)))))
for i, m in enumerate(meshes):
    nodes.append(dict(name=m['name'], mesh=i))

gltf = dict(asset=dict(version='2.0', generator='cimos dune weaver packer'),
            extensionsUsed=['KHR_mesh_quantization'], extensionsRequired=['KHR_mesh_quantization'],
            scene=0, scenes=[dict(nodes=[0])], nodes=nodes, meshes=meshes, materials=materials,
            accessors=accessors, bufferViews=views, buffers=[dict(byteLength=len(buf))])
while len(buf) % 4:
    buf.append(0)
gltf['buffers'][0]['byteLength'] = len(buf)
js = json.dumps(gltf, separators=(',', ':')).encode()
js += b' ' * ((4 - len(js) % 4) % 4)
out = struct.pack('<III', 0x46546C67, 2, 12 + 8 + len(js) + 8 + len(buf))
out += struct.pack('<II', len(js), 0x4E4F534A) + js + struct.pack('<II', len(buf), 0x004E4942) + bytes(buf)
open(dst, 'wb').write(out)
tris = sum(a['count'] for a in accessors if a['type'] == 'SCALAR') // 3
print(f'{dst}: {len(out)/1e6:.2f} MB, {tris} triangles, {len(meshes)} materials, quant {q:.4f} mm')
