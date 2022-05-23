# Calculte time for inactivity leak

# define annualised base reward (measured in ETH) for n validators
# assuming all validators have an effective balance of 32 ETH
import math



def penality(balance):
    n = 400000 #number of validators from https://beaconcha.in/
    total_balance = 32 #ETH last 30 days from https://explore.flashbots.net/tal beacon valic
    BalTotalActive = n * total_balance
    
    BaseRewardFactor = 64
    BaseRewardPerEpoch =  4


    effBalance = round((balance - 0.25),0)
    #print(f"Effictive balance: {effBalance:.6f}")
    basereward = ( effBalance * 1E9 * BaseRewardFactor ) / (math.sqrt(BalTotalActive * 1E9) * BaseRewardPerEpoch) / 1E9
    
    #print("{:10.6f}".format(basereward))
    penality = -3 * basereward
    balance = balance + penality
    #print(f"The final balance is {balance:.6f}")
    return balance

    
global balance
NOdeposit = 16.6 # float(input("What is the NO deposit in ETH?"))
balance = 32 #float(input("What is the minipool balance in ETH?")) Set this to 31.5 for a slahing time estimate
epochCnt = 0
#finalizing == 'true'

    

while balance > (32 - NOdeposit):
    balance = penality(balance)
    epochCnt = epochCnt +1 
    #print(f"The final balance is {balance:.6f}")

print(f"The final balance is {balance:.6f}")
print(f"The number of epoch(s) needed {epochCnt}")
print(f"The number of day(s) needed {(epochCnt * 6.4 / 1440):.1f}")
print(f"The number of year(s) needed {(epochCnt * 6.4 / 525600):.1f}")
