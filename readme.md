# A Risk Analysis of Rocket Pool Low Ether Bonded (LEB) Minipools
Ken Smith (@shtimseht) | Nextblock Solutions
May 2022

## Abstract

This is an analysis of low ether bonded (LEB) minipools which are Rocket Pool (RP) Ethereum validators formed with less than 16 ether (ETH) as the node operator (NO) deposit.  This analysis attempts to quantify a risk profile by first defining a set of performance specifications as the minimal design criteria of a LEB minipool.  To determine the smallest NO deposit that is acceptable we first performed a series of predictions on how a set of minipools might perform based upon known and predicted probabilities.


In order to accomplish this modeling, we estimated the number of beacon chain validators for the purposes of determining average annual staking rewards.  We assume that the current ethereum protocol parameter setting for rewards and penalties continues to be constant during the time modeled.  We next performed a monte carlo prediction using historical Ethereum proof-of-work mining block rewards to calculate future Ethereum staking (beacon chain) proposer payment value (PPV) rewards.  PPV includes both priority fees and inclusion payments that are made payable to the coinbase address.  Many of the analytical approaches and computer python codes were derived from the earlier work of pintail.xyz.   This report also details certain attack strategies that would reduce the APR of the rETH staking derivatives and measures the impact that such attacks would have based on a selected level of success.


Finally, a risk matrix is assembled that compares the predicted risk quantification to the established design specifications to determine the smallest NO deposit of a LEB that will meet the pre-determined risk profile.  This minimal NO deposit can be used to lower the financial barriers to forming a minipool while maintaining RP’s risk profile.


**Tl;dr A NO deposit of [E] ETH and 1.6 ΞRPL meets the minimum design specification of a LEB minipool**

## Contents

* `figures` - Contains all Figrues from the report
* `pythonModels` - Contains all the python3 scripts 
* `report` - Download a complete copy of the Risk Analysis Report. 
