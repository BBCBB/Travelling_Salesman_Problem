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
        
solution=[0]            #creating an initial route based on a greedy algorithm
for i in solution:
    l=float("Inf") 
    for j in range(1,nodeCount):
        if j in solution:
            continue
        else:
            s=abs(points[i].x-points[j].x)+abs(points[i].y-points[j].y)
            l=min(l,s)
            if l==s:
                ngbr=j
    solution.append(ngbr)
    if len(solution)==nodeCount:
        break
solution.append(0)
maxiter=5000
o=[]
sol=solution.copy()
for i in range(maxiter):
    iter=i+1
    objval=obj(solution)
    o.append(objval)
    if sum(o[len(o)-250:len(o)])/250==objval:
        break
    
    tbc3opt=sorted(random.sample(range(1, nodeCount+1), 3))
    ind1=tbc3opt[0]
    ind2=tbc3opt[1]
    ind3=tbc3opt[2]
    inds=sorted([ind1,ind2,ind3])
    
    if inds[2]-inds[0]==2:
        b=solution.copy()
        a=b.pop(inds[0])
        b.insert(inds[1],a)
        if obj(b)<objval:
            a=solution.pop(inds[0])
            solution.insert(inds[1],a)
        
        
    elif inds[2]-inds[1]!=1 and inds[1]-inds[0]==1:
        b=solution.copy()
        c=solution.copy()
        a=b.pop(inds[0])
        b.insert(inds[2]-1,a)
        ob=obj(b)
        c[inds[0]:inds[2]]=c[inds[2]-1:inds[0]-1:-1]
        oc=obj(c)
        op=[ob,oc]
        if min(op)<objval:
            if obj(b)>obj(c):
               solution[inds[0]:inds[2]]=solution[inds[2]-1:inds[0]-1:-1]
            else:
               a=solution.pop(inds[0])
               solution.insert(inds[2]-1,a)
           
           
    elif inds[2]-inds[1]==1 and inds[1]-inds[0]!=1:
        b=solution.copy()
        a=b.pop(inds[1])
        b.insert(inds[1],a)
        ob=obj(b)
        c=solution.copy()
        c[inds[0]:inds[1]]=c[inds[1]-1:inds[0]-1:-1]
        oc=obj(c)
        d=solution.copy()
        d[inds[0]:inds[2]]=d[inds[2]-1:inds[0]-1:-1]
        od=obj(d)
        op=[ob,oc,od]
        if min(op)<=objval:
            if min(op) == od:
               solution[inds[0]:inds[2]]=solution[inds[2]-1:inds[0]-1:-1] 
            elif min(op) == oc:
               solution[inds[0]:inds[1]]=solution[inds[1]-1:inds[0]-1:-1]
            else:
                a=solution.pop(inds[1])
                solution.insert(inds[1],a)
    else:
            b=solution.copy()
            b[inds[0]:inds[2]]=b[inds[2]-1:inds[0]-1:-1]
            ob=obj(b)
            
            c=solution.copy()
            c[inds[1]:inds[2]]=c[inds[2]-1:inds[1]-1:-1]
            a=c[inds[0]:inds[1]].copy()
            del c[inds[0]:inds[1]]
            c[inds[0]+inds[2]-inds[1]:inds[0]+inds[2]-inds[1]]=a
            oc=obj(c)
            
        
            d=solution.copy()    
            d[inds[0]:inds[1]]=d[inds[1]-1:inds[0]-1:-1]
            d[inds[1]:inds[2]]=d[inds[2]-1:inds[1]-1:-1]
            od=obj(d)
            
            
            e=solution.copy()
            e[inds[0]:inds[1]]=e[inds[1]-1:inds[0]-1:-1]
            oe=obj(e)
            
        
            f=solution.copy()
            f[inds[1]:inds[2]]=f[inds[2]-1:inds[1]-1:-1]
            of=obj(f)
            
       
            g=solution.copy()
            a=g[inds[0]:inds[1]].copy()
            del g[inds[0]:inds[1]]
            g[inds[0]+inds[2]-inds[1]:inds[0]+inds[2]-inds[1]]=a
            og=obj(g)
            
        
            h=solution.copy()
            h[inds[0]:inds[1]]=h[inds[1]-1:inds[0]-1:-1]
            a=h[inds[0]:inds[1]].copy()
            del h[inds[0]:inds[1]]
            h[inds[0]+inds[2]-inds[1]:inds[0]+inds[2]-inds[1]]=a
            oh=obj(h)
            
            
            op=[ob,oc,od,oe,of,og,oh]
            if min(op)<objval:
                if min(op)==ob:
                   solution[inds[0]:inds[2]]=solution[inds[2]-1:inds[0]-1:-1]
                elif min(op)==oc:
                   solution[inds[1]:inds[2]]=solution[inds[2]-1:inds[1]-1:-1]
                   a=solution[inds[0]:inds[1]].copy()
                   del solution[inds[0]:inds[1]]
                   solution[inds[0]+inds[2]-inds[1]:inds[0]+inds[2]-inds[1]]=a
                elif min(op)==od:
                    solution[inds[0]:inds[1]]=solution[inds[1]-1:inds[0]-1:-1]
                    solution[inds[1]:inds[2]]=solution[inds[2]-1:inds[1]-1:-1]
                elif min(op)==oe:
                    solution[inds[0]:inds[1]]=solution[inds[1]-1:inds[0]-1:-1]
                elif min(op)==of:
                    solution[inds[1]:inds[2]]=solution[inds[2]-1:inds[1]-1:-1]
                elif min(op)==og:
                    a=solution[inds[0]:inds[1]].copy()
                    del solution[inds[0]:inds[1]]
                    solution[inds[0]+inds[2]-inds[1]:inds[0]+inds[2]-inds[1]]=a
                else:
                    solution[inds[0]:inds[1]]=solution[inds[1]-1:inds[0]-1:-1]
                    a=solution[inds[0]:inds[1]].copy()
                    del solution[inds[0]:inds[1]]
                    solution[inds[0]+inds[2]-inds[1]:inds[0]+inds[2]-inds[1]]=a
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
