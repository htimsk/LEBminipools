# Adapted from : https://pintail.xyz/posts/beacon-chain-validator-rewards/
# define annualised base reward (measured in ETH) for n validators
# assuming all validators have an effective balance of 32 ETH
import math
import matplotlib.pyplot as plt
from scipy.stats import binom
import numpy as np
import random
import csv


            
    
def loadFlashBotCSV():
    
    from numpy import genfromtxt
    flashbot_data = genfromtxt('blockReward.csv', delimiter=',')

    #print("This is flashbot_data") # debug line
    #print(flashbot_data) # debug line
    return flashbot_data
            


## LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL
## Load flashbots data
#Load the data back from flashbots and at the same time strips commas from the readback
print('===================================================')
print("+ Begining")
print('===================================================')
print(' ')


print("Loading the etherscan.io blockRewards data\n")

MEVblocks = loadFlashBotCSV()

##print("Print the first line uploaded from minerREV.csv as MEVblocks array")
##print(MEVblocks[0])
##print("THIS IS THE OUTPUT TABLE")



#### Save file as csv
#write_matrix_to_textfile(outputTable, "classesperhour.csv")


#x = [el for el in range(500)]
#t = int(input("Enter the number of years you will be node operating: "))
#secValidating = int(t*31556952/12)
#print(f"Seconds validating: {secValidating}")

n = 625000 #number of validators from https://beaconcha.in/
m = 3877 #ETH last 30 days from https://explore.flashbots.net/
MEVblock = m / (6750 * 32)  #MEV per block where 6750 epochs per month 32 slots per epoch
#MEVblock = 0.185242203  #MEV per block (trimmed mean with 1% trimmed) from Flashbots csv data https://hackmd.io/@flashbots/mev-in-eth2 https://dashboard.flashbots.net/
# https://github.com/flashbots/eth2-research/blob/main/notebooks/mev-in-eth2/miner-REV.csv

mcTries = 50000 #The number of monte carlo tries to model.
#var = binom.rvs(secValidating, (1/n), size=mcTries)
##
##print("var")
##print(var)
##print("MEVblocks")
##print(MEVblocks)

d=4

roll = 1
print(1/n)
rndm = random.random()

def validate():
    rndm = random.random()
    global roll
    #print(rndm)

    while random.random() > (1/n):
        roll = roll + 1
    else:
        #print('You proposed a block')
        #print(f'The number of slots needed was {roll}')
        REV = random.choice(MEVblocks)
        #print(REV)
    return REV

while validate() < d*1e18:
    validate()
else:
    print(f'The number of slots needed to reach NOdeposit was {roll}')
    print(f'The time was {roll/2608200:.2f} years')


