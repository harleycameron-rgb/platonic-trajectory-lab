"""Geometry-referenced computational image gradients; no optical calibration."""
from math import sqrt, isfinite
from .geometry import fixtures, graph

SCHEMA="scandoc-gradient-optics-platonic/0.1"
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def unit(v):
    n=sqrt(dot(v,v))
    if n<1e-12: raise ValueError("zero projection")
    return tuple(x/n for x in v)
def project(v,view=(0,0,1)):
    """Orthogonal projection onto the image plane for z-view only (explicit frame)."""
    if tuple(view)!=(0,0,1): raise ValueError("unsupported view frame")
    return (v[0],v[1])
def directions(name):
    """Unique unoriented 2D axes from projected vertices, sorted deterministically."""
    if name not in fixtures(): raise ValueError("unknown fixture")
    axes=set()
    for v in fixtures()[name]:
        x,y=project(v)
        if x*x+y*y<1e-12: continue
        a=unit((x,y))
        if a[0]<-1e-12 or (abs(a[0])<=1e-12 and a[1]<0): a=(-a[0],-a[1])
        axes.add(tuple(round(t,10) for t in a))
    return tuple(sorted(axes))
def gradient(image,axis=(1,0),gain=1.0):
    """Central difference directional gradient with replicated-edge boundary."""
    if not image or not image[0] or any(len(r)!=len(image[0]) for r in image):
        raise ValueError("nonrectangular/empty image")
    if not isfinite(gain) or gain<=0: raise ValueError("gain must be finite positive")
    if any(not isfinite(float(v)) for row in image for v in row): raise ValueError("nonfinite pixel")
    ax=unit(axis);h=len(image);w=len(image[0])
    def sample(x,y):return float(image[min(h-1,max(0,y))][min(w-1,max(0,x))])
    return tuple(tuple(gain*(ax[0]*(sample(x+1,y)-sample(x-1,y))/2+
                              ax[1]*(sample(x,y+1)-sample(x,y-1))/2)
                       for x in range(w)) for y in range(h))
def compare_opposites(image,axis=(1,0)):
    a=gradient(image,axis)
    b=gradient(image,(-axis[0],-axis[1]))
    error=max(abs(a[y][x]+b[y][x]) for y in range(len(a)) for x in range(len(a[0])))
    return {"opposite_antisymmetry_error":error,
            "classification":"PASS" if error<=1e-9 else "FAIL"}
def report(name,image,axis_index=0):
    axes=directions(name)
    if not 0<=axis_index<len(axes): raise ValueError("axis index")
    axis=axes[axis_index]
    g=gradient(image,axis)
    return {"schema_version":SCHEMA,"fixture":name,"projection":"orthographic-z",
      "axis":axis,"axis_count":len(axes),"width":len(image[0]),"height":len(image),
      "opposite_pair":compare_opposites(image,axis),
      "gradient":g,"geometry_reference":"unit-radius-vertices",
      "optical_calibration":"UNKNOWN","physical_density":"UNKNOWN",
      "geometry_hash":None,"temporal_receipt":None,
      "native_gate":"CLOSED","sphere_writes":False,"evidence_status":"UNVERIFIED"}
