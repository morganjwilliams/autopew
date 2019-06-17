import pandas as pd
import numpy as np
import networkx
import matplotlib.pyplot as plt

class Net(object):
    """
    Network of transformations between objects.

        This object stores the individual node objects including their properties and
        registration points, in addition to the edges which involve specific
        coordinate transforms.
    """

    def __init__(self):
        self.graph = networkx.DiGraph()  # directed graph
        self.components = {}

    def update(self, name, object):
        """
        """
        self.components = {**self.components, name: object}

    def add_edge(self, A, B, transform=None, **kwargs):
        """
        Add an edge between components A and B.
        Optionally specify the specific transform.

        Parameters
        ----------
        A, B : :class:`str`
            Names of components to link.
        transform : :class:`function`
            Function to transform coordinates from A space to B space.
        inverse_transform : :class:`function`
            Function to transform coordinates from B space to A space.
        """
        # check the components have been registered
        assert (A in self.components.keys()) and (B in self.components.keys())

        attrs = kwargs
        edge = [[A, B, {**attrs, "transform": transform}]]
        self.graph.add_edges_from(edge, **kwargs)

    def link(self, A, B, transform=None, inverse_transform=None, **kwargs):
        """
        Link nodes A and B with transforms along edges.
        """
        attrs = kwargs
        edges = [[A, B, attrs]]

        if transform is not None:
            self.add_edge(A, B, transform=transform, **attrs)
        if inverse_transform is not None:
            self.add_edge(B, A, transform=inverse_transform, **attrs)

    def shortest_path(self, A, B, astransform=False):
        return networkx.algorithms.single_source_shortest_path(self.graph, A)[B]

    def draw(self, ec="k", ax=None):
        if ax is None:
            fig, ax = plt.subplots(1, figsize=(10, 10))
        df = pd.DataFrame(self.graph.edges, columns=["A", "B"])
        df["attrs"] = [self.graph.edges[a, b] for [a, b] in self.graph.edges]
        df = df.set_index(df.A + "-" + df.B)
        df = df.loc[["-".join(e) for e in list(self.graph.edges)], :]

        ec = [self.graph.edges[a, b].get("color", ec) for [a, b] in self.graph.edges]
        networkx.draw(
            self.graph,
            edge_color=ec,
            with_labels=True,
            ax=ax,
            node_shape="h",
            node_color="seagreen",
            node_size=2500,
            font_color="white",
            font_size=9,
            arrowsize=15,
            arrowstyle="->",
            connectionstyle="arc3,rad=0.1",
        )
        ax.axis(np.array(ax.axis()) * 1.1)  # 110% range, as the axis is about 0, 0
        return ax
