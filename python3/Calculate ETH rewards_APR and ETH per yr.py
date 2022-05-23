# source based on : https://medium.com/future-vision/plotting-equations-in-python-d0edd9f088c8

# THis file is the correct full complex calcultion of the ETH staking returns
# It provides a more accurate APR calculation than the simple calculations 
import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd
from IPython.display import display


c = 0.15 #Comission Set node commision
p = 1 #Penality assessed for defecting
f = 1 - p #Fine amount

n_validators = [400000, 450000, 500000, 550000, 600000, 625000, 650000]

data = pd.DataFrame(columns=[
    'n_validators' ,
    'total_staked (ETH)',
    'annual_reward b (ETH)',
    'annual_yield (%)'
])

pd.options.display.float_format = '{:.2f}'.format

def beacon (n):
    global data
    totalStaked = int(n * 32)
    slotTimeInSec = 12
    slotsInEpoch = 32
    baseRewardFactor = 64
    weightDenominator = 64
    proposerWeight = 8

    averageNetworkPctOnline = 0.95
    validatorUptime = 0.99
    validatorDeposit = 32

    effectiveBalanceIncrement = 1e9

    epochPerYear = 31556908.8 / (slotTimeInSec * slotsInEpoch) # 60 * 60 * 24 * 365.242;
    #print(f'\n\n               epochPerYear = {epochPerYear}')

    baseRewardPerIncrement = (effectiveBalanceIncrement * baseRewardFactor) / math.sqrt(totalStaked * 1e9);
    #print(f'     baseRewardPerIncrement =   {baseRewardPerIncrement:.0f} Gwei; = {baseRewardPerIncrement/1e9:.6f} ETH') 

    baseGweiRewardFullValidator = validatorDeposit * 1e9 / effectiveBalanceIncrement * baseRewardPerIncrement;
    #print(f'baseGweiRewardFullValidator = {baseGweiRewardFullValidator:.0f} Gwei; = {baseGweiRewardFullValidator/1e9:.6f} ETH')

    reward = baseGweiRewardFullValidator * averageNetworkPctOnline * validatorUptime;
    #print(f'                     reward = {reward:.0f} Gwei; = {reward/1e9:.6f} ETH')

    offlineEpochGweiPentalty = baseGweiRewardFullValidator * ((weightDenominator - proposerWeight) / weightDenominator);
    #print(f'\n   offlineEpochGweiPentalty = {offlineEpochGweiPentalty:.0f} Gwei; = {offlineEpochGweiPentalty/1e9:.6f} ETH')

    penalty = offlineEpochGweiPentalty * (1 - validatorUptime);
    #print(f'                      penalty = {penalty:.0f} Gwei; = {penalty/1e9:.6f} ETH')

    b2 = epochPerYear * (reward - penalty) / 1e9;
    #print(f'\n b2 = {b2:.4f} ETH/year')

    APR = epochPerYear * (reward - penalty) / 1e9 / validatorDeposit;
    #print(f'APR = {APR*100:.2f}%')

    data = data.append({
        'n_validators': n,
        'total_staked (ETH)': totalStaked,
        'annual_reward b (ETH)': b2,
        'annual_yield (%)': APR*100
    }, ignore_index=True)


for n in n_validators:
    beacon(n)

display(data)
