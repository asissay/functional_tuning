### File reads in output files for the neutral ground state and charge
### +1 calculations and generates an error calculate as
### J = |SCF-neutral - SCF-charge1 + IP| 

import os
import numpy as np
import math
import csv
import sys
from scipy import optimize
from matplotlib import pyplot as plt
from sklearn.metrics import r2_score

###----------Neutral Calculation----------------###

# Reads in output file and REMOVES first 500 lines 
cmd = "tail %s neutral.nwo > coarse1.nwo"%"-n +500"
os.system(cmd)

# Grep for tuning parameters
cmd1 = "grep %s coarse1.nwo> cam3.dat"%"cam"
os.system(cmd1)


# Get rids of unwanted strings (cam, cam_alpha, energy)
cmd3 = "awk  '%s' cam3.dat > neutral_tmp.dat"%"{print$3,$6,$9}"
os.system(cmd3)


cmd4 = "awk  '%s' neutral_tmp.dat > neutral_tmp_1.dat"%'{gsub("cam","");print}'
os.system(cmd4)

# Deletes repeated lines 
cmd2 = "awk  %s neutral_tmp_1.dat > neutral.dat"%"NR%30==1"
os.system(cmd2)


# ###----------Charge 1 Calculation----------------###

# Reads in output file and REMOVES first 500 lines 
cmd5 = "tail %s charge1.nwo > coarse_charge1_1.nwo"%"-n +500"
os.system(cmd5)

# Grep for tuning parameters
cmd6 = "grep %s coarse_charge1_1.nwo> cam4.dat"%"cam' '"
os.system(cmd6)

# Deletes repeated lines 
cmd7 = "awk  %s cam4.dat > charge1_tmp.dat"%"NR%30==0"
os.system(cmd7)

# Get rids of unwanted strings (cam, cam_alpha, energy)
cmd8 = "awk  '%s' charge1_tmp.dat > charge1_tmp_1.dat"%"{print$3,$6,$9}"
os.system(cmd8)

cmd9 = "awk  '%s' charge1_tmp_1.dat > charge1_tmp_2.dat"%'{gsub("cam","");print}'
os.system(cmd9)

cmd10 = "awk  '%s' charge1_tmp_2.dat > charge1.dat"%'NR>0'
os.system(cmd10)

#print(cmd9)

###----------Ionization potential (IP)----------------###
 
# Grep for IP 
cmd11 = "grep %s neutral.nwo> vector_tmp.dat"%"Vector'   '38"
os.system(cmd11)

# Deletes repeated lines 
cmd12 = "awk  %s vector_tmp.dat > vector_tmp_1.dat"%"NR%2==0"
os.system(cmd12)

# Get rids of unwanted strings (cam, cam_alpha, energy)
cmd13 = "awk  '%s' vector_tmp_1.dat > vector_tmp_2.dat"%'gsub("D","E")'
os.system(cmd13)

cmd14 = "awk  '%s' vector_tmp_2.dat > vector_tmp_3.dat"%'NR>0'
os.system(cmd14)

cmd15 = "awk  '%s' vector_tmp_3.dat > vector.dat"%'{gsub("E=","");print}'
os.system(cmd15)

#print (cmd14)


#----------------------------------------------------------------------------------
neutral  =  np.genfromtxt("neutral.dat") # , usecols = (2,5,8))
mu_n     =  neutral[:,0]
alpha_n  =  neutral[:,1]
energy_n =  neutral[:,2]
#print(energy_n)

#cmd3 = "awk  %s c1.dat > charge1.dat"%"NR%19==0"
#os.system(cmd3)

charge1  = np.genfromtxt("charge1.dat") # usecols = (2,5,8))
mu_c     = charge1[:,0]
alpha_c  = charge1[:,1]
energy_c = charge1[:,2]
#print(energy_c)

vector =  np.genfromtxt("vector.dat", usecols = 3 )

### Check if there is length mismatch

#successfully_read_in = True
if (len(mu_n)) != (len(mu_c)): 
    print("Length mismatch: possibly calculations did not finish")
    sys.exit()
else:
    print("Calculations finished - Files successfully processed")
error = abs((energy_c-energy_n)+vector)

combo = []
f = open('combo.dat', 'w')
for i,j,k in zip((range(len(mu_n))),(range(len(alpha_n))), (range(len(error)))):
    comb = (mu_n[i], alpha_n[j], error[k])
    
    f.write(str(mu_n[i]) + "   " + str(alpha_n[j])+ "    " + str(error[k]) + "\n")
f.close()

# Plot mu,alpha, and error in one plot 
os.system('gnuplot tmp.gp')

###----------------------Straight line test----------------------------###
cmd19 = "tail %s straight.nwo > energy_tmp.nwo"%"-n +200"
os.system(cmd19)

# Grep for tuning parameters
cmd20 = "grep %s energy_tmp.nwo> energy.dat"%"*energy' '='  '"
os.system(cmd20)

cmd21 = "awk '%s' energy.dat > energy1.dat"%"NR==10||NR%36==0"
#awk 'NR == 10 || NR % 36 == 0' energy.dat  > energy1.dat
os.system(cmd21)

cmd22 = "awk  '%s' energy1.dat > energy2.dat"%"{print$4,$11}"
os.system(cmd22)

tot_energy  =  np.genfromtxt("energy2.dat") # , usecols = (2,5,8))
char_n = tot_energy[:,0]
ener_n = tot_energy[:,1]
# #energy_n =  neutral[:,2]
# #print(ener_n)

def test_func(x, m, b):
    # y = mx + b
    return  m*x + b

params, params_covariance = optimize.curve_fit(test_func, char_n, ener_n, p0=[2, 2])

np.savetxt("params.dat", params, delimiter = "    ")

r2 = r2_score(ener_n, test_func(char_n, params[0], params[1]))
print("R^2 = {}".format(r2))

plt.figure(figsize=(6, 4))
plt.scatter(char_n, ener_n, label='Data')
plt.plot(char_n, test_func(char_n, params[0], params[1]),label='Fitted function')
plt.legend(loc='best')
plt.xlabel("Number of Electrons Added to Ion")
plt.ylabel("Total DFT Energy")
plt.show()






