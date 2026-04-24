

#Sensitivity Analysis for Full Multi

import pandas as pd
import numpy as np
import SALib
from SALib.sample import saltelli, latin, fast_sampler
from SALib.analyze import fast, rbd_fast, sobol
from timeit import default_timer as timer
from SA_Attempt3_cond13 import SA_FullMulti
#import SAProcessing_ as SAP
import matplotlib.pyplot as plt
from SALib.plotting.bar import plot as barplot
from SALib.test_functions import Ishigami

import os
num_threads = int(os.environ['SLURM_CPUS_PER_TASK'])

import mkl
mkl.set_num_threads(num_threads)

#%%#Universal Input Parameters#################################################
#Identify SA method (FAST, RBD, or Sobol)
method = 'Sobol' 
#How many samples should be generated per variable:
N_samples = 256 #180 #2358 #393 for FAST
#Ntot = N_samples x ((2*num_var) + 2)
#convergence properties only valid if N_samples = 2^n

start = timer() #used for timing the function

#%%#Set Up Analysis############################################################

problem = {
    'num_vars': 7,
    'names': ['TotDepth','widthRS', 'lengthTotal', 'SPM','density','shape','sizeBin'],
             #  'alpha','t_half_d',,,,'t_frag_d','t_biof_growth_d'
             # ,'discharge','length_a','diameter''G', 'T_K', 'vflow'],
             # , ,'length_b','length_c'],
    'bounds': [[1,10], #0, totdepth
               [5,500], #1 widthRS
               [0.1,10], #2 lengthTotal
               #[1,100], #3 G
              # [273.15,308.15], #4 T_K
               [1,2000], #5 SPM
              # [0.2,2], #6 vflow
              # [400,40000], #7 discharge
              # [0.001,0.2], #8 alpha
              # [500,920000], #9 t_half_d
             
               [850,1600], #12 density
              # [1,5000], #13 diameter
             #  [1,5000], #14 length_a
              # [1,5000], #15 length_b
               #[1,5000], #16 length_c
               [1,3.9999], #17 shape
               [1,5.9999],#size bin]
             #  [30,7250], #10 t_frag_d
              # [0.01,300] #11 t_biof_growth_d
               ]
}

if method.lower() in ['fast']: 
    param_values = fast_sampler.sample(problem, N_samples) #For Fourier Amplitude Sensitivity Test
    print("FAST")
elif method.lower() in ['rbd']:
    param_values = latin.sample(problem, N_samples) #For RBD_FAST Method
    print("RBD")
elif method.lower() in ['sobol']:
    param_values = saltelli.sample(problem, N_samples) #For Sobol Method
    print("Sobol")

param_values[:, 5] = 3.5

results_df = pd.DataFrame(columns=[
    "Surface Water (Total number)",
    "Flowing Water (Total number)",
    "Stagnant Water (Total number)",
    "Sediment (Total number)"
])

Y = pd.DataFrame()
J = pd.DataFrame()
K = pd.DataFrame()
L = pd.DataFrame()
#Y = np.zeros([param_values.shape[0]])

for i, X in enumerate(param_values):
    #Y[i] = SA_FullMulti(X)
    output1 = SA_FullMulti(X)
    Y[i] = output1.iloc[:,0]
    J[i] = output1.iloc[:,1]
    K[i] = output1.iloc[:,2]
    L[i] = output1.iloc[:,3]
    row3 = output1.iloc[3, :]
    results_df.loc[len(results_df)] = row3.values
    #print(Y[i])

# Label rows with run number
results_df.index = [f"Run_{i+1}" for i in range(len(results_df))]

# Save to CSV
results_df.to_csv("sensitivity_resultscond13.csv", index=True)

'''
Y_T = Y.T
J_T = J.T
K_T = K.T
L_T = L.T

#%%#Run Analysis###############################################################
# Note that: for Sobol method, Y.size % (2 * D + 2) == 0 where D = Num of variables
#Note: for Fast method, len(Y) % D must = 0 where D = Num of variables, and N = ((Y/D)+1)/2 might be adjusted to be < specific number! 
# if method.lower() in ['fast']:
#     Si = fast.analyze(problem, Y) #For Fourier Amplitude Sensitivity Test
# elif method.lower() in ['rbd']:
#     Si = rbd_fast.analyze(problem, Y, param_values) #For RBD-FAST Method
# elif method.lower() in ['sobol']:
#     Si = sobol.analyze(problem, Y) #For Sobol Method

Y_T['Avg'] = Y_T.mean(axis=1)
J_T['Avg'] = J_T.mean(axis=1)
K_T['Avg'] = K_T.mean(axis=1)
L_T['Avg'] = L_T.mean(axis=1)

D = Y_T['Avg']
E = J_T['Avg']
F = K_T['Avg']
G = L_T['Avg']


Si = sobol.analyze(problem, D.values)    
#Type: input the analysis type, e.g. "sobol"
Si_Var = SAP.SA_indices(problem,Si,'Output_Mean',method,'SA_ResultsFQ','No_Notes',N_samples)
#Placed at end so that files not unnecessarily generated for failed tests
sys_in = SAP.SAin(problem,param_values,'SA_InputsFQ')

Ti = sobol.analyze(problem, E.values)
Ti_Var = SAP.SA_indices(problem,Ti,'Output_Mean',method,'SA_ResultsFQ','No_Notes',N_samples)
sys_in = SAP.SAin(problem,param_values,'SA_InputsFQ')

Ui = sobol.analyze(problem, F.values)
Ui_Var = SAP.SA_indices(problem,Ui,'Output_Mean',method,'SA_ResultsFQ','No_Notes',N_samples)
sys_in = SAP.SAin(problem,param_values,'SA_InputsFQ')

Vi = sobol.analyze(problem, G.values)
Vi_Var = SAP.SA_indices(problem,Vi,'Output_Mean',method,'SA_ResultsFQ','No_Notes',N_samples)
sys_in = SAP.SAin(problem,param_values,'SA_InputsFQ')
'''
end = timer()
print(end - start) # Time in seconds

# total, first, second = Si.to_df()
# barplot(first).get_figure().savefig("C:/LOONE/X.png", dpi=600, bbox_inches = 'tight')


# %%
