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
            
##print("Loading the etherscan.io blockRewards data\n")

PPVblocks = loadFlashBotCSV()
cntBlocks = np.shape(PPVblocks)


#x = [el for el in range(500)]
t = int(input("Enter the number of years you will be node operating: "))
secValidating = int(t*31556952/12)

n = 400000 #number of validators from https://beaconcha.in/
m = 3877 #ETH last 30 days from https://explore.flashbots.net/
PPVblock = m / (6750 * 32)  #PPV per block where 6750 epochs per month 32 slots per epoch

# https://github.com/flashbots/eth2-research/blob/main/notebooks/mev-in-eth2/miner-REV.csv

mcTries = 100000 #The number of monte carlo tries to model.
var = binom.rvs(secValidating, (1/n), size=mcTries)

##print("var")
##print(var)
##print("PPVblocks")
##print(PPVblocks)

OUTPUTdata = np.zeros(shape=(0,6))# create empty np array 0 rows 6 columns
i = 0

for _ in var:
    blocks = var.astype(int)[i]    
    blockRewards = np.empty([0])# create empty np array

    #print(f"The number of block proposals by this minipool is {blocks}")
    
    for block in range(blocks):
        REV = random.choice(PPVblocks)
        blockRewards = np.append(blockRewards, [REV], axis=0).astype(np.float)

    try:
        blockMin = np.amin(blockRewards)
        blockMax = np.amax(blockRewards)
        blockMean = np.mean(blockRewards)
        blockSum = np.sum(blockRewards)
    except ValueError: #Needed when the validaoator is prediced to receive 0 blocks, more likely the shourt the time validating.
        blockMin = 0
        blockMax = 0
        blockMean = 0
        blockSum = 0


    newrow = [i, blocks, blockMin, blockMax, blockMean, blockSum]
 
    OUTPUTdata = np.vstack([OUTPUTdata, newrow])
    
    i = i + 1


num_rows = np.shape(OUTPUTdata)[0]
print(f"The number of validators assumed was {n}.")
print(f"The number of monte carlo tries evaluated was {num_rows}.")
print(f' number of blocks analyzed = {cntBlocks[0]}')
print(f' The timespan of block rewards sampled is {cntBlocks[0]*12/(60*60*24):.1f} day(s)')
tspan = cntBlocks[0]*12/(60*60*24)
# print(OUTPUTdata)
miniMean = np.mean(OUTPUTdata, axis=0)
miniMedian = np.median(OUTPUTdata, axis=0)

print(f"\nProposer Payment Statistical Analysis:")
print(f"\nThe mean (average) stats of the OUTPUTdata are :")
print(f"   mean min {(miniMean[2]/1e18):.4f} ETH in a block ")
print(f"   mean max {(miniMean[3]/1e18):.4f} ETH in block ")
print(f"   mean avg {(miniMean[4]/1e18):.4f} ETH/block")
print(f"   mean sum {(miniMean[5]/1e18):.4f} ETH in {t} year(s)")
print(f"   mean avg {(miniMean[5]/1e18/t):.4f} ETH/yr")

print(f"\n        m = {(miniMean[5]/1e18/t):.2f} ETH/yr")


print(f"\nThe median stats of the OUTPUTdata are :")
print(f"   median min {(miniMedian[2]/1e18):.4f} ETH in a block")
print(f"   median max {(miniMedian[3]/1e18):.4f} ETH in a block")
print(f"   median avg {(miniMedian[4]/1e18):.4f} ETH/block")
print(f"   median sum {(miniMedian[5]/1e18):.4f} ETH in {t} year(s)")
print(f"   median avg {(miniMedian[5]/1e18)/t:.4f} ETH/yr")

print(f"\nBased on the mean avg {(miniMean[4]/1e18):.4f} ETH/block we expect {(miniMean[4]/1e18*50400):.0f} ETH in PPV for 7D of PPV")
print(f"Based on the mean avg {(miniMean[4]/1e18):.4f} ETH/block we expect {(miniMean[4]/1e18*216000):.0f} ETH in PPV for 1M of PPV")

