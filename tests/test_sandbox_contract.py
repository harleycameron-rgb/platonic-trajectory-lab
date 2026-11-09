import unittest
from platonic_lab.sandbox_contract import validate_plan,CANONICAL_SEQUENCE
class SandboxBoundaryTests(unittest.TestCase):
    def test_canonical_sequence(self):
        self.assertEqual(validate_plan(CANONICAL_SEQUENCE)["classification"],"ACCEPTED_RESEARCH_ONLY")
    def test_pyramid_never_canonical(self):
        for sequence in (("sentinel","cube","pyramid","sphere"),("sentinel","pyramid","cube","sphere"),("sentinel","cube","pyramid"),("sentinel","cube","sphere","pyramid")):
            with self.subTest(sequence=sequence):
                self.assertEqual(validate_plan(sequence)["reason"],"canonical_sequence_modified")
    def test_pyramid_not_platonic_fixture(self):
        self.assertEqual(validate_plan(CANONICAL_SEQUENCE,fixture="pyramid")["reason"],"non_platonic_fixture")
    def test_five_valid_fixtures(self):
        for name in ("tetrahedron","cube","octahedron","dodecahedron","icosahedron"):
            self.assertEqual(validate_plan(CANONICAL_SEQUENCE,fixture=name)["classification"],"ACCEPTED_RESEARCH_ONLY")
    def test_sandbox_gate_only(self):
        ok=validate_plan(CANONICAL_SEQUENCE,gate="state_access_boundary",sandbox="square_pyramid")
        self.assertEqual(ok["classification"],"ACCEPTED_RESEARCH_ONLY")
        self.assertFalse(ok["native_authority"])
        self.assertEqual(validate_plan(CANONICAL_SEQUENCE,sandbox="square_pyramid")["reason"],"sandbox_requires_state_gate")
        self.assertEqual(validate_plan(CANONICAL_SEQUENCE,gate="geometry_transform",sandbox="square_pyramid")["classification"],"REJECTED")
    def test_no_native_writes(self):
        self.assertEqual(validate_plan(CANONICAL_SEQUENCE,write=True)["reason"],"native_writes_forbidden")
    def test_universal_advance_unknown(self):
        self.assertEqual(validate_plan(CANONICAL_SEQUENCE)["universal_advance"],"UNKNOWN")
if __name__=="__main__":unittest.main()
