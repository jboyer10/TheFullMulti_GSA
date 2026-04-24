#!/usr/bin/env python
# coding: utf-8



def SA_FullMulti(SA_Par):

    from Functions.objectGenerationRiver_func import preProcessLayers, preProcessElements
    #from helpers.GlobalConstants import * 
    from Functions.readImputParam import readProcessparam, microplasticData,readCompartmentData
    from Functions.dilutionVol_calculator_func import volumesVector
    from Functions.RC_estimation_function_v2_0 import RC_estimation_function_v2_0
    from Functions.reshape_RC_df_fun import reshape_RC_df
    from Functions.fillInteractions_df_fun_v2_0 import fillInteractions_fun_v2_0
    from timeit import default_timer as timer
    '''
    from Functions.objectGenerationRiver_func import* 
    from helpers.GlobalConstants import *
    from Functions.readImputParam import readProcessparam, microplasticData,readCompartmentData
    from Functions.dilutionVol_calculator_func import*
    from Functions.RC_estimation_function_v2_0 import*
    from Functions.reshape_RC_df_fun import*
    from Functions.fillInteractions_df_fun_v2_0 import* 
    '''

    #from IPython.core.display import display, HTML
   # display(HTML("<style>.container { width:80% !important; }</style>"))

    import os
    import math
    import pandas as pd
    import itertools
    import numpy as np
    import matplotlib.patches as mpatches
    from matplotlib import pyplot as plt
    import seaborn as sns
    from matplotlib.colors import LogNorm
    from scipy.integrate import odeint
    #from celluloid import Camera
    #from cycler import cycler
    import warnings
    warnings.filterwarnings('ignore')

   # get_ipython().run_line_magic('matplotlib', 'inline')
   # plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'


    ### Import imput files
    from pathlib import Path
    data_folder = Path("Inputs/") 


    # Create Compartment_Props file
    # Define river 
    compartments = ["surface", "flowingWater", "stagnantWater", "sediment"]
    compDepth= [(0.2*SA_Par[0]), (0.65*SA_Par[0]), (0.1*SA_Par[0]), (0.05*SA_Par[0])]
    widthRS= SA_Par[1]
    #all calculations are in m!
    lengthTotal_km = SA_Par[2] #Total modelled length in Km 20
    numRS= 20
    G = "10" #was text 10
    T_K = "273.15"#asummed the same for all compartments - was text 273.15
    SPM_mgL = SA_Par[3] # "30" #was text "30"
    vflow_m_s = 1.3 #2

    indexList= list(range(numRS*4))
    #generate list of river sections (RS) with same dimensions and list of their corresponding lengths 
    #according to Praetorius et al subdivission.
    RS_length_m= int(lengthTotal_km*1000/numRS)
    listRS=list(range(numRS))
    RSlengths_list= [RS_length_m]*numRS

    #Cummulative lengths
    RSCumLength=[RS_length_m]
    for l in range (1,len(RSlengths_list)):
        RSCumLength.append(RSlengths_list[l]+RSCumLength[l-1])

    ##CREATE RIVER IMPUT FILE

    file_name = "compartments_prop_cond2.txt"
    file_path = data_folder / file_name

    out_file = open(file_path, "w")
    out_file.write("riverSection,nameRS,compartment,compType,depth_m,length_m,volume_m3,width_m,G,T_K,vFlow_m_s,SPM_mgL\n")
    for rs in range(numRS):
        for comp in range(len(compartments)):
            out_file.write(str(rs) + "," +
                    "RS" + str(rs) + "," +
                    str(comp + 1) + "," +
                    str(compartments[comp]) + "," +
                    str(compDepth[comp]) + "," +
                    str(RS_length_m) + "," +
                    str(compDepth[comp] * RS_length_m * widthRS) + "," +
                    str(widthRS) + "," +
                    str(G) + "," +
                    str(T_K) + "," +
                    str(vflow_m_s) + "," +
                    str(SPM_mgL) + "\n")    
    out_file.close()


    #Flow_connectivity file
    
    def create_csv_with_n_rows(n, filename="output.csv"):
        # Create the data for the columns
        col1 = list(range(1, n+1))          # First column: 1 to n
        col2 = list(range(2, n+1)) + [np.nan]   # Second column: 2 to n-1, then NaN
        col3 = (vflow_m_s*SA_Par[0]*widthRS*60*60) 

        # Create a DataFrame using the data
        df = pd.DataFrame({
        'Region_I': col1,
        'Region_J': col2,
        'q(m3/h)' : col3
        })

        file_path = data_folder / filename

        # Write the DataFrame to a CSV file
        df.to_csv(file_path, index=True)

        print(f"CSV file '{filename}' created with {n} rows.")
        print(col3)

    # Example usage
    create_csv_with_n_rows(numRS, "flow_connectivity_cond2.csv")

    
    # Process_param df
    '''
    # Create the data for the columns
    colu1 = list(range(1, 17))         
    colu2 = [1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4]
    colu3 = ['A','B','C','D','A','B','C','D','A','B','C','D','A','B','C','D']
    colu4 = [0.01, np.nan, 0.02, np.nan, 0.01, np.nan, 0.02, np.nan, 0.01, np.nan, 0.02, np.nan, 0, np.nan, 0, np.nan]
    colu5 = [5000,50000,25000,100000,5000,50000,25000,100000,5000,50000,25000,100000,5000,50000,25000,100000]
    colu6 = SA_Par[7]
    colu7 = SA_Par[8]
    colu8 = np.nan

    # Create a DataFrame using the data
    process_df = pd.DataFrame({
    'ID': colu1,
    'compartment': colu2,
    'aggState' : colu3,
    'alpha': colu4,
    't_half_d': colu5,
    't_frag_d': colu6,
    't_biof_growth_d': colu7,
    't_biof_degrad_d': colu8
    })    

    #print(process_df)
    ''''''
    #Input Files

    '''

    shape = int(SA_Par[5])
    if shape == 1:
        MPshape = "fiber"
    elif shape == 2:
        MPshape = "sphere"
    elif shape == 3:
        MPshape = "fragment"


    print(shape)
    print(MPshape)
    
    sizeBinJB = int(SA_Par[6])
    if sizeBinJB == 1:
        MPsizeBinJB = "a"
    elif sizeBinJB == 2:
        MPsizeBinJB = "b"
    elif sizeBinJB == 3:
        MPsizeBinJB = "c"
    elif sizeBinJB == 4:
        MPsizeBinJB = "d"
    elif sizeBinJB == 5:
        MPsizeBinJB = "e"

    print(sizeBinJB)
    print(MPsizeBinJB)


    MP_prop = pd.DataFrame(
    data=[[1,'MP1','Poly',SA_Par[4],MPshape,'a',1,1,1,1], 
        [1,'MP1','Poly',SA_Par[4],MPshape,'b',10,10,10,10], 
        [1,'MP1','Poly',SA_Par[4],MPshape,'c',100,100,100,100], 
        [1,'MP1','Poly',SA_Par[4],MPshape,'d',1000,1000,1000,1000],
        [1,'MP1','Poly',SA_Par[4],MPshape,'e',5000,5000,5000,5000], 
        [2,'SPM1','mixed',2000,'sphere','a',0.5,0,0,0], [2,'SPM1','mixed',2000,'sphere','b',0.5,0,0,0], 
        [2,'SPM1','mixed',2000,'sphere','c',0.5,0,0,0], [2,'SPM1','mixed',2000,'sphere','d',0.5,0,0,0], 
        [2,'SPM1','mixed',2000,'sphere','e',0.5,0,0,0]],  
    index=[0,1,2,3,4,5,6,7,8,9],                 
    columns=['ID','name','composition','density_kg_m3','MPshape','sizeBin','diameter_um','length_a_um','length_b_um','length_c_um']  )
  
    ''' 
    MP_prop = pd.DataFrame(
    data=[[1,'MP1','Poly',980,'sphere','a',(SA_Par[4]/10000),10,0,0], 
        [1,'MP1','Poly',980,'sphere','b',(SA_Par[4]/1000),10,0,0], 
        [1,'MP1','Poly',980,'sphere','c',(SA_Par[4]/100),10,0,0], 
        [1,'MP1','Poly',980,'sphere','d',(SA_Par[4]/10),10,0,0],
        [1,'MP1','Poly',980,'sphere','e',SA_Par[4],10,0,0], 
        [2,'SPM1','mixed',2000,'sphere','a',0.5,0,0,0], [2,'SPM1','mixed',2000,'sphere','b',0.5,0,0,0], 
        [2,'SPM1','mixed',2000,'sphere','c',0.5,0,0,0], [2,'SPM1','mixed',2000,'sphere','d',0.5,0,0,0], 
        [2,'SPM1','mixed',2000,'sphere','e',0.5,0,0,0]],  
    index=[0,1,2,3,4,5,6,7,8,9],                 
    columns=['ID','name','composition','density_kg_m3','MPshape','sizeBin','diameter_um','length_a_um','length_b_um','length_c_um']  )
   '''
    process_df= readProcessparam (data_folder / "process_paramRiver.txt")
   # MP_prop = microplasticData(data_folder /"microplasticsSizeClass.txt") #
    compartments_prop = readCompartmentData(data_folder /"compartments_prop_cond2.txt")
    river_flows=pd.read_csv(data_folder /"flow_connectivity_cond2.csv")
    
    #Add river section depth field
    RSdepth = []
    for row in range(len(compartments_prop)):
            RSdepth.append(round(sum(compartments_prop.depth_m[0:4]),2))
    compartments_prop["depthRS_m"]=RSdepth

    # # Model set up

    #RIVER COMPARTMENTS
    compartments = ["Surface Water", "Flowing Water", "Stagnant Water", "Sediment"]
    riverComp = ["1", "2", "3", "4"]


    #MICROPLASTICS FORMS 
    MPforms = ["A", "B", "C", "D"]
    MPformslabels = ["Free", "Heteroaggregated", "Biofilm-covered", "Biofilm-heteroaggregated"]


    #SIZE BINS
    sizeBin =["a", "b", "c", "d", "e"]
    sizeBinLabel = ["1um", "10um","100um", "1000um", "5000um"]# Detection limit for MPs via Fourier Transform Infrared Spectroscopy is 20um

    #MPS RIVER PROCESSES (FATE AND TRANSPORT) LIST
    processList = ["degradation", "fragmentation", "heteroagg", "breakup", "settling","rising", "advection", "mixing", "biofilm", "resusp", "burial","sedTransport", "defouling"]

    #RIVER SECTIONS
    numberRS=len (compartments_prop)/len(riverComp)
    listRS = [*range(0,int(numberRS),1)]
    riverSect = [str(item) for item in listRS]
    riverLengths = [str(it) for it in compartments_prop["length_m"]]
    riverSectLength= riverLengths[0::4]
    RS_cumLength_m =[]
    for d in range(len(riverSectLength)):
        if d==0:
            RS_cumLength_m.append(float(riverSectLength[d]))
        else:
            RS_cumLength_m.append(float(riverSectLength[d])+float(RS_cumLength_m[d-1]))


    SOLVER = "Dynamic" 
    mode = "Standard" 
    mode2 = "Timelimit" 
    record = "False"

    composition = "Poly" #Poly
    connector = (str(str('02A') + str(MPsizeBinJB)))
  #  imputMP= "02Ae"
    imputMP= connector
    imputFlow=100 
    imputPulse=0


    t0 = 0 
    daysSimulation = 90
    tmax = 24*60*daysSimulation*60 
    sec_day = 24*60*60
    stepSize= 60*60*24 #time step of 1day
    timesteps = int(sec_day*daysSimulation/stepSize) 
    t_span = np.linspace(0, tmax, int(timesteps)+1, dtype=int)


    #Set up current date label#
    from datetime import datetime, timedelta
    date_time_str = '2020-01-01 00:00'
    DayStart = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
    LastDay = DayStart + timedelta(seconds=tmax)
    date = DayStart
    daterun = date.today()
    daterun_label = daterun.strftime("%Y_%m_%d")


    #Generate COMBINATIONS
    combinations = list(itertools.product(riverSect,riverComp,MPforms,sizeBin))
    #Generate raw list of combinations and lists of concentrations (C) and inflows (I)
    CombList = []
    Ilist = []
    Clist =[]
    def convertTuple(tup): 
        str =  ''.join(tup) 
        return str
    for e in combinations:
        Clist.append("C_" + convertTuple(e))
        Ilist.append("I_" + convertTuple(e))
        CombList.append(convertTuple(e))

    # # Model Run
    # ## -Estimate Rate constants

    RC_df=RC_estimation_function_v2_0(processList,CombList,Clist,MP_prop,compartments_prop,process_df,numberRS, composition,mode2, mode, date,riverComp,MPforms,sizeBin,river_flows)

    ### Reshape table of RC
    RC_df_tidy=reshape_RC_df(RC_df,CombList)
    RC_df_final=RC_df_tidy.pivot_table(index=["Compartment", "MP_form", "SizeFrac"],columns='Process', values='k_s-1')
    RC_df_final

    # ## -Generate Interactions Matrix

    interactions_df= fillInteractions_fun_v2_0(RC_df, Clist,river_flows)

    # ## - SOLVER

    #Initial number of particles in the system 
    PartNum_t0 = pd.DataFrame(index=Clist, columns=['number of particles'])
    for p in range(len(PartNum_t0)):
            PartNum_t0.iloc[p][0]= 0
    PartNum_t0.loc["C_"+imputMP]=imputPulse

    #Inflow of particles as particles per second 
    Ilist = []
    for C in Clist:
        Ilist.append("I"+ C[1:])
    inflow_vector = pd.DataFrame(index=Ilist, columns=["number of particles"])
    inflow_vector.loc[:,:] = 0
    inflow_vector.loc["I_"+imputMP] = imputFlow/60 #transformed to particles per sec

    #Model funcion
    def dNdt_2(N,t,k,I):  
        dNdt=np.dot(N,k)+I
        return np.squeeze(dNdt)


    # intitial condition
    N0 = PartNum_t0['number of particles'].to_numpy(dtype="float")
    I= inflow_vector['number of particles'].to_numpy(dtype="float")
    # time points
    time = np.linspace(0, tmax, int(timesteps)+1, dtype=int)##in seconds


    #Solve ODEs
    if SOLVER == 'Dynamic':
        k=interactions_df.to_numpy()
        Nfinal=odeint(dNdt_2, N0, time, args =(k,I), col_deriv=True)
        NFinal_num = pd.DataFrame(data = Nfinal, index=t_span , columns= Clist)  
        
    elif SOLVER == "SteadyState":
        print("Steady State not yet implemented")
    NFinal_num    


    #Vector of volumes corresponding to the compartments of the river
    dilution_vol_m3= volumesVector(Clist,compartments_prop)

    ConcFinal_num_m3= pd.DataFrame(data = 0, index=t_span , columns= Clist) 
    ConcFinal_num_m3 = NFinal_num.div(dilution_vol_m3, axis=1)

   # for ind in range(len(NFinal_num)):
   #     ConcFinal_num_m3.iloc[ind]=NFinal_num.iloc[ind]/dilution_vol_m3

    #Substitute values smaller than 10-5 to 0
    ConcFinal_num_m3 = ConcFinal_num_m3.apply(lambda x: [y if y >= 1e-15 else 0 for y in x])


    # ### Concentrations dataframe (mg/m3)

    volume= RC_df.loc["volume_m3"].to_numpy()
    density= RC_df.loc["density_kg_m3"].to_numpy()
    ConcFinal_mg_m3=ConcFinal_num_m3*volume*density*10**6
    ConcFinal_mg_m3

    # ### Select time span units for plotting (t_span_plot)

    t_span_sec = np.linspace(t0, tmax, int(timesteps)+1, dtype=int)
    t_span_min=t_span_sec/60
    t_span_h = t_span_min/60
    t_span_days = t_span_h/24
    t_span_months = t_span_days/30


    t_span_plot = t_span_months

    # ### Select river sections to plot

    RS= ["0","3","5","9","10","11","12"] 

    #Select Concentration Units: number of particles or mass
    ConcPlot_choice="ConcFinal_num_m3"
    if ConcPlot_choice == "ConcFinal_num_m3":
        ConcPlot = ConcFinal_num_m3
        ConcPlot_units= ["(No/$m^3$)","Num_m3"]
    elif ConcPlot_choice == "ConcFinal_mg_m3":
        ConcPlot = ConcFinal_mg_m3
        ConcPlot_units= ["(mg/$m^3$)","mg_m3"]
    else:
        print ("Choose correct concentration dataframe")


    def extract_SizeBins (t, comp, MPform,):
        Aa=[]
        Ab=[]
        Ac=[]
        Ad=[]
        Ae=[]
        for i in range(len(listRS)):
            Aa.append(ConcPlot.values[t, Clist.index("C_"+str(listRS[i])+comp+MPform+"a")])
            Ab.append(ConcPlot.values[t, Clist.index("C_"+str(listRS[i])+comp+MPform+"b")])
            Ac.append(ConcPlot.values[t, Clist.index("C_"+str(listRS[i])+comp+MPform+"c")])
            Ad.append(ConcPlot.values[t, Clist.index("C_"+str(listRS[i])+comp+MPform+"d")]) 
            Ae.append(ConcPlot.values[t, Clist.index("C_"+str(listRS[i])+comp+MPform+"e")]) 
        return [Aa, Ab, Ac, Ad, Ae]


    # #### Function to extract lists from a list by criteria

    def listofindex(criteria,Clist):                                                                                                             
        lista= [[] for x in range(len(criteria))]
        for i in range(len(lista)):
            lista[i] = [n for n in Clist if criteria[i] in n[-3:]]
        return lista

    # #### Extract list of indexes needed for plotting

    list_of_indexesMpType=listofindex(MPforms,Clist)
    list_of_indexesCompartments=listofindex(riverComp,Clist)
    list_ofindexesSizeBins=listofindex(sizeBin,Clist)


    # #### Define time resolution for extracting results (time_extract)

    numTstep_hour=(60*60/stepSize)
    Time_months=t_span[::(int(numTstep_hour*24*30))]
    Time_days=t_span[::(int(numTstep_hour*24))]
    Time_halfMonth=t_span[::(int(numTstep_hour*24*15))]
    Time_5days=t_span[::(int(numTstep_hour*24*5))]#5 days

    time_extract=Time_months

    #Distance values
    x =[d/1000 for d in RS_cumLength_m]
    compartmentsLabel=["Surface\n Water", "Flowing\n Water", "Stagnant\n Water", "Sediment"]


    # Distribution of MPs per aggregation state and compartment over time relative to particle number

    MpTypeNum_t=pd.DataFrame(index=range(len(time_extract)),columns=["Timepoint (min)"]+[m+" (Total number)" for m in MPformslabels]+["Total"])
    RelativeAbun_MPtype_t=pd.DataFrame(0, columns=["Timepoint (days)"]+[m+" (%)" for m in MPformslabels], index=MpTypeNum_t.index)
    compNum_t=pd.DataFrame(index=range(len(time_extract)),columns=["Timepoint (min)"]+[m+" (Total number)" for m in compartments]+["Total"])
    #print(compNum_t)
    RelativeAbun_Comp=pd.DataFrame(0, columns=["Timepoint (days)"]+[m+" (%)" for m in compartments], index=MpTypeNum_t.index)
    for t in range(len(time_extract)):
        #Convert concentration to particle number
        PartNum_timestep=ConcFinal_num_m3.iloc[int(time_extract[t]/stepSize)]*dilution_vol_m3
        MpTypeNum_t.iloc[t,len(MPforms)+1]=sum(PartNum_timestep)
        PartNum_timestep=PartNum_timestep.to_frame()
        for mp in range(1,1+len(MPforms)):
            MpTypeNum_t.iloc[t,mp]=sum(PartNum_timestep.loc[list_of_indexesMpType[mp-1], :][time_extract[t]].to_list())
            if MpTypeNum_t.iloc[t,len(MPforms)+1] == 0:
                RelativeAbun_MPtype_t.iloc[t,mp]= 0
            else:
                RelativeAbun_MPtype_t.iloc[t,mp]=round((MpTypeNum_t.iloc[t,mp]/MpTypeNum_t.iloc[t,len(MPforms)+1])*100,2)
        for com in range(1,1+len(compartments)):
            compNum_t.iloc[t,com]=sum(PartNum_timestep.loc[list_of_indexesCompartments[com-1], :][time_extract[t]].to_list())
            if MpTypeNum_t.iloc[t,len(MPforms)+1]== 0:
                RelativeAbun_Comp.iloc[t,com]=0
            else:
                RelativeAbun_Comp.iloc[t,com]=round((compNum_t.iloc[t,com]/MpTypeNum_t.iloc[t,len(MPforms)+1])*100,2)
        RelativeAbun_MPtype_t.iloc[t,0]=t
        MpTypeNum_t.iloc[t,0]=time_extract[t]/stepSize
        compNum_t.iloc[t,0]=time_extract[t]/stepSize
        RelativeAbun_Comp.iloc[t,0]=t
    SAOutput1 = compNum_t.iloc[:,[1,2,3,4]]
    #SAOutput2 = MpTypeNum_t.iloc[:,[1,3]]
    #SAOutput = (compNum_t.iloc[3,2])
    #SAOutputCombined = pd.concat([SAOutput1, SAOutput2], axis=1)
    print(SAOutput1)
    return(SAOutput1)
   # print(SAOutput)
   # return(SAOutput)

    # Calling points for Sensitivity Analysis (total number of particles)

    # # Flowing Water
    #compNum_t.iloc[12,2]

    # # Sediment
    #compNum_t.iloc[12,4]

    # # Free    
    #MpTypeNum_t.iloc[12,1]

    # # Biofouled
    #MpTypeNum_t.iloc[12,3]
