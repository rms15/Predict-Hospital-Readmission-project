#!/usr/bin/python
from __future__ import division

import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from itertools import *


from sklearn import hmm

#param = 'test'
param = 'train'
short_run = 'no'
print('Running in ' + param  + ' mode')

os.chdir("/users/riazm_shaik/Rice/COMP540-StatisticalMachineLearning/project/")
os.getcwd()
###########Tranpose the file vertically. One record per patient, per admissionid per each lab test report#####
fw = open("labrecs_" + param + ".csv","wt")
writer = csv.writer(fw);

if param == 'train':
    writer.writerow(('label', 'admissionid','patientid','age','gender','admission_type','outcome','start_date','discharge_date',
    'no_prior_readm','test','count','date','result'))
else:
    writer.writerow(('admissionid','patientid','age','gender','admission_type','outcome','start_date','discharge_date',
    'no_prior_readm','test','count','date','result'))
j = 1
prev_test_cleanse = ''
if param == 'train':
    #with open("train_short.txt", 'rb') as f:
    with open("train.csv", 'rb') as f:
    #with open("train_debug.txt", 'rb') as f:
        freader = csv.reader(f, delimiter=',')
        for row in freader:
            i = 0;
            if (len(row) <= 10):
                test_record = row[0:10];
                writer.writerow(test_record)
            else:
                for i in range(10,len(row), 3):  
                    test_cleanse = row[i].replace("\t","")
                    test_record = row[0:10] 
                    test_record.append(test_cleanse) 
                    if test_cleanse == prev_test_cleanse:
                        j = j+1
                    else:
                        j = 1
                        prev_test_cleanse = test_cleanse
                    test_record.append(j)
                    test_record = test_record + row[i+1:i+3] ;
                    
#                    print test_record;
                    writer.writerow(test_record)
else:                    
        # open("test.csv", 'rb') as f:
        with open("test_short.txt", 'rb') as f:
            freader = csv.reader(f, delimiter=',')
            for row in freader:
                    i = 0;
                    if (len(row) <= 9):
                        test_record = row[0:9];
                        writer.writerow(test_record)
                    else:
                        for i in range(9,len(row), 3):  
                            test_cleanse = row[i].replace("\t","")
                            test_record = row[0:9] 
                            test_record.append(test_cleanse) 
                            if test_cleanse == prev_test_cleanse:
                                j = j+1
                            else:
                                j = 1
                                prev_test_cleanse = test_cleanse    
                            test_record.append(j)                                                                    
                            test_record = test_record + row[i+1:i+3] ;
                            writer.writerow(test_record)
    
fw.close()
f.close()

if param == 'train':
#################Summary of the file created above. Max number of test , repeat tests######
            f_labs = pd.read_csv('labrecs_'+param+'.csv',keep_default_na=False);
            print("Counts of lab tests in the file")
            print f_labs['test'].value_counts()            
            test_labels_temp = list(sorted(f_labs['test'].unique()))              
            test_labels = test_labels_temp[1:len(test_labels_temp)]
            print("List of test codes from the file",test_labels)   
            
            
            f_labs = pd.read_csv('unique_labtests.csv',keep_default_na=False);
            print f_labs['test'].value_counts()            
            test_labels_temp = list(sorted(f_labs['test'].unique()))              
            test_labels = test_labels_temp[0:len(test_labels_temp)]
            
            
            # To refresh the master data of lab test codes
            #unique_labtests = pd.DataFrame(list(sorted(f_labs['test'].unique()))[1:])
            #unique_labtests.to_csv('unique_labtests.csv',header=["test"])
            
            # to get an estimate of max number of repeat tests 
            #f_labs_grp = f_labs.groupby(['patientid','admissionid','test'])
            #test_labels.remove(nan)
            
            ### This is a static master data file for lab test codes
            if (os.path.isfile("unique_labtests.csv")):
                labtest_ref = pd.read_csv('unique_labtests.csv',keep_default_na=False);
                print("List of test codes from the master file",labtest_ref)
                if (len(labtest_ref) != len(test_labels)):
                    print("============================================================================")
                    print("There is a difference between lab test codes in the file and master data file")
                    print("Please check if the master data file needs to be updated with any new arriving codes")
                    print("count of test codes in data file:",len(test_labels),"count of test codes in master data file:",len(labtest_ref))
                    print("============================================================================")
                
                else:
                    print("============================================================================")
                    print("No new test codes in the incoming data file")
                    print("============================================================================")
else:    
            #################Summary of the file created above. Max number of test , repeat tests######
        f_labs = pd.read_csv('labrecs_' + param + '.csv',keep_default_na=False);
        print("Counts of lab tests in the file")
        print f_labs['test'].value_counts()            
        test_labels_temp = list(sorted(f_labs['test'].unique()))              
        test_labels = test_labels_temp[1:len(test_labels_temp)]
        print("List of test codes from the file",test_labels)   
        
        # To refresh the master data of lab test codes
        #unique_labtests = pd.DataFrame(list(sorted(f_labs['test'].unique()))[1:])
        #unique_labtests.to_csv('unique_labtests.csv',header=["test"])
        
        # to get an estimate of max number of repeat tests 
        #f_labs_grp = f_labs.groupby(['patientid','admissionid','test'])
        #test_labels.remove(nan)
        
        ### This is a static master data file for lab test codes
        if (os.path.isfile("unique_labtests.csv")):
            labtest_ref = pd.read_csv('unique_labtests.csv',keep_default_na=False);
            print("List of test codes from the master file",labtest_ref)
            if (len(labtest_ref) < len(test_labels)):
                print("============================================================================")
                print("There is a difference between lab test codes in the file and master data file")
                print("Please check if the master data file needs to be updated with any new arriving codes")
                print("count of test codes in data file:",len(test_labels),"count of test codes in master data file:",len(labtest_ref))
                print("============================================================================")
                sys.exit(1)    
            else:
                print("============================================================================")
                print("No new test codes in the incoming data file")
                print("============================================================================")
        
        f_labs = pd.read_csv('unique_labtests.csv',keep_default_na=False); ## Note, here we use the file created from the training data
        test_labels_temp = list(sorted(f_labs['test'].unique()))              
        test_labels = test_labels_temp[0:len(test_labels_temp)]
        print("List of test codes from the file",test_labels)   


#################Create header for the final reformatted file ####
#columns_labtest = [[] for _ in range(len(test_labels))]
counters_labtest = []
for  i in range(0,len(test_labels)) :
    counters_labtest.append(str(test_labels[i])+'_counter');   
 
#for i in range(0,len(test_labels)) :
#    counters_labtest.append(str(test_labels[i])+'_trend');     
#    counters_labtest.append(str(test_labels[i])+'_qty_inc');  
#    counters_labtest.append(str(test_labels[i])+'_qty_dec');     
     
#for i in range(0,len(test_labels)) :
#    counters_labtest.append(str(test_labels[i])+'_mean_value');  

for i in range(0,len(test_labels)) :
    counters_labtest.append(str(test_labels[i])+'_prob_devn');     
 
               
for i in range(0,len(test_labels)) :
    counters_labtest.append(str(test_labels[i])+'_devn_stats');     

for i in range(0,len(test_labels)) :
    counters_labtest.append(str(test_labels[i])+'_disch_devn_stats');     

for i in range(0,len(test_labels)) :
    counters_labtest.append(str(test_labels[i])+'_wt_devn_stats');     

#for i in range(0,len(test_labels)) :    counters_labtest.append(str(test_labels[i])+'_median_value'); 

        
columns_labtest = []      
for  i in range(0,len(test_labels)) :
#    for j in range(1,21):
#        columns_labtest.append(str(test_labels[i])+'_test'+str(j));        
#        columns_labtest.append(str(test_labels[i])+'_count'+str(j));
#        columns_labtest.append(str(test_labels[i])+'_ind'+str(j));  
#        columns_labtest.append(str(test_labels[i])+'_date'+str(j));  
#        columns_labtest.append(str(test_labels[i])+'_result'+str(j));  
         columns_labtest.append(str(test_labels[i])+'_result');  

if param == 'train':
    existing_cols = ['label', 'admissionid','patientid','age','gender','admission_type','outcome','start_date','discharge_date',
    'no_prior_readm','total_no_of_tests']
else:
    existing_cols = ['admissionid','patientid','age','gender','admission_type','outcome','start_date','discharge_date',
    'no_prior_readm','total_no_of_tests']
#newcols_list = existing_cols + list(chain(*columns_labtest))
newcols_list = existing_cols + counters_labtest + columns_labtest
newcols_list2 = existing_cols + counters_labtest
#
#only_testcols = ['test','date','result']


def identify_trend(test_devn_list):
        trend_inc = 0;
        trend_dec = 0;
        i = 0;
#        print(test_devn_list)

        for i in range(0,len(test_devn_list)-1):
          diff = abs(test_devn_list[i+1]) - abs(test_devn_list[i]);
          if (diff > 0):
                trend_inc = trend_inc + diff;
          elif (diff < 0):
                trend_dec = trend_dec + diff;
# 1 indicates increasing trend                
        if abs(trend_inc) > abs(trend_dec) :
             return ('1')
  #          return(1,trend_inc,trend_dec)
# 0 indicates decreasing trend
        else:
             return ('0')
  #          return(0,trend_inc,trend_dec)
            
     
ALB_ref_median = ALB_ref_mean = round(np.mean((35,55)),2)
ALB_ref_sd = (55-35)/4
ALP_ref_median = ALP_ref_mean = round(np.mean((44,147)),2)
ALP_ref_sd = (147-44)/4
ALT_ref_median = ALT_ref_mean = round(np.mean((7,56)),2)
ALT_ref_sd = (56-7)/4
AMYLASE_ref_median = AMYLASE_ref_mean = round(np.mean((53,123)),2)
AMYLASE_ref_sd = (123-53)/4
CAI_ref_median = CAI_ref_mean = round(np.mean((4.8,5.9)),2)
CAI_ref_sd = (5.9-4.8)/4
CK_ref_median = CK_ref_mean = round(np.mean((38,499)),2)
CK_ref_sd = (499-38)/4
CL_ref_median = CL_ref_mean = round(np.mean((96,106)),2)
CL_ref_sd = (106-96)/4
CREAT_ref_median = CREAT_ref_mean = round(np.mean((60,130)),2)
CREAT_ref_sd = (130-60)/4
GLUC_ref_median = GLUC_ref_mean = round(np.mean((7.8,11)),2)
GLUC_ref_sd = (11-7.8)/4
HB_ref_median = HB_ref_mean = round(np.mean((9.5,24)),2)
HB_ref_sd = (24-9.5)/4
LACTATE_ref_median = LACTATE_ref_mean = round(np.mean((0.5,2.2)),2)
LACTATE_ref_sd = (2.2-0.5)/4
MCH_ref_median = MCH_ref_mean = round(np.mean((27,31)),2)
MCH_ref_sd = (31-27)/4
MCHC_ref_median = MCHC_ref_mean = round(np.mean((32,36)),2)
MCHC_ref_sd = (36-32)/4
MCV_ref_median = MCV_ref_mean = round(np.mean((80,100)),2)
MCV_ref_sd = (100-80)/4
MG_ref_median = MG_ref_mean = round(np.mean((1.5,3.6)),2)
MG_ref_sd = (3.6-1.5)/4
NEUTS_ref_median = NEUTS_ref_mean = round(np.mean((1.8,7)),2)
NEUTS_ref_sd = (7-1.8)/4
OSM_ref_median = OSM_ref_mean = round(np.mean((285,295)),2)
OSM_ref_sd = (295-285)/4
PHOS_ref_median = PHOS_ref_mean = round(np.mean((1.8,3.8)),2)
PHOS_ref_sd = (3.8-1.8)/4
POT_ref_median = POT_ref_mean = round(np.mean((3.5,5.1)),2)
POT_ref_sd = (5.1-3.5)/4
RDW_ref_median = RDW_ref_mean = round(np.mean((11.6,14.6)),2)
RDW_ref_sd = (14.6-11.6)/4
TROPI_ref_median = TROPI_ref_mean = 0.5
TROPI_ref_median = TROPI_ref_mean = round(np.mean((0,0.39)),2)
TROPI_ref_sd = (0.39-0)/4

UREA_ref_median = UREA_ref_mean = round(np.mean((2.5,7.1)),2)
UREA_ref_sd = (7.1-2.5)/4
WBC_ref_median = WBC_ref_mean = round(np.mean((3.5,10.5)),2)
WBC_ref_sd = (10.5-3.5)/4

