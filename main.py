from graph import Graph

g = Graph(4)
print(g)
print()
g.print_adjacency_matrix()
print()
g.print_adjacency_matrix(with_degrees=True)
print()
g.print_incidence_matrix()
