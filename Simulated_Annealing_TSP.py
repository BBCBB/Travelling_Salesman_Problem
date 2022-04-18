
import random
import math
from collections import namedtuple
import networkx as nx
import matplotlib.pyplot as plt
import sys
import time
import numpy as np

Point = namedtuple("Point", ['x', 'y'])      # function for calculating the length between two points
def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

f = open(r"E:\Education\Discrete Optimization\HW4-TSP\data\tsp_100_1","r")

input_data = ''.join(f.readlines())
lines = input_data.split('\n')

nodeCount = int(lines[0])

points = []
for i in range(1, nodeCount+1):
    line = lines[i]
    parts = line.split()
    points.append(Point(float(parts[0]), float(parts[1])))
   
def obj(s):                               # OBJECTIVE VALUE
    objective=0
    for j in range(nodeCount):
        l= length(points[s[j]],points[s[j+1]])
        objective = objective + l
    return objective

def deltap(y,w,z,s):                        # a function to calculate the IMPROVEMENT or DETERIORATION ...
    imp=0                                   # ... in the Objective value based on each swap
    if w==0:
        imp=length(points[s[y-1]],points[s[y]])+length(points[s[z]],points[s[z+1]])  
    elif w==-1:
        imp=length(points[s[y-1]],points[s[y]])+length(points[s[z-1]],points[s[z]])  
    else:
        imp=length(points[s[y-1]],points[s[y]])+length(points[s[z-1]],points[s[z]])+\
            length(points[s[w-1]],points[s[w]])
    return imp   

Dist_mat=[[0 for i in range(nodeCount)] for i in range(nodeCount)]       #calculating Distance Matrix to reduce the search space when choosing an arc to swap randomly
for i in range(nodeCount):
    for j in range(i,nodeCount):
       Dist_mat[i][j]=abs(points[i].x-points[j].x)+abs(points[i].y-points[j].y)
       Dist_mat[j][i]=Dist_mat[i][j]

solution=[0]                                                             #Generating an initial solution   
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

solution.append(0)                                               # transforming the initial solution to a cycle
# determining different parameters based the size of the problem
if nodeCount<80:
    t=5                                                          # initial temperature of the system
    maxiter=500                                                  # number of different temperatures the system will experience
    m=400                                                        # number of iterations over a specific temperature
    trenew=1000                                                  # a threshold to warm up the system when the algorithm's stuck in a local optima
    cp=0.99                                                      # cooling parameter
    ngbr=0.25                                                    # the percentage of nodes close to a random node to be investigated to make a move (neighborhood)
elif nodeCount<150:
    t=20                                                         # initial temperature of the system
    maxiter=550                                                  # number of different temperatures the system will experience
    m=650
    trenew=1000
    cp=0.99
    ngbr=0.25
elif nodeCount<500:
    t=30                                                         # initial temperature of the system
    maxiter=600                                                  # number of different temperatures the system will experience
    m=700
    trenew=500
    cp=0.95
    ngbr=0.15
elif nodeCount<1000:
    t=20                                                         # initial temperature of the system
    maxiter=800                                                  # number of different temperatures the system will experience
    m=900
    trenew=2000
    cp=0.99
    ngbr=0.08
elif nodeCount<2000:
    t=20                                                         # initial temperature of the system
    maxiter=900                                                  # number of different temperatures the system will experience
    m=1000
    trenew=3000
    cp=0.99
    ngbr=0.06
else:
    t=20                                                        # initial temperature of the system
    maxiter=800                                                  # number of different temperatures the system will experience
    m=1000
    trenew=4000
    cp=0.99
    ngbr=0.04