AST_ref_median = AST_ref_mean = 715
AST_ref_median = AST_ref_mean = round(np.mean((5,40)),2)
AST_ref_sd = (40-5)/4

BASOCNT_ref_median = BASOCNT_ref_mean = 0.065
BASOCNT_ref_median = BASOCNT_ref_mean = round(np.mean((0,0.5)),2)
BASOCNT_ref_sd = 0.5/4

BILI_ref_median = BILI_ref_mean = 12.875
BILI_ref_median = BILI_ref_mean = round(np.mean((1.7,20.5)),2)
BILI_ref_sd = (20.5-1.7)/4
BILICON_ref_median = BILICON_ref_mean = 27.28

## could not find ref range online. This is based on the data
BILICON_ref_median = BILICON_ref_mean = round(np.mean((5,50)),2)
BILICON_ref_sd = (50-5)/4

CA_ref_median = CA_ref_mean = 2.267
CA_ref_median = CA_ref_mean = round(np.mean((2.15,2.55)),2)
CA_ref_sd = (2.55-2.15)/4
CAUNCOR_ref_median = CAUNCOR_ref_mean = 2.235
## could not find ref range online. This is based on the data
CAUNCOR_ref_median = CAUNCOR_ref_mean = round(np.mean((1.375, 3.32)),2)
CAUNCOR_ref_sd = (3.32-1.375)/4

CRP_ref_median = CRP_ref_mean = 41.86

CRP_ref_median = CRP_ref_mean = round(np.mean((5,300)),2)
CRP_ref_sd  = (300-5)/4

EOSINCNT_ref_median = EOSINCNT_ref_mean = 0.2
EOSINCNT_ref_median = EOSINCNT_ref_mean = round(np.mean((0.08,0.4)),2)
EOSINCNT_ref_sd = (0.4-0.08)/4

GGT_ref_median = GGT_ref_mean = 182.7
GGT_ref_median = GGT_ref_mean = round(np.mean((5, 38)),2)
GGT_ref_sd = (38-5)/4

HCT_ref_median = HCT_ref_mean = 0.37
HCT_ref_median = HCT_ref_mean = round(np.mean((0.35,0.5)),2)
HCT_ref_sd = (0.5-0.35)/4

LYMPCNT_ref_median = LYMPCNT_ref_mean = 1.86
LYMPCNT_ref_median = LYMPCNT_ref_mean = round(np.mean((0.8, 4.8)),2)
LYMPCNT_ref_sd = (4.8-0.8)/4

MONOCNT_ref_median = MONOCNT_ref_mean = 0.73
MONOCNT_ref_median = MONOCNT_ref_mean = round(np.mean((0.2, 0.9)),2)
MONOCNT_ref_sd = (0.9-0.2)/4

PLT_ref_median = PLT_ref_mean = 267.27
PLT_ref_median = PLT_ref_mean = round(np.mean((150,400)),2)
PLT_ref_sd = (400-150)/4


TP_ref_median = TP_ref_mean = 66.76
TP_ref_median = TP_ref_mean = round(np.mean((60,80)),2)
TP_ref_sd = (80-60)/4

URATE_ref_median = URATE_ref_mean = 409
URATE_ref_median = URATE_ref_mean = round(np.mean((143, 416)),2)
URATE_ref_sd = (416-143)/4

POT_ref_median = POT_ref_mean = 4.24
POT_ref_median = POT_ref_mean = round(np.mean((2.4,7.4)),2)
POT_ref_sd = (7.4-2.4)/4

NA_ref_median = NA_ref_mean = round(np.mean((135,145)),2)
NA_ref_sd = (145-135)/4


################Function to populate lab test reports into fixed columns#####
##### Tests are in alphabetical order. Max repeat tests are 10 ######
##### Each test record will have 5 fields - test code, #repeat, indicator(redundant), date, result####
def populate_test_columns (test_arg,date_arg,result_arg,gender,age):
#        print('in the function')
#        print(test_arg)
#        print('test_arg passed:',test_arg)
        devn_ref = 0
        if test_arg == 'ALB':
#            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
 #           ALB_list.append(test_arg)
 #           ALB_list.append(test_counters[test_labels.index(test_arg)]);
 #           ALB_list.append(str(1));
 #           ALB_list.append(date_arg);
#            ALB_test_val.append(result_arg);  
#            if (result_arg <35 or result_arg > 55):
#                ALB_cross_range = ALB_cross_range + 1
#            ALB_count_test = test_counters[test_labels.index(test_arg)]
            devn_ref = - ALB_ref_mean + round(float(result_arg),2)
            ALB_devn_list.append(round(devn_ref,2))      
            ALB_list.append(round(devn_ref/ALB_ref_sd,2));            
        elif test_arg ==  'ALP':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
#            ALP_list.append(test_arg)
#            ALP_list.append(test_counters[test_labels.index(test_arg)]);
#            ALP_list.append(str(1));
#            ALP_list.append(date_arg);
#            ALP_list.append(result_arg); 
            ALP_test_val.append(result_arg);
#        if (result_arg <44 or result_arg > 147):
            devn_ref = - ALP_ref_mean + round(float(result_arg),2)
            #devn_prop = devn_ref/np.mean((44,147))
            ALP_devn_list.append(round(devn_ref,2))       
            ALP_list.append(round(devn_ref/ALP_ref_sd,2));            
                         
        elif test_arg ==  'ALT':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
#            ALT_list.append(test_arg)
#            ALT_list.append(test_counters[test_labels.index(test_arg)],2));
#            ALT_list.append(str(1));
#            ALT_list.append(date_arg);
#            ALT_list.append(result_arg);  
            ALT_test_val.append(result_arg);         
#        if (result_arg <7 or result_arg > 56):
            devn_ref = - ALT_ref_mean + round(float(result_arg),2)
            #devn_prop = devn_ref/np.mean((7,56))
            ALT_devn_list.append(round(devn_ref,2))    
            ALT_list.append(round(devn_ref/ALT_ref_sd,2));            
                         
        elif test_arg ==  'AMYLASE':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
#            AMYLASE_list.append(test_arg)
#            AMYLASE_list.append(test_counters[test_labels.index(test_arg)]);
 #           AMYLASE_list.append(str(1));
#            AMYLASE_list.append(date_arg);
#            AMYLASE_list.append(result_arg); 
            AMYLASE_test_val.append(result_arg);          
#        if (result_arg <53 or result_arg > 123):
            devn_ref =  - AMYLASE_ref_mean + round(float(result_arg),2)
            #devn_prop = devn_ref/np.mean((53,123))
            AMYLASE_devn_list.append(round(devn_ref,2)) 
            AMYLASE_list.append(round(devn_ref/AMYLASE_ref_sd,2));            
         
        elif test_arg ==  'AST':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
#            AST_list.append(test_arg)
#            AST_list.append(test_counters[test_labels.index(test_arg)]);
  #          AST_list.append(str(1));
#            AST_list.append(date_arg);
#            AST_list.append(result_arg);   
            AST_test_val.append(result_arg); 
            devn_ref = - AST_ref_mean + round(float(result_arg),2)       
            AST_devn_list.append(round(devn_ref,2))                                
            AST_list.append(round(devn_ref/AST_ref_sd,2));            
        elif test_arg ==  'BASOCNT':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
#            BASOCNT_list.append(test_arg)
#            BASOCNT_list.append(test_counters[test_labels.index(test_arg)]);
 #           BASOCNT_list.append(str(1));
#            BASOCNT_list.append(date_arg);
#            BASOCNT_list.append(result_arg); 
            BASOCNT_test_val.append(result_arg);  
            devn_ref = - BASOCNT_ref_mean + round(float(result_arg),2)        
            BASOCNT_devn_list.append(round(devn_ref,2))                                
            BASOCNT_list.append(round(devn_ref/BASOCNT_ref_sd,2));            

        elif test_arg ==  'BILI':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
#            BILI_list.append(test_arg)
#            BILI_list.append(test_counters[test_labels.index(test_arg)]);
   #         BILI_list.append(str(1));
#            BILI_list.append(date_arg);
#            BILI_list.append(result_arg);
            BILI_test_val.append(result_arg);
            devn_ref = - BILI_ref_mean + round(float(result_arg),2)           
            BILI_devn_list.append(round(devn_ref,2))                                
            BILI_list.append(round(devn_ref/BILI_ref_sd,2));            

        elif test_arg ==  'BILICON':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
#            BILICON_list.append(test_arg)
#            BILICON_list.append(test_counters[test_labels.index(test_arg)]);
  #          BILICON_list.append(str(1));
#            BILICON_list.append(date_arg);
#            BILICON_list.append(result_arg); 
            BILICON_test_val.append(result_arg);
            devn_ref = - BILICON_ref_mean + round(float(result_arg),2)          
            BILICON_devn_list.append(round(devn_ref,2))                                
            BILICON_list.append(round(devn_ref/BILICON_ref_sd,2));            
 
        elif test_arg ==  'CA':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
#            CA_list.append(test_arg)
#            CA_list.append(test_counters[test_labels.index(test_arg)]);
   #         CA_list.append(str(1));
#            CA_list.append(date_arg);
#            CA_list.append(result_arg);  
            CA_test_val.append(result_arg);  
            devn_ref = - CA_ref_mean + round(float(result_arg),2)       
            CA_devn_list.append(round(devn_ref,2))                                
            CA_list.append(round(devn_ref/CA_ref_sd,2));            

        elif test_arg ==  'CAI':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
#            CAI_list.append(test_arg)
#            CAI_list.append(test_counters[test_labels.index(test_arg)]);
  #          CAI_list.append(str(1));
#            CAI_list.append(date_arg);
#            CAI_list.append(result_arg);
            CAI_test_val.append(result_arg);           
#        if (result_arg <4.8 or result_arg > 5.9):
            devn_ref = - CAI_ref_mean + round(float(result_arg),2)
            #devn_prop = devn_ref/np.mean((4.8,5.9))
            CAI_devn_list.append(round(devn_ref,2))         
            CAI_list.append(round(devn_ref/CAI_ref_sd,2));            
 
        elif test_arg ==  'CAUNCOR':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
#            CAUNCOR_list.append(test_arg)
#            CAUNCOR_list.append(test_counters[test_labels.index(test_arg)]);
   #         CAUNCOR_list.append(str(1));
#            CAUNCOR_list.append(date_arg);
#            CAUNCOR_list.append(result_arg); 
            CAUNCOR_test_val.append(result_arg);  
            devn_ref = - CAUNCOR_ref_mean + round(float(result_arg),2)        
            CAUNCOR_devn_list.append(round(devn_ref,2))                                
            CAUNCOR_list.append(round(devn_ref/CAUNCOR_ref_sd,2));            

        elif test_arg ==  'CK':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
            CK_list.append(test_arg)
            CK_list.append(test_counters[test_labels.index(test_arg)]);
 #           CK_list.append(str(1));
            CK_list.append(date_arg);
            CK_list.append(result_arg);   
            CK_test_val.append(result_arg);        
#        if (result_arg <38 or result_arg > 499):
            devn_ref = -  CK_ref_mean + round(float(result_arg),2)
            #devn_prop = devn_ref/np.mean((38,499))
            CK_devn_list.append(round(devn_ref,2))          
            CK_list.append(round(devn_ref/CK_ref_sd,2));            

        elif test_arg ==  'CL':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
#            CL_list.append(test_arg)
#            CL_list.append(test_counters[test_labels.index(test_arg)]);
  #          CL_list.append(str(1));
#            CL_list.append(date_arg);
#            CL_list.append(result_arg); 
            CL_test_val.append(result_arg);          
 #       if (result_arg <96 or result_arg > 106):
            devn_ref = - CL_ref_mean + round(float(result_arg),2)
            #devn_prop = devn_ref/np.mean((96,106))
            CL_devn_list.append(round(devn_ref,2))  
            CL_list.append(round(devn_ref/CL_ref_sd,2));            
        
        elif test_arg ==  'CREAT':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
#            CREAT_list.append(test_arg)
#            CREAT_list.append(test_counters[test_labels.index(test_arg)]);
  #          CREAT_list.append(str(1));
#            CREAT_list.append(date_arg);
#            CREAT_list.append(result_arg);
            CREAT_test_val.append(result_arg);           
