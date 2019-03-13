import unittest
import matplotlib.pyplot as plt
from autopew.transform.calibration import *


class TestCalibration(unittest.TestCase):
    def test_calibration(self):
        p0, p1 = (
            np.array(((1.0, 1.0, 1.0), (1.0, 2.0, 1.0), (1.0, 1.0, 2.0))),
            np.array(
                (
                    (2.4142135623730940, 5.732050807568877, 0.7320508075688767),
                    (2.7677669529663684, 6.665063509461097, 0.6650635094610956),
                    (2.7677669529663675, 5.665063509461096, 1.6650635094610962),
                )
            ),
        )
        A = affine_from_AB(p0, p1)
        out = transform_from_affine(A)(p0)
        self.assertTrue(np.isclose(out, p1).all())
