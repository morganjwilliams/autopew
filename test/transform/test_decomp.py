import unittest
import numpy as np
import matplotlib.pyplot as plt
from autopew.transform.affine import (
    compose_affine2d,
    decompose_affine2d,
    zoom,
    translate,
    rotate,
    shear,
)


class TestAffineCompDecomp(unittest.TestCase):
    def setUp(self):
        x0, x1, y0, y1 = np.array([[0, 0], [1, 1]]).T.flatten()
        self.corners = np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]])

    def test_combined(self):
        _T, _Z, _R = translate(40, 50), zoom(1.5, 0.5), rotate(-15)
        A = _T @ _Z @ _R  # TZR
        T, Z, R = decompose_affine2d(A)
        for expect, out in zip([_T, _Z, _R], [T, Z, R]):
            with self.subTest(out=out, expect=expect):
                self.assertTrue(np.isclose(expect, out).all())

    def test_rotate(self):
        _T, _Z, _R = translate(), zoom(), rotate(-15)
        A = _T @ _Z @ _R  # TZR
        T, Z, R = decompose_affine2d(A)
        for expect, out in zip([_T, _Z, _R], [T, Z, R]):
            with self.subTest(out=out, expect=expect):
                self.assertTrue(np.isclose(expect, out).all())

    def test_translate(self):
        _T, _Z, _R = translate(40, 50), zoom(), rotate()
        A = _T @ _Z @ _R  # TZR
        T, Z, R = decompose_affine2d(A)
        for expect, out in zip([_T, _Z, _R], [T, Z, R]):
            with self.subTest(out=out, expect=expect):
                self.assertTrue(np.isclose(expect, out).all())

    def test_zoom(self):
        _T, _Z, _R = translate(), zoom(1.2, 0.7), rotate()
        A = _T @ _Z @ _R  # TZR
        T, Z, R = decompose_affine2d(A)
        for expect, out in zip([_T, _Z, _R], [T, Z, R]):
            with self.subTest(out=out, expect=expect):
                self.assertTrue(np.isclose(expect, out).all())

    def test_reconstruction(self):
        _T, _Z, _R = translate(40, 50), zoom(1.5, 0.5), rotate(-15)
        A = _T @ _Z @ _R  # TZR
        _A = compose_affine2d(*decompose_affine2d(A))
        self.assertTrue(np.isclose(A, _A).all())

    def tearDown(self):
        plt.close("all")


if __name__ == "__main__":
    unittest.main()