#          if (result_arg < 60 or result_arg > 130):
            devn_ref = - CREAT_ref_mean + round(float(result_arg),2)
            #devn_prop = devn_ref/np.mean((60,130))
            CREAT_devn_list.append(round(devn_ref,2))   
            CREAT_list.append(round(devn_ref/CREAT_ref_sd,2));            
       
        elif test_arg ==  'CRP':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
#            CRP_list.append(test_arg)
#            CRP_list.append(test_counters[test_labels.index(test_arg)]);
  #          CRP_list.append(str(1));
#            CRP_list.append(date_arg);
#            CRP_list.append(result_arg);
            CRP_test_val.append(result_arg); 
            devn_ref = - CRP_ref_mean + round(float(result_arg),2)          
            CRP_devn_list.append(round(devn_ref,2))                                
            CRP_list.append(round(devn_ref/CRP_ref_sd,2));            

        elif test_arg ==  'EOSINCNT':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
#            EOSINCNT_list.append(test_arg)
#            EOSINCNT_list.append(test_counters[test_labels.index(test_arg)]);
 #           EOSINCNT_list.append(str(1));
#            EOSINCNT_list.append(date_arg);
#            EOSINCNT_list.append(result_arg);  
            EOSINCNT_test_val.append(result_arg); 
            devn_ref = - EOSINCNT_ref_mean + round(float(result_arg),2)        
            EOSINCNT_devn_list.append(round(devn_ref,2))                                
            EOSINCNT_list.append(round(devn_ref/EOSINCNT_ref_sd,2));            

        elif test_arg ==  'GGT':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
#            GGT_list.append(test_arg)
#            GGT_list.append(test_counters[test_labels.index(test_arg)]);
 #           GGT_list.append(str(1));
#            GGT_list.append(date_arg);
#            GGT_list.append(result_arg);  
            GGT_test_val.append(result_arg); 
            devn_ref = - GGT_ref_mean + round(float(result_arg),2)        
            GGT_devn_list.append(round(devn_ref,2))                                
            GGT_list.append(round(devn_ref/GGT_ref_sd,2));            

        elif test_arg ==  'GLUC':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
#            GLUC_list.append(test_arg)
#            GLUC_list.append(test_counters[test_labels.index(test_arg)]);
   #         GLUC_list.append(str(1));
#            GLUC_list.append(date_arg);
#            GLUC_list.append(result_arg); 
            GLUC_test_val.append(result_arg);          
#        if (result_arg <7.8 or result_arg > 11):
            devn_ref = - GLUC_ref_mean + round(float(result_arg),2)
            #devn_prop = devn_ref/np.mean((7,8,11))
            GLUC_devn_list.append(round(devn_ref,2))          
            GLUC_list.append(round(devn_ref/GLUC_ref_sd,2));            

        elif test_arg ==  'HB':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
#            HB_list.append(test_arg)
#            HB_list.append(test_counters[test_labels.index(test_arg)]);
 #           HB_list.append(str(1));
#            HB_list.append(date_arg);
#            HB_list.append(result_arg);   
            HB_test_val.append(result_arg);        
            if gender == 'M' and age >= 5:
#                if (result_arg < 13.8 or result_arg > 17.2 ):
                    devn_ref = - (np.mean((13.8,17.2)) - round(float(result_arg),2))
                    #devn_prop = devn_ref/np.mean((13.8,17.2))
            elif gender == 'F' and age >= 5:
#                 if (result_arg < 12.1 or result_arg > 15.1 ):
                    devn_ref = - (np.mean((12.1,15.1)) - round(float(result_arg),2))
                    #devn_prop = devn_ref/np.mean((12.1,15.1))
            elif age >= 1:
#                 if (result_arg < 9.5 or result_arg > 13):
                    devn_ref =  -(np.mean((9.5,13)) - round(float(result_arg),2))
                    #devn_prop = devn_ref/np.mean((9.5,13))
            elif age < 1:
#                 if (result_arg < 14 or result_arg > 24):
                    devn_ref = -(np.mean((14,24)) - round(float(result_arg),2))
                    #devn_prop = devn_ref/np.mean((14,24))
            HB_devn_list.append(round(devn_ref,2))
            HB_list.append(round(devn_ref/HB_ref_sd,2));            

        elif test_arg ==  'HCT':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
#            HCT_list.append(test_arg)
#            HCT_list.append(test_counters[test_labels.index(test_arg)]);
#            HCT_list.append(str(1));
#            HCT_list.append(date_arg);
#            HCT_list.append(result_arg); 
            HCT_test_val.append(result_arg);  
            devn_ref =  - HCT_ref_mean + round(float(result_arg),2)        
            HCT_devn_list.append(round(devn_ref,2))                                
            HCT_list.append(round(devn_ref/HCT_ref_sd,2));            

        elif test_arg ==  'LACTATE':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
#            LACTATE_list.append(test_arg)
#            LACTATE_list.append(test_counters[test_labels.index(test_arg)]);
 #           LACTATE_list.append(str(1));
#            LACTATE_list.append(date_arg);
#            LACTATE_list.append(result_arg);   
            LACTATE_test_val.append(result_arg);        
#        if (result_arg <0.5 or result_arg > 2.2):
            devn_ref = - LACTATE_ref_mean + round(float(result_arg),2)
            #devn_prop = devn_ref/np.mean((0.5,2.2))
            LACTATE_devn_list.append(round(devn_ref,2))          
            LACTATE_list.append(round(devn_ref/LACTATE_ref_sd,2));            

        elif test_arg ==  'LYMPCNT':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
#            LYMPCNT_list.append(test_arg)
#            LYMPCNT_list.append(test_counters[test_labels.index(test_arg)]);
  #          LYMPCNT_list.append(str(1));
#            LYMPCNT_list.append(date_arg);
#            LYMPCNT_list.append(result_arg);  
            LYMPCNT_test_val.append(result_arg);  
            devn_ref = - LYMPCNT_ref_mean + round(float(result_arg),2)       
            LYMPCNT_devn_list.append(round(devn_ref,2))                                
            LYMPCNT_list.append(round(devn_ref/LYMPCNT_ref_sd,2));            

        elif test_arg ==  'MCH':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
#            MCH_list.append(test_arg)
#            MCH_list.append(test_counters[test_labels.index(test_arg)]);
 #           MCH_list.append(str(1));
#            MCH_list.append(date_arg);
#            MCH_list.append(result_arg); 
            MCH_test_val.append(result_arg);
#       if (result_arg <27 and result_arg > 31):
            devn_ref = - MCH_ref_mean + round(float(result_arg),2)
            #devn_prop = devn_ref/np.mean((27,31))
            MCH_devn_list.append(round(devn_ref,2))
            MCH_list.append(round(devn_ref/MCH_ref_sd,2));            
          
        elif test_arg ==  'MCHC':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
 #           MCHC_list.append(test_arg)
 #           MCHC_list.append(test_counters[test_labels.index(test_arg)]);
 #           MCHC_list.append(str(1));
 #           MCHC_list.append(date_arg);
 #           MCHC_list.append(result_arg); 
            MCHC_test_val.append(result_arg);
 #       if (result_arg <32 or result_arg > 36):
            devn_ref = - MCHC_ref_mean + round(float(result_arg),2)
            #devn_prop = devn_ref/np.mean((32,36))
            MCHC_devn_list.append(round(devn_ref,2))  
            MCHC_list.append(round(devn_ref/MCHC_ref_sd,2));            
        
        elif test_arg ==  'MCV':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
#            MCV_list.append(test_arg)
#            MCV_list.append(test_counters[test_labels.index(test_arg)]);
  #          MCV_list.append(str(1));
#            MCV_list.append(date_arg);
#            MCV_list.append(result_arg); 
            MCV_test_val.append(result_arg);          
#        if (result_arg <80 or result_arg > 100):
            devn_ref = - MCV_ref_mean + round(float(result_arg),2)
            #devn_prop = devn_ref/np.mean((80,100))
            MCV_devn_list.append(round(devn_ref,2)) 
            MCV_list.append(round(devn_ref/MCV_ref_sd,2));            
         
        elif test_arg ==  'MG':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
#            MG_list.append(test_arg)
#            MG_list.append(test_counters[test_labels.index(test_arg)]);
  #          MG_list.append(str(1));
#            MG_list.append(date_arg);
 #           MG_list.append(result_arg);
            MG_test_val.append(result_arg);           
#        if (result_arg <1.5 or result_arg > 3.6):
            devn_ref = - MG_ref_mean + round(float(result_arg),2)
            #devn_prop = devn_ref/np.mean((1.5,3.6))
            MG_devn_list.append(round(devn_ref,2))     
            MG_list.append(round(devn_ref/MG_ref_sd,2));     
        elif test_arg ==  'MONOCNT':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
  #          MONOCNT_list.append(test_arg)
  #          MONOCNT_list.append(test_counters[test_labels.index(test_arg)]);
  #          MONOCNT_list.append(str(1));
  #          MONOCNT_list.append(date_arg);
  #          MONOCNT_list.append(result_arg);  
            MONOCNT_test_val.append(result_arg); 
            devn_ref = - MONOCNT_ref_mean + round(float(result_arg),2)        
            MONOCNT_devn_list.append(round(devn_ref,2))   
            MONOCNT_list.append(round(devn_ref/MONOCNT_ref_sd,2));                             
        elif test_arg ==  'NA':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
#            NA_list.append(test_arg)
#            NA_list.append(test_counters[test_labels.index(test_arg)]);
  #         NA_list.append(str(1));
#            NA_list.append(date_arg);
#            NA_list.append(result_arg);  
            NA_test_val.append(result_arg); 
            devn_ref = - NA_ref_mean + round(float(result_arg),2)        
            NA_devn_list.append(round(devn_ref,2)) 
            NA_list.append(round(devn_ref/NA_ref_sd,2));   
        elif test_arg ==  'NEUTS':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
 #           NEUTS_list.append(test_arg)
 #           NEUTS_list.append(test_counters[test_labels.index(test_arg)]);
 #           NEUTS_list.append(str(1));
 #           NEUTS_list.append(date_arg);
 #           NEUTS_list.append(result_arg); 
            NEUTS_test_val.append(result_arg);          
 #       if (result_arg <1.8 or result_arg > 7):
            devn_ref = - NEUTS_ref_mean + round(float(result_arg),2)
            #devn_prop = devn_ref/np.mean((1.8,7))
            NEUTS_devn_list.append(round(devn_ref,2))   
            NEUTS_list.append(round(devn_ref/NEUTS_ref_sd,2));       
        elif test_arg ==  'OSM':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
 #           OSM_list.append(test_arg)
 #           OSM_list.append(test_counters[test_labels.index(test_arg)]);
  #          OSM_list.append(str(1));
 #           OSM_list.append(date_arg);
 #           OSM_list.append(result_arg); 
            OSM_test_val.append(result_arg);          
#        if (result_arg <285 or result_arg > 295):
            devn_ref = - OSM_ref_mean + round(float(result_arg),2)
            #devn_prop = devn_ref/np.mean((285,295))
            OSM_devn_list.append(round(devn_ref,2))      
            OSM_list.append(round(devn_ref/OSM_ref_sd,2)); 
        elif test_arg ==  'PHOS':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
 #           PHOS_list.append(test_arg)
 #           PHOS_list.append(test_counters[test_labels.index(test_arg)]);
 #           PHOS_list.append(str(1));
 #           PHOS_list.append(date_arg);
 #           PHOS_list.append(result_arg); 
            PHOS_test_val.append(result_arg);          
#        if (result_arg <1.8 or result_arg > 3.8):
            devn_ref = - PHOS_ref_mean + round(float(result_arg),2)
            #devn_prop = devn_ref/np.mean((1.8,3.8))
            PHOS_devn_list.append(round(devn_ref,2)) 
            PHOS_list.append(round(devn_ref/PHOS_ref_sd,2));         
        elif test_arg ==  'PLT':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
 #           PLT_list.append(test_arg)
 #           PLT_list.append(test_counters[test_labels.index(test_arg)]);
 #           PLT_list.append(str(1));
 #           PLT_list.append(date_arg);
 #           PLT_list.append(result_arg);
            PLT_test_val.append(result_arg);  
            devn_ref = - PLT_ref_mean + round(float(result_arg),2)
# COMMENTED as it was giving very high values
#            if (result_arg < 150000 or result_arg > 400000):
#                  devn_ref = np.mean((150000,400000))- round(float(result_arg),2)
            PLT_devn_list.append(round(devn_ref,2))  
            PLT_list.append(round(devn_ref/PLT_ref_sd,2));                
        elif test_arg ==  'POT':
            # print('match found')
            
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
  #          POT_list.append(test_arg)
  #          POT_list.append(test_counters[test_labels.index(test_arg)]);
