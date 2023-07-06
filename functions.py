## Defining some functions that are useful for netwrork analysis and visualization

import networkx as nx
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from pyvis.network import Network

def draw(G, pos, measures, measure_name):
    if type(measures) is list:
        sizes = np.fromiter(measures, float)
    else:
        sizes = np.fromiter(measures.values(), float)
    colormap = mpl.cm.viridis
    normalize = mpl.colors.Normalize(vmin=sizes.min(), vmax=sizes.max())

    mappable = mpl.cm.ScalarMappable(cmap=colormap, norm=normalize)
    mappable.set_array(sizes)

    nx.draw(G, pos, with_labels=True, node_color=sizes, node_size=sizes*1e3/sizes.max(), cmap=colormap)
    plt.colorbar(mappable, ax=plt.gca())
    plt.title(measure_name)

def saveGraph(G, pos, measures, measure_name):
    sizes = np.fromiter(measures.values(), float)
    colormap = mpl.cm.get_cmap('viridis')
    normalize = mpl.colors.Normalize(vmin=sizes.min(), vmax=sizes.max())

    #Label nodes by measure
    counter = 0
    for n in G.nodes(data=True):
        n[1]['title']= "%.3f" % sizes[counter]
        n[1]['color'] = colormap(sizes[counter]/sizes.max())
        counter += 1

    #Visualize the network
    net = Network(notebook=True,height='800px', width='100%', select_menu=True, cdn_resources='remote')#, select_menu=True, filter_menu=True)
    net.from_nx(G)
    # net.save_graph("output/model-network-"+measure_name+".html")
    net.show("output/model-network-"+measure_name+".html")

def shapleyGame1(G: nx.Graph) -> list[float]:
    sv = []
    for i in range(1, len(G.nodes)+1):
        sv.append(1/(1+G.degree[i]))
        for j in range(0, len(G.nodes)):
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