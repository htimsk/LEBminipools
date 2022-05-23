#!/usr/bin/env python3
import math
import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors

## Assumes that no RPL is penalitzed for stealing, on the ETH deposit and ETH rewards. 
n = 625000 # number of validators
b = 1.11 #Beacon chain in ETH/yr include only eth2.0 APR rewards (from https://rocketpool.net/node-operators)
m = 0.72 #PPV Annual average PPV in ETH eared in a year per minipool; includes inclusion fees and coinbase payments.
c = 0.15 #Comission Set node commision
d = 16 # NO Deposit Note: APR does not change with d
t = 1 #year(s)
#ConfidanceLevels = [50, 84.1, 95, 97.7, 97.7, 99, 99.9, 100]

def loadFlashBotCSV():
    #from numpy import genfromtxt
    #Load the data back from flashbots and at the same time strips commas from the readback
    flashbot_data = np.genfromtxt('blockReward.csv', delimiter=',')

    return flashbot_data
            

##print('===================================================')
##print("Loading the etherscan.io blockRewards data")
##print('===================================================')
##print(' ')

PPVblocks = np.sort(loadFlashBotCSV())
totalBlockRewards = np.sum(PPVblocks, axis=0)


def upperSum(k):

    for cell in np.nditer(k):
        result = sum(PPVblocks)-(PPVblocks[:(PPVblocks<np.percentile(PPVblocks, cell)).argmin()].sum())
    return result # sum(PPVblocks)-(PPVblocks[:(PPVblocks<np.percentile(PPVblocks, k)).argmin()].sum())

def honestrETHROI(d):
    s = d/32 #NO Share
    return ((1-s)*(1-c)*b*t)+((1-s)*(1-c)*m*t) #Honest rETH holder gains in ETH

def rougerETHROI(d,CL,a):
    s = d/32 #NO Share
    #stolen = upperSum(CL) / totalBlockRewards * a
    stolen = (UParray * a) / totalBlockRewards 
    return ((1-s)*(1-c)*b*t)+((1-s)*(1-c)*m*t*(1-stolen)) #Rougee rETH holder gains in ETH

def honestAPR(d):
    return honestrETHROI(d)/(32-d)*100
     
def rougeAPR(d,CL,a):
    return rougerETHROI(d,CL,a)/(32-d)*100

def APRloss(d,CL,a):
    return honestAPR(d) - rougeAPR(d,CL,a)

def z_func(x,y):
     return APRloss(4,x,y)
            



# Create Matrix dimension

x = np.arange(50,100,5) # CL from 50 to 100 in increments of 5
y = np.arange(0.1,1.1,0.1) # values of a
[X,Y] = np.meshgrid(x, y) # grid of point


# np.percentile can not accepty an array so we need to manually iterate of the upperSum values by CL
UParray = np.array([])
for cell in np.nditer(x):
    upSumAmt = sum(PPVblocks)-(PPVblocks[:(PPVblocks<np.percentile(PPVblocks, cell)).argmin()].sum())
    UParray = np.append(UParray, upSumAmt)



Z = z_func(X,Y) # evaluation of the function on the grid



# Create a X,Y plot

yLabels = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0', ]
xLabels = ['50', '55', '60', '65', '70', '75', '80', '85', '90', '95']

fig, ax = plt.subplots()

p1 = plt.imshow(Z, origin="lower", cmap='turbo') # Adjust vmina and vmax for the color spectrum 
plt.colorbar()

plt.suptitle('Reduction in rETH APY Plotted against the Stealing Threshold and Alignment (a) of the Node Operator', fontsize=14)
plt.title('Assumes ' +str(n)+' validators; b = ' +str(b)+' m = ' +str(m)+'.', fontsize=12)

plt.xlabel("Percentile of PPV that tempts the NO steal.")
ax.set_yticks([0,1,2,3,4,5,6,7,8,9])
ax.set_yticklabels(yLabels)
ax.set_xticks([0,1,2,3,4,5,6,7,8,9])
ax.set_xticklabels(xLabels)

plt.ylabel("Alignmnet (a). 1 = evil, 0= good")
#plt.xlim([0, 10]) # Set range of x axis here Need scale....
#plt.ylim([0, 10]) # Set range of y axis here


#Add contours
CS = plt.contour(Z, levels=[.25, .5, .75, 1], colors=['#FFFFFF'], extend='both') #

fmt = {}
strs = ['25bp', '50bp', '75bp', '100bp'] #  
for l, s in zip(CS.levels, strs):
    fmt[l] = s
    
plt.clabel((CS), inline=True, manual=True, fmt=fmt, fontsize=8)

plt.show()






