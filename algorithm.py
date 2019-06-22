import graph


"""
Contains the definition of the algorithms
"""

class Algorithm:
    def __init__(self):
        pass

    #these are the algorithms for any metric graph (satisfies triangular inequality)

    def double_tree(self, graph): #double tree method, factor=2
        T = graph.min_tree()
        MG = graph.add(T, T)
        er = graph.min_euler(MG)
        route=[]
        for i in er:
            if i[0] not in route:
                route.append(i[0])
        graph.route=route
        return route

    def christofides(self, graph): #christofides method, factor=3/2
        T = graph.min_tree()
        M = graph.min_weight_match_odd_nodes(T)
        GS = graph.add(T, M)
        er = graph.min_euler(GS)
        route=[]
        for i in er:
            if i[0] not in route:
                route.append(i[0])
        graph.route=route
        return route

    def greed(self, g): #greed method, factor=log(2,n)/2+1/2
        graph=g.graph
        n = graph.number_of_nodes()
        result = [0]
        for i in range(n-1):
            k=g.nearest(result[-1], exclude=result)
            result.append(k[1])
        return result

    def k_opt(self, k, g, route=None): #n-opt method, factor=1+n^(1/2k)/4   local optimization needs initialize
        graph=g.graph
        if route is None:
            route = self.greed(g)
        n = len(route)
        route1 = [None] * n
        if k not in [2,3]:
            print("only supporting 2(or 3)-opt")
            return
        flag2=False
        while(1):
            flag=False
            if k == 2:
                for i in range(n):
                    flag1=False
                    for j in range(i-1):
                        if ((i-j+n) % n) in [n-1, 0, 1]:
                            continue
                        value1 = graph[route[i]][route[(i+1)%n]]["weight"] + graph[route[j]][route[(j+1)%n]]["weight"]
                        value2 = graph[route[i]][route[j]]["weight"] + graph[route[(i+1)%n]][route[(j+1)%n]]["weight"]
                        if value2 < value1:
                            for i_ in range(i-j):
                                route1[i_] = route[i_+j+1]
                            for i_ in range(n+j-i):
                                route1[i_+i-j] = route[(j+n-i_)%n]
                            route = route1.copy()
                            flag1=True
                            flag=True
                            break
                    if flag1:
                        break
                if not flag:
                    break
            elif k == 3:
                route = self.k_opt(k-1, g)# k-1 opt first!
                for i in range(n):
                    for j in range(i-1):
                        flag2=False
                        for m in range(j-1):
                            if ((i-j+n) % n) in [n-1, 0, 1]:
                                continue
                            if ((j-m+n) % n) in [n-1, 0, 1]:
                                continue
                            if ((i-m+n) % n) in [n-1, 0, 1]:
                                continue
                            value1 = graph[route[i]][route[(i + 1) % n]]["weight"] + graph[route[j]][route[(j + 1) % n]]["weight"] + graph[route[m]][route[(m + 1) % n]]["weight"]
                            value2 = graph[route[i]][route[(m + 1) % n]]["weight"] + graph[route[(i + 1) % n]][route[(j + 1) % n]]["weight"] + graph[route[m]][route[j]]["weight"]
                            value3 = graph[route[i]][route[(m + 1) % n]]["weight"] + graph[route[(i + 1) % n]][route[j]]["weight"] + graph[route[m]][route[(j + 1) % n]]["weight"]
                            value4 = graph[route[i]][route[m]]["weight"] + graph[route[(i + 1) % n]][route[j]]["weight"] + graph[route[(m + 1) % n]][route[(j + 1) % n]]["weight"]
                            value5 = graph[route[i]][route[j]]["weight"] + graph[route[(i + 1) % n]][route[(m + 1) % n]]["weight"] + graph[route[m]][route[(j + 1) % n]]["weight"]
                            min_v = min([value1, value2, value3,value4,value5])
                            if min_v == value1:
                                continue
                            elif min_v == value2:
                                for i_ in range(i-j):
                                    route1[i_] = route[i_+j+1]
                                for i_ in range(j-m):
                                    route1[i_+i-j] = route[i_+m+1]
                                for i_ in range(n+m-i):
                                    route1[i_+i-m] = route[(-i_+m+n)%n]
                                route = route1.copy()
                                flag2=True
                                flag=True
                                break
                            elif min_v == value3:
                                for i_ in range(i-j):
                                    route1[i_] = route[i_+j+1]
                                for i_ in range(j-m):
                                    route1[i_+i-j] = route[i_+m+1]
                                for i_ in range(n+m-i):
                                    route1[i_+i-m] = route[(i_+i+1)%n]
                                route = route1.copy()
                                flag2=True
                                flag=True
                                break
                            elif min_v == value4:
                                for i_ in range(i-j):
                                    route1[i_] = route[-i_+i]
                                for i_ in range(j-m):
                                    route1[i_+i-j] = route[m+i_+1]
                                for i_ in range(n+m-i):
                                    route1[i_+i-m] = route[(i_+i+1)%n]
                                route = route1.copy()
                                flag2=True
                                flag=True
                                break
                            elif min_v == value5:
                                for i_ in range(j-m):
                                    route1[i_] = route[m+i_+1]
                                for i_ in range(i-j):
                                    route1[i_+i-j] = route[i-i_]
                                for i_ in range(n+m-i):
                                    route1[i_+i-m] = route[(-i_+m+n)%n]
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

    def nearest(self, g): #nearest method, factor=2
        graph=g.graph
        nlist=[0]
        nlist.append(g.nearest(nlist[0],exclude=nlist)[1])
        nodes=graph.number_of_nodes()
        while len(nlist)<nodes:
            x0=float("inf")
            for r in nlist:
                (x, index) = g.nearest(r, exclude=nlist)
                if x < x0:
                    x0 = x
                    index0 = index
            s0=float("inf")
            nelem=len(nlist)
            for t in range(nelem):
                s = g.savings(nlist[t], nlist[(t+1)%nelem], index0)
                if s < s0:
                    s0 = s
                    ind_s = t
            nlist.insert((ind_s+1)%nelem, index0) # default inserts BEFORE the elem, here modified to AFTER the elem
        return nlist

    def cheapest(self, g): #cheapest method, factor=2
        graph=g.graph
        nlist=[0]
        nlist.append(g.nearest(nlist[0],exclude=nlist)[1])
        nodes=graph.number_of_nodes()
        while len(nlist) < nodes:
            cost_min=float("inf")
            nelem=len(nlist)
            for n2 in range(nodes):
                if n2 in nlist:
                    continue
                for i in range(nelem):
                    cost = g.savings(nlist[i], nlist[(i+1)%nelem],n2)
                    if cost < cost_min:
                        cost_min=cost
                        indices=[i,n2]
            nlist.insert((indices[0]+1)%nelem, indices[1])
        return nlist

    def farthest(self, g): #farthest method, factor=log(2,n)+0.16
        graph=g.graph
        nlist=[0]
        nlist.append(g.farthest(nlist[0],exclude=nlist)[1])
        nodes=graph.number_of_nodes()
        while len(nlist)<nodes:
            x0=float("-inf")
            for r in nlist:
                (x, index) = g.farthest(r, exclude=nlist)
                if x > x0:
                    x0 = x
                    index0 = index
            s0=float("inf")
            nelem=len(nlist)
            for t in range(nelem):
                s = g.savings(nlist[t], nlist[(t+1)%nelem], index0)
                if s < s0:
                    s0 = s
                    ind_s = t
            nlist.insert((ind_s+1)%nelem, index0)
        return nlist


