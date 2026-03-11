# Graph Theory Project
Finding shortest paths using the Floyd–Warshall algorithm

# int3 - Our Team :
Arthur Donnat
Arthur Delannoy
Raphaël Lesterlin

# GitHub link :
https://github.com/Miner205/Graph-Theory-Project

# Project specification :
- vertices are numbered from 0 to nbofvertices-1.
- weight numerical values : negative values allowed, '0' allowed. No path is represented by '_'.
- graph format I of txt used - from Project pdf Appendix :
    - Line 1 - Number of vertices
    - Line 2 - Number of arcs
    - Lines 3 to 3 + number of arcs - Initial vertex, terminal vertex, arc value
- graph format II of txt used :
...

# ToDo :
- main while loop
- floyd-warshall algo
- absorbing circuit stuff
- execution traces txt
- ...

# Functionalities done :
- Graph: load graph, save graph, adjacency matrix, 
    degrees(for fun), incidence matrix(for fun).

# Test graphs list - provenance/use case :
- 1 to 13 = test graphs provided.
- 14 = from Project pdf, Appendix Example.
- 15 = graph from ppt cours 1, pour test incidence matrix.
/!\ attention en prenant des graph du cours : ici la numérotation des vertex commence à partir de 0 et non 1 comme dans le cours.
- 16 = from HW2.
- 17 = from HW4.
- 18 = from Shortest path problem Wikipedia page.
- 19 = plan of the correspondences of Paris's metro.

# Technicalities about the metro plan :
- The vertices are the different correspondences of Paris's metro wether it is with another metro line or anything else.
- The values of the arcs is the distance from one correspondence to the next in terms of number of station.
- When they were 2 metro lines that contained the same arc, we only kept 1.
- When they were 2 metro lines that contained the same arc but with different values, we kept the smallest value ignoring the time to change line.
- We did not include the correspondence between Carrefour - Pleyel and Saint-Denis - Pleyel since we have to walk outside between the 2 but kept the vertex in case we changed our minds.
- We did not include the correspondence between Saint-Augustin and Saint-Lazare since they are linked by an underground corridor, and it is weird on the metro plan but kept the vertex in case we changed our minds.
