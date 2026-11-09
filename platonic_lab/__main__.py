import json
from .geometry import fixtures,report,dual_cube_octahedron
print(json.dumps({'suite':'platonic-trajectory-lab/0.1',
 'results':[report(k,v) for k,v in fixtures().items()],
 'cube_octahedron_duality':dual_cube_octahedron(),
 'trajectory_invariance':'UNKNOWN'},indent=2))
