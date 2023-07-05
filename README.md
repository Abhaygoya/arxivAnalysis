# Arxiv Analysis

Looking into doing some analysis of arxiv papers using the dataset made available by kaggle. To run this code, you'll need to download the dataset here: https://www.kaggle.com/datasets/Cornell-University/arxiv

Building from a notebook created by Fred Navruzov and shared on Kaggle: https://www.kaggle.com/code/frednavruzov/arxiv-exploring-spatial-structure/notebook#Produce-Graph-visualizations-(no-ML)

This will start with exploratory analysis of the network structure and build from there. The goal is to learn more network analysis tools through application to an interesting dataset.

Another notebook on coauthor network analysis for astrophysics: https://www.kaggle.com/code/jacowu/astrophysics-network-analysis-arxiv

After some preliminary work, it became clear that a simplified model system would be useful to build out some intuition for the different measures of centrality. The modelNetwork notebook builds and analyzes a simple network of 13 nodes. Computing different measures of centrality shows how each identifies different features of the graph. Will be using this as a testing ground for code to compute shapley value centrality.