#            POT_list.append(str(1));
  #          POT_list.append(date_arg);
  #          POT_list.append(result_arg);  
            POT_test_val.append(result_arg);
#            if age > 18:
#            if  result_arg >= 3.5 and result_arg <= 5.1:
            devn_ref = - POT_ref_mean + round(float(result_arg),2)
                    #devn_prop = devn_ref/np.mean((3.5,5.1))                       
            POT_list.append(round(devn_ref,2))
            POT_list.append(round(devn_ref/POT_ref_sd,2));
        elif test_arg ==  'RDW':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
  #          RDW_list.append(test_arg)
  #          RDW_list.append(test_counters[test_labels.index(test_arg)]);
#            RDW_list.append(str(1));
  #          RDW_list.append(date_arg);
  #          RDW_list.append(result_arg); 
            RDW_test_val.append(result_arg);          
 #       if (result_arg < 11.6 or result_arg > 14.6):
            devn_ref = - RDW_ref_mean + round(float(result_arg),2)
            #devn_prop = devn_ref/np.mean((11.6,14.6))
            RDW_devn_list.append(round(devn_ref,2)) 
            RDW_list.append(round(devn_ref/RDW_ref_sd,2));         
        elif test_arg ==  'TP':
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
 #           TP_list.append(test_arg)
 #           TP_list.append(test_counters[test_labels.index(test_arg)]);
   #         TP_list.append(str(1));
 #           TP_list.append(date_arg);
 #           TP_list.append(result_arg);   
            TP_test_val.append(result_arg);  
            devn_ref = - TP_ref_mean + round(float(result_arg),2)      
            TP_devn_list.append(round(devn_ref,2)) 
            TP_list.append(round(devn_ref/TP_ref_sd,2));                               

        elif test_arg ==  'TROPI':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
 #           TROPI_list.append(test_arg)
 #           TROPI_list.append(test_counters[test_labels.index(test_arg)]);
 #           TROPI_list.append(str(1));
 #           TROPI_list.append(date_arg);
 #           TROPI_list.append(result_arg);  
            TROPI_test_val.append(result_arg);         
 #       if (result_arg > 0.5):
            devn_ref = - TROPI_ref_mean + round(float(result_arg),2)
            TROPI_devn_list.append(round(devn_ref,2))    
            TROPI_list.append(round(devn_ref/TROPI_ref_sd,2));      

        elif test_arg ==  'URATE':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
  #          URATE_list.append(test_arg)
  #          URATE_list.append(test_counters[test_labels.index(test_arg)]);
  #          URATE_list.append(str(1));
  #          URATE_list.append(date_arg);
  #          URATE_list.append(result_arg); 
            URATE_test_val.append(result_arg);
            devn_ref = - URATE_ref_mean + round(float(result_arg),2)          
            URATE_devn_list.append(round(devn_ref,2))  
            URATE_list.append(round(devn_ref/URATE_ref_sd,2));                              

        elif test_arg ==  'UREA':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
   #         UREA_list.append(test_arg)
   #         UREA_list.append(test_counters[test_labels.index(test_arg)]);
  #          UREA_list.append(str(1));
   #         UREA_list.append(date_arg);
   #         UREA_list.append(result_arg); 
            UREA_test_val.append(result_arg);          
#        if (result_arg < 2.5 or result_arg > 7.1):
            devn_ref = - UREA_ref_mean + round(float(result_arg),2)
            #devn_prop = devn_ref/np.mean((2.5,7.1))
            UREA_devn_list.append(round(devn_ref,2))   
            UREA_list.append(round(devn_ref/UREA_ref_sd,2));       
        elif test_arg ==  'WBC':
            # print('match found')
            test_counters[test_labels.index(test_arg)] = test_counters[test_labels.index(test_arg)] + 1;
 #           WBC_list.append(test_arg)
 #           WBC_list.append(test_counters[test_labels.index(test_arg)]);
 #           WBC_list.append(str(1));
 #           WBC_list.append(date_arg);
  #          WBC_list.append(result_arg);
            WBC_test_val.append(result_arg);
#        if (result_arg <3.5 or result_arg > 10.5):
            devn_ref =  - WBC_ref_mean + round(float(result_arg),2)
            #devn_prop = devn_ref/np.mean((3.5,10.5))
            WBC_devn_list.append(round(devn_ref,2))   
            WBC_list.append(round(devn_ref/WBC_ref_sd,2));         
        return test_counters,ALB_list,ALP_list,ALT_list,AMYLASE_list,AST_list,BASOCNT_list,BILI_list,BILICON_list,\
        CA_list,CAI_list,CAUNCOR_list,CK_list,CL_list,CREAT_list,CRP_list,\
        EOSINCNT_list,GGT_list,GLUC_list,HB_list,HCT_list,\
        LACTATE_list,LYMPCNT_list,MCH_list,MCHC_list,MCV_list,MG_list,MONOCNT_list,NA_list,\
        NEUTS_list,OSM_list,PHOS_list,PLT_list,POT_list,RDW_list,TP_list,TROPI_list,\
        URATE_list,UREA_list,WBC_list,
        ALP_devn_list,
        ALT_devn_list,
        AMYLASE_devn_list,
        AST_devn_list,
        BASOCNT_devn_list,
        BILI_devn_list,
        BILICON_devn_list,
        CA_devn_list,
        CAI_devn_list,
        CAUNCOR_devn_list,
        CK_devn_list,
        CL_devn_list,
        CREAT_devn_list,
        CRP_devn_list,
        EOSINCNT_devn_list,
        GGT_devn_list,
        GLUC_devn_list,
        HB_devn_list,
        HCT_devn_list,
        LACTATE_devn_list,
        LYMPCNT_devn_list,
        MCH_devn_list,
        MCHC_devn_list,
        MCV_devn_list,
        MG_devn_list,
        MONOCNT_devn_list,
        NA_devn_list,
        NEUTS_devn_list,
        OSM_devn_list,
        PHOS_devn_list,
        PLT_devn_list,
        POT_devn_list,
        RDW_devn_list,
        TP_devn_list,
        TROPI_devn_list,
        URATE_devn_list,
        UREA_devn_list,
        WBC_devn_list,
        ALB_test_val,
        ALP_test_val,
        ALT_test_val,
        AMYLASE_test_val,
        AST_test_val,
        BASOCNT_test_val,
        BILI_test_val,
        BILICON_test_val,
        CA_test_val,
        CAI_test_val,
        CAUNCOR_test_val,
        CK_test_val,
        CL_test_val,
        CREAT_test_val,
        CRP_test_val,
        EOSINCNT_test_val,
        GGT_test_val,
        GLUC_test_val,
        HB_test_val,
        HCT_test_val,
        LACTATE_test_val,
        LYMPCNT_test_val,
        MCH_test_val,
        MCHC_test_val,
        MCV_test_val,
        MG_test_val,
        MONOCNT_test_val,
        NA_test_val,
        NEUTS_test_val,
        OSM_test_val,
        PHOS_test_val,
        PLT_test_val,
        POT_test_val,
        RDW_test_val,
        TP_test_val,
        TROPI_test_val,
        URATE_test_val,
        UREA_test_val,
        WBC_test_val
        





#fl = open("labrecs.csv", 'rb') 
#wr_fnew.writerow(newcols_list)
global ALB_list  
global ALP_list  
global ALT_list  
global AMYLASE_list  
global AST_list  
global BASOCNT_list  
global BILI_list  
global BILICON_list  
global CA_list  
global CAI_list  
global CAUNCOR_list  
global CK_list  
global CL_list  
global CREAT_list  
global CRP_list  
global EOSINCNT_list  
global GGT_list  
global GLUC_list  
global HB_list  
global HCT_list  
global LACTATE_list  
global LYMPCNT_list  
global MCH_list  
global MCHC_list  
global MCV_list  
global MG_list  
global MONOCNT_list
global NA_list  
global NEUTS_list  
global OSM_list  
global PHOS_list  
global PLT_list  
global POT_list  
global RDW_list  
global TP_list  
global TROPI_list  
global URATE_list  
global UREA_list  
global WBC_list
global test_counters





ALB_list = []
ALP_list = []
ALT_list = []
AMYLASE_list = []
AST_list = []
BASOCNT_list = []
BILI_list = []
BILICON_list = []
CA_list = []
CAI_list = []
CAUNCOR_list = []
CK_list = []
CL_list = []
CREAT_list = []
CRP_list = []
EOSINCNT_list = []
GGT_list = []
GLUC_list = []
HB_list = []
HCT_list = []
LACTATE_list = []
LYMPCNT_list = []
MCH_list = []
MCHC_list = []
MCV_list = []
MG_list = []
MONOCNT_list = []
NA_list = []
NEUTS_list = []
OSM_list = []
PHOS_list = []
PLT_list = []
POT_list = []
RDW_list = []
TP_list = []
TROPI_list = []
URATE_list = []
UREA_list = []
WBC_list = []

global ALP_devn_list 
global ALT_devn_list 
global AMYLASE_devn_list 
global AST_devn_list 
global BASOCNT_devn_list 
global BILI_devn_list 
global BILICON_devn_list 
global CA_devn_list 
global CAI_devn_list 
global CAUNCOR_devn_list 
global CK_devn_list 
global CL_devn_list 
global CREAT_devn_list 
global CRP_devn_list 
global EOSINCNT_devn_list 
global GGT_devn_list 
global GLUC_devn_list 
global HB_devn_list 
global HCT_devn_list 
global LACTATE_devn_list 
global LYMPCNT_devn_list 
global MCH_devn_list 
global MCHC_devn_list 
global MCV_devn_list 
global MG_devn_list 
global MONOCNT_devn_list 
global NA_devn_list
global NEUTS_devn_list 
global OSM_devn_list 
global PHOS_devn_list 
global PLT_devn_list 
global POT_devn_list 
global RDW_devn_list 
global TP_devn_list 
global TROPI_devn_list 
global URATE_devn_list 
global UREA_devn_list 
global WBC_devn_list 

global ALB_test_val 
global ALP_test_val 
global ALT_test_val 
global AMYLASE_test_val 
global AST_test_val 
global BASOCNT_test_val 
global BILI_test_val 
global BILICON_test_val 
global CA_test_val 
global CAI_test_val 
global CAUNCOR_test_val 
global CK_test_val 
global CL_test_val 
global CREAT_test_val 
global CRP_test_val 
global EOSINCNT_test_val 
global GGT_test_val 
global GLUC_test_val 
global HB_test_val 
global HCT_test_val 
global LACTATE_test_val 
global LYMPCNT_test_val 
global MCH_test_val 
global MCHC_test_val 
global MCV_test_val 
global MG_test_val 
global MONOCNT_test_val 
global NA_test_val
global NEUTS_test_val 
global OSM_test_val 
global PHOS_test_val 
global PLT_test_val 
global POT_test_val 
global RDW_test_val 
global TP_test_val 
global TROPI_test_val 
global URATE_test_val 
global UREA_test_val 
global WBC_test_val 

ALB_devn_list = [0]
ALP_devn_list = [0]
ALT_devn_list = [0]
AMYLASE_devn_list = [0]
AST_devn_list = [0]
BASOCNT_devn_list = [0]
BILI_devn_list = [0]
BILICON_devn_list = [0]
CA_devn_list = [0]
CAI_devn_list = [0]
CAUNCOR_devn_list = [0]
CK_devn_list = [0]
CL_devn_list = [0]
CREAT_devn_list = [0]
CRP_devn_list = [0]
EOSINCNT_devn_list = [0]
GGT_devn_list = [0]
GLUC_devn_list = [0]
HB_devn_list = [0]
HCT_devn_list = [0]
LACTATE_devn_list = [0]
LYMPCNT_devn_list = [0]
MCH_devn_list = [0]
MCHC_devn_list = [0]
MCV_devn_list = [0]
MG_devn_list = [0]
MONOCNT_devn_list = [0]
NA_devn_list = [0]
NEUTS_devn_list = [0]
OSM_devn_list = [0]
PHOS_devn_list = [0]
PLT_devn_list = [0]
POT_devn_list = [0]
RDW_devn_list = [0]
TP_devn_list = [0]
TROPI_devn_list = [0]
URATE_devn_list = [0]
UREA_devn_list = [0]
WBC_devn_list = [0]

