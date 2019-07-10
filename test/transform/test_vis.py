import unittest
import matplotlib.pyplot as plt
from autopew.transform.affine import affine_transform, shear, translate, zoom, rotate
from autopew.transform.vis import vis


class TestAffineVis(unittest.TestCase):
    """
    Test the affine visualisation.
    """

    def setUp(self):
        pass

    def test_default(self):

        fig, ax = plt.subplots(2, 4, sharey=True, sharex=True, figsize=(10, 4))
        ax = ax.flat
        for ix, A in enumerate(
            [
                translate(0.5, 1.0),
                zoom(1.0, 0.5),
                rotate(30),
                shear(0.5, 0),
                translate(0.5, 0),
                zoom(2, 1),
                rotate(-30),
                shear(0, 0.5),
            ]
        ):
            vis(A, ax=ax[ix])

        plt.tight_layout()

    def tearDown(self):
        plt.close("all")


if __name__ == "__main__":
    unittest.main()
