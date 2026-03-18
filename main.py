import os

from graph import Graph


def choosing_graph(current_graph) -> Graph:
    graph_choice = None
    while graph_choice is None or ((graph_choice != "go back" or current_graph is None) and os.path.isfile("./graphs/" + graph_choice + ".txt") is False):
        if graph_choice is not None:
            if graph_choice == "go back":
                print("No graph currently loaded.\n")
            else:
                print("The specified graph does not exist.\n")
        print("Choose a graph to use:")
        print('"1" to "13": Provided test graphs.')
        print('"14": Appendix example from Project pdf.')
        print('"15": Graph from the first ppt, to test the incidence matrix.')
        print('"16": Graph from HW2.')
        print('"17": Graph from HW4.')
        print('"18": Graph from "Shortest path problem" Wikipedia page.')
        print('"19": Paris metro interchange graph')
        print('"20+" (or anything really): Your own saved graph (only if you saved a graph).')
        if current_graph is not None:
            print('Type "go back" to continue with the current graph.')
        graph_choice = input()
        print()
    if graph_choice == "go back":
        return current_graph
    return Graph(graph_choice)


def display_graph(current_graph) -> None:
    display_choice = None
    while display_choice not in ["adjacency", "incidence", "both", "go back"]:
        if display_choice is not None:
            print("This is not a valid display.\n")
        print("How would you like to display the graph:")
        print('"adjacency": Adjacency matrix of the graph.')
        print('"incidence": Incidence matrix of the graph.')
        print('"both": Both matrices of the graph')
        print('Type "go back" to go back to the main options.')
        display_choice = input()
        print()
    if display_choice != "go back":
        print(current_graph)
        print()
        if display_choice == "adjacency" or display_choice == "both":
            print("Adjacency matrix:")
            current_graph.print_adjacency_matrix()
            print()
        if display_choice == "incidence" or display_choice == "both":
            print("Incidence matrix:")
            current_graph.print_incidence_matrix()
            print()
    print("\n")


def copy_graph(current_graph) -> Graph:
    name_choice = None
    while name_choice is None or (name_choice != "go back" and os.path.isfile("./graphs/" + name_choice + ".txt") is True):
        if name_choice is not None:
            print("A graph with this name already exists.\n")
        print('Enter a name for the copy (Type "go back" to go back to the main options):')
        name_choice = input()
        print()
    if name_choice != "go back":
        current_graph.save_graph_as_x(name_choice)
        print('A copy of the graph "' + current_graph.name + '" named "' + name_choice + '" as been created.')
        print('Would you like to set "' + name_choice + '" as your current graph ("yes"):')
        set_graph_choice = input()
        print()
        if set_graph_choice == "yes":
            return Graph(name_choice)
    return current_graph


def path_to_str(distances, path) -> str:
    path_str = "\t"
    for rank in range(len(path)):
        path_str += str(path[rank])
        if rank != len(path) - 1:
            path_str += " (" + str(distances[rank]) + ") -> "
    return path_str


