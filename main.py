import argparse
import logging
import algorithm
import graph
import numpy as np
import networkx as nx
import sys

# # 2to3 compatibility
# try:
#     input = raw_input
# except NameError:
#     pass

# Set up logger
logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(message)s',
    level=logging.INFO
)

parser = argparse.ArgumentParser(description='TSP runner')
parser.add_argument('--graph_nbr', type=int, default='3000', help='number of differente graph to generate for calculating')
parser.add_argument('--node_min', type=int, metavar='nnode',default='70', help="Minimum number of node in generated graphs")
parser.add_argument('--node_max', type=int, metavar='nnode',default='100', help="Maximum number of node in generated graphs")
parser.add_argument('--input_mode', metavar='INPUT', default='random', help='Type of graph input (random, input_weight, input_point)')

def main():
    n_test = 1000
    args = parser.parse_args()
    logging.info('Loading random graphs')
    g1=graph.Graph(args.node_min, args.node_max, 'random')
    alg=algorithm.Algorithm()
    print(alg.double_tree(g1))
    print(alg.christofides(g1))
    print(alg.greed(g1))
    print(alg.cheapest(g1))
    print(alg.nearest(g1))
    print(alg.k_opt(3, g1))
    """
    graph_list=[None]*graph_nbr
    for i in range(graph_nbr):
        graph_list[i]=graph.Graph(graph_type,node_min,node_max,input_mode)
    logging.info('Loading algorithm')
    alg_class = alg.Algorithm()
    """


if __name__ == "__main__":
    main()
