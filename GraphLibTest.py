import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import isomorphism

G1 = nx.path_graph(4)
G2 = nx.path_graph(4)
GM = isomorphism.GraphMatcher(G1, G2)
print(GM.is_isomorphic())

'''
G = nx.Graph()
G.add_edges_from([(1, 2), (1, 3)])
print(G.number_of_nodes())
print(G.number_of_edges())
#'''

nx.draw(G1, with_labels=True, font_weight='bold')
plt.show()
