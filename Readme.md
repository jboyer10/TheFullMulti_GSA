# TheFullMulti Global Sensitivity Analysis
Data from Boyer et al. (2026) for A Structured Multilevel Sensitivity Analysis Framework for Reducing Complexity in High-Dimensional Environmental Models: Case Study of Riverine Microplastic Vertical Transport 

### Notes on Files in FullMultiGSA Folder
- SARun2: Sensitivity Analysis (SA) run setup file
- SA_Attempt3: Model Code including SA parameters to be run using SARun2 file
- SAProcessing: Processes SA data from SA_Attempt 3 into Input and Results files
- job_slurm: SLURM job submission file

- A/A2: Many-at-a-Time Particle Characteristics simulations (1024/2048 samples)
- C/C2: Many-at-a-Time Water Body Properties simulations (1024/2048 samples)
- F/F2: Reduced-Dimensional Global Sensitivity Analysis simulations (1024/2048 samples)
- cond1-15: Conditional Expectation Evaluation for each minimum and maximum bound of the 7 Reduced-Dimensional Global Sensitivity Analysis parameters

SA Results folder contains the Inputs and Results included in Boyer et al. (2026)

### Authors
===========

Sensitivity Analysis: Dr. Jessica Boyer, Long Dang, Dr. Jeffrey Cunningham, and Dr. Mauricio Arias 
CONTACT: mearias@usf.edu

FullMulti Model: Dr. Maria del Prado Domercq and Dr. Antonia Praetorius
