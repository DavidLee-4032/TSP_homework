import argparse
import logging
import algorithm
import graph
import os
import numpy as np
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
parser.add_argument('--graph_nbr', type=int, default='3000', help='number of different graphs to generate')
parser.add_argument('--node_min', type=int, metavar='nnode',default='60', help="Minimum number of nodes")
parser.add_argument('--node_max', type=int, metavar='nnode',default='65', help="Maximum number of nodes")
parser.add_argument('--input_mode', metavar='INPUT', default='random', help='Type of graph input (random, input_weight, input_point, files_pr2392)')


def main():
    if os.path.exists("result"):
        os.remove("result")
    #clear and recreate the result file
    result_=open("result","w")
    args = parser.parse_args()
    alg = algorithm.Algorithm()

    if args.input_mode=="files_tsp225":
        #result_.write("Instance\tOPT\tFarthest\t3-opt\tCheapest\tchristofides\tNearest\tDT\n")
        data_path="data/"
        TSP_START_LINE=6
        TSP_END_LINE = -1
        TOUR_STAT_LINE=5
        TOUR_END_LINE=-2
        node_list=[]
        route=[]
        name="tsp225"
        tfile_name=data_path+name+".tsp"
        sfile_name=data_path+name+".opt.tour"
        tfile_=open(tfile_name,"r")
        sfile_=open(sfile_name,"r")
        tfile=tfile_.readlines()
        sfile=sfile_.readlines()
        result_dic={}
        for j in tfile[TSP_START_LINE:TSP_END_LINE]:
            node_coord=j.lstrip().rstrip("\n").split(" ")
            node_list.append((float(node_coord[1]),float(node_coord[2])))
        for j in sfile[TOUR_STAT_LINE:TOUR_END_LINE]:
            node_coord=j.rstrip("\n")
            route.append(int(node_coord)-1)
        g1=graph.Graph("input_point",input_data=node_list)
        result_.write(name+"\t")
        g1.route=route
        result_dic["opt"]=g1.cal()
        alg.farthest(g1)
        result_dic["farthest"]=g1.cal()
        alg.k_opt(3,g1)
        result_dic["k_opt"]=g1.cal()
        alg.cheapest(g1)
        result_dic["cheapest"]=g1.cal()
        alg.christofides(g1)
        result_dic["christofides"]=g1.cal()
        alg.nearest(g1)
        result_dic["nearest"]=g1.cal()
        alg.double_tree(g1)
        result_dic["DT"]=g1.cal()
        for i in result_dic:
            result_.write(i+"\t"+str(result_dic[i])+"\t"+str(result_dic[i]/result_dic["opt"]) + "\n")
        tfile_.close()
        sfile_.close()
    elif args.input_mode=="input_weight":
        with open('2dmatrix.data') as f:
            array = [int(x) for x in next(f).split()]  # read first line
            for line in f:  # read rest of lines
                array.append([float(x) for x in line.split()])
        k=len(array[-1])
        nparray=np.zeros((k,k))
        for i in range(k):
            for j in range(i):
                nparray[i,j]=array[i][j]
        g1=graph.Graph("input_weight",input_data=nparray)
        result_dic={"double_tree":0,"christofides":0,"greed":0,"cheapest":0,"nearest":0,"farthest":0,"k_opt":0}
        alg.double_tree(g1)
        result_dic["double_tree"]=g1.cal()
        alg.christofides(g1)
        result_dic["christofides"]=g1.cal()
        alg.greed(g1)
        result_dic["greed"]=g1.cal()
        alg.cheapest(g1)
        result_dic["cheapest"]=g1.cal()
        alg.nearest(g1)
        result_dic["nearest"]=g1.cal()
        alg.farthest(g1)
        result_dic["farthest"]=g1.cal()
        alg.k_opt(3,g1)
        result_dic["k_opt"]=g1.cal()
        for i in result_dic:
            result_.write(i+"\t"+str(result_dic[i])+"\n")

        sfile_name="data/pa561.opt.tour"
        sfile_ = open(sfile_name, "r")
        sfile=sfile_.readlines()
        route = []
        for j in sfile[5:-2]:
            node_coord=j.rstrip("\n")
            route.append(int(node_coord)-1)
        g1.route=route
        opt=g1.cal()
        for i in result_dic:
            result_.write(i+"\t"+str(result_dic[i])+"\t"+str(result_dic[i]/opt)+"\n")

    elif args.input_mode=="input_point":
        with open('coordinates.data') as f:
            w, h = [int(x) for x in next(f).split()]  # read first line
            node_list = []
            for line in f:  # read rest of lines
                node_list.append((float(x) for x in line.split()))
        g1=graph.Graph("input_point",input_data=node_list)
        result_dic={"double_tree":0,"christofides":0,"greed":0,"cheapest":0,"nearest":0,"farthest":0,"k_opt":0}
        alg.double_tree(g1)
        result_dic["double_tree"]=g1.cal()
        alg.christofides(g1)
        result_dic["christofides"]=g1.cal()
        alg.greed(g1)
        result_dic["greed"]=g1.cal()
        alg.cheapest(g1)
        result_dic["cheapest"]=g1.cal()
        alg.nearest(g1)
        result_dic["nearest"]=g1.cal()
        alg.farthest(g1)
        result_dic["farthest"]=g1.cal()
        alg.k_opt(3,g1)
        result_dic["k_opt"]=g1.cal()
        for i in result_dic:
            result_.write(i+"\t"+str(result_dic[i])+"\n")



    elif args.input_mode=="random": #in random generating, there is only so-called
        n_test = 100
        cum_result_dic={"double_tree":0,"christofides":0,"greed":0,"cheapest":0,"nearest":0,"farthest":0,"k_opt":0}
        for i in range(n_test):
            g1=graph.Graph('random', args.node_min, args.node_max)
            alg.double_tree(g1)
            cum_result_dic["double_tree"]+=g1.cal()
            alg.christofides(g1)
            cum_result_dic["christofides"]+=g1.cal()
            alg.greed(g1)
            cum_result_dic["greed"]+=g1.cal()
            alg.cheapest(g1)
            cum_result_dic["cheapest"]+=g1.cal()
            alg.nearest(g1)
            cum_result_dic["nearest"]+=g1.cal()
            alg.farthest(g1)
            cum_result_dic["farthest"]+=g1.cal()
            alg.k_opt(3,g1)
            cum_result_dic["k_opt"]+=g1.cal()
        for i in cum_result_dic:
            result_.write(i+"\t"+str(cum_result_dic[i]/1000)+"\n")
    else:
        exit(0)

    result_.close()

if __name__ == "__main__":
    main()
