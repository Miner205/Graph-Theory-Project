import folium
from get_stations_coords import get_stations_pos, get_all_stations_pos
from graph import Graph


def draw_metro_graph(graph, with_all_stations=False):
    # 1. Définir quelques sommets avec GPS (latitude, longitude)
    vertices = get_stations_pos()

    # 2. Définir des arêtes entre les sommets
    edges = graph.list_arcs

    # 3. Créer une carte centrée sur Paris
    m = folium.Map(location=(48.8566, 2.3522), zoom_start=12)

    # 4. Ajouter les sommets
    for name, (lat, lon) in vertices.items():
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

    # 5. Ajouter les arêtes (lignes entre sommets)
    for start, end, weight in edges:
        folium.PolyLine(
            locations=[vertices[start], vertices[end]],
            color='red',
            weight=2,
            tooltip=weight
        ).add_to(m)

    # 6. Sauver dans un fichier HTML
    if with_all_stations:
        file_name = "graphs drawing/metro_graph_with_all_stations_map.html"
        m.save(file_name)
    else:
        file_name = "graphs drawing/metro_graph_map.html"
        m.save(file_name)
    print(f">html file \"{file_name}\" created.")
    curr_choice = None
    while curr_choice is None or (curr_choice != "yes" and curr_choice != "no"):
        if curr_choice is not None:
            print("yes or no ?\n")
        else:
            print("Do you want to automatically open the html file in your browser? : \"yes\" or \"no\"?")
        curr_choice = input()
    if curr_choice == "yes":
        import webbrowser
        webbrowser.open(file_name)


gg = Graph("19")
draw_metro_graph(gg, with_all_stations=False)