ALB_test_val = []
ALP_test_val = []
ALT_test_val = []
AMYLASE_test_val = []
AST_test_val = []
BASOCNT_test_val = []
BILI_test_val = []
BILICON_test_val = []
CA_test_val = []
CAI_test_val = []
CAUNCOR_test_val = []
CK_test_val = []
CL_test_val = []
CREAT_test_val = []
CRP_test_val = []
EOSINCNT_test_val = []
GGT_test_val = []
GLUC_test_val = []
HB_test_val = []
HCT_test_val = []
LACTATE_test_val = []
LYMPCNT_test_val = []
MCH_test_val = []
MCHC_test_val = []
MCV_test_val = []
MG_test_val = []
MONOCNT_test_val = []
NA_test_val = []
NEUTS_test_val = []
OSM_test_val = []
PHOS_test_val = []
PLT_test_val = []
POT_test_val = []
RDW_test_val = []
TP_test_val = []
TROPI_test_val = []
URATE_test_val = []
UREA_test_val = []
WBC_test_val = []
devn_stats = []
disch_devn_stats = []
wt_devn_stats = []
prob_devn = []

def get_sum_wtsq_devn(arg_test_list):
    i = 1
    sum_wtsq_devn = 0
    if len(arg_test_list) == 0:
        return 0
    else:
        for i in range(1,len(arg_test_list)):
#            print(arg_test_list[i])
            sum_wtsq_devn = sum_wtsq_devn + (i*(arg_test_list[i]**2) )
#            print("sum_wtsq_devn:",sum_wtsq_devn)
        return round(sum_wtsq_devn/float(i),2)
        
# last few readings

def get_discharge_devn(arg_test_list):
    i = 1
    sum_wtsq_devn = 0
    if len(arg_test_list) <=5:
        for i in range(1,len(arg_test_list)):
#            print(arg_test_list[i])
            sum_wtsq_devn = sum_wtsq_devn + (arg_test_list[i]**2)
#            print("sum_wtsq_devn:",sum_wtsq_devn)
        return round(sum_wtsq_devn/float(i),2)
    else:
        for i in range(len(arg_test_list)-1,len(arg_test_list)-6,-1):
 #               print(arg_test_list[i])
                sum_wtsq_devn = sum_wtsq_devn + (arg_test_list[i]**2)
#                print("sum_wtsq_devn:",sum_wtsq_devn)
        return round(sum_wtsq_devn/5.0,2)

    
report_trend = []

prev_admissionid = ''
prev_patientid = ''
first_rec = 1

testlim=0
record_count = 0

if param == 'train':
    if short_run == 'yes':
        fnew = open("train_mod_short.txt","wt")    
        fmodc = open("train_mod_counts_short.txt","wt")
    else:
        fnew = open("train_mod.txt","wt")    
        fmodc = open("train_mod_counts.txt","wt")
else:
        if short_run == 'yes':            
                fnew = open("test_mod_short.txt","wt")
                fmodc = open("test_mod_counts_short.txt","wt")
        else:
                fnew = open("test_mod.txt","wt")
                fmodc = open("test_mod_counts.txt","wt")


wr_fnew = csv.writer(fnew, delimiter='\t');
wr_fnew.writerow(newcols_list)
wr_fmodc = csv.writer(fmodc, delimiter='\t');
wr_fmodc.writerow(newcols_list2)

if param == 'train':
    basic_cols_index = 10
else:
    basic_cols_index = 9

def map_emission_states(arg_list):
        for i in range(len(arg_list)):
            if arg_list[i] <= -1.6 :
                arg_list[i] = 1
            elif arg_list[i] >= 1.6:
                arg_list[i] = 1
            else:
                arg_list[i] = 0
#        print("arg_list:",arg_list)
        return arg_list
################ Go thru the vertical formatted file and populate the new reformatted file with fixed test record columns####

with open("labrecs_" + param + ".csv", 'rb') as fl:
    flreader = csv.reader(fl, delimiter=',')
    flreader.next()
    for row in flreader:
#        print('entered the loop')
#        record = flreader.next()
#        print prev_admissionid
#        print prev_patientid
        if param == 'train':
            curr_admissionid = row[1:2]
            curr_patientid = row[2:3] 
        else:
            curr_admissionid = row[0:1]
            curr_patientid = row[1:2]
 
        if (prev_admissionid != curr_admissionid or prev_patientid != curr_patientid): 
            
#                print('different patient record')
                if param == 'train':
                    prev_admissionid = row[1:2]
                    prev_patientid = row[2:3]
                else:
                    prev_admissionid = row[0:1]
                    prev_patientid = row[1:2]
## if the keys are different, write the record to the file
                if first_rec !=1:



