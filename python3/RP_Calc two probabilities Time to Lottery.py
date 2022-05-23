# Adapted from : https://pintail.xyz/posts/beacon-chain-validator-rewards/
# define annualised base reward (measured in ETH) for n validators
# assuming all validators have an effective balance of 32 ETH
import math
import matplotlib.pyplot as plt
from scipy.stats import binom
import numpy as np
import random
import csv

##
##EPOCHS_PER_YEAR = 82180
##
##def annualised_base_reward(n):
##    return EPOCHS_PER_YEAR * 512 / math.sqrt(n * 32e9)
            
    
def loadFlashBotCSV():
    
    from numpy import genfromtxt
    flashbot_data = genfromtxt('blockReward.csv', delimiter=',')

    #print("This is flashbot_data") # debug line
    #print(flashbot_data) # debug line
    return flashbot_data
            


## LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL
## Load flashbots data
#Load the data back from flashbots and at the same time strips commas from the readback

########
########print('===================================================')
########print("+ Begining")
########print('===================================================')
########print(' ')
########
########
########print("Loading the etherscan.io blockRewards data\n")
########
########MEVblocks = loadFlashBotCSV()

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
proposalProb = 1/n
mevProb = 1-.9960622595488948


combineProb = proposalProb * mevProb

avgTimeToWin = 1 / combineProb * 12 / 60 / 60 / 24 / 365.25

print(proposalProb)
print(mevProb)
print(combineProb)


print(f'The time to winning the block lottery is {avgTimeToWin} year(s).')

######roll = 1
######print(1/n)
######rndm = random.random()
######
######def validate():
######    rndm = random.random()
######    global roll
######    #print(rndm)
######
######    while random.random() > (1/n):
######        roll = roll + 1
######    else:
######        #print('You proposed a block')
######        #print(f'The number of slots needed was {roll}')
######        REV = random.choice(MEVblocks)
######        #print(REV)
######    return REV
######
######while validate() < d*1e18:
######    validate()
######else:
######    print(f'The number of slots needed to reach NOdeposit was {roll}')
######    print(f'The time was {roll/2608200:.2f} years')


##
##OUTPUTdata = np.zeros(shape=(0,6))# create empty np array 0 rows 6 columns
##i = 0
##
##for _ in var:
##    blocks = var.astype(int)[i]    
##    blockRewards = np.empty([0])# create empty np array
##
##    #print(f"The number of block proposals by this minipool is {blocks}")
##    
##    for block in range(blocks):
##        REV = random.choice(MEVblocks)
##        blockRewards = np.append(blockRewards, [REV], axis=0).astype(np.float)
##
##    try:
##        blockMin = np.amin(blockRewards)
##        blockMax = np.amax(blockRewards)
##        blockMean = np.mean(blockRewards)
##        blockSum = np.sum(blockRewards)
##    except ValueError: #Needed when the validaoator is prediced to receive 0 blocks, more likely the shourt the time validating.
##        blockMin = 0
##        blockMax = 0
##        blockMean = 0
##        blockSum = 0
##

