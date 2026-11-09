"""Canonical engine boundary versus gated pyramidal sandbox: explicit deny-by-default model."""
from .geometry import fixtures
CANONICAL_SEQUENCE=("sentinel","cube","sphere")
PLATONIC_FIXTURES=frozenset(fixtures())
SANDBOX_SHAPE="square_pyramid"
GATE_ROLE="state_access_boundary"
def validate_plan(sequence,fixture=None,gate=None,sandbox=None,write=False):
    """Validate proposed state topology; never execute it."""
    if not isinstance(sequence,(tuple,list)) or tuple(sequence)!=CANONICAL_SEQUENCE:
        return {"classification":"REJECTED","reason":"canonical_sequence_modified","native_gate":"CLOSED"}
    if fixture is not None and fixture not in PLATONIC_FIXTURES:
        return {"classification":"REJECTED","reason":"non_platonic_fixture","native_gate":"CLOSED"}
    if sandbox is not None and (sandbox!=SANDBOX_SHAPE or gate!="state_access_boundary"):
        return {"classification":"REJECTED","reason":"sandbox_requires_state_gate","native_gate":"CLOSED"}
    if gate is not None and gate!=GATE_ROLE:
        return {"classification":"REJECTED","reason":"invalid_gate_role","native_gate":"CLOSED"}
    if write:
        return {"classification":"REJECTED","reason":"native_writes_forbidden","native_gate":"CLOSED"}
    return {"classification":"ACCEPTED_RESEARCH_ONLY","reason":"structure_consistent",
            "native_gate":"CLOSED","native_authority":False,
            "sandbox_shape":sandbox,"gate_role":gate,
            "optical_equivalence":"UNKNOWN","universal_advance":"UNKNOWN"}
