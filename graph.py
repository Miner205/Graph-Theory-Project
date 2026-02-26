
class Graph:
    def __init__(self, x: int):
        self.nb_vertices: int = 0
        self.nb_arcs: int = 0
        self.list_arcs: list[tuple[int, int, int]] = list()
        self.load_graph_x(x)
        self.adjacency_matrix: list[list[int]] = [[0 for _ in range(self.nb_vertices)] for _ in range(self.nb_vertices)]
        self.compute_adjacency_matrix()
        self.floyd_warshall_graph = []

    def __str__(self):
        return ("nb of vertices: " + str(self.nb_vertices) + '\n' +
                "nb of arcs: " + str(self.nb_arcs) + '\n' +
                str([arc for arc in self.list_arcs]))

    def load_graph_x(self, x: int) -> None:
        with open("./graphs/"+str(x)+".txt", 'r') as f:
            line = f.readline()
            self.nb_vertices = int(line.strip('\n'))
            line = f.readline()
            self.nb_arcs = int(line.strip('\n'))
            for i in range(self.nb_arcs):
                line = f.readline()
                l_temp = line.strip('\n').split(' ')
                self.list_arcs.append((int(l_temp[0]), int(l_temp[1]), int(l_temp[2])))

    def save_graph_as_x(self, x: int) -> None:
        with open("./graphs/" + str(x) + ".txt", 'w') as f:
            f.write(str(self.nb_vertices) + '\n')
            f.write(str(self.nb_arcs) + '\n')
            for arc in self.list_arcs:
                f.write(str(arc[0]) + ' ' + str(arc[1]) + ' ' + str(arc[2]) + '\n')

    def compute_adjacency_matrix(self) -> None:
        for arc in self.list_arcs:
            self.adjacency_matrix[arc[0]][arc[1]] = arc[2]

    def reverse_adjacency_matrix(self) -> None:
        temp = []
        for i in range(0, len(self.adjacency_matrix)):
            for j in range(0, len(self.adjacency_matrix)):
                if self.adjacency_matrix[i][j] != "_":
                    temp.append((i,j,self.adjacency_matrix[i][j]))
        self.list_arcs = temp
        self.nb_arcs = len(temp)

    def print_adjacency_matrix(self, with_degrees=False) -> None:
        if with_degrees: in_degree, out_degree = self.compute_degrees()
        max_char_size = 0
        for i in range(self.nb_vertices):
            for j in range(self.nb_vertices):
                size_char = len(str(self.adjacency_matrix[i][j]))
                if size_char > max_char_size:
                    max_char_size = size_char
        if with_degrees and max_char_size < 3: max_char_size = 3

        print(' ', end=(max_char_size-1)*' '+' ')
        for k in range(self.nb_vertices):
            size_char = len(str(k))
            print(k, end=(max_char_size-size_char)*' '+' ')
        if with_degrees: print("d°+", end="")
        print()

        h = 0
        for i in range(self.nb_vertices):
            print(h, end=(max_char_size-len(str(h)))*' '+' ')
            for j in range(self.nb_vertices):
                size_char = len(str(self.adjacency_matrix[i][j]))
                print(self.adjacency_matrix[i][j], end=(max_char_size-size_char)*' '+' ')
            if with_degrees: print(out_degree[i], end="")
            print()
            h += 1

        if with_degrees:
            print('d°-', end=(max_char_size - 3) * ' ' + ' ')
            for k in range(self.nb_vertices):
                size_char = len(str(k))
                print(in_degree[k], end=(max_char_size - size_char) * ' ' + ' ')
            print()

    def compute_degrees(self) -> tuple[list[int], list[int]]:
        """return: ([in-degrees=d°-], [out-degrees=d°+])"""
        in_degree = [0 for _ in range(self.nb_vertices)]
        out_degree = [0 for _ in range(self.nb_vertices)]

        for i in range(self.nb_vertices):
            for j in range(self.nb_vertices):
                in_degree[j] += 1 if self.adjacency_matrix[i][j] else 0
                out_degree[i] += 1 if self.adjacency_matrix[i][j] else 0

        return in_degree, out_degree

    def compute_incidence_matrix(self) -> list[list[int]]:
        """For a directed graph : directed_incidence_matrix"""
        incidence_matrix = [[0 for _ in range(self.nb_arcs)] for _ in range(self.nb_vertices)]
        for arc_i in range(len(self.list_arcs)):
            incidence_matrix[self.list_arcs[arc_i][0]][arc_i] = 1
            incidence_matrix[self.list_arcs[arc_i][1]][arc_i] = -1
        return incidence_matrix

    def print_incidence_matrix(self) -> None:
        incidence_matrix = self.compute_incidence_matrix()
        max_char_size = 0
        for i in range(self.nb_vertices):
            for j in range(self.nb_arcs):
                size_char = len(str(incidence_matrix[i][j]))
                if size_char > max_char_size:
                    max_char_size = size_char

        print(' ', end=(max_char_size-1)*' '+' ')
        for k in range(self.nb_arcs):
            size_char = len(str(k))
            print(k, end=(max_char_size-size_char)*' '+' ')
        print()

        h = 0
        for i in range(self.nb_vertices):
            print(h, end=(max_char_size-len(str(h)))*' '+' ')
            for j in range(self.nb_arcs):
                size_char = len(str(incidence_matrix[i][j]))
                print(incidence_matrix[i][j], end=(max_char_size-size_char)*' '+' ')
            print()
            h += 1

    def floyd_warshall(self) -> None:
        distance = [["_" for i in range(self.nb_vertices)] for j in range(self.nb_vertices)]
        for i in range(self.nb_vertices):
            distance[i][i] = 0
        for arc in self.list_arcs:
            distance[arc[0]][arc[1]] = arc[2]
        # Not handling _ case atm (suggesting + infinity = no edge)
        for i in range(self.nb_vertices):
            for j in range(self.nb_vertices):
                for k in range(self.nb_vertices):
                    if distance[i][j] > distance[i][k] + distance[k][j]: # Is the current distance at i->j bigger than the sum of distances i->k and k->j ?
                        distance[i][j] = distance[i][k] + distance[k][j] # If it does, reassign that distance to the smaller one, the sum.
        print(distance)
        for i in range(self.nb_vertices):
            if distance[i][i] < 0: # The check is simple : if a path from a vertice to itself is negative, it means 1 - There is a cycle, 2 - Per definition it's absorbent (negative cost). Thus not possible to seek shortest paths here.
                print("The graph contains an absorbent cycle starting and ending in " + str(i) + ".")
                self.floyd_warshall_graph = ["absorbent"]
                return
        self.floyd_warshall_graph = distance
        return