t0=t
temprec=[]
start_time = time.time()                        # Establishing the start time to calculate the run time
objval=obj(solution)                            # calcuclating the objective function based on the initial solution
bestval=objval                                  # determining an initial value for the best objective value achieved so far
bestsol=solution.copy()                         # determining an initial value for the best solution achieved so far
objrec=[]                                       # storing a record of all objective values obtained through the algorithm
counter=0
for iteration in range(1,maxiter+1):
    for j in range(m):
        objrec.append(objval)
    #------------------------------   2 OPT   -------------------------------------   
        ind1=random.randint(1,nodeCount)
        num=solution[ind1-1]
        order_sel=Dist_mat[num]
        order=sorted(range(len(order_sel)), key=lambda k: order_sel[k])
        
        ind2=order[random.randint(1,int(len(order)*ngbr))]
        ind2=solution.index(ind2)
        if ind2==0:
            ind2=1
            
        inds=sorted([ind1,ind2])
        if inds[1]==nodeCount and inds[0]==nodeCount-1:
            inds[0]=nodeCount-2
        
        rp=random.uniform(0,1)
        if inds[1]-inds[0]==1:
            oo=deltap(inds[0],0,inds[1],solution)
            x=solution.copy()
            a=x.pop(inds[0])
            x.insert(inds[1],a)
            ox=deltap(inds[0],0,inds[1],x)
            if ox>oo:
                pr=math.exp((int(oo-ox)-1)/t)
            else:
                pr=0
            if ox<=oo or rp<pr:
                a=solution.pop(inds[0])
                solution.insert(inds[1],a)
                objval=objval-oo+ox
                            
        else:
            oo=deltap(inds[0],-1,inds[1],solution)
            x=solution.copy()
            x[inds[0]:inds[1]]=x[inds[1]-1:inds[0]-1:-1]
            ox=deltap(inds[0],-1,inds[1],x)
            if ox>oo:
                pr=math.exp((int(oo-ox)-1)/t)
            else:
                pr=0
            if ox<=oo or rp<pr:
                solution[inds[0]:inds[1]]=solution[inds[1]-1:inds[0]-1:-1]
                objval=objval-oo+ox
    #-------------------------------   3 OPT   ------------------------------------
    
        ind1=random.randint(1,nodeCount)
        num=solution[ind1-1]
        order_sel=Dist_mat[num]
        order=sorted(range(len(order_sel)), key=lambda k: order_sel[k])
        order.remove(solution[ind1])
        if 0 in order:
            order.remove(0)
        tbc3opt=random.sample(order[1:int(len(order)*ngbr)],2)
        ind2=solution.index(tbc3opt[0])
        ind3=solution.index(tbc3opt[1])
        inds=sorted([ind1,ind2,ind3])
        oo=deltap(inds[0],inds[1],inds[2],solution)
        rp=random.uniform(0,1)
        if inds[2]-inds[0]==2:
            b=solution.copy()
            a=b.pop(inds[0])
            b.insert(inds[1],a)
            ob=deltap(inds[0],inds[1],inds[2],b)
            if ob>oo:
                pr=math.exp((int(oo-ob)-1)/t)
            else:
                pr=0
            if ob<=oo or rp<=pr:
                a=solution.pop(inds[0])
                solution.insert(inds[1],a)
                objval=objval-oo+ob
            
            
        elif inds[2]-inds[1]!=1 and inds[1]-inds[0]==1:
            b=solution.copy()
            c=solution.copy()
            a=b.pop(inds[0])
            b.insert(inds[2]-1,a)
            ob=deltap(inds[0],inds[2]-1,inds[2],b)
            c[inds[0]:inds[2]]=c[inds[2]-1:inds[0]-1:-1]
            oc=deltap(inds[0],inds[2]-1,inds[2],c)
            op=[ob,oc]
            if min(op)>oo:
                pr=math.exp((int(oo-min(op))-1)/t)
            else:
                pr=0
            if min(op)<=oo or rp<pr:
                if ob>oc:
                    solution[inds[0]:inds[2]]=solution[inds[2]-1:inds[0]-1:-1]
                    objval=objval-oo+oc
                else:
                    a=solution.pop(inds[0])
                    solution.insert(inds[2]-1,a)
                    objval=objval-oo+ob
               
               
        elif inds[2]-inds[1]==1 and inds[1]-inds[0]!=1:
            b=solution.copy()
            a=b.pop(inds[1])
            b.insert(inds[0],a)
            ob=deltap(inds[0],inds[0]+1,inds[2],b)
            c=solution.copy()
            c[inds[0]:inds[1]]=c[inds[1]-1:inds[0]-1:-1]
            oc=deltap(inds[0],inds[1],inds[2],c)
            d=solution.copy()
            d[inds[0]:inds[2]]=d[inds[2]-1:inds[0]-1:-1]
            od=deltap(inds[0],inds[0]+1,inds[2],d)
            op=[ob,oc,od]
            if min(op)>oo:
                pr=math.exp((int(oo-min(op))-1)/t)
            else:
                pr=0
            if min(op)<=oo or rp<pr:
                if min(op) == od:
                    solution[inds[0]:inds[2]]=solution[inds[2]-1:inds[0]-1:-1] 
                    objval=objval-oo+od
                elif min(op) == oc:
                    solution[inds[0]:inds[1]]=solution[inds[1]-1:inds[0]-1:-1]
                    objval=objval-oo+oc
                else:
                    a=solution.pop(inds[1])
                    solution.insert(inds[0],a)
                    objval=objval-oo+ob
        else:
            b=solution.copy()
            b[inds[0]:inds[2]]=b[inds[2]-1:inds[0]-1:-1]
            ob=deltap(inds[0],inds[0]+inds[2]-inds[1],inds[2],b)
            
            c=solution.copy()
            c[inds[1]:inds[2]]=c[inds[2]-1:inds[1]-1:-1]
            a=c[inds[0]:inds[1]].copy()
            del c[inds[0]:inds[1]]
            c[inds[0]+inds[2]-inds[1]:inds[0]+inds[2]-inds[1]]=a
            oc=deltap(inds[0],inds[0]+inds[2]-inds[1],inds[2],c)
            
        
            d=solution.copy()    
            d[inds[0]:inds[1]]=d[inds[1]-1:inds[0]-1:-1]
            d[inds[1]:inds[2]]=d[inds[2]-1:inds[1]-1:-1]
            od=deltap(inds[0],inds[1],inds[2],d)
            
            
            e=solution.copy()               #2-OPT
            e[inds[0]:inds[1]]=e[inds[1]-1:inds[0]-1:-1]
            oe=deltap(inds[0],inds[1],inds[2],e)
            
        
            f=solution.copy()               #2-OPT
            f[inds[1]:inds[2]]=f[inds[2]-1:inds[1]-1:-1]
            of=deltap(inds[0],inds[1],inds[2],f)
            
       
            g=solution.copy()
            a=g[inds[0]:inds[1]].copy()
            del g[inds[0]:inds[1]]
            g[inds[0]+inds[2]-inds[1]:inds[0]+inds[2]-inds[1]]=a
            og=deltap(inds[0],inds[0]+inds[2]-inds[1],inds[2],g)
            
        
            h=solution.copy()
            h[inds[0]:inds[1]]=h[inds[1]-1:inds[0]-1:-1]
            a=h[inds[0]:inds[1]].copy()
            del h[inds[0]:inds[1]]
            h[inds[0]+inds[2]-inds[1]:inds[0]+inds[2]-inds[1]]=a
            oh=deltap(inds[0],inds[0]+inds[2]-inds[1],inds[2],h)
            
            op=[ob,oc,od,oe,of,og,oh]
            if min(op)>oo:
                pr=math.exp((int(oo-min(op))-1)/t)
            else:
                pr=0
            if min(op)<=oo or rp<pr:
                if min(op)==ob:
                    solution[inds[0]:inds[2]]=solution[inds[2]-1:inds[0]-1:-1]
                    objval=objval-oo+ob
                elif min(op)==oc:
                    solution[inds[1]:inds[2]]=solution[inds[2]-1:inds[1]-1:-1]
                    a=solution[inds[0]:inds[1]].copy()
                    del solution[inds[0]:inds[1]]
                    solution[inds[0]+inds[2]-inds[1]:inds[0]+inds[2]-inds[1]]=a
                    objval=objval-oo+oc
                elif min(op)==od:
                    solution[inds[0]:inds[1]]=solution[inds[1]-1:inds[0]-1:-1]
                    solution[inds[1]:inds[2]]=solution[inds[2]-1:inds[1]-1:-1]
                    objval=objval-oo+od
                elif min(op)==oe:
                    solution[inds[0]:inds[1]]=solution[inds[1]-1:inds[0]-1:-1]
                    objval=objval-oo+oe
                elif min(op)==of:
                    solution[inds[1]:inds[2]]=solution[inds[2]-1:inds[1]-1:-1]
                    objval=objval-oo+of
                elif min(op)==og:
                    a=solution[inds[0]:inds[1]].copy()
                    del solution[inds[0]:inds[1]]
                    solution[inds[0]+inds[2]-inds[1]:inds[0]+inds[2]-inds[1]]=a
                    objval=objval-oo+og
                elif min(op)==oh:
                    solution[inds[0]:inds[1]]=solution[inds[1]-1:inds[0]-1:-1]
                    a=solution[inds[0]:inds[1]].copy()
                    del solution[inds[0]:inds[1]]
                    solution[inds[0]+inds[2]-inds[1]:inds[0]+inds[2]-inds[1]]=a
                    objval=objval-oo+oh
    
        counter+=1
        if objval<bestval:
            bestsol=solution.copy()
            bestval=objval
        temprec.append(t)
    if counter> trenew and max(objrec[counter-trenew:counter])-min(objrec[counter-trenew:counter])==0:
        t=min(t0,t*1.5)
        
    else:
        t=cp*t
    

sol=bestsol.copy()
sol.pop()
output_data = '%.2f' % bestval + ' ' + str(0) + '\n'
output_data += ' '.join(map(str, sol))        
print(output_data)
print(' Execution time is {} seconds'.format(round(time.time() - start_time,5)))

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
fig1, ax1 = plt.subplots(figsize=(10, 10))
nx.draw_networkx_nodes(G,pos,node_size=1,node_color='blue',ax=ax1)
nx.draw_networkx_edges(G,pos, width=0.4,edge_color='black')
nx.draw_networkx_labels(G,pos,font_size=8)
ax1.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)


x = np.array(list(range(0,iteration*m)))
fig2, ax2 = plt.subplots(figsize=(10, 10))
ax2.set_title('Objective value and Temperature')
ax2.set_xlabel('Iteration')
ax2.set_ylabel('Objective')
ax2.plot(x,objrec, 'r', label='Objective')
ax3=ax2.twinx()
ax3.plot(x,temprec, 'g', label='temperature')
ax3.set_xlabel('Iteration')
ax3.set_ylabel('t')
plt.legend()
# show the plot
plt.show()
