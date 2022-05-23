# source based on : https://medium.com/future-vision/plotting-equations-in-python-d0edd9f088c8
import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd

## Assumes that no RPL is penalitzed for stealing, on the ETH deposit and ETH rewards. 
n = 625000 # number of validators
####base_reward =  82180 * 512 / math.sqrt(n * 32e9)
####ideal_reward = 4 * base_reward

#b = ideal_reward #Beacon chain in ETH/yr include only eth2.0 APR rewards (from https://rocketpool.net/node-operators)
b = 1.11 # from more accutate APR calculation
m = 0.72 #PPV Annual average PPV in ETH eared in a year per minipool; includes inclusion fees and coinbase payments.

c = 0.10 #Comission Set node commision
p = 1 #Penality assessed for defecting
f = 1 - p #Fine amount5
#d = Deposit amount

# Create a dataFrame
df = pd.DataFrame([],['NO Deposit', 'minipool APR', 'Beacon APR', 'PPVonly APR' ])

# Create and array of time (t) in years
t = np.array(range(20))

def honestROI(d):
    s = d / 32 #NO Share
    return (s*b*t)+((1-s)*c*b*t)+(s*m*t)+((1-s)*c*m*t)+(d) #Honest NO formula

def rougeROI(d):
    s = d / 32 #NO Share
    return (f*s*b*t)+(f*(1-s)*c*b*t)+(m*t)+(f*d) #Rougee NO formula

def minipoolAPR(d):
    return (honestROI(d)-d)/d #CombinedAPR

def beaconAPR(d):
    s = d / 32 #NO Share
    return ((s*b*t)+((1-s)*c*b*t))/d #Beacon Chain only APR

def ppvAPR(d):
    s = d / 32 #NO Share
    return ((s*m*t)+((1-s)*c*m*t))/d #PPV only APR



Deposits = [2,4,6,6.4,8,16,32]
t = 1
print(f'Assuming :')
print(f'n = {n} Validators')
print(f'c = {c*100}% Node Commission')
print(f'm = {m} ETH/yr average PPV per minipool')
print(f'b = {b} ETH /yr average beacon chain (Consensys Layer) rewards per minipool')


for d in Deposits:
    df[d] = [d, minipoolAPR(d)*100, beaconAPR(d)*100, ppvAPR(d)*100]

pd.set_option('precision', 2)

df_t = df.T # or df1.transpose()
df_t

print('\n')
print(df_t)
# Color maps form : http://scipy.github.io/old-wiki/pages/Cookbook/Matplotlib/Show_colormaps
df_t[['Beacon APR','PPVonly APR']].plot(kind='bar', stacked=True, colormap='Accent')

# Add a title
plt.suptitle('MiniPool Node Operator APR Estimates')
plt.title('Assumes ' + str(n) + ' validators; average PPV of ' + str(m) +'ETH/yr; Beacon rewards of ' + str(b) +'ETH/yr; Node Commission of ' + str(c*100) + '%.')

# Add X and y Label
plt.xlabel("NO Deposit Size")
plt.ylabel("APR")

label_2 = str("{:.1f}".format(minipoolAPR(2)*100)) + "%"
label_4 = str("{:.1f}".format(minipoolAPR(4)*100)) + "%"
label_6 = str("{:.1f}".format(minipoolAPR(6)*100)) + "%"
label_64 = str("{:.1f}".format(minipoolAPR(6.4)*100)) + "%"
label_8 = str("{:.1f}".format(minipoolAPR(8)*100)) + "%"
label_16 = str("{:.1f}".format(minipoolAPR(16)*100)) + "%"
label_32 = str("{:.1f}".format(minipoolAPR(32)*100)) + "%"

plt.text(0,2,label_2, backgroundcolor='w', horizontalalignment='center')
plt.text(1,2,label_4, backgroundcolor='w', horizontalalignment='center')
plt.text(2,2,label_6, backgroundcolor='w', horizontalalignment='center')
plt.text(3,2,label_64, backgroundcolor='w', horizontalalignment='center')
plt.text(4,2,label_8, backgroundcolor='w', horizontalalignment='center')
plt.text(5,2,label_16, backgroundcolor='w', horizontalalignment='center')
plt.text(6,2,label_32, backgroundcolor='w', horizontalalignment='center')
plt.text(6,10,'Solo\nStaking', horizontalalignment='center')

plt.show()

