
class Graph:
    def __init__(self, x: int):
        self.nb_vertices: int = 0
        self.nb_arcs: int = 0
        self.list_arcs: list = list()
        self.load_graph_x(x)
        self.adjacency_matrix: list = [[0 for j in range(self.nb_vertices)] for i in range(self.nb_vertices)]
        self.compute_adjacency_matrix()

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

    def print_adjacency_matrix(self) -> None:
        max_char_size = 0
        for i in range(self.nb_vertices):
            for j in range(self.nb_vertices):
                size_char = len(str(self.adjacency_matrix[i][j]))
                if size_char > max_char_size:
                    max_char_size = size_char

        print('-', end=(max_char_size-1)*' '+' ')
        for k in range(self.nb_vertices):
            size_char = len(str(k))
            print(k, end=(max_char_size-size_char)*' '+' ')
        print()

        h = 0
        for i in range(self.nb_vertices):
            print(h, end=(max_char_size-len(str(h)))*' '+' ')
            for j in range(self.nb_vertices):
                size_char = len(str(self.adjacency_matrix[i][j]))
                print(self.adjacency_matrix[i][j], end=(max_char_size-size_char)*' '+' ')
            print()
            h += 1
