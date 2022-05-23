
# Source: https://pintail.xyz/posts/beacon-chain-validator-rewards/


# define annualised base reward (measured in ETH) for n validators
# assuming all validators have an effective balance of 32 ETH
import math

EPOCHS_PER_YEAR = 82180

def annualised_base_reward(n):
    return EPOCHS_PER_YEAR * 512 / math.sqrt(n * 32e9)


import matplotlib.pyplot as plt



# plot pdf

##from scipy.stats import binom
##
##x = [el for el in range(51)]
##y = binom.pmf(x, 31556952/12/6, 8.09e-6)
##
##fig, ax = plt.subplots(figsize=(12, 8))
##ax.bar(x, y)
##ax.set_xlim(xmin=0)
##ax.set_ylim(ymin=0)
##ax.set_title('Probability mass function (123,492 validators) — number of block proposal RP minipool opportunities per 2 month beta3 window')
##ax.set_xlabel('Number of block proposal opportunities in 2 months')
##ax.set_ylabel('Probability')
##
##lmu = binom.ppf([0.01, 0.5, 0.99],31556952/12/6, 8.09e-6)
##avg = 31556952 / (12 * 6 * 123492)
##print(f"With 123,492 validators, the mean number of blocks proposed per validator per 2 month beta period is {avg:.2f}\n")
##print(f"The unluckiest 1% of RP minipools will have the opportunity to produce at most {int(lmu[0])} blocks in a year")
##print(f"The median (average) RP minipools will have the opportunity to produce {int(lmu[1])} blocks in a year")
##print(f"The luckiest 1% of RP minipools will have the opportunity to produce at least {int(lmu[2])} blocks in a year")
##
##plt.show()

# MAINNET plot pdf

from scipy.stats import binom

x = [el for el in range(51)]

n = 143981

# Ken: lasr number is inverse of the number of validaotrs: 1/n
y = binom.pmf(x, 31556952/12, (1/n))

fig, ax = plt.subplots(figsize=(12, 8))
ax.bar(x, y)
ax.set_xlim(xmin=0)
ax.set_ylim(ymin=0)
ax.set_title('Probability mass function (121,152 validators) — number of block proposal opportunities per year')
ax.set_xlabel('Number of block proposal opportunities in a year')
ax.set_ylabel('Probability')

# adjust the last number to be:

lmu = binom.ppf([0.01, 0.5, 0.99],31556952/12, (1/n))


# adjust the last number to be the # of validatorss
avg = 31556952 / (12 * n)
print(f"With {str(n)} validators, the mean number of blocks proposed per validator per year is {avg:.2f}\n")
print(f"The unluckiest 1% of validators will have the opportunity to produce at most {int(lmu[0])} blocks in a year")
print(f"The median (average) validator will have the opportunity to produce {int(lmu[1])} blocks in a year")
print(f"The luckiest 1% of validators will have the opportunity to produce at least {int(lmu[2])} blocks in a year")

plt.show()

## Reference: https://ethminingpools.tk/#best 
