
# Adapted from : https://pintail.xyz/posts/beacon-chain-validator-rewards/


# define annualised base reward (measured in ETH) for n validators
# assuming all validators have an effective balance of 32 ETH
import math

EPOCHS_PER_YEAR = 82180

def annualised_base_reward(n):
    return EPOCHS_PER_YEAR * 512 / math.sqrt(n * 32e9)


import matplotlib.pyplot as plt


from scipy.stats import binom

x = [el for el in range(51)]

n = 400000 #number of validators from https://beaconcha.in/
m = 36043 #ETH last 30 days from https://explore.flashbots.net/
#MEVblock = m / (6750 * 32)  #MEV per block where 6750 epochs per month
MEVblock = 0.224967456  #MEV per block from Flashbots csv data https://hackmd.io/@flashbots/mev-in-eth2 https://dashboard.flashbots.net/
# https://github.com/flashbots/eth2-research/blob/main/notebooks/mev-in-eth2/miner-REV.csv

# Ken: last number is inverse of the number of validaotrs: 1/n
y = binom.pmf(x, 31556952/12, (1/n))

fig, ax = plt.subplots(figsize=(12, 8))
ax.bar(x, y)
ax.set_xlim(0,20)
ax.set_xticks(range(1, 20))
ax.set_ylim(ymin=0)
ax.set_title('Probability mass function (' +str(n)+ ' validators) — number of block proposal opportunities per year')
ax.set_xlabel('Number of block proposal opportunities in a year')
ax.set_ylabel('Probability')

# adjust the last number to be:

lmu = binom.ppf([0.01, 0.5, 0.99],31556952/12, (1/n))


# adjust the last number to be the # of validatorss
avg = 31556952 / (12 * n)


print(f"With {str(n)} validators, the mean number of blocks proposed per validator per year is {avg:.2f} generating an estimated {avg*MEVblock:.2f} ETH in MEV\n")
print(f"The unluckiest 1% of validators will have the opportunity to produce at most {int(lmu[0])} blocks in a year generating an estimated {int(lmu[0])*MEVblock:.2f} ETH in MEV")
print(f"The median (average) validator will have the opportunity to produce {int(lmu[1])} blocks in a year generating an estimated {int(lmu[1])*MEVblock:.2f} ETH in MEV")
print(f"The luckiest 1% of validators will have the opportunity to produce at least {int(lmu[2])} blocks in a year generating an estimated {int(lmu[2])*MEVblock:.2f} ETH in MEV")

plt.show()

## Reference: https://ethminingpools.tk/#best 
