
import networkx as nx
import numpy as np
import queue


def shapleyGame1(G: nx.Graph) -> list[float]:
    sv = []
    for i in range(1, len(G.nodes)+1):
            sv.append(1/(1+G.degree[i]))
            for j in range(1, len(G.nodes)+1):
                if i != j:
                    if G.has_edge(i,j):
                        sv[i-1] += 1/(1+G.degree[j])
    return sv

def shapleyGame2(G: nx.Graph, k: int) -> list[float]:
    sv = []
    for i in range(1, len(G.nodes)+1):
        sv.append(min(1,k/(1+G.degree[i])))
        for j in range(0, len(G.nodes)):
            if i != j:
                if G.has_edge(i,j):
                    sv[i-1] += max(0,(G.degree[j]-k+1)/(G.degree[j]*(1+G.degree[j])))
    return sv

#Input - G: networkX graph
#Output - cSh: array of ShapelyBetweeness of each node
def ShapelyBetweeness(G):
    #Distance between nodes
    d = np.zeros((G.number_of_nodes(), G.number_of_nodes()))
    #list of predecessors on all node pairs
    Pred_s = [[] for i in range(G.number_of_nodes()) ]
    #Length of shortest path on each pair
    sigma = np.zeros((G.number_of_nodes(), G.number_of_nodes()))
    #One-side dependency of source node on target node
    delta = np.zeros((G.number_of_nodes(), G.number_of_nodes()))
    cSh = np.zeros(G.number_of_nodes()) 
    #Sructs
    Q = queue.Queue()
    S = []
    #Create node list
    nodes = []
    for n in G.nodes.data():
        nodes.append(n[0])
    for s in range(0, G.number_of_nodes()):
        for v in range(0, G.number_of_nodes()):
            Pred_s[v] = []; d[s,v] = float("inf") ;sigma[s,v] = 0
        d[s,s] = 1; sigma[s,s] = 1;  
        Q.put(s)
        while Q.empty() == False:
            v = Q.get()
            S.append(v)
            w = list(G.edges(nodes[v], data=True))
            for i in range(0,len(w)):
                if d[s, nodes.index(w[i][1])] == float("inf"):
                    d[s, nodes.index(w[i][1])] = d[s, v] + 1
                    Q.put(nodes.index(w[i][1]))
                if d[s, nodes.index(w[i][1])] == d[s, v] + 1:
                    sigma[s,nodes.index(w[i][1])] += sigma[s,v]
                    Pred_s[nodes.index(w[i][1])].append(v)

    for v in range(0, G.number_of_nodes()-1):
        delta[s,v] = 0

    while len(S) > 0:
        w = S.pop()
        for v in Pred_s[w]:
            delta[s,v] += (sigma[s,v]/sigma[s,w])*(1/d[s,w] + delta[s,w])
        if w != s:
            cSh[w] += delta[s,w] + (2-d[s,w])/d[s,w]

    for v in range(0, G.number_of_nodes()):
        cSh[v] = cSh[v]/2

    return cSh