## Defining some functions that are useful for netwrork analysis and visualization

import networkx as nx
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from pyvis.network import Network

def draw(G, pos, measures, measure_name):
    if type(measures) is list:
        sizes = np.fromiter(measures, float)
    elif type(measures) is np.ndarray:
        sizes = measures
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

def createZachary():
    G = nx.karate_club_graph()
    pos = nx.spring_layout(G)
    return G, pos