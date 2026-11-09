# MDL — Gradient Optics Platonic V1

STATUS: EXPERIMENTAL / READ-ONLY / NATIVE GATE CLOSED

## Hypothesis
Projected regular-polyhedron vertex directions supply reproducible directional references for a computational image gradient. This is not a physical Schlieren instrument or calibrated substitute for its knife-edge optical transfer function.

## Implemented
- Five deterministic geometry fixtures, projected into a declared z-view image plane.
- Antipodal directions canonicalised as unoriented axes.
- Finite-difference directional gradient on a finite 2D scalar image.
- Opposite-axis antisymmetry, linear ramp and rotation covariance tests.
- Explicit rejection of empty, nonrectangular, nonfinite or zero-axis input.
- UNKNOWN optical calibration and density status; no native authority.

## Limits
A projection can collapse vertex directions (notably octahedron poles along the viewing axis). Direction counts are not identical to 3D face counts. No measured refractive-index calibration, knife-edge transfer modelling, camera optical flow, video adapter, physical velocity field, Planck boundary verification or 1536-bit commitment is implemented.

## Acceptance
Run `python -m unittest discover -s tests -v`. CI results must be checked independently. Tests measure computational consistency, not physical equivalence.

## Next
Consumer-side test vectors for browser gradient operator; then explicit read-only Chaos Lab/Orrery record ingestion. No cross-repository execution authority.
