import numpy as np
import pickle
import matplotlib.pyplot as plt
import os

N = pickle.load(open("../results/N.dat", "rb"))
Nsources = pickle.load(open("../results/Nsources.dat", "rb"))
Nwells = pickle.load(open("../results/Nwells.dat", "rb"))
wells_colors = pickle.load(open("../results/wells_colors.dat", "rb"))

#%% Calculating compression
N = np.array(N)
Nsources = np.array(Nsources)
Nwells = np.array(Nwells)
compr = 1 - (N-Nsources-Nwells)/N

compr_bytype = []
for id in np.unique(wells_colors):
    compr_temp = []
    for index in range(len(wells_colors)):
        if id == wells_colors[index]:
            compr_temp.append(compr[index])
    compr_bytype.append(compr_temp)

for i in range(3):
    plt.hist(compr_bytype[i])
    plt.show()

fig = plt.figure()
plt.xscale('log')
plt.scatter(N, compr, marker = 'o', c = wells_colors)
plt.legend()
plt.xlabel("Total number of vertices")
plt.ylabel("Compression factor")
#plt.savefig('../figures/realWorldLogLog.png', format='png', dpi=300)
#plt.savefig('../figures/realWorldLogLog.svg', format='svg')
#plt.savefig('../figures/realWorldLogLog.eps', format='eps')
plt.show()

web = compr_bytype[0]
bio = compr_bytype[1]
air = compr_bytype[2]

print("Web mean: " + str(np.mean(web)))
print("Web median: " + str(np.median(web)))
print("Web min: " + str(np.min(web)))
print("Web 25th: " + str(np.percentile(web, 25)))
print("Web 75th: " + str(np.percentile(web, 75)))
print("Web max: " + str(np.max(web)))
print("")

print("bio mean: " + str(np.mean(bio)))
print("bio median: " + str(np.median(bio)))
print("bio min: " + str(np.min(bio)))
print("bio 25th: " + str(np.percentile(bio, 25)))
print("bio 75th: " + str(np.percentile(bio, 75)))
print("bio max: " + str(np.max(bio)))
print("")

print("air mean: " + str(np.mean(air)))
print("air median: " + str(np.median(air)))
print("air min: " + str(np.min(air)))
print("air 25th: " + str(np.percentile(air, 25)))
print("air 75th: " + str(np.percentile(air, 75)))
print("air max: " + str(np.max(air)))
print("")

print("ALL mean: " + str(np.mean(compr)))
print("ALL median: " + str(np.median(compr)))
print("ALL min: " + str(np.min(compr)))
print("ALL 25th: " + str(np.percentile(compr, 25)))
print("ALL 75th: " + str(np.percentile(compr, 75)))
print("ALL max: " + str(np.max(compr)))