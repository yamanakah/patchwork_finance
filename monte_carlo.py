# Monte Carlo simulation test code
import random
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def drawNumber():
    roll = random.random()
    return roll

# Now, just to test our dice, let's roll the dice 100 times.

# x = 0
# while x < 100:
#     result = drawNumber()
#     print(result)
#     x+=1

# Load csv test data
df = pd.read_csv("testdata_credit_pool.csv", thousands=',')

sim_num = 10000
s = 0

sim_losses = []

while s < sim_num:
    # Simulated Year 1 defaults
    defaults_1y = []

    i = 0
    while i < df.shape[0]:
        result = drawNumber()
        if df['Default_Prob_1Y'][i] < result:
            defaults_1y.append(0)
        else:
            defaults_1y.append(1)
        i = i+1

    df['Defaults_1Y'] = defaults_1y

    # Simulated Year 2 defaults
    defaults_2y = []

    i = 0
    while i < df.shape[0]:
        if df['Defaults_1Y'][i] == 0:
            result = drawNumber()
            if df['Default_Prob_2Y'][i] < result:
                defaults_2y.append(0)
            else:
                defaults_2y.append(1)
        else:
            defaults_2y.append(1)
        i = i+1

    df['Defaults_2Y'] = defaults_2y

    # Simulated Year 3 defaults
    defaults_3y = []

    i = 0
    while i < df.shape[0]:
        if df['Defaults_2Y'][i] == 0:
            result = drawNumber()
            if df['Default_Prob_3Y'][i] < result:
                defaults_3y.append(0)
            else:
                defaults_3y.append(1)
        else:
            defaults_3y.append(1)
        i = i+1

    df['Defaults_3Y'] = defaults_3y

    # Calculate losses
    loss = 0
    i = 0
    while i < df.shape[0]:
        if df['Defaults_1Y'][i] == 1:
            loss = loss + df['Loan_Amount_1Y'][i]
        elif df['Defaults_2Y'][i] == 1:
            loss = loss + df['Loan_Amount_2Y'][i]
        elif df['Defaults_3Y'][i] == 1:
            loss = loss + df['Loan_Amount_3Y'][i]
        i = i+1

    # Add loss to losses vector
    sim_losses.append(loss)

    # Add to iterator
    s = s+1

# Charting the losses
# fixed number of bins
fig, ax = plt.subplots()

plt.hist(sim_losses, bins=50, density=True, alpha=0.5)
ax.ticklabel_format(useOffset=False, style='plain')

plt.show()