# TODO: extract floyd-warshall + modifications in .txt
def get_minimum_path(current_graph) -> None:
    floyd_warshall_choice = "yes"
    if current_graph.floyd_warshall_graph:
        print('The Floyd-Warshall algorithm was already computed for graph "' + current_graph.name + '", do you want to redo it ("yes"):')
        floyd_warshall_choice = input()
        print()

    if floyd_warshall_choice == "yes":
        print('Do you want to see all intermediate modifications ("yes"):')
        modification_display_choice = input()
        print()
        if modification_display_choice == "yes":
            modification_display_choice = True
            print("Floyd-Warshall algorithm:")
        else:
            modification_display_choice = False
        current_graph.floyd_warshall(modification_display_choice)

    if current_graph.floyd_warshall_graph == ["absorbent"]:
        print("No minimum-value path can be computed.")
    else:
        print(current_graph.floyd_warshall_graph)
        print('Do you want to see all minimum-value paths ("yes"):')
        all_path_choice = input()
        print()
        if all_path_choice == "yes":
            for starting_vertex in range(current_graph.nb_vertices):
                for end_vertex in range(current_graph.nb_vertices):
                    total_path_value, path_values, minimum_path = current_graph.minimum_path(starting_vertex, end_vertex)
                    if minimum_path != ["nonexistent"]:
                        print("The minimum-value path from " + str(starting_vertex) + " to " + str(end_vertex) + " has a value of " + str(total_path_value) + " and goes as follows:")
                        print(path_to_str(path_values, minimum_path))
        else:
            starting_point_choice = None
            while starting_point_choice is None or starting_point_choice >= current_graph.nb_vertices or starting_point_choice < 0:
                if starting_point_choice is not None:
                    print("The vertex does not exist in the graph.\n")
                # TODO: go back
                print('Choose a starting point:')
                # TODO: prevent other types
                starting_point_choice = int(input())
                print()
            end_point_choice = None
            while end_point_choice is None or end_point_choice >= current_graph.nb_vertices or end_point_choice < 0:
                if end_point_choice is not None:
                    print("The vertex does not exist in the graph.\n")
                # TODO: go back
                print('Choose an end point:')
                # TODO: prevent other types
                end_point_choice = int(input())
                print()
            total_path_value, path_values, minimum_path = current_graph.minimum_path(starting_point_choice, end_point_choice)
            if minimum_path != ["nonexistent"]:
                print("The minimum-value path from " + str(starting_point_choice) + " to " + str(end_point_choice) + " has a value of " + str(total_path_value) + " and goes as follows:")
                print(path_to_str(path_values, minimum_path))
    print("\n\n")


# TODO: prevent when absorbent
# TODO: go back
def minimum_value_as_graph(current_graph) -> Graph:
    if not current_graph.floyd_warshall_graph:
        current_graph.floyd_warshall(False)
    current_graph.save_minimum_value_paths_as_graph(current_graph.name + "_minimum_value_paths")
    print('The graph "' + current_graph.name + '_minimum_value_paths" as been created.')
    print('Would you like to set "' + current_graph.name + '_minimum_value_paths" as your current graph ("yes"):')
    set_graph_choice = input()
    print()
    if set_graph_choice == "yes":
        return Graph(current_graph.name + '_minimum_value_paths')
    return current_graph


def quitting() -> bool:
    print('Are you sure you want to quit the program ("YES"):')
    quit_choice = input()
    print("\n\n")
    if quit_choice == "YES":
        return True
    return False


if __name__ == '__main__':
    graph = choosing_graph(None)
    print('The graph "' + graph.name + '" as been set as the current graph.\n\n\n')
    quit_program = False
    while quit_program is False:
        option_choice = None
        while option_choice not in ["graph", "display", "copy", "minimum-value path", "save minimum-value graph", "quit"]:
            if option_choice is not None:
                print("This is not a valid option.\n")
            print("What would you like to do:")
            print('"graph": Change graph.')
            print('"display": Display graph.')
            print('"copy": Copy graph.')
            print('"minimum-value path": Compute the minimum-value paths in the graph using Floyd-Warshall algorithm.')
            print('"save minimum-value graph": save the minimum-value paths as a new graph.')
            print('"quit": Quit the program.')
            option_choice = input()
            print()
        print("\n")
        if option_choice == "graph":
            graph = choosing_graph(graph)
        elif option_choice == "display":
            display_graph(graph)
        elif option_choice == "copy":
            graph = copy_graph(graph)
        elif option_choice == "minimum-value path":
            get_minimum_path(graph)
        elif option_choice == "save minimum-value graph":
            graph = minimum_value_as_graph(graph)
        elif option_choice == "quit":
            quit_program = quitting()
        if option_choice in ["graph", "copy", "save minimum-value graph"]:
            print('The graph "' + graph.name + '" as been set as the current graph.\n\n\n')
    print("Goodbye!")
