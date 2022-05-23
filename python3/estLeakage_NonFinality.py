# Calculte time for inactivity leak
# Formula from https://github.com/ethereum/consensus-specs/blob/dev/specs/phase0/beacon-chain.md#rewards-and-penalties-1


# Notes: https://github.com/ethereum/consensus-specs/issues/2883
# Description: https://github.com/ethereum/consensus-specs/blob/dev/specs/phase0/beacon-chain.md#rewards-and-penalties-1
import math
import matplotlib.pyplot as plt



EPOCHS_PER_YEAR = 82180

def annualised_base_reward(n):
    return EPOCHS_PER_YEAR * 512 / math.sqrt(n * 32e9)

INACTIVITY_PENALTY_QUOTIENT = 2**24

#Note this value will be upgraded to 2**24 after Phase 0 mainnet stabilizes to provide a faster recovery in the event of an inactivity leak.

def retained(n):
    return (1 - 1/INACTIVITY_PENALTY_QUOTIENT)**(n**2/2)


fig = plt.figure(figsize=(12, 8))
ax1=fig.add_subplot(111, label="1")
ax1.set_title('Inactivity Penalty')


# CHART IN EPOCHS AND FRACTION
# (Uncomment and comment out the other chart lines)
# +++++++++++++++++++++++++

#n_epochs = [n for n in range(0,10000)]
#balance = [retained(n) for n in n_epochs]
#ax1.plot(n_epochs, balance)
#ax1.set_ylabel('Fraction Retained')
#ax1.set_xlabel('Epochs')


# CHART IN DAYS AND ETH
# +++++++++++++++++++++++++
n_epochs = [n for n in range(0,10000)]
balance = [retained(n) for n in n_epochs]
days = [n * 6.4/1440 for n in n_epochs]
ETHbalance = [retained(n)*32 for n in n_epochs]
ax1.plot(days, ETHbalance)
plt.xlim([0, 45])
ax1.set_ylabel('ETH Retained')
ax1.set_xlabel('Days')

# Plot the INVERSE_SQRT_E_DROP_TIME := 2**13 epochs (about 36 days) is the time
# it takes the inactivity penalty to
# reduce the balance of non-participating validators to about 1/sqrt(e) ~= 60.6%

plt.axvline(x=2**13, color='k', linestyle='--')
plt.axvline(x=2**13 * 6.4/1444, color='g', linestyle='dotted')
plt.axhline(y=15.75, color='orange', linestyle='dashed')


#plt.show()

nodeDeposit = 17.6
startingBal = 32 #float(input("What is the minipool balance in ETH?")) Set this to 31.5 for a slahing time estimate

def epochtobalance():
    reduction = (startingBal-nodeDeposit) / 32
    return math.sqrt ( 2 * ((math.log(reduction)) / math.log(1 - 1/INACTIVITY_PENALTY_QUOTIENT)))

timetoempty = epochtobalance() * 6.4
print(f"The time to exhaust the node operator balance is {int(epochtobalance())} epochs")
print(f"The time to exhaust the node operator balance is {timetoempty:.1} minutes")
print(f"The time to exhaust the node operator balance is {(timetoempty/1440):.1f} days")

