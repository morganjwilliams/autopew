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

    def test_affine_pure_translate(self):
        """Check function for translations."""

        p0 = np.array([[0.0, 0.0], [1.0, 1.0], [0.0, 1.0]])
        translate = lambda x: x + np.array([1, 1])
        p1 = translate(p0)
        A = affine_from_AB(p0, p1)  # matrix
        tfm = affine_transform(A)
        for src in [np.array([[-1, 1]]), np.array([[-100, 1]]), np.array([[100, 1]])]:
            with self.subTest(src=src):
                out = tfm(src)
                expect = translate(src)
                self.assertTrue(np.isclose(out, expect).all())

    def test_affine_right_angle_rotate(self):
        """Check function for translations."""

        p0 = np.array([[0.0, 0.0], [1.0, 1.0], [0.0, 1.0]])
        rotate = lambda x: x[:, ::-1] * np.array([1, -1])  # 90 degree right rotation
        p1 = rotate(p0)
        A = affine_from_AB(p0, p1)  # matrix
        tfm = affine_transform(A)
        for src in [np.array([[-1, 1]]), np.array([[-100, 1]]), np.array([[100, 1]])]:
            with self.subTest(src=src):
                out = tfm(src)
                expect = rotate(src)
                self.assertTrue(np.isclose(out, expect).all())

    def test_affine_homogeneous_scale(self):
        """Check function for in homegeneous scale."""

        p0 = np.array([[0.0, 0.0], [1.0, 1.0], [0.0, 1.0]])
        scale = lambda x: x * np.array([2.0, 1.5])  # 150% y stretch
        p1 = scale(p0)
        A = affine_from_AB(p0, p1)  # matrix
        tfm = affine_transform(A)
        for src in [np.array([[-1, 1]]), np.array([[-100, 1]]), np.array([[100, 1]])]:
            with self.subTest(src=src):
                out = tfm(src)
                expect = scale(src)
                self.assertTrue(np.isclose(out, expect).all())

    def test_affine_negative_homogeneous_scale(self):
        """Check function for in homegeneous scale."""

        p0 = np.array([[0.0, 0.0], [1.0, 1.0], [0.0, 1.0]])
        scale = lambda x: x * np.array([-2.0, -1.5])  # 150% y stretch
        p1 = scale(p0)
        A = affine_from_AB(p0, p1)  # matrix
        tfm = affine_transform(A)
        for src in [np.array([[-1, 1]]), np.array([[-100, 1]]), np.array([[100, 1]])]:
            with self.subTest(src=src):
                out = tfm(src)
                expect = scale(src)
                self.assertTrue(np.isclose(out, expect).all())

    def test_affine_inhomogeneous_scaley(self):
        """Check function for inhomegeneous scale."""

        p0 = np.array([[0.0, 0.0], [1.0, 1.0], [0.0, 1.0]])
        scale = lambda x: x * np.array([1, 1.5])  # 150% y stretch
        p1 = scale(p0)
        A = affine_from_AB(p0, p1)  # matrix
        tfm = affine_transform(A)
        for src in [np.array([[-1, 1]]), np.array([[-100, 1]]), np.array([[100, 1]])]:
            with self.subTest(src=src):
                out = tfm(src)
                expect = scale(src)
                self.assertTrue(np.isclose(out, expect).all())

    def test_affine_composite_transform(self):
        scale = lambda x: x * np.array([1, 1.5])  # 150% y stretch
        rotate = lambda x: x[:, ::-1] * np.array([1, -1])  # 90 degree right rotation
        translate = lambda x: x + np.array([1, 1])
        p0 = np.array([[0.0, 0.0], [1.0, 1.0], [0.0, 1.0]])
        p1 = rotate(scale(translate(p0)))
        A = affine_from_AB(p0, p1)  # matrix
        tfm = affine_transform(A)
        for src in [np.array([[-1, 1]]), np.array([[-100, 1]]), np.array([[100, 1]])]:
            with self.subTest(src=src):
                out = tfm(src)
                expect = rotate(scale(translate(src)))
                self.assertTrue(np.isclose(out, expect).all())

    def test_affine_reversibility(self):
        """Check that the functions are reverisble."""
        A = affine_from_AB(self.p0, self.p1)  # matrix
        _A = affine_from_AB(self.p1, self.p0)  # matrix
        fore = affine_transform(A)  # function
        hind = affine_transform(_A)  # function

        _p1 = fore(self.p0)
        _p0 = hind(self.p1)
        self.assertTrue(np.isclose(_p1, self.p1).all())
        self.assertTrue(np.isclose(_p0, self.p0).all())


if __name__ == "__main__":
    unittest.main()