#                    print('merge list')
#                    print test_record

                    ALB_test_valN = map(float,ALB_test_val)	
                    ALP_test_valN = map(float,ALP_test_val)
                    ALT_test_valN = map(float,ALT_test_val)
                    AMYLASE_test_valN = map(float,AMYLASE_test_val)
                    AST_test_valN = map(float,AST_test_val)
                    BASOCNT_test_valN = map(float,BASOCNT_test_val)
                    BILI_test_valN = map(float,BILI_test_val)
                    BILICON_test_valN = map(float,BILICON_test_val)
                    CA_test_valN = map(float,CA_test_val)
                    CAI_test_valN = map(float,CAI_test_val)
                    CAUNCOR_test_valN = map(float,CAUNCOR_test_val)
                    CK_test_valN = map(float,CK_test_val)
                    CL_test_valN = map(float,CL_test_val)
                    CREAT_test_valN = map(float,CREAT_test_val)
                    CRP_test_valN = map(float,CRP_test_val)
                    EOSINCNT_test_valN = map(float,EOSINCNT_test_val)
                    GGT_test_valN = map(float,GGT_test_val)
                    GLUC_test_valN = map(float,GLUC_test_val)
                    HB_test_valN = map(float,HB_test_val)
                    HCT_test_valN = map(float,HCT_test_val)
                    LACTATE_test_valN = map(float,LACTATE_test_val)
                    LYMPCNT_test_valN = map(float,LYMPCNT_test_val)
                    MCH_test_valN = map(float,MCH_test_val)
                    MCHC_test_valN = map(float,MCHC_test_val)
                    MCV_test_valN = map(float,MCV_test_val)
                    MG_test_valN = map(float,MG_test_val)
                    MONOCNT_test_valN = map(float,MONOCNT_test_val)
                    NA_test_valN = map(float,NA_test_val)
                    NEUTS_test_valN = map(float,NEUTS_test_val)
                    OSM_test_valN = map(float,OSM_test_val)
                    PHOS_test_valN = map(float,PHOS_test_val)
                    PLT_test_valN = map(float,PLT_test_val)
                    POT_test_valN = map(float,POT_test_val)
                    RDW_test_valN = map(float,RDW_test_val)
                    TP_test_valN = map(float,TP_test_val)
                    TROPI_test_valN = map(float,TROPI_test_val)
                    URATE_test_valN = map(float,URATE_test_val)
                    UREA_test_valN = map(float,UREA_test_val)
                    WBC_test_valN = map(float,WBC_test_val)
                    
                    ALB_list= (map_emission_states(ALB_list))
                    ALP_list= (map_emission_states(ALP_list))
                    ALT_list=(map_emission_states(ALT_list))
                    AMYLASE_list= (map_emission_states(AMYLASE_list))
                    AST_list= (map_emission_states(AST_list))
                    BASOCNT_list=  (map_emission_states(BASOCNT_list))
                    BILI_list=  (map_emission_states(BILI_list))
                    BILICON_list= (map_emission_states(BILICON_list))
                    CA_list= (map_emission_states(CA_list))
                    CAI_list=(map_emission_states(CAI_list))
                    CAUNCOR_list= (map_emission_states(CAUNCOR_list))
                    CK_list=  (map_emission_states(CK_list))
                    CK_list= (map_emission_states(CK_list))
                    CREAT_list=  (map_emission_states(CREAT_list))
                    CRP_list=  (map_emission_states(CRP_list))
                    EOSINCNT_list= (map_emission_states(EOSINCNT_list))
                    GGT_list= (map_emission_states(GGT_list))
                    GLUC_list=(map_emission_states(GLUC_list))
                    HB_list= (map_emission_states(HB_list))
                    HCT_list= (map_emission_states(HCT_list))
                    LACTATE_list= (map_emission_states(LACTATE_list))
                    LYMPCNT_list= (map_emission_states(LYMPCNT_list))
                    MCH_list= (map_emission_states(MCH_list))
                    MCHC_list= (map_emission_states(MCHC_list))
                    MCV_list=  (map_emission_states(MCV_list))
                    MG_list=  (map_emission_states(MG_list))
                    MONOCNT_list=  map_emission_states(MONOCNT_list)
                    NA_list= (map_emission_states(NA_list))
                    NEUTS_list= (map_emission_states(NEUTS_list))
                    OSM_list=  (map_emission_states(OSM_list))
                    PHOS_list= (map_emission_states(PHOS_list))
                    PLT_list=  (map_emission_states(PLT_list))
                    POT_list= (map_emission_states(POT_list))
                    RDW_list=   (map_emission_states(RDW_list))
                    TP_list=  (map_emission_states(TP_list))
                    TROPI_list= (map_emission_states(TROPI_list))
                    URATE_list=   (map_emission_states(URATE_list))
                    UREA_list=  (map_emission_states(UREA_list))
                    WBC_list=  (map_emission_states(WBC_list))

                    prob_devn.append(round(sum(ALB_list)/(1+len(ALB_list)),2))                    
                    prob_devn.append(sum(ALP_list)/(1+len(ALP_list)))
                    prob_devn.append(sum(ALT_list)/(1+len(ALT_list)))
                    prob_devn.append(sum(AMYLASE_list)/(1+len(AMYLASE_list)))
                    prob_devn.append(sum(AST_list)/(1+len(AST_list)))
                    prob_devn.append(sum(BASOCNT_list)/(1+len(BASOCNT_list)))
                    prob_devn.append(sum(BILI_list)/(1+len(BILI_list)))
                    prob_devn.append(sum(BILICON_list)/(1+len(BILICON_list)))
                    prob_devn.append(sum(CA_list)/(1+len(CA_list)))
                    prob_devn.append(sum(CAI_list)/(1+len(CAI_list)))
                    prob_devn.append(sum(CAUNCOR_list)/(1+len(CAUNCOR_list)))
                    prob_devn.append(sum(CK_list)/(1+len(CK_list)))
                    prob_devn.append(sum(CL_list)/(1+len(CL_list)))
                    prob_devn.append(sum(CREAT_list)/(1+len(CREAT_list)))
                    prob_devn.append(sum(CRP_list)/(1+len(CRP_list)))
                    prob_devn.append(sum(EOSINCNT_list)/(1+len(EOSINCNT_list)) )
                    prob_devn.append(sum(GGT_list)/(1+len(GGT_list)))
                    prob_devn.append(sum(GLUC_list)/(1+len(GLUC_list)))
                    prob_devn.append(sum(HB_list)/(1+len(HB_list)))
                    prob_devn.append(sum(HCT_list)/(1+len(HCT_list)))
                    prob_devn.append(sum(LACTATE_list)/(1+len(LACTATE_list)))
                    prob_devn.append(sum(LYMPCNT_list)/(1+len(LYMPCNT_list)))
                    prob_devn.append(sum(MCH_list)/(1+len(MCH_list)))
                    prob_devn.append(sum(MCHC_list)/(1+len(MCHC_list)))
                    prob_devn.append(sum(MCV_list)/(1+len(MCV_list)))
                    prob_devn.append(sum(MG_list)/(1+len(MG_list)))
                    prob_devn.append(sum(MONOCNT_list)/(1+len(MONOCNT_list)))
                    prob_devn.append(sum(NA_list)/(1+len(NA_list)))
                    prob_devn.append(sum(NEUTS_list)/(1+len(NEUTS_list)))
                    prob_devn.append(sum(OSM_list)/(1+len(OSM_list)))
                    prob_devn.append(sum(PHOS_list)/(1+len(PHOS_list)))
                    prob_devn.append(sum(PLT_list)/(1+len(PLT_list)))
                    prob_devn.append(sum(POT_list)/(1+len(POT_list)))
                    prob_devn.append(sum(RDW_list)/(1+len(RDW_list)))
                    prob_devn.append(sum(TP_list)/(1+len(TP_list)))
                    prob_devn.append(sum(TROPI_list)/(1+len(TROPI_list)))
                    prob_devn.append(sum(URATE_list)/(1+len(URATE_list)))
                    prob_devn.append(sum(UREA_list)/(1+len(UREA_list)))
                    prob_devn.append(sum(WBC_list)/(1+len(WBC_list))) 
                    
                    if len(ALB_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(ALB_devn_list)/ALB_ref_sd)**2))/(len(ALB_devn_list)-1))
                    else:
                        devn_stats.append(0)
                    
                    if len(ALP_devn_list) > 1:    
                        devn_stats.append(np.sum(((np.asarray(ALP_devn_list)/ALP_ref_sd)**2))/(len(ALP_devn_list)-1))
                    else:
                        devn_stats.append(0)
                        
                    if len(ALT_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(ALT_devn_list)/ALT_ref_sd)**2))/(len(ALT_devn_list)-1))
                    else:
                        devn_stats.append(0)
                        
                    if len(AMYLASE_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(AMYLASE_devn_list)/AMYLASE_ref_sd)**2))/(len(AMYLASE_devn_list)-1))
                    else:
                        devn_stats.append(0)
                    
                    if len(AST_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(AST_devn_list)/AST_ref_sd)**2))/(len(AST_devn_list)-1))
                    else:
                        devn_stats.append(0)
                    
                    if len(BASOCNT_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(BASOCNT_devn_list)/BASOCNT_ref_sd)**2))/(len(BASOCNT_devn_list)-1))
                    else:
                        devn_stats.append(0)
                    
                    if len(BILI_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(BILI_devn_list)/BILI_ref_sd)**2))/(len(BILI_devn_list)-1))
                    else:
                        devn_stats.append(0)
                            
                    if len(BILICON_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(BILICON_devn_list)/BILICON_ref_sd)**2))/(len(BILICON_devn_list)-1))
                    else:
                        devn_stats.append(0)
                            
                    if len(CA_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(CA_devn_list)/CA_ref_sd)**2))/(len(CA_devn_list)-1))
                    else:
                        devn_stats.append(0)
                    
                    if len(CAI_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(CAI_devn_list)/CAI_ref_sd)**2))/(len(CAI_devn_list)-1))
                    else:
                        devn_stats.append(0)
                        
                    if len(CAUNCOR_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(CAUNCOR_devn_list)/CAUNCOR_ref_sd)**2))/(len(CAUNCOR_devn_list)-1))
                    else:
                        devn_stats.append(0)
                    
                    if len(CK_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(CK_devn_list)/CK_ref_sd)**2))/(len(CK_devn_list)-1))
                    else:
                        devn_stats.append(0)
                            
                    if len(CL_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(CL_devn_list)/CL_ref_sd)**2))/(len(CL_devn_list)-1))
                    else:
                        devn_stats.append(0)
                        
                    if len(CREAT_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(CREAT_devn_list)/CREAT_ref_sd)**2))/(len(CREAT_devn_list)-1))
                    else:
                        devn_stats.append(0)
                        
                    if len(CRP_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(CRP_devn_list)/CRP_ref_sd)**2))/(len(CRP_devn_list)-1))
                    else:
                        devn_stats.append(0)
                        
                    if len(EOSINCNT_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(EOSINCNT_devn_list)/EOSINCNT_ref_sd)**2))/(len(EOSINCNT_devn_list)-1))
                    else:
                        devn_stats.append(0)
                            
                    if len(GGT_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(GGT_devn_list)/GGT_ref_sd)**2))/(len(GGT_devn_list)-1))
                    else:
                        devn_stats.append(0)
                            
                    if len(GLUC_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(GLUC_devn_list)/GLUC_ref_sd)**2))/(len(GLUC_devn_list)-1))
                    else:
                        devn_stats.append(0)
                            
                    if len(HB_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(HB_devn_list)/HB_ref_sd)**2))/(len(HB_devn_list)-1))
                    else:
                        devn_stats.append(0)
                        
                    if len(HCT_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(HCT_devn_list)/HCT_ref_sd)**2))/(len(HCT_devn_list)-1))
                    else:
                        devn_stats.append(0)
                        
                    if len(LACTATE_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(LACTATE_devn_list)/LACTATE_ref_sd)**2))/(len(LACTATE_devn_list)-1))
                    else:
                        devn_stats.append(0)
                        
                    if len(LYMPCNT_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(LYMPCNT_devn_list)/LYMPCNT_ref_sd)**2))/(len(LYMPCNT_devn_list)-1))
                    else:
                        devn_stats.append(0)
                    
                    if len(MCH_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(MCH_devn_list)/MCH_ref_sd)**2))/(len(MCH_devn_list)-1))
                    else:
                        devn_stats.append(0)
                    
                    if len(MCHC_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(MCHC_devn_list)/MCHC_ref_sd)**2))/(len(MCHC_devn_list)-1))
                    else:
                        devn_stats.append(0)
                        
                    if len(MCV_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(MCV_devn_list)/MCV_ref_sd)**2))/(len(MCV_devn_list)-1))
                    else:
                        devn_stats.append(0)
                        
                    if len(MG_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(MG_devn_list)/MG_ref_sd)**2))/(len(MG_devn_list)-1))
                    else:
                        devn_stats.append(0)
                        
                    if len(MONOCNT_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(MONOCNT_devn_list)/MONOCNT_ref_sd)**2))/(len(MONOCNT_devn_list)-1))
                    else:
                        devn_stats.append(0)
                        
                    if len(NA_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(NA_devn_list)/NA_ref_sd)**2))/(len(NA_devn_list)-1))                    
                    else:
                        devn_stats.append(0)
                        
                    if len(NEUTS_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(NEUTS_devn_list)/NEUTS_ref_sd)**2))/(len(NEUTS_devn_list)-1))
                    else:
                        devn_stats.append(0)
                        
                    if len(OSM_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(OSM_devn_list)/OSM_ref_sd)**2))/(len(OSM_devn_list)-1))
                    else:
                        devn_stats.append(0)
                    
                    if len(PHOS_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(PHOS_devn_list)/PHOS_ref_sd)**2))/(len(PHOS_devn_list)-1))
                    else:
                        devn_stats.append(0)
                    
                    if len(PLT_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(PLT_devn_list)/PLT_ref_sd)**2))/(len(PLT_devn_list)-1))
                    else:
                        devn_stats.append(0)
                    
                    if len(POT_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(POT_devn_list)/POT_ref_sd)**2))/(len(POT_devn_list)-1))
                    else:
                        devn_stats.append(0)
                        
                    if len(RDW_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(RDW_devn_list)/RDW_ref_sd)**2))/(len(RDW_devn_list)-1))
                    else:
                        devn_stats.append(0)
                    
                    if len(TP_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(TP_devn_list)/TP_ref_sd)**2))/(len(TP_devn_list)-1))
                    else:
                        devn_stats.append(0)
                        
                    if len(TROPI_devn_list) > 1:
                        devn_stats.append(np.sum(((np.asarray(TROPI_devn_list)/TROPI_ref_sd)**2))/(len(TROPI_devn_list)-1))
                    else:
                        devn_stats.append(0)
                        
                    if len(URATE_devn_list) > 1:
                        devn_stats.append(round(np.sum(((np.asarray(URATE_devn_list)/URATE_ref_sd)**2))/(len(URATE_devn_list)-1),2))
                    else:
                        devn_stats.append(0)
                        
                    if len(UREA_devn_list) > 1:
                        devn_stats.append(round(np.sum(((np.asarray(UREA_devn_list)/UREA_ref_sd)**2))/(len(UREA_devn_list)-1),2))
                    else:
                        devn_stats.append(0)
                    
                    if len(WBC_devn_list) > 1:
                        devn_stats.append(round(np.sum(((np.asarray(WBC_devn_list)/WBC_ref_sd)**2))/(len(WBC_devn_list)-1),2))
                    else:
                        devn_stats.append(0)
                    disch_devn_stats.append(get_discharge_devn(ALB_devn_list))
                    disch_devn_stats.append(get_discharge_devn(ALP_devn_list))
                    disch_devn_stats.append(get_discharge_devn(ALT_devn_list))
                    disch_devn_stats.append(get_discharge_devn(AMYLASE_devn_list))
                    disch_devn_stats.append(get_discharge_devn(AST_devn_list))
                    disch_devn_stats.append(get_discharge_devn(BASOCNT_devn_list))
                    disch_devn_stats.append(get_discharge_devn(BILI_devn_list))
                    disch_devn_stats.append(get_discharge_devn(BILICON_devn_list))
                    disch_devn_stats.append(get_discharge_devn(CA_devn_list))
                    disch_devn_stats.append(get_discharge_devn(CAI_devn_list))
                    disch_devn_stats.append(get_discharge_devn(CAUNCOR_devn_list))
                    disch_devn_stats.append(get_discharge_devn(CK_devn_list))
                    disch_devn_stats.append(get_discharge_devn(CL_devn_list))
                    disch_devn_stats.append(get_discharge_devn(CREAT_devn_list))
                    disch_devn_stats.append(get_discharge_devn(CRP_devn_list))
                    disch_devn_stats.append(get_discharge_devn(EOSINCNT_devn_list))
                    disch_devn_stats.append(get_discharge_devn(GGT_devn_list))
                    disch_devn_stats.append(get_discharge_devn(GLUC_devn_list))
                    disch_devn_stats.append(get_discharge_devn(HB_devn_list))
                    disch_devn_stats.append(get_discharge_devn(HCT_devn_list))
                    disch_devn_stats.append(get_discharge_devn(LACTATE_devn_list))
                    disch_devn_stats.append(get_discharge_devn(LYMPCNT_devn_list))
                    disch_devn_stats.append(get_discharge_devn(MCH_devn_list))
                    disch_devn_stats.append(get_discharge_devn(MCHC_devn_list))
                    disch_devn_stats.append(get_discharge_devn(MCV_devn_list))
                    disch_devn_stats.append(get_discharge_devn(MG_devn_list))
                    disch_devn_stats.append(get_discharge_devn(MONOCNT_devn_list))
                    disch_devn_stats.append(get_discharge_devn(NA_devn_list))
                    disch_devn_stats.append(get_discharge_devn(NEUTS_devn_list))
                    disch_devn_stats.append(get_discharge_devn(OSM_devn_list))
                    disch_devn_stats.append(get_discharge_devn(PHOS_devn_list))
                    disch_devn_stats.append(get_discharge_devn(PLT_devn_list))
                    disch_devn_stats.append(get_discharge_devn(POT_devn_list))
                    disch_devn_stats.append(get_discharge_devn(RDW_devn_list))
                    disch_devn_stats.append(get_discharge_devn(TP_devn_list))
                    disch_devn_stats.append(get_discharge_devn(TROPI_devn_list))
                    disch_devn_stats.append(get_discharge_devn(URATE_devn_list))
                    disch_devn_stats.append(get_discharge_devn(UREA_devn_list))
                    disch_devn_stats.append(get_discharge_devn(WBC_devn_list))

                    wt_devn_stats.append(get_sum_wtsq_devn(ALB_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(ALP_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(ALT_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(AMYLASE_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(AST_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(BASOCNT_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(BILI_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(BILICON_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(CA_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(CAI_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(CAUNCOR_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(CK_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(CL_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(CREAT_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(CRP_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(EOSINCNT_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(GGT_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(GLUC_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(HB_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(HCT_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(LACTATE_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(LYMPCNT_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(MCH_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(MCHC_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(MCV_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(MG_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(MONOCNT_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(NA_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(NEUTS_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(OSM_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(PHOS_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(PLT_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(POT_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(RDW_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(TP_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(TROPI_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(URATE_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(UREA_devn_list))
                    wt_devn_stats.append(get_sum_wtsq_devn(WBC_devn_list))                                                 
                    test_record2.append(sum(test_counters))
#                    test_record2 = test_record2 + test_counters + list(chain(*report_trend)) + devn_stats
                    test_record2 = test_record2 + test_counters +  prob_devn + devn_stats + disch_devn_stats +wt_devn_stats

                    test_record.append(sum(test_counters))

#                    test_record = test_record + test_counters + list(chain(*report_trend)) + devn_stats + test_record
                    test_record = test_record + test_counters + prob_devn + devn_stats +disch_devn_stats + wt_devn_stats
                    test_record.append((ALB_list))
                    test_record.append((ALP_list))
                    test_record.append((ALT_list))
                    test_record.append((AMYLASE_list))
                    test_record.append((AST_list))
                    test_record.append((BASOCNT_list))
                    test_record.append((BILI_list))
                    test_record.append((BILICON_list))
                    test_record.append((CA_list))
                    test_record.append((CAI_list))
                    test_record.append((CAUNCOR_list))
                    test_record.append((CK_list))
                    test_record.append((CK_list))
                    test_record.append((CREAT_list))
                    test_record.append((CRP_list))
                    test_record.append((EOSINCNT_list))
                    test_record.append((GGT_list))
                    test_record.append((GLUC_list))
                    test_record.append((HB_list))
                    test_record.append((HCT_list))
                    test_record.append((LACTATE_list))
                    test_record.append((LYMPCNT_list))
                    test_record.append((MCH_list))
                    test_record.append((MCHC_list))
                    test_record.append((MCV_list))
                    test_record.append((MG_list))
                    test_record.append((MONOCNT_list))
                    test_record.append((NA_list))
                    test_record.append((NEUTS_list))
                    test_record.append((OSM_list))
                    test_record.append((PHOS_list))
                    test_record.append((PLT_list))
                    test_record.append((POT_list))
                    test_record.append((RDW_list))
                    test_record.append((TP_list))
                    test_record.append((TROPI_list))
                    test_record.append((URATE_list))
                    test_record.append((UREA_list))
                    test_record.append((WBC_list))

                    wr_fnew.writerow(test_record)
                    wr_fmodc.writerow(test_record2)
                    record_count = record_count + 1 
                    if record_count%5 == 0 : 
#                        print('Id + demographic:', test_record2[0:9])                                         
#                        print('Test Report trend:', report_trend)
#                        print('Test Counters:',test_counters)
 #                       print('Deviation Stats:', devn_stats)
 #                       print('Test Time-series data:', merge_list)
                        print('record number written:', record_count)  
                        print('Admission id:', curr_admissionid)
                        print('Patient id:', curr_patientid) 
#                        print('Deviation Stats:' ,devn_stats)                                        
                ALB_list = []
                ALP_list = []
                ALT_list = []
                AMYLASE_list = []
                AST_list = []
                BASOCNT_list = []
                BILI_list = []
                BILICON_list = []
                CA_list = []
                CAI_list = []
                CAUNCOR_list = []
                CK_list = []
                CL_list = []
                CREAT_list = []
                CRP_list = []
                EOSINCNT_list = []
                GGT_list = []
                GLUC_list = []
                HB_list = []
                HCT_list = []
                LACTATE_list = []
                LYMPCNT_list = []
                MCH_list = []
                MCHC_list = []
                MCV_list = []
                MG_list = []
                MONOCNT_list = []
                NA_list = []               
                NEUTS_list = []
                OSM_list = []
                PHOS_list = []
                PLT_list = []
                POT_list = []
                RDW_list = []
                TP_list = []
                TROPI_list = []
                URATE_list = []
                UREA_list = []
                WBC_list = []
                report_trend = []
                                
                ALB_devn_list = [0]                                                
                ALP_devn_list = [0]
                ALT_devn_list = [0]
                AMYLASE_devn_list = [0]
                AST_devn_list = [0]
                BASOCNT_devn_list = [0]
                BILI_devn_list = [0]
                BILICON_devn_list = [0]
                CA_devn_list = [0]
                CAI_devn_list = [0]
                CAUNCOR_devn_list = [0]
                CK_devn_list = [0]
                CL_devn_list = [0]
                CREAT_devn_list = [0]
                CRP_devn_list = [0]
                EOSINCNT_devn_list = [0]
                GGT_devn_list = [0]
                GLUC_devn_list = [0]
                HB_devn_list = [0]
                HCT_devn_list = [0]
                LACTATE_devn_list = [0]
                LYMPCNT_devn_list = [0]
                MCH_devn_list = [0]
                MCHC_devn_list = [0]
                MCV_devn_list = [0]
                MG_devn_list = [0]
                MONOCNT_devn_list = [0]
                NA_devn_list = [0]
                NEUTS_devn_list = [0]
                OSM_devn_list = [0]
                PHOS_devn_list = [0]
                PLT_devn_list = [0]
                POT_devn_list = [0]
                RDW_devn_list = [0]
                TP_devn_list = [0]
                TROPI_devn_list = [0]
                URATE_devn_list = [0]
                UREA_devn_list = [0]
                WBC_devn_list = [0]
                devn_stats = []
                disch_devn_stats = []
                wt_devn_stats = []
                prob_devn = []
                merge_list=[]
                test_record2 = []
                test_record = []
                test_counters=[0 for i in range(len(test_labels))]
                
                ALB_test_val = []
                ALP_test_val = []
                ALT_test_val = []
                AMYLASE_test_val = []
                AST_test_val = []
                BASOCNT_test_val = []
                BILI_test_val = []
                BILICON_test_val = []
                CA_test_val = []
                CAI_test_val = []
                CAUNCOR_test_val = []
                CK_test_val = []
                CL_test_val = []
                CREAT_test_val = []
                CRP_test_val = []
                EOSINCNT_test_val = []
                GGT_test_val = []
                GLUC_test_val = []
                HB_test_val = []
                HCT_test_val = []
                LACTATE_test_val = []
                LYMPCNT_test_val = []
                MCH_test_val = []
                MCHC_test_val = []
                MCV_test_val = []
                MG_test_val = []
                MONOCNT_test_val = []
                NA_test_val = []
                NEUTS_test_val = []
                OSM_test_val = []
                PHOS_test_val = []
                PLT_test_val = []
                POT_test_val = []
                RDW_test_val = []
                TP_test_val = []
                TROPI_test_val = []
                URATE_test_val = []
                UREA_test_val = []
                WBC_test_val = []
                test_record = row[0:basic_cols_index] 
                test_record2 = row[0:basic_cols_index] 
                first_rec = 0   
                if (len(row) <= basic_cols_index):
                    continue
                else:
                    populate_test_columns(" ".join(row[basic_cols_index:basic_cols_index+1])," ".join(row[basic_cols_index+2:basic_cols_index+3]),
                    " ".join(row[basic_cols_index+3:basic_cols_index+4])," ".join(row[4:5])," ".join(row[3:4]))              
        else:
#                print('same patient record')
                test_record = row[0:basic_cols_index] 
                test_record2 = row[0:basic_cols_index]                 
                populate_test_columns(" ".join(row[basic_cols_index:basic_cols_index+1]),
                " ".join(row[basic_cols_index+2:basic_cols_index+3])," ".join(row[basic_cols_index+3:basic_cols_index+4])," ".join(row[4:5])," ".join(row[3:4]))  


ALB_list= (map_emission_states(ALB_list))
ALP_list= (map_emission_states(ALP_list))
ALT_list=(map_emission_states(ALT_list))
AMYLASE_list= (map_emission_states(AMYLASE_list))
AST_list= (map_emission_states(AST_list))
BASOCNT_list=  (map_emission_states(BASOCNT_list))
BILI_list=  (map_emission_states(BILI_list))
BILICON_list= (map_emission_states(BILICON_list))
CA_list= (map_emission_states(CA_list))
CAI_list=(map_emission_states(CAI_list))
CAUNCOR_list= (map_emission_states(CAUNCOR_list))
CK_list=  (map_emission_states(CK_list))
CK_list= (map_emission_states(CK_list))
CREAT_list=  (map_emission_states(CREAT_list))
CRP_list=  (map_emission_states(CRP_list))
EOSINCNT_list= (map_emission_states(EOSINCNT_list))
GGT_list= (map_emission_states(GGT_list))
GLUC_list=(map_emission_states(GLUC_list))
HB_list= (map_emission_states(HB_list))
HCT_list= (map_emission_states(HCT_list))
LACTATE_list= (map_emission_states(LACTATE_list))
LYMPCNT_list= (map_emission_states(LYMPCNT_list))
MCH_list= (map_emission_states(MCH_list))
MCHC_list= (map_emission_states(MCHC_list))
MCV_list=  (map_emission_states(MCV_list))
MG_list=  (map_emission_states(MG_list))
MONOCNT_list=  (map_emission_states(MONOCNT_list))
NA_list= (map_emission_states(NA_list))
NEUTS_list= (map_emission_states(NEUTS_list))
OSM_list=  (map_emission_states(OSM_list))
PHOS_list= (map_emission_states(PHOS_list))
PLT_list=  (map_emission_states(PLT_list))
POT_list= (map_emission_states(POT_list))
RDW_list=   (map_emission_states(RDW_list))
TP_list=  (map_emission_states(TP_list))
TROPI_list= (map_emission_states(TROPI_list))
URATE_list=   (map_emission_states(URATE_list))
UREA_list=  (map_emission_states(UREA_list))
WBC_list=  (map_emission_states(WBC_list))

prob_devn.append(sum(ALB_list)/(1+len(ALB_list)))
prob_devn.append(sum(ALP_list)/(1+len(ALP_list)))
prob_devn.append(sum(ALT_list)/(1+len(ALT_list)))
prob_devn.append(sum(AMYLASE_list)/(1+len(AMYLASE_list)))
prob_devn.append(sum(AST_list)/(1+len(AST_list)))
prob_devn.append(sum(BASOCNT_list)/(1+len(BASOCNT_list)))
prob_devn.append(sum(BILI_list)/(1+len(BILI_list)))
prob_devn.append(sum(BILICON_list)/(1+len(BILICON_list)))
prob_devn.append(sum(CA_list)/(1+len(CA_list)))
prob_devn.append(sum(CAI_list)/(1+len(CAI_list)))
prob_devn.append(sum(CAUNCOR_list)/(1+len(CAUNCOR_list)))
prob_devn.append(sum(CK_list)/(1+len(CK_list)))
prob_devn.append(sum(CL_list)/(1+len(CL_list)))
prob_devn.append(sum(CREAT_list)/(1+len(CREAT_list)))
prob_devn.append(sum(CRP_list)/(1+len(CRP_list)))
prob_devn.append(sum(EOSINCNT_list)/(1+len(EOSINCNT_list)))
prob_devn.append(sum(GGT_list)/(1+len(GGT_list)))
prob_devn.append(sum(GLUC_list)/(1+len(GLUC_list)))
prob_devn.append(sum(HB_list)/(1+len(HB_list)))
prob_devn.append(sum(HCT_list)/(1+len(HCT_list)))
prob_devn.append(sum(LACTATE_list)/(1+len(LACTATE_list)))
prob_devn.append(sum(LYMPCNT_list)/(1+len(LYMPCNT_list)))
prob_devn.append(sum(MCH_list)/(1+len(MCH_list)))
prob_devn.append(sum(MCHC_list)/(1+len(MCHC_list)))
prob_devn.append(sum(MCV_list)/(1+len(MCV_list)))
prob_devn.append(sum(MG_list)/(1+len(MG_list)))
prob_devn.append(sum(MONOCNT_list)/(1+len(MONOCNT_list)))
prob_devn.append(sum(NEUTS_list)/(1+len(NEUTS_list)))
prob_devn.append(sum(NA_list)/(1+len(NA_list)))
prob_devn.append(sum(OSM_list)/(1+len(OSM_list)))
prob_devn.append(sum(PHOS_list)/(1+len(PHOS_list)))
prob_devn.append(sum(PLT_list)/(1+len(PLT_list)))
prob_devn.append(sum(POT_list)/(1+len(POT_list)))
prob_devn.append(sum(RDW_list)/(1+len(RDW_list)))
prob_devn.append(sum(TP_list)/(1+len(TP_list)))
prob_devn.append(sum(TROPI_list)/(1+len(TROPI_list)))
prob_devn.append(sum(URATE_list)/(1+len(URATE_list)))
prob_devn.append(sum(UREA_list)/(1+len(UREA_list)))
prob_devn.append(sum(WBC_list)/(1+len(WBC_list)))

print("prob_devn:", prob_devn)

if len(ALB_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(ALB_devn_list)/ALB_ref_sd)**2))/(len(ALB_devn_list)-1))
else:
    devn_stats.append(0)

if len(ALP_devn_list) > 1:    
    devn_stats.append(np.sum(((np.asarray(ALP_devn_list)/ALP_ref_sd)**2))/(len(ALP_devn_list)-1))
else:
    devn_stats.append(0)
    
if len(ALT_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(ALT_devn_list)/ALT_ref_sd)**2))/(len(ALT_devn_list)-1))
else:
    devn_stats.append(0)
    
if len(AMYLASE_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(AMYLASE_devn_list)/AMYLASE_ref_sd)**2))/(len(AMYLASE_devn_list)-1))
else:
     devn_stats.append(0)
   
if len(AST_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(AST_devn_list)/AST_ref_sd)**2))/(len(AST_devn_list)-1))
else:
    devn_stats.append(0)

if len(BASOCNT_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(BASOCNT_devn_list)/BASOCNT_ref_sd)**2))/(len(BASOCNT_devn_list)-1))
else:
    devn_stats.append(0)

if len(BILI_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(BILI_devn_list)/BILI_ref_sd)**2))/(len(BILI_devn_list)-1))
else:
    devn_stats.append(0)
        
if len(BILICON_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(BILICON_devn_list)/BILICON_ref_sd)**2))/(len(BILICON_devn_list)-1))
else:
    devn_stats.append(0)
        
if len(CA_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(CA_devn_list)/CA_ref_sd)**2))/(len(CA_devn_list)-1))
else:
    devn_stats.append(0)
   
if len(CAI_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(CAI_devn_list)/CAI_ref_sd)**2))/(len(CAI_devn_list)-1))
else:
    devn_stats.append(0)
    
if len(CAUNCOR_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(CAUNCOR_devn_list)/CAUNCOR_ref_sd)**2))/(len(CAUNCOR_devn_list)-1))
else:
    devn_stats.append(0)
   
if len(CK_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(CK_devn_list)/CK_ref_sd)**2))/(len(CK_devn_list)-1))
else:
    devn_stats.append(0)
        
if len(CL_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(CL_devn_list)/CL_ref_sd)**2))/(len(CL_devn_list)-1))
else:
    devn_stats.append(0)
       
if len(CREAT_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(CREAT_devn_list)/CREAT_ref_sd)**2))/(len(CREAT_devn_list)-1))
else:
    devn_stats.append(0)
    
