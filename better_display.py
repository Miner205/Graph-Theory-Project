import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from pygame.display import get_desktop_sizes, init


def draw_weighted_graph(adj_matrix, is_metro_graph=False, metro_graph_with_compression=True) -> None:
    n = len(adj_matrix)
    G = nx.DiGraph()

    # add nodes
    for i in range(n):
        G.add_node(i)

    # add weighted edges
    for i in range(n):
        for j in range(n):
            if adj_matrix[i][j] != '_':
                G.add_edge(i, j, weight=adj_matrix[i][j])

    for u, v, d in G.edges(data=True):
        if d['weight'] != 0:
            d['inv_weight'] = 1 / d['weight']  # to make the pos right below a bit better.
        else:
            d['inv_weight'] = 0
    pos = nx.spring_layout(G, k=2/n**0.5, weight='inv_weight')  # used if not planar and not metro plan ; quite 'random' positioning. Never used in the example graphs.

    is_planar, embedding = nx.check_planarity(G)
    print("Graph is planar ? :", is_planar)
    if is_planar:
        pos = nx.combinatorial_embedding_to_pos(embedding)  # if planar, draw planar graph.

    from get_stations_coords import get_stations_pos
    if is_metro_graph:
        vertex_positions = get_stations_pos()

        if metro_graph_with_compression:
            xy_positions = vertex_positions
            import numpy as np
            # center
            xs = np.array([x for x, y in xy_positions.values()])
            ys = np.array([y for x, y in xy_positions.values()])
            cx, cy = xs.mean(), ys.mean()
            # distances from the center
            def dist(x, y):
                return np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            dists = {v: dist(x, y) for v, (x, y) in xy_positions.items()}
            threshold = np.percentile(list(dists.values()), 90)  # threshold = the 10% furthest away.
            threshold2 = np.percentile(list(dists.values()), 70)  # second threshold = the 10% to 30% furthest away.
            def transform(x, y):
                dx, dy = x - cx, y - cy
                d = np.sqrt(dx ** 2 + dy ** 2)
                # compression of the outliers
                if d > threshold:
                    factor = (threshold / d)**1.5
                    dx *= factor
                    dy *= factor
                elif d > threshold2:
                    factor = (threshold2 / d)**0.5
                    dx *= factor
                    dy *= factor
                return cx + dx, cy + dy
            vertex_positions = {v: transform(x, y) for v, (x, y) in xy_positions.items()}

        def gps_to_xy(lat, lon):
            import math
            R = 6371000  # earth radius (meters).
            x = R * math.radians(lon)
            y = R * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
            return (x, y)

        xy_positions = {v: gps_to_xy(lat, lon) for v, (lat, lon) in vertex_positions.items()}

        pos = xy_positions

    # plot window size
    init()
    screen_width, screen_height = get_desktop_sizes()[0]
    dpi = 100
    figsize = (screen_width / (dpi*4) + n*0.5, screen_height / (dpi*4) + n*0.5)
    plt.figure(figsize=figsize, dpi=dpi)

    edge_style = 'arc3, rad = 0.075'
    # draw nodes & edges
    nx.draw(
        G, pos,
        with_labels=True,
        node_color="lightblue",
        node_size=700,
        font_size=12,
        font_weight="bold",
        edge_color="gray",
        connectionstyle=edge_style
    )

    # draw edge labels (weights)
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=nx.get_edge_attributes(G, 'weight'),
        font_color='red',
        connectionstyle=edge_style,
        label_pos=0.3,
        bbox={"boxstyle": 'round,pad=0.05', "fc": (1.0, 1.0, 1.0), "ec": (1.0, 1.0, 1.0)}
    )

    plt.title("Graph Visualization")
    plt.show()
