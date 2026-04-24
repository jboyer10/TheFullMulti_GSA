

#This Script Saves SA Inputs and Analyse SA Outputs.
import math
import operator
from scipy.optimize import brentq
import pandas as pd
import numpy as np
import os

#%%#Sensitivity Analysis Input Saver###########################################
'''Saves inputs from Sensitivity Analysis as dataframe and CSV File'''
def SAin(problem,param_values,csv_name):
    
    p = pd.Categorical(['TotDepth', 'widthRS', 'lengthTotal','G', 'T_K', 'SPM', 'vflow'
                        ])
                        #'alpha','t_half_d','density','shape','sizeBin','t_frag_d','t_biof_growth_d'
                        #,'diameter''length_b','length_c'],'length_a','shape''density','discharge',)
    
    sys_in = pd.DataFrame(data=param_values,
              index=np.arange(1, (len(param_values)+1)),
              columns=p)
    inbound = pd.DataFrame.from_dict(problem['bounds'])
    if len(p) != len(problem['names']) == True:
        inbound.index = pd.DataFrame.from_dict(problem['names'])
    else:
        inbound.index = p
    inbound.columns = ['min','max']
    inbound = inbound.transpose()

    path = "C:/SA_Results" #'C:/LOONE_SA_Feb23/SA_Feb23' #folder that test files will be saved to
    inbound.to_csv(os.path.join(path,r'%s.csv'%csv_name))
    
    sys_in.to_csv(os.path.join(path,r'%s.csv'%csv_name),mode ='a')
    return sys_in

#%%#Sensitivity Analysis Output Saver##########################################
'''Saves inputs from Sensitivity Analysis as CSV File'''
#Type: input the analysis type, e.g. "sobol"

def SA_indices(problem,Si,Y,method,csv_title_SI,Notes,N_Samples):
    path = "C:/SA_Results" #folder that test files will be saved to
    if not os.path.exists(path):
        os.makedirs(path)
    M = pd.DataFrame(columns = ["Method used: %s"%method,"Sensitivity Analysis on %s"%Y,"Notes: %s"%Notes,
                      "Number of samples: %s"%N_Samples])
    M.to_csv(os.path.join(path,r'%s.csv'%csv_title_SI),mode ='a',header=False,index=False)
    
    if method.lower() in ["rbd"]:
        DS1 = pd.DataFrame(["","S1"])
        DS1.to_csv(os.path.join(path,r'%s.csv'%csv_title_SI),mode ='a',header=False,index=False)
        S1 = pd.DataFrame.from_dict(Si['S1'])
        S1.index = problem['names']
        S1.to_csv(os.path.join(path,r'%s.csv'%csv_title_SI),mode ='a',header=False)
    
    if method.lower() in ["fast"]:
        DS1 = pd.DataFrame(["","S1"])
        DS1.to_csv(os.path.join(path,r'%s.csv'%csv_title_SI),mode ='a',header=False,index=False)
        S1 = pd.DataFrame.from_dict(Si['S1'])
        S1.index = problem['names']
        S1.to_csv(os.path.join(path,r'%s.csv'%csv_title_SI),mode ='a',header=False)
        
        DST = pd.DataFrame(["","ST"])
        DST.to_csv(os.path.join(path,r'%s.csv'%csv_title_SI),mode ='a',header=False,index=False)
        ST = pd.DataFrame.from_dict(Si['ST'])
        ST.index = problem['names']
        ST.to_csv(os.path.join(path,r'%s.csv'%csv_title_SI),mode ='a',header=False)
        
    elif method.lower() in ["sobol"]:
        DS1 = pd.DataFrame(["","S1"])
        DS1.to_csv(os.path.join(path,r'%s.csv'%csv_title_SI),mode ='a',header=False,index=False)
        S1 = pd.DataFrame.from_dict(Si['S1'])
        S1.index = problem['names']
        S1.to_csv(os.path.join(path,r'%s.csv'%csv_title_SI),mode ='a',header=False)
        
        DS1_conf = pd.DataFrame(["","S1_conf"])
        DS1_conf.to_csv(os.path.join(path,r'%s.csv'%csv_title_SI),mode ='a',header=False,index=False)
        S1_conf = pd.DataFrame.from_dict(Si['S1_conf'])
        S1_conf.index = problem['names']
        S1_conf.to_csv(os.path.join(path,r'%s.csv'%csv_title_SI),mode ='a',header=False)
        
        DS2 = pd.DataFrame(["","S2"])
        DS2.to_csv(os.path.join(path,r'%s.csv'%csv_title_SI),mode ='a',header=False,index=False)
        S2 = pd.DataFrame.from_dict(Si['S2'])
        S2.index = problem['names']
        S2.columns = problem['names']
        S2.to_csv(os.path.join(path,r'%s.csv'%csv_title_SI),mode ='a')
        
        DS2_conf = pd.DataFrame(["","S2_conf"])
        DS2_conf.to_csv(os.path.join(path,r'%s.csv'%csv_title_SI),mode ='a',header=False,index=False)
        S2_conf = pd.DataFrame.from_dict(Si['S2_conf'])
        S2_conf.index = problem['names']
        S2_conf.columns = problem['names']
        S2_conf.to_csv(os.path.join(path,r'%s.csv'%csv_title_SI),mode ='a')
        
        DST = pd.DataFrame(["","ST"])
        DST.to_csv(os.path.join(path,r'%s.csv'%csv_title_SI),mode ='a',header=False,index=False)
        ST = pd.DataFrame.from_dict(Si['ST'])
        ST.index = problem['names']
        ST.to_csv(os.path.join(path,r'%s.csv'%csv_title_SI),mode ='a',header=False)
        
        DST_conf = pd.DataFrame(["","ST_conf"])
        DST_conf.to_csv(os.path.join(path,r'%s.csv'%csv_title_SI),mode ='a',header=False,index=False)
        ST_conf = pd.DataFrame.from_dict(Si['ST_conf'])
        ST_conf.index = problem['names']
        ST_conf.to_csv(os.path.join(path,r'%s.csv'%csv_title_SI),mode ='a',header=False)
        