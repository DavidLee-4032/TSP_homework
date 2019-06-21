import numpy as np
import networkx as nx
import random as rdm
import scipy as sp


class Graph:
    def __init__(self, min_n, max_n, input_mode):
        if input_mode == "random":
            self.cur_n=np.random.randint(max_n-min_n+1)+min_n
            self.graph = nx.Graph()
            self.graph.add_nodes_from(range(self.cur_n))
            for i in range(self.cur_n):
                for j in range(i):
                    self.graph.add_edge(i, j, weight=1.6/rdm.uniform(0.01,0.5))
            fl = nx.algorithms.shortest_paths.dense.floyd_warshall_numpy(self.graph)
            for i in range(self.cur_n):
                for j in range(i):
                    self.graph[i][j]["weight"] = fl[i,j]
        elif input_mode == "input_point": #pointwise coordinate input
            pass
        elif input_mode == "input_weight": #adjacent matrix input
            pass
        else:
            assert(0)

    def min_tree(self, graph=None):
        if not graph:
            graph = self.graph
        return nx.algorithms.tree.mst.minimum_spanning_tree(graph, algorithm='prim', ignore_nan=False)

    def add(self, graph1, graph2): # add graph2 into graph1
        MG = nx.MultiGraph()
        MG.add_nodes_from(graph1)
        MG.add_weighted_edges_from(graph1.edges.data("weight"))
        MG.add_weighted_edges_from(graph2.edges.data("weight"))
        return MG

    def min_euler(self, c_graph):
        return nx.algorithms.euler.eulerian_circuit(c_graph)

    def min_weight_match_odd_nodes(self, graph=None): #negates the edge weight and make a max match
        if not graph:
            graph = self.graph
        neg_g=nx.Graph()
        for node in graph.nodes:
            if node.degree[node] % 2 == 1:
                neg_g.add_node(node)
        n = graph.number_of_nodes()
        for i in neg_g.nodes:
            for j in neg_g.nodes:
                if i<j:
                    neg_g.add_edge(i, j, weight=-graph.edges[i][j])
        m = nx.algorithms.matching.max_weight_matching(neg_g, maxcardinality=True)#
        return m

    def nearest(self, node, graph=None):
        
        if not graph:
            graph = self.graph
        n = graph.number_of_nodes()
        x = float("inf")
        index = -1
        for i in range(n):
            if graph[i][node]["weight"] < x:
                x = graph[i][node]["weight"]
                index = i
        return (x, index)

    def savings(self, node, graph=None):
        if not graph:
            graph = self.graph
        n = graph.number_of_nodes()
        ar = np.zeros(n, n)
        for i in range(n):
            for j in range(i):
                ar[i, j] = graph[node][i]["weight"] + graph[node][j]["weight"] - graph[i][j]["weight"]
        return ar
