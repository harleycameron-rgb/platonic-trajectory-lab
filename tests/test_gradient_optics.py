import unittest
from math import nan
from platonic_lab.gradient_optics import directions,gradient,compare_opposites,report

class GradientOpticsTests(unittest.TestCase):
    def test_all_five_have_axes(self):
        for name in ("tetrahedron","cube","octahedron","dodecahedron","icosahedron"):
            with self.subTest(name=name):
                axes=directions(name)
                self.assertTrue(axes)
                self.assertEqual(len(axes),len(set(axes)))
                self.assertTrue(all(abs(x*x+y*y-1)<1e-8 for x,y in axes))
    def test_linear_ramp_horizontal(self):
        image=[[float(x) for x in range(7)] for y in range(5)]
        g=gradient(image,(1,0))
        self.assertAlmostEqual(g[2][3],1)
        self.assertAlmostEqual(gradient(image,(0,1))[2][3],0)
    def test_opposite_antisymmetry(self):
        image=[[x*y for x in range(7)] for y in range(5)]
        self.assertEqual(compare_opposites(image)["classification"],"PASS")
    def test_rotation_covariance_for_ramp(self):
        horizontal=[[float(x) for x in range(7)] for _ in range(7)]
        vertical=[[float(y) for _ in range(7)] for y in range(7)]
        self.assertAlmostEqual(gradient(horizontal,(1,0))[3][3],gradient(vertical,(0,1))[3][3])
    def test_cube_octahedron_axis_overlap(self):
        self.assertIn((1.0,0.0),directions("octahedron"))
        self.assertIn((0.0,1.0),directions("octahedron"))
    def test_unknown_remains_unknown(self):
        r=report("cube",[[0,1,2],[0,1,2],[0,1,2]])
        self.assertEqual(r["physical_density"],"UNKNOWN")
        self.assertEqual(r["optical_calibration"],"UNKNOWN")
        self.assertEqual(r["native_gate"],"CLOSED")
        self.assertFalse(r["sphere_writes"])
    def test_invalid_inputs(self):
        for image in ([],[[]],[[1],[1,2]],[[nan]]):
            with self.assertRaises(ValueError):gradient(image)
        with self.assertRaises(ValueError):gradient([[1]],(0,0))
        with self.assertRaises(ValueError):gradient([[1]],gain=nan)
        with self.assertRaises(ValueError):directions("sphere")
if __name__=="__main__":unittest.main()
