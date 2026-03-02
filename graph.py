import os


class Graph:
    def __init__(self, x: int):
        self.nb_vertices: int = 0
        self.nb_arcs: int = 0
        self.list_arcs: list[tuple[int, int, int]] = list()
        self.load_graph_x(x)
        self.adjacency_matrix: list[list] = [['_' for _ in range(self.nb_vertices)] for _ in range(self.nb_vertices)]
        self.compute_adjacency_matrix()
        self.floyd_warshall_graph = []

    def __str__(self):
        return ("nb of vertices: " + str(self.nb_vertices) + '\n' +
                "nb of arcs: " + str(self.nb_arcs) + '\n' +
                str([arc for arc in self.list_arcs]))

    def load_graph_x(self, x: int) -> None:
        if not os.path.isfile("./graphs/"+str(x)+".txt"):
            raise ValueError("The specified graph does not exist.")
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

        for k in range(self.nb_vertices):
            max_char_size = max(max_char_size, len(str(k)))
        max_char_size += 4 # Aesthetics

        print(" " * max_char_size, end="")
        for k in range(self.nb_vertices):
            print(f"{k:>{max_char_size}}", end="") # i.e., align to the right with a maximum width of max_char_size
        if with_degrees: print(f"{'d°+':>{max_char_size}}", end="")
        print()

        for i in range(self.nb_vertices):
            print(f"{i:>{max_char_size}}", end="")
            for j in range(self.nb_vertices):
                print(f"{self.adjacency_matrix[i][j]:>{max_char_size}}", end="")
            if with_degrees: print(f"{out_degree[i]:>{max_char_size}}", end="")
            print()

        if with_degrees:
            print(f"{'d°-':>{max_char_size}}", end="")
            for k in range(self.nb_vertices):
                print(f"{in_degree[k]:>{max_char_size}}", end="")
            print()

    def compute_degrees(self) -> tuple[list[int], list[int]]:
        """return: ([in-degrees=d°-], [out-degrees=d°+])"""
        in_degree = [0 for _ in range(self.nb_vertices)]
        out_degree = [0 for _ in range(self.nb_vertices)]

        for i in range(self.nb_vertices):
            for j in range(self.nb_vertices):
                in_degree[j] += 1 if self.adjacency_matrix[i][j] != '_' else 0
                out_degree[i] += 1 if self.adjacency_matrix[i][j] != '_' else 0

        return in_degree, out_degree

    def compute_incidence_matrix(self) -> list[list]:
        """For a directed graph : directed_incidence_matrix"""
        incidence_matrix: list[list] = [['_' for _ in range(self.nb_arcs)] for _ in range(self.nb_vertices)]
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
        if len(str(self.nb_vertices - 1)) > max_char_size: max_char_size = len(str(self.nb_vertices - 1))
        if len(str(self.nb_arcs - 1)) > max_char_size: max_char_size = len(str(self.nb_arcs - 1))

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
        distance = [[float('inf') for i in range(self.nb_vertices)] for j in range(self.nb_vertices)] # L
        predecessors = [[j for i in range(self.nb_vertices)] for j in range(self.nb_vertices)] # P
        for i in range(self.nb_vertices):
            distance[i][i] = 0 # Set diagonal at 0, since there's no distance from a vertice to itself in our loopless scenario
        for arc in self.list_arcs:
            distance[arc[0]][arc[1]] = arc[2] # Put the weight of known edges in the correct spots of the distance matrix for initialization
        counter = 0
        for i in range(self.nb_vertices):
            for j in range(self.nb_vertices):
                for k in range(self.nb_vertices):
                    if distance[i][j] > distance[i][k] + distance[k][j]: # Is the current distance at i->j bigger than the sum of distances i->k and k->j ?
                        counter += 1
                        distance[i][j] = distance[i][k] + distance[k][j] # If it does, reassign that distance to the smaller one, the sum.
                        predecessors[i][j] = predecessors[k][j] # Updates predecessor in the matrix
                        print("Modification n°" + str(counter) + " :\n")
                        print("Updated distance matrix")
                        max_char_size = 0 # Prints L
                        for l in range(self.nb_vertices):
                            for m in range(self.nb_vertices):
                                size_char = len(str(distance[l][m]))
                                if size_char > max_char_size:
                                    max_char_size = size_char

                        for l in range(self.nb_vertices):
                            max_char_size = max(max_char_size, len(str(l)))
                        max_char_size += 4 # Aesthetics

                        print(" " * max_char_size, end="")
                        for l in range(self.nb_vertices):
                            print(f"{l:>{max_char_size}}", end="")
                        print()

                        for l in range(self.nb_vertices):
                            print(f"{l:>{max_char_size}}", end="")
                            for m in range(self.nb_vertices):
                                print(f"{distance[l][m]:>{max_char_size}}", end="")
                            print()

                        print("Updated predecessor matrix")
                        max_char_size = 0 # Prints P
                        for l in range(self.nb_vertices):
                            for m in range(self.nb_vertices):
                                size_char = len(str(predecessors[l][m]))
                                if size_char > max_char_size:
                                    max_char_size = size_char

                        for l in range(self.nb_vertices):
                            max_char_size = max(max_char_size, len(str(l)))
                        max_char_size += 4 # Aesthetics

                        print(" " * max_char_size, end="")
                        for l in range(self.nb_vertices):
                            print(f"{l:>{max_char_size}}", end="")
                        print()

                        for l in range(self.nb_vertices):
                            print(f"{l:>{max_char_size}}", end="")
                            for m in range(self.nb_vertices):
                                print(f"{predecessors[l][m]:>{max_char_size}}", end="")
                            print()

        for i in range(self.nb_vertices):
            if distance[i][i] < 0: # The check is simple : if a path from a vertice to itself is negative, it means 1 - There is a cycle, 2 - Per definition it's absorbent (negative cost). Thus not possible to seek shortest paths here.
                print("The graph contains an absorbent cycle starting and ending in " + str(i) + ".")
                self.floyd_warshall_graph = ["absorbent"]
                return
        self.floyd_warshall_graph = [distance,predecessors]
        return

    def minimum_path(self, a, b) -> list:
        if self.floyd_warshall_graph == []:
            print("The Floyd_Warshall algorithm was not executed.")
            return []
        elif self.floyd_warshall_graph == ["absorbent"]:
            print("The graph contains an absorbent cycle ; minimum paths cannot be found.")
            return ["absorbent"]
        elif a > len(self.adjacency_matrix) or b > len(self.adjacency_matrix) or b < 0 or a < 0:
            print("Invalid start and endpoint")
            return ["Error"]
        else: 
            path = [b]
            while a not in path:
                if self.floyd_warshall_graph[0][a][path[0]] == float('inf'):
                    print('There is no path between the provided vertices')
                    return ["nonexistent"]
                path.insert(0,self.floyd_warshall_graph[1][a][path[0]])
            return path

        
