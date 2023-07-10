# Network analysis

## Centrality

Centrality is a term used to describe the importance of nodes in a network. The most important nodes being those towards the center, which peripheral nodes interact through. However, in a quantitative sense, this is not well-defined. There are many approaches/methods for calculating centrality, which are relevant in different cases. 

Examples:
* Betweenness centrality
* Degree centrality
* Eigenvector centrality
* Percolation centrality
* Pagerank centrality
* Game-theoretic centrality: https://arxiv.org/abs/1402.0567

Side note: came across this in the context of game theory. It's a way of ranking the power that different coalitions wield in a vote-based system.
Shapley-Shubik power index
https://en.wikipedia.org/wiki/Shapley%E2%80%93Shubik_power_index

### Degree centrality

Possibly the simplest measure of centrality, degree centrality is simply defined as the degree of a node. I.e. the centrality of node $i$ is the number of nodes directly connected to $i$. Usually, this is normalized by the number of other nodes in the network ($N-1$), so it is represented as a fraction of all possible connections.

### Betweenness centrality

Another relatively straightforward algorithm, this simply looks at each pair of vertices in the network and determines the shortest path between said vertices (where shortest means fewest edges). The centrality of a node $i$ is the number of shortest paths in the network that pass through $i$. Mathematically, 

$$C(i) = \sum_{a\neq i \neq b} \dfrac{ \sigma_{ab}(i)}{\sigma_{ab}}$$

where $\sigma_{ab}$ is the number of shortest paths between $a$ and $b$, while $\sigma_{ab}(i)$ is the number of shortest paths containing node $i$. 

### Closeness centrality

Closeness is determined from the average distance of node $i$ to all other nodes in the network (this is only well-defined for a connected graph). The closeness centrality is the reciprocal of that average. Formally,

$$ C(i) = \dfrac{N-1}{\sum_j d(i,j)} $$

where $N$ is the total number of nodes and $d(i,j)$ is the distance, i.e. number of edges, between nodes $i$ and $j$.

### Eigenvector centrality

While the metrics thus far are fairly intuitive in terms of what they say about a node, the eigenvector centrality is best understood in terms of the network as a whole. Let us define the adjacency matrix $A$ with vertices $a_{ij}=1$ if nodes $i$ and $j$ are neighbors, and $a_{ij}=0$ otherwise. Note $a_{ii}=0$ as nodes do not count themselves as neighbors. One can think of this as a linear transformation which, taking a vector $x$ that represents some set of nodes, returns the nodes which are adjacent to those. Given this matrix, consider all eigenvectors:

$$Ax = \lambda x$$

where $\lambda$ is a scalar. If we select the maximal eigenvalue, and let $x'$ be the associated eigenvector, we get the eigenvector centrality as

$$C(i) = x'_i$$

Intuitively, an eigenvector of $A$ is a selection of nodes that are well-connected with each other. Choosing the highest eigenvalue selects for the nodes of the highest degree that are also strongly connected to each other. In other words, nodes with high eigenvector centrality are those that are connected to many nodes with high eigenvector centrality.

This is an important metric upon which many famous algorithms, including Google's PageRank, are based.

## PageRank

Like eigenvector centrality, PageRank highlights nodes that are connected to other high-ranking nodes. In the context of websites, this means it measures links to a page (node) weighted by the ranking of the page that links to it. While the PageRank is designed for directed graphs, we can handle non-directed graphs by treating each edge as a bidirectional link.

### The basic algorithm

Formally, consider a network with $N$ nodes and $E$ edges connecting those nodes. For each node $i$ in the network, there are theoretical PageRank values $P_i$, and we can define the set $B_i \subset V$ that contains the nodes which link to node $i$. The PageRank values are such that for each node:

$$ P_i = \sum_{j \in B_i} \dfrac{P_j}{L_j} $$

where $L_j$ is the total number of links from node $j$. Thus far, the PageRank we have described is simply the eigenvector centrality (with adjacency matrix values $a_{ij}=1/L_j$ or $0$) for a directed graph. This can be solved for by simply starting with an arbirtrary ranking vector and iterating until convergence. 

However, there is an issue with this definition. Consider 2 nodes such that they each only link to each other, but are linked to by an outside source. Each iteration, some page rank gets transferred from the outside to these two nodes, but nothing is transferred out. This is a Rank Sink that will, every iteration, drain Rank from the rest of the system. Any such closed loop will cause issues with this definition of PageRank--leading to a meaningless ranking.

### The random surfer (walk)

The issue above is solved by the introduction of a damping factor $\alpha$. To understand this, let us think of the PageRank in the context of a random walk across the network (referred to as a random surfer in the context of webpages). If there were no sinks, the Rank would reflect the probability that an agent, clicking links at random, would end up at a specific node after a long time (long meaning that the result is independent of starting location).

Now clearly, the basic algorithm captures an important aspect of this: highly linked sites are ranked higher, with links from highly ranked sites weighted more than those from lower ranked sites. However, there are some mathematical idiosyncracies that don't necessarily align with the actual goal of the metric in practice. Rank sinks (and sources) for example, can lead to non-meaningful ranks due to the directed nature of the graph. 

This is where the damping factor $\alpha$ enters. Think of this as a chance for the surfer to pick a node independently from the links on their current node. In principle, their choice could follow any distribution, but in practice this is usually taken to be a uniform distribution over all existing nodes. Mathematically, the PageRank becomes:

$$ P_i = \frac{1-\alpha}{N} + \alpha \sum_{j \in B_i} \dfrac{P_j}{L_j} $$

