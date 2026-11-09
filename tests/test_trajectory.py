import unittest
from math import nan
from platonic_lab.trajectory import run, all_reports

class TrajectoryTests(unittest.TestCase):
    def test_rotation_preserves_edge_metric(self):
        for r in all_reports():
            with self.subTest(r=r["fixture"]):
                self.assertEqual(r["metric_edge_preservation"],"PASS")
                self.assertEqual(r["centroid_preservation"],"PASS")
                self.assertEqual(r["physical_invariance"],"UNKNOWN")
    def test_scaling_breaks_metric(self):
        for r in all_reports(radial_drift=0.1):
            self.assertEqual(r["metric_edge_preservation"],"FAIL")
            self.assertEqual(r["centroid_preservation"],"PASS")
    def test_determinism(self):
        self.assertEqual(run("cube"),run("cube"))
    def test_rejects_nonfinite(self):
        with self.assertRaises(ValueError): run("cube",angle=nan)
    def test_rejects_unbounded(self):
        with self.assertRaises(ValueError): run("cube",radial_drift=2)
    def test_rejects_unknown_fixture(self):
        with self.assertRaises(ValueError): run("sphere")
if __name__=="__main__": unittest.main()