if len(CRP_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(CRP_devn_list)/CRP_ref_sd)**2))/(len(CRP_devn_list)-1))
else:
    devn_stats.append(0)
    
if len(EOSINCNT_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(EOSINCNT_devn_list)/EOSINCNT_ref_sd)**2))/(len(EOSINCNT_devn_list)-1))
else:
    devn_stats.append(0)
        
if len(GGT_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(GGT_devn_list)/GGT_ref_sd)**2))/(len(GGT_devn_list)-1))
else:
    devn_stats.append(0)
        
if len(GLUC_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(GLUC_devn_list)/GLUC_ref_sd)**2))/(len(GLUC_devn_list)-1))
else:
    devn_stats.append(0)
        
if len(HB_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(HB_devn_list)/HB_ref_sd)**2))/(len(HB_devn_list)-1))
else:
    devn_stats.append(0)
    
if len(HCT_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(HCT_devn_list)/HCT_ref_sd)**2))/(len(HCT_devn_list)-1))
else:
    devn_stats.append(0)
    
if len(LACTATE_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(LACTATE_devn_list)/LACTATE_ref_sd)**2))/(len(LACTATE_devn_list)-1))
else:
    devn_stats.append(0)
    
if len(LYMPCNT_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(LYMPCNT_devn_list)/LYMPCNT_ref_sd)**2))/(len(LYMPCNT_devn_list)-1))
else:
    devn_stats.append(0)
   
