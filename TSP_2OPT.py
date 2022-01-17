import random
import math
from collections import namedtuple
import networkx as nx
import matplotlib.pyplot as plt
Point = namedtuple("Point", ['x', 'y'])
def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

f = open(r"C:\\Users\data\data_file","r")

input_data = ''.join(f.readlines())
lines = input_data.split('\n')

nodeCount = int(lines[0])

points = []
for i in range(1, nodeCount+1):
    line = lines[i]
    parts = line.split()
    points.append(Point(float(parts[0]), float(parts[1])))
    
def obj(s):
    objective=0
    for j in range(nodeCount):
        objective = objective + length(points[s[j]],points[s[j+1]])
    return objective
        
solution=list(range(1,nodeCount))
random.shuffle(solution)
solution.insert(0,0)
solution.append(0)
maxiter=15000
o=[]
sol=solution.copy()
for i in range(maxiter):
    iter=i+1
    objval=obj(solution)
    o.append(objval)
    if sum(o[len(o)-250:len(o)])/250==objval:
        break
    
    tbc2opt=sorted(random.sample(range(1, nodeCount+1), 2))
    ind1=tbc2opt[0]
    ind2=tbc2opt[1]
    inds=sorted([ind1,ind2])
    if inds[1]-inds[0]==1:
        a=solution.pop(inds[0])
        solution.insert(inds[1],a)
    else:
        solution[inds[0]:inds[1]]=solution[inds[1]-1:inds[0]-1:-1]
               
    if obj(sol)<obj(solution):
       solution=sol.copy()
    else:
       sol=solution.copy()
print('Objective function value: {}',format(obj(solution)))
print('The optimal sequence of the nodes: {}',format(solution))
#plot
G=nx.DiGraph()
nodes=range(nodeCount)
G.add_nodes_from(nodes)
edges=[]
for i in range(nodeCount):
    edges.append((solution[i],solution[i+1]))
G.add_edges_from(edges)
pos = {}
for i in range(len(nodes)):
    pos[i]=[]
for i in range(len(nodes)):
    pos[i].append(points[i][0])
    pos[i].append(points[i][1])
fig, ax = plt.subplots(figsize=(6, 6))
nx.draw_networkx_nodes(G,pos,node_size=55,node_color='yellow',ax=ax)
nx.draw_networkx_edges(G,pos, width=0.4,edge_color='black')
nx.draw_networkx_labels(G,pos,font_size=8)
ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
