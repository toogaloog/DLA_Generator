# -*- coding: utf-8 -*-
"""
This program is designed to simulate 2D diffusion limited Aggregation
Created on Mon May  7 14:32:18 2018

@author: Teague
"""
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time

def init_Latt (x,y):
    
    #Make Lattice dimensions odd, forcing origin to center
    if (sp.mod(x,2)==0 and sp.mod(x,2)==0):   #if both(x,y) are even, add one to both
        x+=1
        y+=1
    elif (sp.mod(x,2)==0 and sp.mod(y,2)): #if x is even, add one to x
        x+=1
    elif (sp.mod(x,2) and sp.mod(y,2)==0): #if y is even, add one to y
        y+=1
    
    latdims=(x,y)       #assign list holding lattice dimensions
    blank_lat=np.zeros(latdims)     #initialiaze lattice, fill with zeros(empty)
    blank_lat[int(x/2),int(y/2)]=1  #set center point as occupied
    
    return blank_lat

def def_start_ring(seed):
    
    latdims=seed.shape
    origin=(int(latdims[0]/2),int(latdims[1]/2))  #set origin at lower indexed middle
    
    #set radius at 1/2.5 of smallest dimension
    if latdims[0]>latdims[1]:
        r=latdims[1]/2.5
    else:
        r=latdims[0]/2.5
    
    starter_circle=np.array((),int)  #initialize blank start circle array
    starter_circle.shape=(0,2)       #reshape to hold vectors
    for i in range(0,latdims[0]):
        for j in range(0,latdims[1]):
            if (((origin[0]-i)**2)+((origin[1]-j)**2) >= r**2 and ((origin[0]-i)**2)+((origin[1]-j)**2) <= (r+1)**2):
                starter_circle=np.vstack((starter_circle,np.array([i,j]).T))
        
    
    return starter_circle,r,origin

def frac_dim_get_1(agg, r):
    squarerad=np.arange(-r,r,1)
    g=0
    
    for i in range(0,agg.shape[0]):
        for j in range(0,agg.shape[1]):
                     
            if agg[i,j]==1:
                for I in squarerad:
                    for J in squarerad:
                        if ((I**2)+(J**2))<=(r**2)+0.5 and ((I**2)+(J**2))>=(r**2)-0.5:
                            g=g+(agg[i,j]*agg[i+I,j+J])
    rawc=g/(agg.sum())
                    
    return rawc,r

def frac_dim_get(agg, r):
    squarerad=np.arange(-r,r,1)
    g=[]
    rawc=[]
    for i in range(0,agg.shape[0]):
        for j in range(0,agg.shape[1]):
            g=0
            
            if agg[i,j]==1:
                for I in squarerad:
                    for J in squarerad:
                        if ((I**2)+(J**2))<=r**2:
                            g=g+(agg[i,j]*agg[i+I,j+J])
                    rawc=np.hstack((rawc,(g/(agg.sum()))))
                    cr=rawc.mean()
    return cr,r

def box_count(agg,size):
    m = int(np.log(size)/np.log(2))
    cnts = []
    for lev in range(m):
        block_size = 2**lev
        cnt = 0
        for j in range(int(size/(2*block_size))):
            for i in range(int(size/block_size)):
                cnt = cnt + agg[j*block_size:(j+1)*block_size, i*block_size:(i+1)*block_size].any()
        cnts.append(cnt)
    data = np.array([(2**(m-(k+1)),cnts[k]) for k in range(m)])
    return data

tic=time.time()   
xres=270
yres=270
lilr=27
neighbors=np.array([[-1,0,0,1],[0,1,-1,0]]).T
starter_lat=init_Latt(xres,yres)
start_ring,r,origin=(def_start_ring(starter_lat))
ring_array_dims=start_ring.shape
nump=int(0)    #initializing number of particles on the aggregate


#for i in range(0,ring_array_dims[0]):
    
    #starter_lat[(start_ring[i-1,0]),(start_ring[i-1,1])]=1
    
while (nump<=(xres*yres/20)):     #run simulation while less than 10% filled w/ particles
    
    rand=np.random.randint(0,ring_array_dims[0])
    pos=np.array([(start_ring[rand,0]),(start_ring[rand,1])])
    starter_lat[(pos[0]),(pos[1])]=1
    
    neibt=0;        #neighbor test, 0=no neighbors
    while (neibt==0):
        j=0
        neibt=0
        if ((((origin[0]-pos[0])**2)+((origin[1]-pos[1])**2))<=((r+r/6)**2)): #if within the circle(adjustments for thickness)  !!!I THINK THIS IS PROBLEM
            
            for j in range(0,neighbors.shape[0]):
                if (starter_lat[(pos[0]+neighbors[j,0]),(pos[1]+neighbors[j,1])]>0):        #if neighbor if occupied
                    neibt+=1
                
            if (neibt==0):
                #move particle
                R=np.random.randint(0,neighbors.shape[0])
                starter_lat[(pos[0]+neighbors[R,0]),(pos[1]+neighbors[R,1])]=1
                #print(R)
                #delete old particle
                starter_lat[pos[0],pos[1]]=0
                #update position, (X->Y)
                pos[0]+=neighbors[R,0]
                pos[1]+=neighbors[R,1]
                
            elif (neibt>=1):    
                    nump=nump+1
                    print(nump/(xres*yres/20)*100)
        else:
            #delete particle
            starter_lat[pos[0],pos[1]]=0
            neibt=1
                
    
    
    

fig=plt.figure()
correlation = np.zeros((1,2))

for f in range (3,24):
    holder=np.array(frac_dim_get_1(starter_lat,f))
    correlation =np.vstack((correlation,holder))

#box_count_data=box_count(starter_lat, starter_lat.shape[0])
plt.imshow(starter_lat, interpolation='nearest', cmap=cm.Greys_r)
plt.show()
#f=open("Box_counting_result.csv","a+")
f1=open("Frac_dim_result_01.csv","a+")
#t=np.array2string(box_count_data, separator=',')
t1=np.array2string(correlation, separator=',')
#s=str(t)
s1=str(t1)
#f.write(s)
f1.write(s1)
#f.write('\n')
f1.write('\n')
#f.close()
f1.close()
toc=time.time()-tic
print("Time Elapsed:", toc)
plt.savefig('fig_C_D_3.png')