##    newrow = [i, blocks, blockMin, blockMax, blockMean, blockSum]
##    # print("This are the randomly selected block rewards from the previous dataset")
##    # print (blockRewards)
##    # print(f"The sum of min blockreward proposed is {blockMin:.4f}")
##    # print(f"The sum of max blockreward proposed is {blockMax:.4f}")
##    # print(f"The average(mean) of all blocks proposed is {blockMean:.4f}")
##    # print(f"The sum of all blocks proposed is {blockSum:.4f}")
##    # print(f"This monte carlo try generated the following data row {newrow}\n")
##    
##    OUTPUTdata = np.vstack([OUTPUTdata, newrow])
##    
##    i = i + 1
##
##
###print(var[1])
###print(OUTPUTdata[1])
##
##num_rows = np.shape(OUTPUTdata)[0]
##print(f"The number of validators assumed was {n}.")
##print(f"The number of monte carlo tries evaluated was {num_rows}.")
### print(OUTPUTdata)
##miniMean = np.mean(OUTPUTdata, axis=0)
##miniMedian = np.median(OUTPUTdata, axis=0)
##
##print(f"\nThe mean (average) stats of the OUTPUTdata are :")
##print(f"   mean min {(miniMean[2]/1e18):.4f} ETH in a block ")
##print(f"   mean max {(miniMean[3]/1e18):.4f} ETH in block ")
##print(f"   mean avg {(miniMean[4]/1e18):.4f} ETH/block")
##print(f"   mean sum {(miniMean[5]/1e18):.4f} ETH in {t} year(s)")
##print(f"   mean avg {(miniMean[5]/1e18/t):.4f} ETH/yr")
##
##print(f"\nThe median stats of the OUTPUTdata are :")
##print(f"   median min {(miniMedian[2]/1e18):.4f} ETH in a block")
##print(f"   median max {(miniMedian[3]/1e18):.4f} ETH in a block")
##print(f"   median avg {(miniMedian[4]/1e18):.4f} ETH/block")
##print(f"   median sum {(miniMedian[5]/1e18):.4f} ETH in {t} year(s)")
##print(f"   median avg {(miniMedian[5]/1e18)/t:.4f} ETH/yr")
##
##print(f"\nBased on the mean avg {(miniMean[4]/1e18):.4f} ETH/block we expect {(miniMean[4]/1e18*50400):.0f} ETH for 7D")
##print(f"Based on the mean avg {(miniMean[4]/1e18):.4f} ETH/block we expect {(miniMean[4]/1e18*216000):.0f} ETH for 1M")
##
##print(f"\nThe         50% minipool will block propose {np.percentile(OUTPUTdata, 50, axis=0)[1]/t:.1f} times a year.")
##print(f"The         50% min MEV is {(np.percentile(OUTPUTdata, 50, axis=0)[2]/1e18):.4f} ETH.")
##print(f"The         50% max MeV is {(np.percentile(OUTPUTdata, 50, axis=0)[3]/1e18):.4f} ETH.")
##print(f"The         50% avg MEV is {(np.percentile(OUTPUTdata, 50, axis=0)[4]/1e18):.4f} ETH/proposal.")
##print(f"The         50% sum MEV is {(np.percentile(OUTPUTdata, 50, axis=0)[5]/1e18):.4f} ETH over {t} year(s).")
##print(f"The         50% avg MEV is {(np.percentile(OUTPUTdata, 50, axis=0)[5]/1e18)/t:.4f} ETH/yr.")
##
##print(f"\nThe 1sigma 84.1% minipool will block propose {(np.percentile(OUTPUTdata, 84.1, axis=0)[1]/t):.1f} times a year.")
##print(f"The 1sigma 84.1% min MEV is {(np.percentile(OUTPUTdata, 84.1, axis=0)[2]/1e18):.4f} ETH.")
##print(f"The 1sigma 84.1% max MEV is {(np.percentile(OUTPUTdata, 84.1, axis=0)[3]/1e18):.4f} ETH.")
##print(f"The 1sigma 84.1% avg MEV is {(np.percentile(OUTPUTdata, 84.1, axis=0)[4]/1e18):.4f} ETH/proposal.")
##print(f"The 1sigma 84.1% sum MEV is {(np.percentile(OUTPUTdata, 84.1, axis=0)[5]/1e18):.4f} ETH over {t} year(s).")
##print(f"The 1sigma 84.1% avg MEV is {(np.percentile(OUTPUTdata, 84.1, axis=0)[5]/1e18)/t:.4f} ETH/yr.")
##
##print(f"\nThe        95% minipool will block propose {(np.percentile(OUTPUTdata, 95, axis=0)[1]/t):.1f} times a year.")
##print(f"The        95% min MEV is {(np.percentile(OUTPUTdata, 95, axis=0)[2]/1e18):.4f} ETH.")
##print(f"The        95% max MEV is {(np.percentile(OUTPUTdata, 95, axis=0)[3]/1e18):.4f} ETH.")
##print(f"The        95% avg MEV is {(np.percentile(OUTPUTdata, 95, axis=0)[4]/1e18):.4f} ETH/proposal.")
##print(f"The        95% sum MEV is {(np.percentile(OUTPUTdata, 95, axis=0)[5]/1e18):.4f} ETH over {t} year(s).")
##print(f"The        95% avg MEV is {(np.percentile(OUTPUTdata, 95, axis=0)[5]/1e18)/t:.4f} ETH/yr.")
##
##print(f"\nThe 2sigma 97.7% minipool will block propose {(np.percentile(OUTPUTdata, 97.7, axis=0)[1]/t):.1f} times a year.")
##print(f"The 2sigma 97.7% min MEV is {(np.percentile(OUTPUTdata, 97.7, axis=0)[2]/1e18):.4f} ETH.")
##print(f"The 2sigma 97.7% max MEV is {(np.percentile(OUTPUTdata, 97.7, axis=0)[3]/1e18):.4f} ETH.")
##print(f"The 2sigma 97.7% avg MEV is {(np.percentile(OUTPUTdata, 97.7, axis=0)[4]/1e18):.4f} ETH/proposal.")
##print(f"The 2sigma 97.7% sum MEV is {(np.percentile(OUTPUTdata, 97.7, axis=0)[5]/1e18):.4f} ETH over {t} year(s).")
##print(f"The 2sigma 97.7% avg MEV is {(np.percentile(OUTPUTdata, 97.7, axis=0)[5]/1e18)/t:.4f} ETH/yr.")
##
##print(f"\nThe        99% minipool will block propose {(np.percentile(OUTPUTdata, 99, axis=0)[1]/t):.1f} times a year.")
##print(f"The        99% min MEV is {(np.percentile(OUTPUTdata, 99, axis=0)[2]/1e18):.4f} ETH.")
##print(f"The        99% max MEV is {(np.percentile(OUTPUTdata, 99, axis=0)[3]/1e18):.4f} ETH.")
##print(f"The        99% avg MEV is {(np.percentile(OUTPUTdata, 99, axis=0)[4]/1e18):.4f} ETH/proposal.")
##print(f"The        99% sum MEV is {(np.percentile(OUTPUTdata, 99, axis=0)[5]/1e18):.4f} ETH over {t} year(s).")
##print(f"The        99% avg MEV is {(np.percentile(OUTPUTdata, 99, axis=0)[5]/1e18)/t:.4f} ETH/yr.")
##
##print(f"\nThe 3sigma 99.9% minipool will block propose {(np.percentile(OUTPUTdata, 99.9, axis=0)[1]/t):.1f} times a year.")
##print(f"The 3sigma 99.9% min MEV is {(np.percentile(OUTPUTdata, 99.9, axis=0)[2]/1e18):.4f} ETH.")
##print(f"The 3sigma 99.9% max MEV is {(np.percentile(OUTPUTdata, 99.9, axis=0)[3]/1e18):.4f} ETH.")
##print(f"The 3sigma 99.9% avg MEV is {(np.percentile(OUTPUTdata, 99.9, axis=0)[4]/1e18):.4f} ETH/proposal.")
##print(f"The 3sigma 99.9% sum MEV is {(np.percentile(OUTPUTdata, 99.9, axis=0)[5]/1e18):.4f} ETH over {t} year(s).")
##print(f"The 3sigma 99.9% avg MEV is {(np.percentile(OUTPUTdata, 99.9, axis=0)[5]/1e18)/t:.4f} ETH/yr.")
##
###OUTPUTcsv = np.vstack([OUTPUTcsv, OUTPUTdata])
##np.savetxt("OUTPUTdata.csv", OUTPUTdata, delimiter=",", header="trial, proposals, blockMin, blockMax, blockMean, blockSum")
##
##
#### Reference: https://ethminingpools.tk/#best 
##
##MEVearned = OUTPUTdata[:,5]/1e18
### print(OUTPUTdata[:,5])
##plt.hist(x=MEVearned, bins='auto', color='lightgreen')
##plt.suptitle('Probability mass function of Total MEV (ETH) for ' +str(t)+ ' year(s)')
##plt.title('Assuming ' + str(n) + ' validators as modeled by ' +str(num_rows)+ ' monte carlo tries.')
##plt.xlabel('Amount of MEV (ETH) in ' +str(t)+ ' year(s)')
##plt.ylabel('Probability')
##plt.xlim([0, 20])
##plt.ylim([0, 2500])
##plt.axvline(x=np.percentile(OUTPUTdata, 50, axis=0)[5]/1e18, color='blue', linestyle='solid')
##plt.axvline(x=np.percentile(OUTPUTdata, 84.1, axis=0)[5]/1e18, color='green', linestyle='dotted')
##plt.axvline(x=np.percentile(OUTPUTdata, 95, axis=0)[5]/1e18, color='red', linestyle='--')
##plt.axvline(x=np.percentile(OUTPUTdata, 97.7, axis=0)[5]/1e18, color='red', linestyle='dotted')
##plt.axvline(x=np.percentile(OUTPUTdata, 99, axis=0)[5]/1e18, color='purple', linestyle='--')
##plt.axvline(x=np.percentile(OUTPUTdata, 99.9, axis=0)[5]/1e18, color='purple', linestyle='dotted')
##
##
##plt.text((np.percentile(OUTPUTdata, 50, axis=0)[5]/1e18),0,'                    50th percentile',rotation=90)
##plt.text((np.percentile(OUTPUTdata, 84.1, axis=0)[5]/1e18),0,'                    1sigma',rotation=90)
##plt.text((np.percentile(OUTPUTdata, 95, axis=0)[5]/1e18),0,'                    95th percentile',rotation=90)
##plt.text((np.percentile(OUTPUTdata, 97.7, axis=0)[5]/1e18),0,'                    2sigma',rotation=90)
##plt.text((np.percentile(OUTPUTdata, 99, axis=0)[5]/1e18),0,'                    99th percentile',rotation=90)
##plt.text((np.percentile(OUTPUTdata, 99.9, axis=0)[5]/1e18),0,'                    3sigma',rotation=90)
##plt.show()
