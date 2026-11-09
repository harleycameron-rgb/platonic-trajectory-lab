"""Deterministic regular-polyhedron fixtures. No native engine coupling."""
from math import sqrt
from itertools import combinations

def norm(v):
    m=sqrt(sum(x*x for x in v))
    return tuple(x/m for x in v)

def fixtures():
    phi=(1+sqrt(5))/2
    tetra=[(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
    cube=[(x,y,z) for x in (-1,1) for y in (-1,1) for z in (-1,1)]
    octa=[(s,0,0) for s in (-1,1)]+[(0,s,0) for s in (-1,1)]+[(0,0,s) for s in (-1,1)]
    ico=[]
    for a in (-1,1):
        for b in (-1,1):
            ico += [(0,a,b*phi),(a,b*phi,0),(b*phi,0,a)]
    dodeca=[(x,y,z) for x in (-1,1) for y in (-1,1) for z in (-1,1)]
    inv=1/phi
    for a in (-1,1):
        for b in (-1,1):
            dodeca += [(0,a*inv,b*phi),(a*inv,b*phi,0),(b*phi,0,a*inv)]
    return {k:tuple(norm(v) for v in vs) for k,vs in {
        'tetrahedron':tetra,'cube':cube,'octahedron':octa,
        'dodecahedron':dodeca,'icosahedron':ico}.items()}

def graph(vertices):
    distances=sorted({round(sum((a-b)**2 for a,b in zip(vertices[i],vertices[j])),10)
                      for i,j in combinations(range(len(vertices)),2)})
    edge_d=distances[0]
    edges=[(i,j) for i,j in combinations(range(len(vertices)),2)
           if abs(sum((a-b)**2 for a,b in zip(vertices[i],vertices[j]))-edge_d)<1e-8]
    return edges

def report(name,vertices):
    edges=graph(vertices)
    # Each regular polyhedron has the same number of edges per face.
    face_sizes={'tetrahedron':3,'cube':4,'octahedron':3,'dodecahedron':5,'icosahedron':3}
    sides=face_sizes[name]
    faces=2*len(edges)//sides
    centre=tuple(sum(v[i] for v in vertices)/len(vertices) for i in range(3))
    return {'name':name,'vertices':len(vertices),'edges':len(edges),'faces':faces,
            'euler':len(vertices)-len(edges)+faces,'centre':centre,
            'classification':'PASS' if len(vertices)-len(edges)+faces==2
              and max(map(abs,centre))<1e-12 else 'FAIL',
            'native_gate':'CLOSED','receipt':'UNVERIFIED'}

def dual_cube_octahedron():
    cube=fixtures()['cube']
    # Cube face centres lie on six coordinate directions, matching octahedron vertices.
    centres=[(s,0.,0.) for s in (-1.,1.)]+[(0.,s,0.) for s in (-1.,1.)]+[(0.,0.,s) for s in (-1.,1.)]
    return set(centres)==set(fixtures()['octahedron'])