print(f"\nThe         50% minipool will block propose {np.percentile(OUTPUTdata, 50, axis=0)[1]/t:.1f} times a year.")
print(f"The         50% min PPV is {(np.percentile(OUTPUTdata, 50, axis=0)[2]/1e18):.4f} ETH.")
print(f"The         50% max PPV is {(np.percentile(OUTPUTdata, 50, axis=0)[3]/1e18):.4f} ETH.")
print(f"The         50% avg PPV is {(np.percentile(OUTPUTdata, 50, axis=0)[4]/1e18):.4f} ETH/proposal.")
print(f"The         50% sum PPV is {(np.percentile(OUTPUTdata, 50, axis=0)[5]/1e18):.4f} ETH over {t} year(s).")
print(f"The         50% avg PPV is {(np.percentile(OUTPUTdata, 50, axis=0)[5]/1e18)/t:.4f} ETH/yr.")

print(f"\nThe 1sigma 84.1% minipool will block propose {(np.percentile(OUTPUTdata, 84.1, axis=0)[1]/t):.1f} times a year.")
print(f"The 1sigma 84.1% min PPV is {(np.percentile(OUTPUTdata, 84.1, axis=0)[2]/1e18):.4f} ETH.")
print(f"The 1sigma 84.1% max PPV is {(np.percentile(OUTPUTdata, 84.1, axis=0)[3]/1e18):.4f} ETH.")
print(f"The 1sigma 84.1% avg PPV is {(np.percentile(OUTPUTdata, 84.1, axis=0)[4]/1e18):.4f} ETH/proposal.")
print(f"The 1sigma 84.1% sum PPV is {(np.percentile(OUTPUTdata, 84.1, axis=0)[5]/1e18):.4f} ETH over {t} year(s).")
print(f"The 1sigma 84.1% avg PPV is {(np.percentile(OUTPUTdata, 84.1, axis=0)[5]/1e18)/t:.4f} ETH/yr.")

print(f"\nThe        95% minipool will block propose {(np.percentile(OUTPUTdata, 95, axis=0)[1]/t):.1f} times a year.")
print(f"The        95% min PPV is {(np.percentile(OUTPUTdata, 95, axis=0)[2]/1e18):.4f} ETH.")
print(f"The        95% max PPV is {(np.percentile(OUTPUTdata, 95, axis=0)[3]/1e18):.4f} ETH.")
print(f"The        95% avg PPV is {(np.percentile(OUTPUTdata, 95, axis=0)[4]/1e18):.4f} ETH/proposal.")
print(f"The        95% sum PPV is {(np.percentile(OUTPUTdata, 95, axis=0)[5]/1e18):.4f} ETH over {t} year(s).")
print(f"The        95% avg PPV is {(np.percentile(OUTPUTdata, 95, axis=0)[5]/1e18)/t:.4f} ETH/yr.")

print(f"\nThe 2sigma 97.7% minipool will block propose {(np.percentile(OUTPUTdata, 97.7, axis=0)[1]/t):.1f} times a year.")
print(f"The 2sigma 97.7% min PPV is {(np.percentile(OUTPUTdata, 97.7, axis=0)[2]/1e18):.4f} ETH.")
print(f"The 2sigma 97.7% max PPV is {(np.percentile(OUTPUTdata, 97.7, axis=0)[3]/1e18):.4f} ETH.")
print(f"The 2sigma 97.7% avg PPV is {(np.percentile(OUTPUTdata, 97.7, axis=0)[4]/1e18):.4f} ETH/proposal.")
print(f"The 2sigma 97.7% sum PPV is {(np.percentile(OUTPUTdata, 97.7, axis=0)[5]/1e18):.4f} ETH over {t} year(s).")
print(f"The 2sigma 97.7% avg PPV is {(np.percentile(OUTPUTdata, 97.7, axis=0)[5]/1e18)/t:.4f} ETH/yr.")

