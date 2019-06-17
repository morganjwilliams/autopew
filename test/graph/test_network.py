import unittest
import matplotlib.pyplot as plt
from autopew.graph.network import Net


class TestNetwork(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_net(self):
        n = Net()
        n.update("A", ["A"])
        n.update("C", ["C"])
        n.update("B", ["B"])
        n.link(
            "A", "B", transform=lambda x: x, inverse_transform=lambda x: x, color="red"
        )
        # n.link("A", "C", transform=lambda x: x, inverse_transform=lambda x: x)
        n.link("B", "C", transform=lambda x: x, inverse_transform=lambda x: x)
        n.graph.edges  # ["A", "B"]

        n.shortest_path("A", "C")
        # n.draw()


if __name__ == "__main__":
    unittest.main()
