# Adapted from : https://pintail.xyz/posts/beacon-chain-validator-rewards/
# define annualised base reward (measured in ETH) for n validators
# assuming all validators have an effective balance of 32 ETH
import math
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import binom
import numpy as np
import random
import csv
import pandas as pd

## Assumes that no RPL is penalitzed for stealing, on the ETH deposit and ETH rewards. 
n = 625000 # number of validators
##base_reward =  82180 * 512 / math.sqrt(n * 32e9)
##ideal_reward = 4 * base_reward
##
##m = 0.91 #PPV Annual average PPV in ETH eared in a year per minipool; includes inclusion fees and coinbase payments.
##b = ideal_reward #Beacon chain in ETH/yr include only eth2.0 APR rewards (from https://rocketpool.net/node-operators)

c = 0.15 #Comission Set node commision
p = 1 #Penality assessed for defecting
f = 1 - p #Fine amount

# Create and array of time (t) in years
t = 1 #year(s)
#t = np.array(range(20))

cutoff = [50, 84.1, 95, 97.7, 99, 99.9]
matrixData = np.zeros(shape=(0,7))# create empty np array (rows, columns)

#d = [16, 8, 6, 4, 2] # NO deposit amount

deposits = [2, 4, 6, 6.4, 8, 16] 
CL = 50

    
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
#print(PPVblocks)


# print(OUTPUTdata)
meanBlocks = np.mean(PPVblocks, axis=0)
medianBlocks = np.median(PPVblocks, axis=0)
stdBlocks = np.std(PPVblocks, axis=0)
cntBlocks = np.shape(PPVblocks)
totalBlocks = np.sum(PPVblocks, axis=0)

def lowerSum(k):
    return (PPVblocks[:(PPVblocks<np.percentile(PPVblocks, k)).argmin()].sum())

def lowerCnt(k):
    aggerate = np.shape(PPVblocks[:(PPVblocks<np.percentile(PPVblocks, k)).argmin()])
    return (aggerate[0])

def upperSum(k):
    return sum(PPVblocks)-(PPVblocks[:(PPVblocks<np.percentile(PPVblocks, k)).argmin()].sum())

def honestrETHROI(d):
    s = d/32 #NO Share
    return ((1-s)*(1-c)*m*t)+(1-s)*((1-c)*b*t) #Honest rETH holder gains in ETH

def rougerETHROI(d,CL):
    s = d/32 #NO Share
    loss = upperSum(CL) / totalBlocks
    print(f'the loss was calcualted at {loss}')
    return (((1-s)*(1-c)*m*t*(1-loss))+(1-s)*(1-c)*b*t) #Rougee rETH holder gains in ETH

def honestAPR(d):
    return honestrETHROI(d)/(32-d)*100
     
def rougeAPR(d,loss):
    return rougerETHROI(d,loss)/(32-d)*100


for k in cutoff:
    blockPPV = (np.percentile(PPVblocks, k, axis=0)/1e18)

    lowerTotal = lowerSum(k)/1e18
    upperTotal = upperSum(k)/1e18
    PPVtotal = lowerTotal + upperTotal

    lowerPercent = lowerTotal / PPVtotal
    upperPercent = upperTotal / PPVtotal
    
    
    checkMath = lowerCnt(k)/int(''.join(map(str, cntBlocks))) #fix tuple math error??
    newrow = [k, blockPPV, lowerTotal, lowerPercent*100, upperTotal, upperPercent*100, PPVtotal] # add checkMath for error checking
    matrixData = np.vstack([matrixData, newrow])

np.set_printoptions(precision=3, suppress=True)


#print(f' number of validators      = {n}')

