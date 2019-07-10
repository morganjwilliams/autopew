import pandas as pd
import numpy as np
import networkx
import matplotlib.pyplot as plt
from ..util.meta import chain
import logging


logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


def autolink(x):
    """Default link function."""
    return x


class Net(object):
    """
    Network of transformations between objects.

        This object stores the individual node objects including their properties and
        registration points, in addition to the edges which involve specific
        coordinate transforms.

    Todo
    -----

        * Type-based markers for each node.
    """

    def __init__(self):
        self.graph = networkx.DiGraph()  # directed graph
        self.components = {}

    @property
    def nodes(self):
        return self.graph.nodes

    @property
    def edges(self):
        return self.graph.edges

    def update(self, name, obj, **kwargs):
        """
        """
        self.components = {**self.components, name: obj}
        self.graph.add_node(name, **kwargs)
        try:  # store a reference on the object, if possible
            obj.autonet = self
        except AttributeError:  # can't add attribute to immutible obejcts..
            pass

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

        Todo
        -----

            * Add check for whether edge exists - and whether this will overwrite etc
        """
        # check the components have been registered
        assert (A in self.components.keys()) and (B in self.components.keys())

        # check whether edge exists?
        attrs = kwargs
        edge = [[A, B, {**attrs, "transform": transform}]]
        logger.debug("Adding Edge: {}".format(edge))
        self.graph.add_edges_from(edge)

    def link(self, A, B, transform=autolink, inverse_transform=autolink, **kwargs):
        """
        Link nodes A and B with transforms along edges.
        """
        attrs = kwargs
        edges = [[A, B, attrs]]

        if transform is not None:
            self.add_edge(A, B, transform=transform, **attrs)
        if inverse_transform is not None:
            self.add_edge(B, A, transform=inverse_transform, **attrs)

    def get_transform(self, A, B):
        """
        Get the function to transform coordinates between nodes A and B.
        """
        E = networkx.algorithms.single_source_shortest_path(self.graph, A)[B]
        fs = [
            self.graph.edges[E[ix], E[ix + 1]].get("transform")
            for ix in range(len(E) - 1)
        ]
        return chain(fs)

    def draw(
        self,
        ec="k",
        nc="seagreen",
        ax=None,
        figsize=(10, 10),
        method=networkx.draw_shell,
    ):
        if ax is None:
            fig, ax = plt.subplots(1, figsize=figsize)
        else:
            figsize = ax.figure.get_size_inches()
        df = pd.DataFrame(self.graph.edges, columns=["A", "B"])
        df["attrs"] = [self.graph.edges[a, b] for [a, b] in self.graph.edges]
        df = df.set_index(df.A + "-" + df.B)
        df = df.loc[["-".join(e) for e in list(self.graph.edges)], :]

        ns = [
            1000.0 * len(n) / 2 for n in self.graph.nodes
        ]  # size of nodes tied to name
        nc = [self.graph.nodes[n].get("color", nc) for n in self.graph.nodes]
        ec = [self.graph.edges[a, b].get("color", ec) for [a, b] in self.graph.edges]

        # Here we could get shapes for individual types of nodes.. but would have to
        # Draw them separately using a nodelist.
        # nodetypes = [self.components[n].__class__.__name__ for n in self.graph.nodes]

        method(
            self.graph,
            edge_color=ec,
            with_labels=True,
            ax=ax,
            node_shape="h",
            node_color=nc,
            node_size=ns,
            font_color="white",
            font_size=figsize[0],
            arrowsize=figsize[0] * 1.5,
            arrowstyle="->",
            connectionstyle="arc3,rad=0.1",
        )
        ax.axis(np.array(ax.axis()) * 1.1)  # 110% range, as the axis is about 0, 0
        return ax
