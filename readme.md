# TSP_homework
This is a little program solving TSP problems.
The following methods are used:
Double Tree method,
2(3)-opt method,
Christofides method,
NN method,
Greed/Nearest/Cheapest/Farthest method.

The following graph genetator is used:
Actual instance with solution (MP-testdata. The nodes are the points in an Euclid plane and the distance in graph is exactly Euclid distance),
Randomized generator (using Floyd-Warshall algorithm to transform into an metric graph).

The following values are evaluated:
optimal ratio (in the worst case) in actual instance
AVERAGE result of randomly generated graph.

Argument used:
--graph_nbr The number of randomly generated graphs.
--node_min Minimum number of Nodes in randomly generated graphs.
--node_max Maximum number of Nodes randomly generated graphs.
--input_mode You can choose the input mode via this argument:
"random" Random generate graphs
"input_weight" input adjacent matrix in 2dmatrix.data
---example(you can also use the lower diag)---
0 4 3 6
4 0 5 4
3 5 0 5
6 4 5 0
-------------
"input_point" input 2d_coordinate of points in coordinates.data
---example---
1.0 3.5
2.2 4.4
2.1 1.3
3.5 3.1
-------------
"files_tsp225" using the data of examples in data/tsp225