print(f' number of blocks analyzed = {cntBlocks[0]}')
print(f' The timespan sampled is {cntBlocks[0]*12/(60*60*24):.1f} day(s)')
print(f"   mean        {(meanBlocks/1e18):.4f} ETH in a block ")
print(f"   median      {(medianBlocks/1e18):.4f} ETH in a block")
print(f"   std         {(stdBlocks/1e18):.4f} ETH")
print(f"   sum     {(totalBlocks/1e18):.2f}   ETH")
print("\n")

print(f"Value of PPV reported in ETH")
print(f"   Cutoff    PPV/blk   lowerSum  lowETH% upperSum      upETH%     sum     ")
print(f"--------------------------------------------------------------------------")
print(f'{matrixData}')


#Given threshold = d (input), about 99.847781% (output) of the items in list d are below this percentile.


# Create a dataFrame
df = pd.DataFrame([],['Deposit', 'Percentile_of_d', 'Yrs_to_win', 'UpperSum_of_PPV', 'upETH%'])


print("\n\n")
print('Deposit, percentile, year(s) to win lottery block=d, sum of PPV above threshold, upETH%')
print(f'Assuming {n} validators.')
#d = 16
for d in deposits:
    depPercentile = stats.percentileofscore(PPVblocks, d*1e18)
    lostETH = upperSum(depPercentile)/1e18
    # Avg # of tries to win is 1/total_probability = 1 / ((1/n) * (1-depPercentile/100))
    # Convert # of tries to year(s). 
    yearsToWin = 1 / ((1/n) * (1-(depPercentile/100))) * 12 / 60 / 60 / 24 / 365.25
    abovePercent = lostETH / PPVtotal  * 100
    #nextrow = [d, depPercentile, yearsToWin, lostETH, abovePercent]
    df[d] = [ d, depPercentile, yearsToWin, lostETH, abovePercent ]
    
    #print(f'{(nextrow):.f2}')

pd.set_option('precision', 2)
print(df)



## Reference: https://ethminingpools.tk/#best 

####PPVearned = OUTPUTdata[:,5]/1e18
### print(OUTPUTdata[:,5])
##plt.hist(x=PPVblocks/1e19, bins='auto', color='lightblue')
##plt.suptitle('Probability mass function of PPV (ETH) by block proposed')
##plt.title('Modeled from ' + str(cntBlocks[0]) + ' blocks recorded from etherscan.io.')
##plt.xlabel('Amount of PPV (ETH) per block')
##plt.ylabel('Probability')
##plt.xlim([0, 1])
####plt.ylim([0, 25000])
##plt.axvline(x=np.percentile(PPVblocks, 50, axis=0)/1e18, color='blue', linestyle='solid')
##plt.axvline(x=np.percentile(PPVblocks, 84.1, axis=0)/1e18, color='green', linestyle='dotted')
##plt.axvline(x=np.percentile(PPVblocks, 95, axis=0)/1e18, color='red', linestyle='--')
##plt.axvline(x=np.percentile(PPVblocks, 97.7, axis=0)/1e18, color='red', linestyle='dotted')
##plt.axvline(x=np.percentile(PPVblocks, 99, axis=0)/1e18, color='purple', linestyle='--')
##plt.axvline(x=np.percentile(PPVblocks, 99.9, axis=0)/1e18, color='purple', linestyle='dotted')
##
##
##plt.text((np.percentile(PPVblocks, 50, axis=0)/1e18),0,'                    50th percentile',rotation=90)
##plt.text((np.percentile(PPVblocks, 84.1, axis=0)/1e18),0,'                    1sigma',rotation=90)
##plt.text((np.percentile(PPVblocks, 95, axis=0)/1e18),0,'                    95th percentile',rotation=90)
##plt.text((np.percentile(PPVblocks, 97.7, axis=0)/1e18),0,'                    2sigma',rotation=90)
##plt.text((np.percentile(PPVblocks, 99, axis=0)/1e18),0,'                    99th percentile',rotation=90)
##plt.text((np.percentile(PPVblocks, 99.9, axis=0)/1e18),0,'                    3sigma',rotation=90)
##plt.show()
