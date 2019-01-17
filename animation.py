# -*- coding: utf-8 -*-
"""
This program is designed to simulate 2D diffusion limited Aggregation(animated)
Created on Wed. June 6 14:32:18 2018

@author: Teague
"""
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time
import imageio as imio

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


#animation start_section

tic=time.time()#Time Init, 
fig=plt.figure() #plot init
#ax=fig.add.subplot(111)#assign plot/subplot space
   
xres=270
yres=270
neighbors=np.array([[-1,-1,0,1,1,1,0,-1],[0,1,1,1,0,-1,-1,-1]]).T
starter_lat=init_Latt(xres,yres)
start_ring,r,origin=(def_start_ring(starter_lat))
ring_array_dims=start_ring.shape
nump=int(0)    #initializing number of particles on the aggregate
images=np.array([])

    
while (nump<=(xres*yres/20)):     #run simulation while less than 5% filled w/ particles
    
    rand=np.random.randint(0,ring_array_dims[0])
    pos=np.array([(start_ring[rand,0]),(start_ring[rand,1])])
    starter_lat[(pos[0]),(pos[1])]=1
   # print(nump/(xres*yres/20)*100)   CAUTION Might slow process down a ton
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
                    frame=starter_lat
                    nump=nump+1
                    plt.imshow(starter_lat, interpolation='nearest', cmap=cm.Greys_r)
                    plt.show()
                    plt.pause(0.001)
                    images=np.dstack(frame)
        else:
            #delete particle
            starter_lat[pos[0],pos[1]]=0
            neibt=1
            #if sp.mod(nump,1000)==0:    
                #plt.imshow(starter_lat, interpolation='nearest', cmap=cm.Greys_r)
                #plt.show()
                #plt.pause(0.001)
    
    


plt.imshow(starter_lat, interpolation='nearest', cmap=cm.Greys_r)
plt.show()
imio.mimsave('DLA_animation.gif',images)
toc=time.time()-tic
print("Time Elapsed:", toc)