This gives each node a baseline factor based on the total number of nodes, which is added to the value defined in the basic algorithm section above (scaled by the damping factor, so the total of all ranks still sums to 1). The damping factor is usually set to $\alpha=0.85$, but there are various reasons one might wish to change that.

## Shapley Values in Networks

All of the above measures quantify a single node's contribution to the overall network. Recently, there has been a realization that this is sometime insufficient. Nodes identified by the traditional metrics have a relatively large impact on their own, but these metrics fail to capture impact in groups. For example, consider the difference between a power network that loses a single node to one that undergoes simultaneous failure at multiple nodes. Traditional metrics are designed for the first case and can completely miss that a group of nodes is absolutely critical if the network can still function without any one of the group.

An approach to tackle this problem is by adapting [Shapley values](/1QA9sUt7ToqXG3C_MyHUtQ) to networks. The premise is that each node's value is determined by its marginal contributions to all possible coalitions of nodes. To compute Shapley Values in network systems, we need to first define some sort of coalitional game. Michalak et al have [a paper on Arxiv](https://arxiv.org/abs/1402.0567) that discusses several games that can be defined and efficient, exact algorithms to compute the Shapley Values corresponding to those games. These are all variations of degree and closeness centrality.

### Game 1

This is analogous to degree centrality, and originally proposed by [Suri and Narahari](https://dl.acm.org/doi/10.5555/1402821.1402911) in the context of determining the top-*k* nodes in social networks. For a graph $G(V,E)$ consider a coalition $C \subseteq V$. The fringe of $C$, denoted $F_C$, is defined as the set of vertices in $C$ or directly connected to it. Formally,

$$F_C =\{ v \in V (G) : v \in C \,{\rm or}\, \exists u \in C {\, \rm such\, that\,} (u, v) \in E(G)\} $$

The game is characterized by the value function $\nu_1={\rm size}(F_C)$. For this game, the Shapley Value of a node indicates average marginal contribution of that node to a coalition. In other words, how much does adding the node increase the size of $F_C$? 

#### Algorithm

There is a simple, exact formula for computing this Shapley value without having to iterate through all possible coalitions. See [Michalak et al](https://arxiv.org/abs/1402.0567) for the proof. 

$$ SV(v_i) = \sum_{v_j\in(\{v_i\} \cup N(v_i))} \frac{1}{1+deg(v_j)} $$

where $N(v_i)$ is the set of neighbors of node $v_i$ and $deg(v_j)$ is the degree of node $v_j$. Intuitively, a high $SV$ corresponds to a node with many neighbors of low degree. This feature indicates a high liklihood that adding the node to a coalition will substantially increase the size of the fringe.

### Game 2

This is a generalized version of the last game. Instead of the fringe containing all nodes with a connection to $C$, we only count nodes with at least $k$ connections to $C$. This introduces a new parameter $k$, and reduces to the Game 1 case if we set $k=1$. This seems like a metric that will be particularly useful for scenarios where there is a threshold of connectivity that is meaningful in some way (as a simple example, consider a network where exposure to $k$ nodes is required for transmission).

Given the extra condition, this calculation seems a bit more daunting. There are many conditionals based on the degree of a node and its existing connections. However, this can still be worked out to a simple algorithm.

> #### Algorithm for Game 2
>**Input**: Unweighted graph $G(V, E)$, positive integer $k$ 
>**Output**: Shapley value of all nodes in $V (G)$ for game $g_2$ 
>
>for $v_i \in V (G)$: 
>>$SV[v_i] = min(1, \frac{k}{1+deg(v_i)} )$ 
>>for $v_j \in N(v_i)$:
>>>$SV[v_i] += max(0, \frac{deg(v_j)−k+1}{ deg(v_j)(1+deg(v_j))} )$ 

A quick test for this is to verify that, with $k=1$, this returns the same Shapley Values as Game 1.

### Game 3

The third approach is one that works with weighted networks. Instead of simply looking at direct connections, we introduce a cutoff distance $d_{\rm cut}$. The distance between two nodes $D_{ij}$ is lowest sum of edge weights that connect $v_i$ to $v_j$. The extended neighborhood of $C$ is defined as the set of all nodes which are at most a distance of $d_{\rm cut}$ from a node in $C$. Formally, let the extended neighborhood of any node be:

$$N(v_i,d_{\rm cut}) = \{v_j \neq v_i: D_{ij} \leq d_{\rm cut}\} $$

The extended degree is then $deg(v_i,d_{\rm cut})=size(N(v_i,d_{\rm cut}))$. With these definitions, the Shapley Value can be calculated in almost exactly the same way as for Game 1, simply substituting degree and neighborhood with their extended versions.

$$SV(v_i) = \sum_{v_j\in(\{v_i\} \cup N(v_i,d_{\rm cut}))} \frac{1}{1+deg(v_j,d_{\rm cut})}$$

This allows for a "smarter" filtering of connections based on some weighted distance from a  coalition $C$ rather than just single edges. This can also be reduced to the first game by simply weighting all edges equally as $d_{\rm cut}$.

### Shapley Betweenness

The Shapley Value approach to centrality has also been extended to a version of betweenness. [A conference paper](https://eprints.soton.ac.uk/337181/1/aamas2011_sample_tm.pdf) by Szczepanski et al introduced this idea in 2012. This is refined further in their [recent paper](https://www.sciencedirect.com/science/article/pii/S0004370215001666). Their algorithm was implemented in python by Adam Price (https://gist.github.com/adamprice97/3bc20831cdb7f4a79955ad7014a4323c).