"""Read-only export envelope for Chaos Lab / Orrery research consumers."""
import json
from .trajectory import run

def envelope(name="cube",angle=0.2,radial_drift=0.0):
    r=run(name,angle,radial_drift)
    return {"schema_version":"scandoc-research-adapter/0.1",
      "producer":"platonic-trajectory-lab",
      "consumer_hint":["chaos-lab","orrery"],
      "source_modality":"synthetic",
      "geometry_frame":"unit-radius-origin-centred",
      "geometry_hash":None,
      "temporal_receipt":None,
      "evidence_status":"UNVERIFIED",
      "native_authority":False,
      "input":r["parameters"],
      "result":r}
def export_json(name="cube",angle=0.2,radial_drift=0.0):
    return json.dumps(envelope(name,angle,radial_drift),sort_keys=True,indent=2)
