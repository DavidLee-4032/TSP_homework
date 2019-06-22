import graph as g


"""
Contains the definition of the algorithms
"""

class Algorithm:
    def __init__(self, graph):
        self.graph = graph
        pass
    
    #these are the algorithms for any metric graph (satisfies triangular inequality)

    def double_tree(self, graph): #double tree method, factor=2
        T = self.graph.min_tree()
        MG = self.graph.add(T, T)
        er = self.graph.min_euler(MG)
        #deleting multi-occurrence(creating new list)
        pass

    def christofides(self, graph): #christofides method, factor=3/2
        T = self.graph.min_tree()
        M = self.graph.min_weight_match_odd_nodes(T)
        GS = self.graph.add(T, M)
        E = self.graph.min_euler(GS)
        return E

        
    def greed(self, graph): #greed method, factor=log(2,n)/2+1/2
        n = graph.number_of_nodes()
        nlist = list(range(n))
        result = [None]*n
        index = -1
        
        for i in range(n):
            x = float("inf")
            for j in nlist:
                if graph[i][j]["weight"] < x:
                    x = graph[i][j]["weight"]
                    index = i
            nlist.remove(index)
            result[i] = index
        return result

    def k_opt(self, k, graph, route): #n-opt method, factor=1+n^(1/2k)/4   local optimization needs initialize
        if route == None:
            route = self.greed(self.graph)
        n = route.len()
        route1 = [None] * n
        if k not in [2,3]:
            print("only supporting 2(or 3)-opt")
            return
        while(1):
            flag=False
            if k == 2:
                for i in range(n):
                    flag1=False
                    for j in range(i-1):
                        if (i-j+n) % n in [n-1, 0, 1]:
                            continue
                        value1 = graph[i][(i + 1) % n]["weight"] + graph[j][(j + 1) % n]["weight"]
                        value2 = graph[i][j]["weight"] + graph[(i + 1) % n][(j + 1) % n]["weight"]
                        if value2 < value1:
                            for i_ in range(i-j):
                                route1[i_] = route[i_+j+1]
                            for i_ in range(n+j-i):
                                route1[i_-i+j] = route[(j+n-i_)%n]
                            route = route1.copy()
                            flag1=True
                            flag=True
                            break
                    if flag1:
                        break
                if not flag:
                    break
            elif k == 3:
                route = self.k_opt(k-1, graph, route)# k-1 opt first!
                for i in range(n):
                    for j in range(i-1):
                        flag2=False
                        for k in range(j-1):
                            if (i-j+n) % n in [n-1, 0, 1]:
                                continue
                            if (j-k+n) % n in [n-1, 0, 1]:
                                continue
                            if (i-k+n) % n in [n-1, 0, 1]:
                                continue
                            value1 = graph[i][(i + 1) % n]["weight"] + graph[j][(j + 1) % n]["weight"] + graph[k][(k + 1) % n]["weight"]
                            value2 = graph[i][(k + 1) % n]["weight"] + graph[(i + 1) % n][(j + 1) % n]["weight"] + graph[k][j]["weight"]
                            value3 = graph[i][(k + 1) % n]["weight"] + graph[(i + 1) % n][j]["weight"] + graph[k][(j + 1) % n]["weight"]
                            value4 = graph[i][k]["weight"] + graph[(i + 1) % n][j]["weight"] + graph[(k + 1) % n][(j + 1) % n]["weight"]
                            value5 = graph[i][j]["weight"] + graph[(i + 1) % n][(k + 1) % n]["weight"] + graph[k][(j + 1) % n]["weight"]
                            min_v = min([value1, value2, value3,value4,value5])
                            if min_v == value1:
                                continue
                            elif min_v == value2:
                                for i_ in range(i-j):
                                    route1[i_] = route[i_+j+1]
                                for i_ in range(j-k):
                                    route1[i_+j-i] = route[i_+k+1]
                                for i_ in range(n+k-i):
                                    route1[i_+i-k] = route[(-i_+k+n)%n]
                                route = route1.copy()
                                flag2=True
                                flag=True
                                break
                            elif min_v == value3:
                                for i_ in range(i-j):
                                    route1[i_] = route[i_+j+1]
                                for i_ in range(j-k):
                                    route1[i_+j-i] = route[i_+k+1]
                                for i_ in range(n+k-i):
                                    route1[i_+i-k] = route[(i_+i+1)%n]
                                route = route1.copy()
                                flag2=True
                                flag=True
                                break
                            elif min_v == value4:
                                for i_ in range(i-j):
                                    route1[i_] = route[-i_+i]
                                for i_ in range(j-k):
                                    route1[i_+j-i] = route[k+i_+1]
                                for i_ in range(n+k-i):
                                    route1[i_+i-k] = route[(i_+i+1)%n]
                                route = route1.copy()
                                flag2=True
                                flag=True
                                break
                            elif min_v == value5:
                                for i_ in range(j-k):
                                    route1[i_] = route[k+i_+1]
                                for i_ in range(i-j):
                                    route1[i_+j-i] = route[i-i_]
                                for i_ in range(n+k-i):
                                    route1[i_+i-k] = route[(-i_+k+n)%n]
                                route = route1.copy()
                                flag2=True
                                flag=True
                                break
                        if flag2:
                            break
                    if flag2:
                        break
                if not flag:
                    break
        return route
    
    #these are the algorithm for any Euclid graph (can be embedded in an Euclidian plane, thus satisfies tri.inequality)

    def nearest(self, graph): #nearest method, factor=2
        nlist=[]
        nlist.append(0)
        nlist.append(graph.nearest(nlist[0])[1])
        nodes=graph.number_of_nodes()
        while len(nlist)<nodes:
            x0=float("inf")
            for r in nlist:
                (x, index) = graph.nearest(r, exclude=nlist)
                if x < x0:
                    x0 = x
                    index0 = index
            s0=float("inf")
            nelem=len(nlist)
            for t in range(nelem):
                s = graph.savings(nlist[t], nlist[(t+1)%nelem], index0)
                if s < s0:
                    s0 = s
                    ind_s = t
            nlist.insert((ind_s+1)%nelem, index0) # default inserts BEFORE the elem, here modified to AFTER the elem
        return nlist
    def cheapest(self, graph): #cheapest method, factor=2
        nlist=[]
        nlist.append(0)
        nlist.append(graph.nearest(nlist[0])[1])
        nodes=graph.number_of_nodes()
        #cost = [None]*nodes
        while len(nlist)<nodes:
            cost_min=float("inf")
            nelem=len(nlist)
            for n2 in range(n):
                if n2 in nlist:
                    continue
                for i in range(nelem):
                    cost = graph.savings(nlist[i], nlist[(i+1)%nelem],n2)
                    if cost_min<cost:
                        cost_min=cost
                        indices=[i,n2]
            nlist.insert((indices[1]+1)%nelem, indices[2])
        return nlist
    def farthest(self, graph): #farthest method, factor=log(2,n)+0.16
        nlist=[]
        nlist.append(0)
        nlist.append(graph.farthest(nlist[0])[1])
        nodes=graph.number_of_nodes()
        while len(nlist)<nodes:
            x0=float("-inf")
            for r in nlist:
                (x, index) = graph.farthest(r, exclude=nlist)
                if x > x0:
                    x0 = x
                    index0 = index
            s0=float("inf")
            nelem=len(nlist)
            for t in range(nelem):
                s = graph.savings(nlist[t], nlist[(t+1)%nelem], index0)
                if s < s0:
                    s0 = s
                    ind_s = t
            nlist.insert((ind_s+1)%nelem, index0)
        return nlist
    

