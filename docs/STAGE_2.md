# Stage 2: trajectory tests and read-only consumer contract

The test trajectory is a rotation about the z-axis plus optional uniform radial scaling, not a physical motion or SCANDOC firing. Each of five solids uses unit-radius vertices. Metric preservation compares nearest-neighbour edge lengths against baseline. Centroid is checked independently. Graph topology is not proven by the metric test, so topology and physical invariance remain UNKNOWN.

## Run
```
python -m unittest discover -s tests -v
python -c "from platonic_lab.adapter import export_json; print(export_json())"
```

## Integration
`platonic_lab.adapter.envelope` returns a read-only, synthetic envelope for future Chaos Lab/Orrery ingestion. No live cross-repository connection or deployment has been made. The envelope does not grant native authority, does not create a receipt, and does not assert that a geometry hash has been computed.

## Acceptance
- All five solids preserve edge metrics under pure rigid rotation.
- All five break edge metrics under nonzero uniform scaling.
- Centre remains at origin under both operations.
- Nonfinite and out-of-range inputs rejected.
- UNKNOWN remains distinct from PASS.
- Native gate CLOSED, sphere writes disabled.

Next: independently validate with CI and consumer-side rendering, then add graph-automorphism and adjacency-preservation tests. Do not infer a Planck-gap invariant from these experiments.