if len(MCH_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(MCH_devn_list)/MCH_ref_sd)**2))/(len(MCH_devn_list)-1))
else:
    devn_stats.append(0)
   
if len(MCHC_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(MCHC_devn_list)/MCHC_ref_sd)**2))/(len(MCHC_devn_list)-1))
else:
    devn_stats.append(0)
    
if len(MCV_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(MCV_devn_list)/MCV_ref_sd)**2))/(len(MCV_devn_list)-1))
else:
    devn_stats.append(0)
    
if len(MG_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(MG_devn_list)/MG_ref_sd)**2))/(len(MG_devn_list)-1))
else:
    devn_stats.append(0)
    
if len(MONOCNT_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(MONOCNT_devn_list)/MONOCNT_ref_sd)**2))/(len(MONOCNT_devn_list)-1))
else:
    devn_stats.append(0)
    
if len(NA_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(NA_devn_list)/NA_ref_sd)**2))/(len(NA_devn_list)-1))                    
else:
    devn_stats.append(0)
    
if len(NEUTS_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(NEUTS_devn_list)/NEUTS_ref_sd)**2))/(len(NEUTS_devn_list)-1))
else:
    devn_stats.append(0)
    
if len(OSM_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(OSM_devn_list)/OSM_ref_sd)**2))/(len(OSM_devn_list)-1))
else:
     devn_stats.append(0)
   
if len(PHOS_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(PHOS_devn_list)/PHOS_ref_sd)**2))/(len(PHOS_devn_list)-1))
else:
      devn_stats.append(0)
   
if len(PLT_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(PLT_devn_list)/PLT_ref_sd)**2))/(len(PLT_devn_list)-1))
else:
    devn_stats.append(0)
   
if len(POT_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(POT_devn_list)/POT_ref_sd)**2))/(len(POT_devn_list)-1))
else:
    devn_stats.append(0)
    
if len(RDW_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(RDW_devn_list)/RDW_ref_sd)**2))/(len(RDW_devn_list)-1))
else:
    devn_stats.append(0)
   
if len(TP_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(TP_devn_list)/TP_ref_sd)**2))/(len(TP_devn_list)-1))
else:
    devn_stats.append(0)
    
if len(TROPI_devn_list) > 1:
    devn_stats.append(np.sum(((np.asarray(TROPI_devn_list)/TROPI_ref_sd)**2))/(len(TROPI_devn_list)-1))
else:
    devn_stats.append(0)
    
if len(URATE_devn_list) > 1:
    devn_stats.append(round(np.sum(((np.asarray(URATE_devn_list)/URATE_ref_sd)**2))/(len(URATE_devn_list)-1),2))
else:
    devn_stats.append(0)
    
if len(UREA_devn_list) > 1:
    devn_stats.append(round(np.sum(((np.asarray(UREA_devn_list)/UREA_ref_sd)**2))/(len(UREA_devn_list)-1),2))
else:
     devn_stats.append(0)
   
if len(WBC_devn_list) > 1:
    devn_stats.append(round(np.sum(((np.asarray(WBC_devn_list)/WBC_ref_sd)**2))/(len(WBC_devn_list)-1),2))
else:
     devn_stats.append(0)
    


disch_devn_stats.append(get_discharge_devn(ALB_devn_list))
disch_devn_stats.append(get_discharge_devn(ALP_devn_list))
disch_devn_stats.append(get_discharge_devn(ALT_devn_list))
disch_devn_stats.append(get_discharge_devn(AMYLASE_devn_list))
disch_devn_stats.append(get_discharge_devn(AST_devn_list))
disch_devn_stats.append(get_discharge_devn(BASOCNT_devn_list))
disch_devn_stats.append(get_discharge_devn(BILI_devn_list))
disch_devn_stats.append(get_discharge_devn(BILICON_devn_list))
disch_devn_stats.append(get_discharge_devn(CA_devn_list))
disch_devn_stats.append(get_discharge_devn(CAI_devn_list))
disch_devn_stats.append(get_discharge_devn(CAUNCOR_devn_list))
disch_devn_stats.append(get_discharge_devn(CK_devn_list))
disch_devn_stats.append(get_discharge_devn(CL_devn_list))
disch_devn_stats.append(get_discharge_devn(CREAT_devn_list))
disch_devn_stats.append(get_discharge_devn(CRP_devn_list))
disch_devn_stats.append(get_discharge_devn(EOSINCNT_devn_list))
disch_devn_stats.append(get_discharge_devn(GGT_devn_list))
disch_devn_stats.append(get_discharge_devn(GLUC_devn_list))
disch_devn_stats.append(get_discharge_devn(HB_devn_list))
disch_devn_stats.append(get_discharge_devn(HCT_devn_list))
disch_devn_stats.append(get_discharge_devn(LACTATE_devn_list))
disch_devn_stats.append(get_discharge_devn(LYMPCNT_devn_list))
disch_devn_stats.append(get_discharge_devn(MCH_devn_list))
disch_devn_stats.append(get_discharge_devn(MCHC_devn_list))
disch_devn_stats.append(get_discharge_devn(MCV_devn_list))
disch_devn_stats.append(get_discharge_devn(MG_devn_list))
disch_devn_stats.append(get_discharge_devn(MONOCNT_devn_list))
disch_devn_stats.append(get_discharge_devn(NA_devn_list))
disch_devn_stats.append(get_discharge_devn(NEUTS_devn_list))
disch_devn_stats.append(get_discharge_devn(OSM_devn_list))
disch_devn_stats.append(get_discharge_devn(PHOS_devn_list))
disch_devn_stats.append(get_discharge_devn(PLT_devn_list))
disch_devn_stats.append(get_discharge_devn(POT_devn_list))
disch_devn_stats.append(get_discharge_devn(RDW_devn_list))
disch_devn_stats.append(get_discharge_devn(TP_devn_list))
disch_devn_stats.append(get_discharge_devn(TROPI_devn_list))
disch_devn_stats.append(get_discharge_devn(URATE_devn_list))
disch_devn_stats.append(get_discharge_devn(UREA_devn_list))
disch_devn_stats.append(get_discharge_devn(WBC_devn_list))

wt_devn_stats.append(get_sum_wtsq_devn(ALB_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(ALP_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(ALT_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(AMYLASE_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(AST_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(BASOCNT_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(BILI_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(BILICON_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(CA_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(CAI_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(CAUNCOR_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(CK_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(CL_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(CREAT_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(CRP_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(EOSINCNT_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(GGT_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(GLUC_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(HB_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(HCT_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(LACTATE_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(LYMPCNT_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(MCH_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(MCHC_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(MCV_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(MG_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(MONOCNT_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(NA_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(NEUTS_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(OSM_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(PHOS_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(PLT_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(POT_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(RDW_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(TP_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(TROPI_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(URATE_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(UREA_devn_list))
wt_devn_stats.append(get_sum_wtsq_devn(WBC_devn_list))  

test_record2.append(sum(test_counters))
#test_record2 = test_record2 + test_counters + list(chain(*report_trend)) + devn_stats
test_record2 = test_record2 + test_counters + prob_devn + devn_stats + disch_devn_stats + wt_devn_stats


test_record.append(sum(test_counters))
#test_record = test_record + test_counters + list(chain(*report_trend)) + devn_stats + merge_list
test_record = test_record + test_counters +  prob_devn + devn_stats  + disch_devn_stats+ wt_devn_stats
test_record.append((ALB_list))
test_record.append((ALP_list))
test_record.append((ALT_list))
test_record.append((AMYLASE_list))
test_record.append((AST_list))
test_record.append((BASOCNT_list))
test_record.append((BILI_list))
test_record.append((BILICON_list))
test_record.append((CA_list))
test_record.append((CAI_list))
test_record.append((CAUNCOR_list))
test_record.append((CK_list))
test_record.append((CK_list))
test_record.append((CREAT_list))
test_record.append((CRP_list))
test_record.append((EOSINCNT_list))
test_record.append((GGT_list))
test_record.append((GLUC_list))
test_record.append((HB_list))
test_record.append((HCT_list))
test_record.append((LACTATE_list))
test_record.append((LYMPCNT_list))
test_record.append((MCH_list))
test_record.append((MCHC_list))
test_record.append((MCV_list))
test_record.append((MG_list))
test_record.append((MONOCNT_list))
test_record.append((NA_list))
test_record.append((NEUTS_list))
test_record.append((OSM_list))
test_record.append((PHOS_list))
test_record.append((PLT_list))
test_record.append((POT_list))
test_record.append((RDW_list))
test_record.append((TP_list))
test_record.append((TROPI_list))
test_record.append((URATE_list))
test_record.append((UREA_list))
test_record.append((WBC_list))
#test_record.append(merge_list)

#print('Record written:', test_record2)
#print('Id + demographic:', test_record2[0:basic_cols_index])                                         
#print('Test Report trend:', report_trend)
#print('Test Counters:',test_counters)
#print('Deviation Stats:', devn_stats)
#print('Test Time-series data:', merge_list)
wr_fnew.writerow(test_record)
wr_fmodc.writerow(test_record2)
record_count = record_count + 1
print('record number written:', record_count)                   

print("Total records written",record_count)

#fnew.close()
#fl.close()

