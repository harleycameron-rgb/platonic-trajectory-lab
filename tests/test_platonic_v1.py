"""Platonic Duality and Resolution V1 regression tests. Synthetic geometry only."""
import math
import unittest
from itertools import combinations
from platonic_lab.geometry import fixtures, graph

def face_sets(vertices):
    edges = set(tuple(sorted(e)) for e in graph(vertices))
    adjacency = {i: set() for i in range(len(vertices))}
    for a,b in edges:
        adjacency[a].add(b); adjacency[b].add(a)
    result = set()
    for k in (3,4,5):
        for ids in combinations(range(len(vertices)),k):
            selected=set(ids)
            if not all(len(adjacency[i]&selected)==2 for i in ids):
                continue
            if sum(a in selected and b in selected for a,b in edges)!=k:
                continue
            a,b,c=(vertices[i] for i in ids[:3])
            u=[b[t]-a[t] for t in range(3)]
            w=[c[t]-a[t] for t in range(3)]
            n=(u[1]*w[2]-u[2]*w[1],u[2]*w[0]-u[0]*w[2],u[0]*w[1]-u[1]*w[0])
            if sum(z*z for z in n)<1e-12:
                continue
            signed=[sum(n[t]*(vertices[j][t]-a[t]) for t in range(3)) for j in range(len(vertices))]
            if any(abs(signed[j])>1e-7 for j in ids):
                continue
            other=[signed[j] for j in range(len(vertices)) if j not in selected]
            if all(s>=-1e-7 for s in other) or all(s<=1e-7 for s in other):
                result.add(frozenset(ids))
    return tuple(sorted(result,key=lambda s:tuple(sorted(s))))

def dual_signature(name_a,name_b):
    vs=fixtures()
    va,vb=vs[name_a],vs[name_b]
    fa,fb=face_sets(va),face_sets(vb)
    ea,eb=graph(va),graph(vb)
    deg_a=sorted(sum(i in e for e in ea) for i in range(len(va)))
    deg_b=sorted(sum(i in e for e in eb) for i in range(len(vb)))
    return (len(fa)==len(vb) and len(va)==len(fb)
            and len(ea)==len(eb)
            and sorted(map(len,fa))==deg_b
            and sorted(map(len,fb))==deg_a)

def sphere_areas(levels=4):
    vs=fixtures()['icosahedron']
    def norm(v):
        mag=math.sqrt(sum(t*t for t in v))
        return tuple(t/mag for t in v)
    def area(a,b,c):
        u=[b[i]-a[i] for i in range(3)]
        v=[c[i]-a[i] for i in range(3)]
        cross=[u[(i+1)%3]*v[(i+2)%3]-u[(i+2)%3]*v[(i+1)%3] for i in range(3)]
        return math.sqrt(sum(t*t for t in cross))/2
    triangles=[tuple(vs[i] for i in sorted(f)) for f in face_sets(vs)]
    areas=[]
    for _ in range(levels+1):
        areas.append(sum(area(*t) for t in triangles))
        refined=[]
        for a,b,c in triangles:
            ab=norm(tuple((a[i]+b[i])/2 for i in range(3)))
            bc=norm(tuple((b[i]+c[i])/2 for i in range(3)))
            ca=norm(tuple((c[i]+a[i])/2 for i in range(3)))
            refined.extend(((a,ab,ca),(ab,b,bc),(ca,bc,c),(ab,bc,ca)))
        triangles=refined
    return areas

class PlatonicV1Tests(unittest.TestCase):
    def test_dual_incidence_signatures(self):
        for a,b in (('tetrahedron','tetrahedron'),('cube','octahedron'),('dodecahedron','icosahedron')):
            with self.subTest(a=a,b=b):
                self.assertTrue(dual_signature(a,b))
    def test_icosahedral_sphere_area_convergence(self):
        errors=[abs(4*math.pi-a) for a in sphere_areas(4)]
        self.assertTrue(all(errors[i+1]<errors[i] for i in range(4)))
        self.assertLess(errors[-1],0.03)
    def test_five_fixtures_only(self):
        self.assertEqual(set(fixtures()),{'tetrahedron','cube','octahedron','dodecahedron','icosahedron'})
