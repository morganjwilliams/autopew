import unittest
import numpy as np
import matplotlib.pyplot as plt
from autopew.transform.affine import affine_from_AB, affine_transform


class TestAffine(unittest.TestCase):
    def setUp(self):
        # Two sets of points in 3D
        self.p0 = np.array(((1.0, 1.0, 1.0), (1.0, 2.0, 1.0), (1.0, 1.0, 2.0)))
        self.p1 = np.array(
            (
                (2.4142135623730940, 5.732050807568877, 0.7320508075688767),
                (2.7677669529663684, 6.665063509461097, 0.6650635094610956),
                (2.7677669529663675, 5.665063509461096, 1.6650635094610962),
            )
        )

    def test_affine_from_AB(self):
        """Check that the affine matrix is generated correctly."""
        A = affine_from_AB(self.p0, self.p1)
        self.assertTrue(A.shape == (4, 4))  # affine matrix is larger by 1r/1c

    def test_affine_functions(self):
        """Check that the functions work as expected, and are reverisble."""
        A = affine_from_AB(self.p0, self.p1)  # matrix
        _A = affine_from_AB(self.p1, self.p0)  # matrix
        fore = affine_transform(A)  # function
        hind = affine_transform(_A)  # function

        _p1 = fore(self.p0)
        _p0 = hind(self.p1)
        print(_p0, self.p0)
        print(_p1, self.p1)
        self.assertTrue(np.isclose(_p1, self.p1).all())
        self.assertTrue(np.isclose(_p0, self.p0).all())
