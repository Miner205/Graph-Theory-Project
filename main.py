from graph import Graph

g = Graph(4)
print(g)
print()
g.print_adjacency_matrix()
print()
g.print_adjacency_matrix(with_degrees=True)
print()
g.print_incidence_matrix()

g.adjacency_matrix[0][4] = 4
g.print_adjacency_matrix()
g.reverse_adjacency_matrix()
print(g.list_arcs)

print("\n\n\n\n\n")
g.floyd_warshall()