print(f"\nThe        99% minipool will block propose {(np.percentile(OUTPUTdata, 99, axis=0)[1]/t):.1f} times a year.")
print(f"The        99% min PPV is {(np.percentile(OUTPUTdata, 99, axis=0)[2]/1e18):.4f} ETH.")
print(f"The        99% max PPV is {(np.percentile(OUTPUTdata, 99, axis=0)[3]/1e18):.4f} ETH.")
print(f"The        99% avg PPV is {(np.percentile(OUTPUTdata, 99, axis=0)[4]/1e18):.4f} ETH/proposal.")
print(f"The        99% sum PPV is {(np.percentile(OUTPUTdata, 99, axis=0)[5]/1e18):.4f} ETH over {t} year(s).")
print(f"The        99% avg PPV is {(np.percentile(OUTPUTdata, 99, axis=0)[5]/1e18)/t:.4f} ETH/yr.")

print(f"\nThe 3sigma 99.9% minipool will block propose {(np.percentile(OUTPUTdata, 99.9, axis=0)[1]/t):.1f} times a year.")
print(f"The 3sigma 99.9% min PPV is {(np.percentile(OUTPUTdata, 99.9, axis=0)[2]/1e18):.4f} ETH.")
print(f"The 3sigma 99.9% max PPV is {(np.percentile(OUTPUTdata, 99.9, axis=0)[3]/1e18):.4f} ETH.")
print(f"The 3sigma 99.9% avg PPV is {(np.percentile(OUTPUTdata, 99.9, axis=0)[4]/1e18):.4f} ETH/proposal.")
print(f"The 3sigma 99.9% sum PPV is {(np.percentile(OUTPUTdata, 99.9, axis=0)[5]/1e18):.4f} ETH over {t} year(s).")
print(f"The 3sigma 99.9% avg PPV is {(np.percentile(OUTPUTdata, 99.9, axis=0)[5]/1e18)/t:.4f} ETH/yr.")

#OUTPUTcsv = np.vstack([OUTPUTcsv, OUTPUTdata])
np.savetxt("OUTPUTdata.csv", OUTPUTdata, delimiter=",", header="trial, proposals, blockMin, blockMax, blockMean, blockSum")


## Reference: https://ethminingpools.tk/#best 

PPVearned = OUTPUTdata[:,5]/1e18
# print(OUTPUTdata[:,5])
plt.hist(x=PPVearned, bins='auto', color='lightgreen')
plt.suptitle('Predicted Probability Mass Function of Total Proposer Payments (ETH) for ' +str(t)+ ' year(s)')
plt.title('Assuming ' + str(n) + ' validators as modeled by ' +str(num_rows)+ ' monte carlo tries. The historic blockchain proposer payment data was sampled over ' + str(tspan) +' days.')
plt.xlabel('Amount of Proposer Payments (ETH) in ' +str(t)+ ' year(s)')
plt.ylabel('Probability')
plt.xlim([0, 20])
plt.ylim([0, 3000])
plt.axvline(x=np.percentile(OUTPUTdata, 50, axis=0)[5]/1e18, color='blue', linestyle='solid')
plt.axvline(x=np.percentile(OUTPUTdata, 84.1, axis=0)[5]/1e18, color='green', linestyle='dotted')
plt.axvline(x=np.percentile(OUTPUTdata, 95, axis=0)[5]/1e18, color='red', linestyle='--')
plt.axvline(x=np.percentile(OUTPUTdata, 97.7, axis=0)[5]/1e18, color='red', linestyle='dotted')
plt.axvline(x=np.percentile(OUTPUTdata, 99, axis=0)[5]/1e18, color='purple', linestyle='--')
plt.axvline(x=np.percentile(OUTPUTdata, 99.9, axis=0)[5]/1e18, color='purple', linestyle='dotted')


plt.text((np.percentile(OUTPUTdata, 50, axis=0)[5]/1e18),0,'                    50th percentile',rotation=90)
plt.text((np.percentile(OUTPUTdata, 84.1, axis=0)[5]/1e18),0,'                    1sigma',rotation=90)
plt.text((np.percentile(OUTPUTdata, 95, axis=0)[5]/1e18),0,'                    95th percentile',rotation=90)
plt.text((np.percentile(OUTPUTdata, 97.7, axis=0)[5]/1e18),0,'                    2sigma',rotation=90)
plt.text((np.percentile(OUTPUTdata, 99, axis=0)[5]/1e18),0,'                    99th percentile',rotation=90)
plt.text((np.percentile(OUTPUTdata, 99.9, axis=0)[5]/1e18),0,'                    3sigma',rotation=90)
plt.show()
