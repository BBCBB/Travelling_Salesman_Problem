
import random
import math
from collections import namedtuple
import networkx as nx
import matplotlib.pyplot as plt
import sys
import time

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
   
def obj(s,k):
    objective=0
    for j in range(nodeCount):
        l= length(points[s[j]],points[s[j+1]])
        objective = objective + l
        if k==1:
            rec.append(l)
    return objective
 
def delta(y,z,s):
    imp=0
    if z!=nodeCount:
        z=z+1
    for j in range(y-1,z):
        l= length(points[s[j]],points[s[j+1]])
        imp = imp + l
    return imp    

def deltap(y,w,z,s):
    imp=0
    if w==0:
        imp=length(points[s[y-1]],points[s[y]])+length(points[s[z]],points[s[z+1]])  
    elif w==-1:
        imp=length(points[s[y-1]],points[s[y]])+length(points[s[z-1]],points[s[z]])  
    else:
        imp=length(points[s[y-1]],points[s[y]])+length(points[s[z-1]],points[s[z]])+\
            length(points[s[w-1]],points[s[w]])
    return imp   

# solution=list(range(1,nodeCount))
# random.shuffle(solution)
# solution.insert(0,0)
solution=[0]
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
sol0=solution.copy()
maxiter=80000
if nodeCount<80:
    lim=8000
    t=2
    maxiter=50000
elif nodeCount<150:
    lim=10000
    t=10
    maxiter=60000
elif nodeCount<300:
    lim=15000
    t=10
    maxiter=80000
elif nodeCount<1000:
    lim=12000
    t=10
    maxiter=100000
else:
    lim=12000
    t=10
    maxiter=120000
t0=t

start_time = time.time()
rec=[]
objval=obj(solution,1)
bestval=objval
bestsol=solution.copy()
o=[objval]
mo=[]
for iteration in range(1,maxiter+1):
    o.append(objval)

    mm=(o[iteration]-o[iteration-1])
    mo.append(mm)
    if iteration>lim:
        m=(o[iteration]-o[iteration-500])/500
        if min(mo[iteration-2000:iteration])-bestval>=0:
            solution=bestsol.copy()
    else:
        m=-1
    if m<0.02 and m>=0 and mm>=0:

        if nodeCount<80:
            t=t0
        elif nodeCount<500:
            t=t0*5
        elif nodeCount<1000:
            t=t0*2
        else:
            t=t0*2
    else:
        t=0.98*t

    trs=((iteration+1000)/maxiter)*120       #pruning the search space based on the longest distance between couple of nodes
    trp=1
#--------------------------------------------------------------------------------------    
    tbc2opt=sorted(random.sample(range(1, nodeCount+1), 2))   # Pure 2-opt part of code
    ind1=tbc2opt[0]
    ind2=tbc2opt[1]
    inds=sorted([ind1,ind2])
    
    if inds[1]==nodeCount and inds[0]==nodeCount-1:
        inds[0]=nodeCount-2
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
        if ox<=oo or random.uniform(0,1)<pr:
            a=solution.pop(inds[0])
            solution.insert(inds[1],a)
    else:
        oo=deltap(inds[0],-1,inds[1],solution)
        x=solution.copy()
        x[inds[0]:inds[1]]=x[inds[1]-1:inds[0]-1:-1]
        ox=deltap(inds[0],-1,inds[1],x)
        if ox>oo:
            pr=math.exp((int(oo-ox)-1)/t)
        else:
            pr=0
        if ox<=oo or random.uniform(0,1)<pr:
            solution[inds[0]:inds[1]]=solution[inds[1]-1:inds[0]-1:-1]
