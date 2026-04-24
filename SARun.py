

#Sensitivity Analysis for Full Multi

import pandas as pd
import SALib
from SALib.sample import saltelli, latin, fast_sampler
from SALib.analyze import fast, rbd_fast, sobol
from timeit import default_timer as timer
from SA_Attempt2 import SA_FullMulti
import SAProcessing as SAP
import matplotlib.pyplot as plt
from SALib.plotting.bar import plot as barplot
from SALib.test_functions import Ishigami


#%%#Universal Input Parameters#################################################
#Identify SA method (FAST, RBD, or Sobol)
method = 'Sobol' 
#How many samples should be generated per variable:
N_samples = 256 #2358 #393 for FAST

start = timer() #used for timing the function

#%%Other Inputs################################################################



#%%#Set Up Analysis############################################################

problem = {
    'num_vars': 20,
    'names': ['discharge_m3_s', 'TotDepth', 'widthRS', 'lengthTotal_km ', 'numRS', 'G', 'T_K', 'SPM_mgL', 'vFlow_m_s', 'alpha', 't_half_d', 't_frag_d', 't_biof_growth_d', 'density_kg_m3', 'MPshape', 'sizeBin', 'diameter_um' ,'length_a_um', 'length_b_um', 'length_c_um'],
    'bounds': [[2000, 230000], #0                       
               [0.5, 220],    #1                
               [10, 11000],  #2
               [0.1, 6700],  #3
               [0,1] ,  #4
               [0, 10000],   #5
               [273.15, 308.15], #6
               [0, 2000], #7
               [0.1, 3], #8
               [0.001, 0.2], #9
               [500, 920000], #10
               [30, 7250], #11
               [10, 300], #12
               [850, 1600], #13
               [0,1], #14 edit
               [0,1], #15 edit
               [0.1, 5000], #16
               [0.1, 5000], #17
               [0.1, 5000], #18
               [0.1, 5000] #19
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

Y = pd.DataFrame()
for i, X in enumerate(param_values):
    Y[i] = SA_FullMulti(X)
Y_T = Y.T
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
D = Y_T['Avg']
Si = sobol.analyze(problem, D.values)    
    #Type: input the analysis type, e.g. "sobol"
Si_Var = SAP.SA_indices(problem,Si,'Output_Mean',method,'SA_Results','No_Notes',N_samples)
#Placed at end so that files not unnecessarily generated for failed tests
sys_in = SAP.SAin(problem,param_values,'SA_Inputs')

end = timer()
print(end - start) # Time in seconds

# total, first, second = Si.to_df()
# barplot(first).get_figure().savefig("C:/LOONE/X.png", dpi=600, bbox_inches = 'tight')
