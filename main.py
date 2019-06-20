import argparse
import logging
import algorithm as alg
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

parser = argparse.ArgumentParser(description='RL running machine')
parser.add_argument('--environment_name', metavar='ENV_CLASS', type=str, default='TSP', help='Class to use for the environment. Must be in the \'environment\' module')
parser.add_argument('--algorithm', type=str, default='greedy', help='algorithm name')
parser.add_argument('--graph_nbr', type=int, default='3000', help='number of differente graph to generate for calculating')
parser.add_argument('--node_min', type=int, metavar='nnode',default='20', help="Minimum number of node in generated graphs")
parser.add_argument('--node_max', type=int, metavar='nnode',default='20', help="Maximum number of node in generated graphs")
parser.add_argument('--input_mode', metavar='INPUT', default='random', help='Type of graph input (random, input_weight, input_point)')

def main():
    n_test = 1000
    args = parser.parse_args()
    logging.info('Loading graph %s' % args.input_mode)
    g1=graph.Graph(args.node_min, args.node_max, args.input_mode)

    print("123")
    """
    graph_list=[None]*graph_nbr
    for i in range(graph_nbr):
        graph_list[i]=graph.Graph(graph_type,node_min,node_max,input_mode)
    logging.info('Loading algorithm')
    alg_class = alg.Algorithm()
    """


if __name__ == "__main__":
    main()
