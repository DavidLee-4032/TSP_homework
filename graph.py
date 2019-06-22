import numpy as np
import networkx as nx
import random as rdm
import scipy as sp


class Graph:
    def __init__(self, min_n, max_n, input_mode,input=None):
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

        elif input_mode == "input_point": #pointwise coordinate input   input:[(2dcoordinates)]*n
            
            pass
        elif input_mode == "input_weight": #adjacent matrix input   input:np.2darray
            pass
        else:
            assert(0)
        self.route = []

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

    def min_weight_match_odd_nodes(self, graph): #negates the edge weight and make a max match, and return a graph of matching
        neg_g=nx.Graph()
        for node in graph.nodes:
            if graph.degree[node] % 2 == 1:
                neg_g.add_node(node)
        n = graph.number_of_nodes()
        for i in neg_g.nodes:
            for j in neg_g.nodes:
                if i<j:
                    neg_g.add_edge(i, j, weight=-self.graph[i][j]["weight"])
        m = nx.algorithms.matching.max_weight_matching(neg_g, maxcardinality=True)
        neg_g1=nx.Graph()
        neg_g1.add_nodes_from(neg_g)
        for e in m:
            neg_g1.add_edge(e[0], e[1], weight=-neg_g[e[0]][e[1]]["weight"])
        return neg_g1

    def nearest(self, node, graph=None, exclude=[]):#get the minimum distance node, excluding a list
        if not graph:
            graph = self.graph
        n = graph.number_of_nodes()
        x = float("inf")
        index = -1
        for i in range(n):
            if i in exclude:
                continue
            if graph[i][node]["weight"] < x:
                x = graph[i][node]["weight"]
                index = i
        return (x, index)

    def farthest(self, node, graph=None, exclude=[]):#get the minimum distance node, excluding a list
        if not graph:
            graph = self.graph
        n = graph.number_of_nodes()
        x = float("-inf")
        index = -1
        for i in range(n):
            if i in exclude:
                continue
            if graph[i][node]["weight"] > x:
                x = graph[i][node]["weight"]
                index = i
        return (x, index)

    def savings(self, node1, node2, node3, graph=None):
        if not graph:
            graph = self.graph
        s = graph[node1][node3]["weight"] + graph[node2][node3]["weight"] - graph[node1][node2]["weight"]
        return s

    def cal(self):
        cost=0
        n=self.cur_n
        for i in range(self.cur_n):
            cost += self.graph[self.route[i]][self.route[(i+1)%n]]["weight"]
        return cost