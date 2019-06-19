import unittest
import numpy as np
import matplotlib.pyplot as plt

from autopew.transform.affine import (
    affine_from_AB,
    affine_transform,
    shear,
    zoom,
    translate,
    rotation,
    _pad,
    _unpad,
)


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

    def test_affine_xyflip(self):
        """Check function for translations."""

        p0 = np.array([[0.0, 0.0], [1.0, 1.0], [0.0, 1.0]])
        rotate = lambda x: x[:, ::-1]
        p1 = rotate(p0)
        A = affine_from_AB(p0, p1)  # matrix
        tfm = affine_transform(A)
        for src in [np.array([[-1, 1]]), np.array([[-100, 1]]), np.array([[100, 1]])]:
            with self.subTest(src=src):
                out = tfm(src)
                expect = rotate(src)
                self.assertTrue(np.isclose(out, expect).all())

    def test_affine_shear(self):
        """Check function for translations."""

        p0 = np.array([[0.0, 0.0], [1.0, 1.0], [0.0, 1.0]])
        shear = lambda x: x + x[:, ::-1] * np.array(
            [1.5, 0]
        )  # 90 degree right rotation
        p1 = shear(p0)
        A = affine_from_AB(p0, p1)  # matrix
        tfm = affine_transform(A)
        for src in [np.array([[-1, 1]]), np.array([[-100, 1]]), np.array([[100, 1]])]:
            with self.subTest(src=src):
                out = tfm(src)
                expect = shear(src)
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

    def test_affine_rhomboid_bounds_graphical(self):
        """
        Graphical test that points bounded by a polygon before transformation
        remain bounded by the transformed polygon.
        """
        start, end = 0, 4
        p0 = np.array([[start, end, end, start], [end, end, start, start]]).T
        pmid0 = np.array(
            [[start, end / 2, end, end / 2], [end / 2, end, end / 2, start]]
        ).T
        rp = np.random.rand(100, 2) * end

        A = zoom(1.0, 1.5) @ rotation(-50) @ shear(0.6, -0.05) @ translate([2, 2])

        tfm = lambda x: _unpad(_pad(x) @ A)

        p1 = tfm(p0)
        pmid1 = tfm(pmid0)
        T = affine_transform(affine_from_AB(pmid0, pmid1))

        fig, ax = plt.subplots(1, 2, sharex=True, sharey=True)
        ax[0].plot(*np.vstack([p0, p0[0]]).T, color="k")
        ax[0].scatter(*pmid0.T, color="r")
        ax[0].scatter(*rp.T, color="0.5")
        ax[1].plot(*np.vstack([p1, p1[0]]).T, color="k", label="Bounds")
        ax[1].scatter(*pmid1.T, color="r", label="Reference Points")
        ax[1].scatter(*T(rp).T, color="0.5", zorder=-1, label="Sample Points")
        ax[1].legend(bbox_to_anchor=(1.0, 1.0), frameon=False, facecolor=None)



if __name__ == "__main__":
    unittest.main()
