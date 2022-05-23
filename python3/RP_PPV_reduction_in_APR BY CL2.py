#!/usr/bin/env python3
import math
import numpy as np
import csv
import pandas as pd

## Assumes that no RPL is penalitzed for stealing, on the ETH deposit and ETH rewards. 
n = 625000 # number of validators

m = 1.11 #PPV Annual average PPV in ETH eared in a year per minipool; includes inclusion fees and coinbase payments.
b = 0.72 #Beacon chain in ETH/yr include only eth2.0 APR rewards (from https://rocketpool.net/node-operators)

c = 0.15 #Comission Set node commision
d = 16 # NO Deposit Note: APR does not change with d
t = 1 #year(s)
a = 0.2
ConfidanceLevels = [50, 84.1, 95, 97.7, 97.7, 99, 99.9]

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
    return sum(PPVblocks)-(PPVblocks[:(PPVblocks<np.percentile(PPVblocks, k)).argmin()].sum())

def honestrETHROI(d):
    s = d/32 #NO Share
    return ((1-s)*(1-c)*b*t)+((1-s)*(1-c)*m*t) #Honest rETH holder gains in ETH

def rougerETHROI(d,CL):
    s = d/32 #NO Share
    stolen = upperSum(CL) / totalBlockRewards * a
    return ((1-s)*(1-c)*b*t)+((1-s)*(1-c)*m*t*(1-stolen)) #Rougee rETH holder gains in ETH

def honestAPR(d):
    return honestrETHROI(d)/(32-d)*100
     
def rougeAPR(d,CL):
    return rougerETHROI(d,CL)/(32-d)*100

def APRloss(d,CL):
    return honestAPR(d) - rougeAPR(d,CL)


print(f'Assuming:')
print(f'   Active Beacon Chain Validaors  n = {n}')
print(f'   Beacon Chain (eth2) rewards    b = {b:.2f} ETH/year.')
print(f'   Proposer Payment rewards       m = {m} ETH/year.')
print(f'   Alignment dishonest            a = {a}')
print('\n')

# Create a dataFrame
df = pd.DataFrame([],['HonestAPR', 'DishonestAPR', 'ARPloss'])
pd.set_option('precision', 2)

for CL in ConfidanceLevels:
    df[CL] = [ honestAPR(d), rougeAPR(d,CL), APRloss(d,CL) ]

pd.set_option('precision', 2)
print(df)
