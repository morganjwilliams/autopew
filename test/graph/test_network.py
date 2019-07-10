import unittest
import matplotlib.pyplot as plt
from autopew.graph.network import Net


class TestNetwork(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_net(self):
        n = Net()
        n.update("A", "A")
        n.update("C", "C")
        n.update("B", "B")
        n.link(
            "A",
            "B",
            transform=lambda x: x + 1,
            inverse_transform=lambda x: x - 1,
            color="red",
        )
        n.link(
            "B", "C", transform=lambda x: x ** 2, inverse_transform=lambda x: x ** 0.5
        )
        tfm = n.get_transform("A", "C")
        self.assertTrue(tfm(1) == 4) # coordinate transform from A to C
        ivtfm = n.get_transform("C", "A")
        self.assertTrue(ivtfm(1) == 0) # coordinate transform from A to C
        ax = n.draw()


if __name__ == "__main__":
    unittest.main()
