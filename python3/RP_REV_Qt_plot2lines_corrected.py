# source based on : https://medium.com/future-vision/plotting-equations-in-python-d0edd9f088c8
import matplotlib.pyplot as plt
import numpy as np
import math


## Assumes that no RPL is penalitzed for stealing, on the ETH deposit and ETH rewards. 
n = 625000 # number of validators

b = 1.11 # from more accutate APR calculation
m = 0.72 #MEV Annual average MEV in ETH eared in a year per minipool; includes inclusion fees and coinbase payments.

c = 0.15 #Comission Set node commision
p = 1 #Penality assessed for defecting
f = 1 - p #Fine amount
#d = Deposit amount


# Create and array of time (t) in years
t = np.array(range(50))

def honestROI(d):
    s = d / 32 #NO Share
    y = (s*b*t)+((1-s)*c*b*t)+(s*m*t)+((1-s)*c*m*t)+(d) #Honest NO formula
    return y 

def rougeROI(d):
    s = d / 32 #NO Share
    z = (f*s*b*t)+(f*(1-s)*c*b*t)+(m*t)+(f*d) #Rougee NO formula
    return z

def Qt(d):
    s = d / 32
    q = (d*f*-d)/(b*s+b*c-b*c*s+s*m+c*m-c*s*m-b*s*f-b*c*f+b*c*s*f-m)#
    return q


# Create the plot
plt.plot(t,honestROI(2),'--',label='Honest NO 2 ETH depoist')
plt.plot(t,honestROI(4),'--',label='Honest NO 4 ETH depoist')
plt.plot(t,honestROI(6),'--',label='Honest NO 6 ETH depoist')
plt.plot(t,honestROI(6.4),'--',label='Honest NO 6.4 ETH depoist')
plt.plot(t,honestROI(8),'--',label='Honest NO 8 ETH depoist')
plt.plot(t,honestROI(16),'--',label='Honest NO 16 ETH depoist')
plt.plot(t,rougeROI(16),label='Dishonest NO',color="black") #Note does not matter the deposit number if p = 1

# Add a title
plt.suptitle('Dishonest vs Honest Rocket Pool NO Returns (Intercept = Qt)')
plt.title('Assumes ' + str(n) + ' validators')
# Add X and y Label
plt.xlabel('Time in year(s)')
plt.ylabel('Earned Revenue and Exited Deposit in ETH')

# Add a grid
plt.grid(alpha=.4,linestyle='--')

# Add a Legend
plt.legend()
txt = "Inputs: penality=" + str(1-f) + ", average MEV m=" + str(m) + "ETH/yr, average Beacon rewards b=" + str(b) + " ETH/yr"
plt.text(6, 65, txt)
plt.xlim([0, 25])

# Show the plot
plt.show()

print('INPUTS:')
print(f'Average validator Beacon Chain rewards (ETH/yr)  b = {b}')
print(f'Minipool commission                              c = {c}')
#print(f'NO deposit (ETH)                                 d = {d}') 
print(f'Fraction returned (f = 1-p)                      f = {f}') 
print(f'Average validator PPV rewards (ETH/yr)           m = {m}')
print(f'Number of validators                             n = {n}')
print(f'Stealing penalty                                 p = {p}')


#print('t = Time validating in years 
print(f'\n')

print(f'The Qt for a  2   ETH NO deposit is {Qt(2):.2f} year(s)')
print(f'The Qt for a  4   ETH NO deposit is {Qt(4):.2f} year(s)')
print(f'The Qt for a  6   ETH NO deposit is {Qt(6):.2f} year(s)')
print(f'The Qt for a  6.4 ETH NO deposit is {Qt(6.4):.2f} year(s)')
print(f'The Qt for a  8   ETH NO deposit is {Qt(8):.2f} year(s)')
print(f'The Qt for a 16   ETH NO deposit is {Qt(16):.2f} year(s)')
