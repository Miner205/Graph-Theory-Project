import folium
from get_stations_coords import get_stations_pos, get_all_stations_pos


def draw_metro_graph(graph, with_all_stations=False) -> None:
    assert graph.name == "19", f"this function is only intended for the Paris metro graph (graph '19', not graph '{graph.name}')."
    vertices = get_stations_pos()  # get the GPS (latitude, longitude) coords of the nodes.

    edges = graph.list_arcs  # get the arcs/edges between the nodes.

    m = folium.Map(location=(48.8566, 2.3522), zoom_start=12)  # create a map centered on Paris.

    for name, (lat, lon) in vertices.items():  # add the nodes to the map.
        folium.CircleMarker(
            location=(lat, lon),
            radius=6,
            popup=name,
            color='blue',
            fill=True,
            fill_color='blue'
        ).add_to(m)
    if with_all_stations:
        for name, (lat, lon) in get_all_stations_pos().items():
            if (lat, lon) not in vertices.values():
                folium.CircleMarker(
                    location=(lat, lon),
                    radius=4,
                    popup=name,
                    color='purple',
                    fill=True,
                    fill_color='purple'
                ).add_to(m)

    for start, end, weight in edges:  # add the edges to the map.
        folium.PolyLine(
            locations=[vertices[start], vertices[end]],
            color='red',
            weight=2,
            tooltip=weight
        ).add_to(m)

    # save the result in an HTML file
    if with_all_stations:
        file_name = "graphs drawing/metro_graph_with_all_stations_map.html"
        m.save(file_name)
    else:
        file_name = "graphs drawing/metro_graph_map.html"
        m.save(file_name)
    print(f"HTML file \"{file_name}\" created.")
    curr_choice = None
    while curr_choice is None or (curr_choice != "yes" and curr_choice != "no"):
        if curr_choice is not None:
            print("yes or no ?\n")
        else:
            print("Do you want to automatically open the HTML file in your browser? : \"yes\" or \"no\"?")
            print("note: only correctly open it automatically on Chrome \n; if it opened automatically on Microsoft Edge, you will need to open it manually.")
        curr_choice = input()
    if curr_choice == "yes":
        import webbrowser
        webbrowser.open(file_name)
