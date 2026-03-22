# Graph Theory Project
Finding shortest paths using the Floyd–Warshall algorithm

# int2 - Our Team - Groupe 4 :
Arthur Donnat
Arthur Delannoy
Raphaël Lesterlin

# GitHub link :
https://github.com/Miner205/Graph-Theory-Project

# Project specification :
- Directed graph.
- Weighted graph.
- weight numerical values : negative values allowed, '0' allowed. No path is represented by '_'.
- vertices are numbered/named from 0 to nbofvertices-1.
- At most one arc from a vertex x to a vertex y.
- graph format I of txt used - from Project pdf Appendix :
    - Line 1 - Number of vertices
    - Line 2 - Number of arcs
    - Lines 3 to 3 + number of arcs - Initial vertex, terminal vertex, arc value
- graph format II of txt used :
... (finally, not done)

# ToDo :
- execution traces txt
- ...

# Functionalities done :
- Graph: load graph, save graph, adjacency matrix, 
    degrees(for fun), incidence matrix(for fun ; loops are represented by the value '2' by convention).
- floyd-warshall algo.
- absorbing circuit stuff.
- main while loop.
- better displays/graphs drawing : method 1 with networkx and matplotlib, method 2 with pygame [WIP/not done], method 3 with folium.
- ...

# Test graphs list - provenance/use case :
- 1 to 13 = Provided test graphs.
- 14 = Appendix example from Project pdf.
- 15 = Graph from the first ppt, to test the incidence matrix.
/!\ attention en prenant des graph du cours : ici la numérotation des vertex commence à partir de 0 et non 1 comme dans le cours.
- 16 = Graph from HW2.
- 17 = Graph from HW4.
- 18 = Graph from "Shortest path problem" Wikipedia page.
- 19 = Paris metro interchange graph.

# Technicalities about the metro interchange graph :
- The vertices are the different correspondences of Paris's metro wether it is with another metro line or anything else.
- The values of the arcs is the distance from one correspondence to the next in terms of number of station.
- When they were 2 metro lines that contained the same arc, we only kept 1.
- When they were 2 metro lines that contained the same arc but with different values, we kept the smallest value ignoring the time to change line.
- We did not include the correspondence between Carrefour - Pleyel and Saint-Denis - Pleyel since we have to walk outside between the 2 but kept the vertex in case we changed our minds.
- We did not include the correspondence between Saint-Augustin and Saint-Lazare since they are linked by an underground corridor, and it is weird on the metro plan but kept the vertex in case we changed our minds.