#----------------------------------------------------------------------------------------- 
    mar=max(rec)
    indexmax=rec.index(mar)+1
    if mar>(sum(rec)/len(rec))*trs and indexmax!=nodeCount:

          r=solution[indexmax-int(trp*indexmax)+1:indexmax+int(trp*(nodeCount-indexmax))-1]
          if indexmax in r:
              r.remove(indexmax)
          tbc3opt=random.sample(r, 2)
          tbc3opt.append(indexmax)
          tbc3opt.sort()
    elif mar>(sum(rec)/len(rec))*trs and indexmax==nodeCount:
          tbc3opt=random.sample((1,nodeCount-1), 2)
          tbc3opt.sort()
          tbc3opt.append(nodeCount)
    else:
        r=random.randint(1, nodeCount)
        tbc3opt=random.sample(range(r-int(trp*r)+1,r+(int(trp*(nodeCount-r)))-1), 2)
        tbc3opt.append(r)
        tbc3opt.sort()
    
    ind1=tbc3opt[0]
    ind2=tbc3opt[1]
    ind3=tbc3opt[2]
    
    inds=sorted([ind1,ind2,ind3])
    oo=delta(inds[0],inds[2],solution)
    if inds[2]-inds[0]==2:
        b=solution.copy()
        a=b.pop(inds[0])
        b.insert(inds[1],a)
        ob=delta(inds[0],inds[2],b)
        if ob>oo:
            pr=math.exp((int(oo-ob)-1)/t)
        else:
            pr=0
        if ob<=oo or random.uniform(0,1)<=pr:
            a=solution.pop(inds[0])
            solution.insert(inds[1],a)
        
        
    elif inds[2]-inds[1]!=1 and inds[1]-inds[0]==1:
        b=solution.copy()
        c=solution.copy()
        a=b.pop(inds[0])
        b.insert(inds[2]-1,a)
        ob=delta(inds[0],inds[2],b)
        c[inds[0]:inds[2]]=c[inds[2]-1:inds[0]-1:-1]
        oc=delta(inds[0],inds[2],c)
        op=[ob,oc]
        if min(op)>oo:
            pr=math.exp((int(oo-min(op))-1)/t)
        else:
            pr=0
        if min(op)<=oo or random.uniform(0,1)<pr:
            if ob>oc:
               solution[inds[0]:inds[2]]=solution[inds[2]-1:inds[0]-1:-1]
            else:
               a=solution.pop(inds[0])
               solution.insert(inds[2]-1,a)
           
           
    elif inds[2]-inds[1]==1 and inds[1]-inds[0]!=1:
        b=solution.copy()
        a=b.pop(inds[1])
        b.insert(inds[0],a)
        ob=delta(inds[0],inds[2],b)
        c=solution.copy()
        c[inds[0]:inds[1]]=c[inds[1]-1:inds[0]-1:-1]
        oc=delta(inds[0],inds[2],c)
        d=solution.copy()
        d[inds[0]:inds[2]]=d[inds[2]-1:inds[0]-1:-1]
        od=delta(inds[0],inds[2],d)
        op=[ob,oc,od]
        if min(op)>oo:
            pr=math.exp((int(oo-min(op))-1)/t)
        else:
            pr=0
        if min(op)<=oo or random.uniform(0,1)<pr:
            if min(op) == od:
               solution[inds[0]:inds[2]]=solution[inds[2]-1:inds[0]-1:-1] 
            elif min(op) == oc:
               solution[inds[0]:inds[1]]=solution[inds[1]-1:inds[0]-1:-1]
            else:
                a=solution.pop(inds[1])
                solution.insert(inds[0],a)
    else:
        oo=deltap(inds[0],inds[1],inds[2],solution)
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
        if min(op)<=oo or random.uniform(0,1)<pr:
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

    rec=[]
    objval=obj(solution,1)
    if objval<bestval:
        bestsol=solution.copy()
        bestval=objval

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
fig, ax = plt.subplots(figsize=(6, 6))
nx.draw_networkx_nodes(G,pos,node_size=55,node_color='yellow',ax=ax)
nx.draw_networkx_edges(G,pos, width=0.4,edge_color='black')
nx.draw_networkx_labels(G,pos,font_size=8)
ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)

import numpy as np
x = np.array(list(range(0,iteration+1)))
fig = plt.figure()
ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
# plot the function
plt.plot(x,o, 'r', label='Objective')
plt.legend()
# show the plot
plt.show()
