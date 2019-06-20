import graph


"""
Contains the definition of the algorithms
"""




class Algorithm:
    def __init__(self,model,lr,bs,n_step,env_name,node_max):
        pass
    
    #these are the algorithms for any metric graph (satisfies triangular inequality)

    def double_tree(self): #double tree method, factor=2
        pass

    def christofides(self): #christofides method, factor=3/2
        pass

    def k_opt(self,k): #n-opt method, factor=1+n^(1/2k)/4
        pass
        
    #these are the algorithm for any Euclid graph (can be embedded in an Euclidian plane, thus satisfies tri.inequality)
    def greed(self): #greed method, factor=log(2,n)/2+1/2
        pass
    def nearest(self): #nearest method, factor=2
        pass
    def cheapest(self): #cheapest method, factor=2
        pass
    def farthest(self): #farthest method, factor=log(2,n)+0.16
        pass
    

