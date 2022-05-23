
# Adapted from : https://pintail.xyz/posts/beacon-chain-validator-rewards/

# define annualised base reward (measured in ETH) for n validators
# assuming all validators have an effective balance of 32 ETH

# 5.9.2022 This just takes an average MEV/bock and makes an estimate using the binomial
# probability. It does not take into account the high varability or MEV blocks. 

import math
import matplotlib.pyplot as plt
from scipy.stats import binom
import numpy as np
import random
import csv


EPOCHS_PER_YEAR = 82180

def annualised_base_reward(n):
    return EPOCHS_PER_YEAR * 512 / math.sqrt(n * 32e9)
            
    
######def loadFlashBotCSV():
######    
######    from numpy import genfromtxt
######    flashbot_data = genfromtxt('minerREV.csv', delimiter=',')
######
######    #print("This is flashbot_data") # debug line
######    #print(flashbot_data) # debug line
######    return flashbot_data
######            
######
######
######## LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL
######## Load flashbots data
#######Load the data back from flashbots and at the same time strips commas from the readback
######
######
######print('===================================================')
######print("+ Begining")
######print('===================================================')
######print(' ')
######
######
######print("Loading the flashbot REV per block data\n")
######
######MEVblocks = loadFlashBotCSV()



x = [el for el in range(500)]


t = int(input("Enter the number of years you will be node operating: "))
secValidating = int(t*365.25 * 24 * 60 * 60 /12)
print(f"Seconds validating: {secValidating}")

n = 400000 #number of validators from https://beaconcha.in/
n1 = 625000
m = 2827 #ETH last 30 days from https://explore.flashbots.net/
######MEVblock = m / (6750 * 32)  #MEV per block where 6750 epochs per month 32 slots per epoch

#MEVblock = 0.185242203  #MEV per block (trimmed mean with 1% trimmed) from Flashbots csv data https://hackmd.io/@flashbots/mev-in-eth2 https://dashboard.flashbots.net/
# https://github.com/flashbots/eth2-research/blob/main/notebooks/mev-in-eth2/miner-REV.csv

# Last number is inverse of the number of validaotrs: 1/n the chance of being selected to propose
# There are 31556952 / 12 = 2629746 slots per year where 31556952 = seconds in a year 
# X is the chart x input number of propsal oppurtunities a year
# Y is the pmf (probability mass function) - number of propsal opportunites per year.

y = binom.pmf(x, secValidating, (1/n))
y1 = binom.pmf(x, secValidating, (1/n1))

fig, ax = plt.subplots()
ax.bar(x, y, label=str(n) + ' validators')
ax.bar(x, y1, alpha=0.75, label=str(n1) + ' validators')
ax.set_xlim(xmin=0)
ax.set_xlim(xmax=20)
plt.xticks(range(1, 20))
ax.set_ylim(ymin=0)
plt.suptitle('Probability mass function per ' + str(t) + ' year(s)')
ax.set_title('')
ax.set_xlabel('Number of block proposal opportunities in ' + str(t) + ' year(s)')
ax.set_ylabel('Probability')
plt.legend()
plt.show()


####### adjust the last number to be:
######
######lmu = binom.ppf([0.01, 0.5, 0.99],secValidating, (1/n))
######mean = binom.mean(t*31556952/12, (1/n))
######median = binom.median(t*31556952/12, (1/n))
######var = binom.var(t*31556952/12, (1/n))
######std = binom.std(t*31556952/12, (1/n))
######
######print(f"The mean {int(mean)} blocks in {t} year(s).\n")
######print(f"The median {int(median)} blocks in {t} year(s).\n")
######print(f"The std {int(std)} blocks in {t} year(s).\n")
######
####### adjust the last number to be the # of validatorss
######avg = 31556952 / (12 * n)
######
######print(f"Flashbots is reporting (https://explore.flashbots.net/) {m} ETH of Realized MEV in the last 30 days.\n") 
######print(f"The average MEV per block is {MEVblock:.3f} ETH.\n")
######print(f"With {str(n)} validators, the mean number of blocks proposed per minipool per year is {avg:.0f} generating an estimated {avg*MEVblock:.2f} ETH/yr in MEV.")
######print(f"The unluckiest 1% of minipools will have the opportunity to produce at most {int(lmu[0])} blocks in {t} year(s) generating an estimated {int(lmu[0])*MEVblock:.2f} ETH in MEV")
######print(f"The median minipools will have the opportunity to produce {int(lmu[1])} blocks in {t} year(s) generating an estimated {int(lmu[1])*MEVblock:.2f} ETH in MEV")
######print(f"The luckiest 1% of minipools will have the opportunity to produce at least {int(lmu[2])} blocks in {t} year(s) generating an estimated {int(lmu[2])*MEVblock:.2f} ETH in MEV\n")
######
######



## Reference: https://ethminingpools.tk/#best 
