import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

DG = nx.DiGraph()

edges = [
    ("Optical\nImage", "EMPA\nImage", {}),
    ("EMPA\nImage", "Optical\nImage", {"color": "red"}),
    # do EMPA
    ("EMPA\nStage", "EMPA\nImage", {"color": "red"}),
    ("EMPA\nImage", "EMPA\nStage", {}),
    # do SIMS
    ("EMPA\nImage", "SIMS\nStage", {}),
    ("SIMS\nStage", "EMPA\nImage", {}),
    # do Laser
    ("Optical\nImage", "Laser\nStage", {"color": "red"}),
    ("Laser\nStage", "Optical\nImage", {})
    ]
DG.add_edges_from(edges)
df = pd.DataFrame(edges, columns=["A", "B", "attrs"])
df = df.set_index(df.A + "-" + df.B)

df= df.loc[['-'.join(e) for e in list(DG.edges)], :]

ec = df.attrs.apply(lambda x: x.get("color", "k"))

# %% Computing shortest path transforms.
nx.algorithms.single_source_shortest_path(DG, "Optical\nImage")
# %% --
fig, ax = plt.subplots(1, figsize=(10, 10))
nx.draw(
    DG,
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
# %% --
from pyrolite.util.plot import save_figure

save_figure(fig, save_at = '../source/_static/', name='transform_concept')
