"""Deterministic bounded trajectories on Platonic solid vertices; research only."""
from math import cos, sin, sqrt, isfinite
from .geometry import fixtures, graph

SCHEMA="platonic-trajectory-report/0.1"
def rotate_z(v,angle):
    c,s=cos(angle),sin(angle)
    return (c*v[0]-s*v[1],s*v[0]+c*v[1],v[2])

def distance(a,b):
    return sqrt(sum((x-y)**2 for x,y in zip(a,b)))

def classify(value,tolerance=1e-9):
    if value is None or not isfinite(value):
        return "UNKNOWN"
    return "PASS" if abs(value)<=tolerance else "FAIL"

def run(name, angle=0.2, radial_drift=0.0):
    if name not in fixtures():
        raise ValueError("unknown Platonic fixture")
    if not all(isfinite(float(x)) for x in (angle,radial_drift)):
        raise ValueError("nonfinite parameter")
    if not -1.0<=radial_drift<=1.0:
        raise ValueError("radial drift outside [-1,1]")
    base=fixtures()[name]
    edges=graph(base)
    moved=tuple(tuple((1+radial_drift)*v for v in rotate_z(p,angle)) for p in base)
    edge_errors=[distance(moved[i],moved[j])-distance(base[i],base[j]) for i,j in edges]
    centroid=tuple(sum(p[k] for p in moved)/len(moved) for k in range(3))
    max_error=max(map(abs,edge_errors))
    return {"schema_version":SCHEMA,"fixture":name,
        "parameters":{"rotation_radians":angle,"radial_drift":radial_drift},
        "sample_count":len(moved),"edge_count":len(edges),
        "metric_edge_max_error":max_error,
        "metric_edge_preservation":classify(max_error),
        "centroid_norm":sqrt(sum(x*x for x in centroid)),
        "centroid_preservation":classify(sqrt(sum(x*x for x in centroid))),
        "topology_preservation":"UNKNOWN",
        "physical_invariance":"UNKNOWN",
        "native_gate":"CLOSED","sphere_writes":False,
        "receipt_trust":"UNVERIFIED","synthetic":True,
        "points":[list(v) for v in moved]}

def all_reports(angle=0.2,radial_drift=0.0):
    return [run(n,angle,radial_drift) for n in fixtures()]
