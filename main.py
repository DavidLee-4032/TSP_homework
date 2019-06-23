import argparse
import logging
import algorithm
import graph
import os
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
parser.add_argument('--node_min', type=int, metavar='nnode',default='70', help="Minimum number of nodes")
parser.add_argument('--node_max', type=int, metavar='nnode',default='100', help="Maximum number of nodes")
parser.add_argument('--input_mode', metavar='INPUT', default='random', help='Type of graph input (random, input_weight, input_point, files)')


def main():
    os.remove("result")
    os.mknod("result") #clear the result file
    result_=open("result","w")
    args = parser.parse_args()

    if args.input_mode=="files":
        result_.write("Instance\tOPT\tFarthest\t3-opt\tCheapest\tchristofides\tNearest\tDT\n")
        data_path="data/"
        file_list_=open("file_list.data","r")
        file_list=file_list_.readlines()
        FILE_NUM=31
        TSP_START_LINE=6
        TOUR_STAT_LINE=5
        TOUR_END_LINE=-2
        ratio_dic={"farthest":1,"k_opt":1,"cheapest":1,"christofides":1,"nearest":1,"DT":1}
        
        for i in range(FILE_NUM):
            node_list=[]
            route=[]
            name=file_list[i].rstrip("\n")
            tfile_name=data_path+name+".tsp"
            sfile_name=data_path+name+".opt.tour"
            tfile_=open(tfile_name,"r")
            sfile_=open(sfile_name,"r")
            tfile=tfile_.readlines()
            sfile=sfile_.readlines()
            result_dic={}
            
            for j in tfile[TSP_START_LINE:]:#
                node_coord=j.rstrip("\n").split(" ")
                node_list.append((float(node_coord[0]),float(node_coord[1])))
            for j in sfile[TOUR_STAT_LINE:TOUR_END_LINE]:
                node_coord=j.rstrip("\n")
                route.append(int(node_coord))
            g1=graph.Graph("input_point",0,0,node_list)
            result_.write(name+"\t")
            g1.route=route
            result_.write(str(g1.cal)+"\t")            
            result_dic["opt"]=g1.cal
            alg.farthest(g1)
            result_.write(str(g1.cal)+"\t")
            result_dic["farthest"]=g1.cal
            alg.k_opt(3,g1)
            result_.write(str(g1.cal)+"\t")
            result_dic["k_opt"]=g1.cal
            alg.cheapest(g1)
            result_.write(str(g1.cal)+"\t")
            result_dic["cheapest"]=g1.cal
            alg.christofides(g1)
            result_.write(str(g1.cal)+"\t")
            result_dic["christofides"]=g1.cal
            alg.nearest(g1)
            result_.write(str(g1.cal)+"\t")
            result_dic["nearest"]=g1.cal
            alg.double_tree(g1)
            result_.write(str(g1.cal)+"\t\n")
            result_dic["DT"]=g1.cal
            for i in ratio_dic:
                if result_dic[i]/result_dic["opt"]>ratio_dic[i]:
                    ratio_dic[i]=result_dic[i]/result_dic["opt"]

    elif args.input_mode=="input_weight":
        with open('2dmatrix.data') as f:
            w, h = [int(x) for x in next(f).split()]  # read first line
            array = []
            for line in f:  # read rest of lines
                array.append([float(x) for x in line.split()])
        pass
    elif args.input_mode=="input_point":

        pass
    elif args.input_mode=="random": #in random generating, there is only so-called
        n_test = 1000
        alg = algorithm.Algorithm()
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
