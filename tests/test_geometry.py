import unittest
from platonic_lab.geometry import fixtures, graph, report, dual_cube_octahedron

class GeometryTests(unittest.TestCase):
    def test_all_five(self):
        expected={'tetrahedron':(4,6,4),'cube':(8,12,6),'octahedron':(6,12,8),
                  'dodecahedron':(20,30,12),'icosahedron':(12,30,20)}
        for name,vertices in fixtures().items():
            with self.subTest(name=name):
                r=report(name,vertices)
                self.assertEqual((r['vertices'],r['edges'],r['faces']),expected[name])
                self.assertEqual(r['euler'],2)
                self.assertEqual(r['classification'],'PASS')
                self.assertEqual(r['native_gate'],'CLOSED')
    def test_duality(self):
        self.assertTrue(dual_cube_octahedron())
    def test_deterministic(self):
        self.assertEqual(fixtures(),fixtures())

if __name__=='__main__': unittest.main()
