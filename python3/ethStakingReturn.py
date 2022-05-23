
# Source: https://pintail.xyz/posts/beacon-chain-validator-rewards/


# define annualised base reward (measured in ETH) for n validators
# assuming all validators have an effective balance of 32 ETH
import math

EPOCHS_PER_YEAR = 82180

def annualised_base_reward(n):
    return EPOCHS_PER_YEAR * 512 / math.sqrt(n * 32e9)


### plot ideal ETH staking return
##
import matplotlib.pyplot as plt

## Ken first number is the amount of ETH staked on chart x axis
## second number is amt of ETH staked max range

n_validators = [n for n in range(int(10e6)//32,int(50e6)//32,3200)]
ideal_reward = [4 * annualised_base_reward(n) for n in n_validators]

fig = plt.figure(figsize=(12, 8))

ax1=fig.add_subplot(111, label="1")
ax2=fig.add_subplot(111, label="2", frame_on=False)

ax1.plot(n_validators, ideal_reward)
ax2.plot([n * 32e-6 for n in n_validators], [100 * r / 32 for r in ideal_reward])

ax1.set_xlabel('Number of validators')
ax1.set_ylabel('Ideal annual per-validator reward (ETH)')

ax2.set_title('Ideal Annualized Validator Returns')
ax2.xaxis.tick_top()
ax2.yaxis.tick_right()
ax2.xaxis.set_label_position('top') 
ax2.yaxis.set_label_position('right') 
ax2.set_xlabel('Total ETH staked (millions)')
ax2.set_ylabel('Annual yield on 32 ETH deposit (%)');

plt.show()
