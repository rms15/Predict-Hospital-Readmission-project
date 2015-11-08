##########################
rm(list=ls())
library(mtcars)
library(ggplot2)
library(plyr)
library(rpart)
library(randomForest)
library(TSclust)
library(MASS)
require("e1071") # for SVM
library("e1071")
library(neuralnet)

setwd("/Users/riazm_shaik/Rice/COMP540-StatisticalMachineLearning/project")

###################################################
# Read training data set
###################################################
# load file with only lab counts data
train_full <-read.csv(file="train_mod.csv")
train_lab<-read.csv(file="labrecs_train.csv")


t(head(train_full))
#train_modc<-read.csv(file="train_mod_counts.csv")
train_modc<-read.csv(file="train_mod_counts.csv")
#train_fullfile<-read.csv(file="train_mod.csv",header=FALSE)
train_modc$duration<-as.Date(train_modc$discharge_date) -as.Date(train_modc$start_date)
#train_modc$discharge_date <-as.character(train_modc$discharge_date)
#train_modc$start_date <-as.character(train_modc$start_date)
head(train_modc$duration)
tail(train_modc)
# drop id and date columns
drops<-c("patientid","start_date","discharge_date",
# if required drop these columnsas there is < 0.0x data present
#         "AST_counter","BILICON_counter","URATE_counter"
#         "AST_trend","BILICON_trend","URATE_trend"
#         "AST_qty_inc","BILICON_qty_inc","URATE_qty_inc"
#         "AST_qty_dec","BILICON_qty_dec","URATE_qty_dec"
#         "AST_devn_stats","BILICON_devn_stats","URATE_counter"
# lab codes for which reference range is not yet coded        
         "AST_trend","BASOCNT_trend", "BILI_trend", "BILICON_trend",
         "CA_trend", "CAUNCOR_trend", "CRP_trend", "EOSINCNT_trend",
         "GGT_trend", "HCT_trend", "LYMPCNT_trend", "MONOCNT_trend", 
         "PLT_trend", "TP_trend", "URATE_trend","POT_trend",
         "AST_qty_inc","BASOCNT_qty_inc", "BILI_qty_inc", "BILICON_qty_inc",
         "CA_qty_inc", "CAUNCOR_qty_inc", "CRP_qty_inc", "EOSINCNT_qty_inc",
         "GGT_qty_inc", "HCT_qty_inc", "LYMPCNT_qty_inc", "MONOCNT_qty_inc", 
         "PLT_qty_inc", "TP_qty_inc", "URATE_qty_inc","POT_qty_inc",
         "AST_qty_dec","BASOCNT_qty_dec", "BILI_qty_dec", "BILICON_qty_dec",
         "CA_qty_dec", "CAUNCOR_qty_dec", "CRP_qty_dec", "EOSINCNT_qty_dec",
         "GGT_qty_dec", "HCT_qty_dec", "LYMPCNT_qty_dec", "MONOCNT_qty_dec", 
         "PLT_qty_dec", "TP_qty_dec", "URATE_qty_dec","POT_qty_dec",
"AST_mean_value","BASOCNT_mean_value", "BILI_mean_value", "BILICON_mean_value",
"CA_mean_value", "CAUNCOR_mean_value", "CRP_mean_value", "EOSINCNT_mean_value",
"GGT_mean_value", "HCT_mean_value", "LYMPCNT_mean_value", "MONOCNT_mean_value", 
"PLT_mean_value", "TP_mean_value", "URATE_mean_value",
"AST_median_value","BASOCNT_median_value", "BILI_median_value", "BILICON_median_value",
"CA_median_value", "CAUNCOR_median_value", "CRP_median_value", "EOSINCNT_median_value",
"GGT_median_value", "HCT_median_value", "LYMPCNT_median_value", "MONOCNT_median_value", 
"PLT_median_value", "TP_median_value", "URATE_median_value","POT_median_value",
 ### variables with no data        
         "CL_trend","CREAT_trend","GLUC_trend","HB_trend","LACTATE_trend","MCH_trend",
         "MCHC_trend","MCV_trend","MG_trend","RDW_trend",
        "CAI_qty_inc","CK_qty_inc",
         "CL_qty_inc","LACTATE_qty_inc","MG_qty_inc","NEUTS_qty_inc","ALT_qty_dec",
         "AMYLASE_qty_dec","GLUC_qty_dec","HB_qty_dec","MCHC_qty_dec","MCV_qty_dec",
         "MG_qty_dec","PHOS_qty_dec",
### to address rank deficiency error during prediction - removing remaining trend variables
"ALB_trend" , "ALP_trend" , "ALT_trend" ,"AMYLASE_trend" ,"CAI_trend","CK_trend",
"NEUTS_trend"   , "OSM_trend" , "PHOS_trend", "TROPI_trend"  ,"UREA_trend","WBC_trend" ,
### remove individual counters, just keep total test count
"ALB_counter" ,"ALP_counter"  ,         "ALT_counter",   "AMYLASE_counter"  ,     "AST_counter" ,         
 "BASOCNT_counter"  ,     "BILI_counter"  , "BILICON_counter"   ,    "CA_counter"   ,        
 "CAI_counter"     ,      "CAUNCOR_counter"     ,"CK_counter"      ,      "CL_counter"  ,         
 "CREAT_counter"    ,     "CRP_counter"       , "EOSINCNT_counter"  ,    "GGT_counter"   ,       
 "GLUC_counter"    ,      "HB_counter"        , "HCT_counter"     ,      "LACTATE_counter",      
 "LYMPCNT_counter"  ,     "MCH_counter"         ,"MCHC_counter"    ,      "MCV_counter"    ,      
 "MG_counter"     ,       "MONOCNT_counter"     ,"NEUTS_counter"   ,      "OSM_counter"     ,     
 "PHOS_counter"    ,      "PLT_counter"         ,"POT_counter"     ,      "RDW_counter"     ,     
 "TP_counter"     ,       "TROPI_counter"       ,"URATE_counter"  ,       "UREA_counter"    ,     
 "WBC_counter"    
)     
     
"AST_devn_stats","BASOCNT_devn_stats", "BILI_devn_stats", "BILICON_devn_stats",
"CA_devn_stats", "CAUNCOR_devn_stats", "CRP_devn_stats", "EOSINCNT_devn_stats",
"GGT_devn_stats", "HCT_devn_stats", "LYMPCNT_devn_stats", "MONOCNT_devn_stats", 
"PLT_devn_stats", "TP_devn_stats", "URATE_devn_stats","POT_devn_stats",


# remove last row which has NA's
train_modc$total_trend = train_modc$ALB_trend + train_modc$ALP_trend + train_modc$ALT_trend + 
  train_modc$AMYLASE_trend + train_modc$CAI_trend +           
  train_modc$CK_trend + train_modc$NEUTS_trend + train_modc$OSM_trend + 
  train_modc$PHOS_trend+
  train_modc$TROPI_trend + train_modc$UREA_trend + train_modc$WBC_trend      


train_modc$total_devn_stats = train_modc$ALB_devn_stats   +    train_modc$ALP_devn_stats  +    
  train_modc$ALT_devn_stats    +   train_modc$AMYLASE_devn_stats + 
  train_modc$AST_devn_stats   +    train_modc$BASOCNT_devn_stats  +
  train_modc$BILI_devn_stats   +   train_modc$BILICON_devn_stats  +
  train_modc$CA_devn_stats     +   train_modc$CAI_devn_stats      +
  train_modc$CAUNCOR_devn_stats +  train_modc$CK_devn_stats       +
  train_modc$CL_devn_stats     +   train_modc$CREAT_devn_stats   + 
  train_modc$CRP_devn_stats    +   train_modc$EOSINCNT_devn_stats +
  train_modc$GGT_devn_stats    +   train_modc$GLUC_devn_stats     +
  train_modc$HB_devn_stats     +   train_modc$HCT_devn_stats      +
  train_modc$LACTATE_devn_stats +  train_modc$LYMPCNT_devn_stats  +
  train_modc$MCH_devn_stats     +  train_modc$MCHC_devn_stats     +
  train_modc$MCV_devn_stats    +   train_modc$MG_devn_stats       +
  train_modc$MONOCNT_devn_stats +  train_modc$NEUTS_devn_stats   + 
  train_modc$OSM_devn_stats    +   train_modc$PHOS_devn_stats    + 
  train_modc$PLT_devn_stats   +    train_modc$POT_devn_stats    +  
  train_modc$RDW_devn_stats    +   train_modc$TP_devn_stats      + 
  train_modc$TROPI_devn_stats +    train_modc$URATE_devn_stats  +  
  train_modc$UREA_devn_stats  +    train_modc$WBC_devn_stats       


train_modc2<- train_modc[1:14873,!(names(train_modc) %in% drops)]
# Replace age 0 with 1
train_modc2[which(train_modc2$age==0),]$age = 1
train_modc2$seq_no = (1:nrow(train_modc2))

############################################################
# Center and Scale training dataset: 
# Columns in dataset replaced in place###########
# Problems with doing centering and scaling -- some columns have zero values
############################################################
train_modc2$age<-as.numeric(as.character(train_modc2$age))
head(train_modc2)$admission
train_modc2$gender<-as.numeric(train_modc2$gender)
train_modc2$admission_type<-as.numeric(train_modc2$admission_type)
train_modc2$outcome<-as.numeric(train_modc2$outcome)
train_modc2$duration<-as.numeric(train_modc2$duration)
which((colMeans(train_modc2))==0)
colnames(which((apply(train_modc2,2,sd)) == 0))

train_modc2.scaled<-scale(train_modc2[2:109],center=TRUE,scale=TRUE)
dim(train_modc2.scaled)
train_modc2.df<-as.data.frame(train_modc2.scaled + jitter(0))
train_modc2.df$label<-train_modc2$label
#train_modc2.jitter<-train_modc2+jitter(0)
#train_modc.wtage<-cbind(train_modc2,age.counters)



############################################################
## ********** Build clustering models **********
###################################################
train_lab_samp[which(train_lab_samp$test == 'HB' & train_lab_samp$label == '1'),]
clusters<- kmeans(train_modc2, centers = 6, iter.max = 500)
train_lab_samp1<-(train_lab_samp[which(train_lab_samp$test == 'HB' & train_lab_samp$label == '1'),])
clusters<- hclust(train_lab_samp1)


############################################################
## ********** Build classification models **********
###################################################
# --- logistic regression on unscaled dataset
logist.mod1<-glm(label ~ . , 
                 data=train_modc2 ,family=binomial)

stepAIC(logist.mod1)
, direction = "forward",trace=1)

logist.mod1<-glm(label ~ age+gender+admission_type+outcome+no_prior_readm+total_no_of_tests +
                   total_trend + total_devn_stats
                 + ALB_devn_stats +  ALP_devn_stats  +  ALT_devn_stats       
                + AMYLASE_devn_stats +   CAI_devn_stats       
                + CK_devn_stats    +     CL_devn_stats        
                + CREAT_devn_stats  +    GLUC_devn_stats      
                + HB_devn_stats    +     LACTATE_devn_stats   
                + MCH_devn_stats  +      MCHC_devn_stats      
                + MCV_devn_stats   +     MG_devn_stats        
                + NEUTS_devn_stats +     OSM_devn_stats       
                + PHOS_devn_stats  +     RDW_devn_stats       
                + TROPI_devn_stats  +    UREA_devn_stats      
                + WBC_devn_stats     +   ALB_median_value     
                +  ALP_median_value   +   ALT_median_value     
                + AMYLASE_median_value + AST_median_value     
                + BASOCNT_median_value + BILI_median_value    
                +  BILICON_median_value + CA_median_value      
                +  CAI_median_value   +   CAUNCOR_median_value 
                +  CK_median_value     +  CL_median_value      
                +  CREAT_median_value  +  CRP_median_value     
                +  EOSINCNT_median_value +GGT_median_value     
                +  GLUC_median_value   +  HB_median_value      
                +  HCT_median_value   +   LACTATE_median_value 
                +   LYMPCNT_median_value + MCH_median_value     
                +   MCHC_median_value  +   MCV_median_value     
                +   MG_median_value   +    MONOCNT_median_value 
                +   NEUTS_median_value  +  OSM_median_value     
                +  PHOS_median_value  +   PLT_median_value     
                +  POT_median_value  +    RDW_median_value     
                +  TP_median_value    +   TROPI_median_value   
                +  URATE_median_value  +  UREA_median_value    
                +  WBC_median_value  +    duration        , 
                 data=train_modc2 ,family=binomial)


plot(HB_mean_value~admissionid, data=train_modc, col=label)
ggplot(train_modc) + aes(ALB_devn_stats,col=factor(label)) + geom_density()

ggplot(train_modc) + geom_line(aes(y=ALB_devn_stats,x=admissionid) )

ggplot(train_lab_samp[which(train_lab_samp$test == 'HB' & train_lab_samp$label == '1'),]) +
  aes(x=count,y=result,group=admissionid,colour=factor(label)) + geom_line()

ggplot(train_lab_samp[which(train_lab_samp$test == 'POT'),]) +
  aes(x=count,y=result,group=admissionid,colour=factor(label)) + geom_line() + facet_wrap(~label)

ggplot(train_lab_samp[which(train_lab_samp$test == 'MCHC'),]) +
  aes(x=count,y=result,group=admissionid,colour=factor(label)) + geom_line()+ facet_wrap(~label)

ggplot(train_lab_samp[which(train_lab_samp$test == 'WBC'),]) +
  aes(x=count,y=result,group=admissionid,colour=factor(label)) + geom_line()+ facet_wrap(~label)

ggplot(train_lab_samp[which(train_lab_samp$test == 'MCH'),]) +
  aes(x=count,y=result,group=admissionid,colour=factor(label)) + geom_line()+ facet_wrap(~label)

ggplot(train_lab_samp[which(train_lab_samp$test == 'HCT'),]) +
  aes(x=count,y=result,group=admissionid,colour=factor(label)) + geom_line()+ facet_wrap(~label)


ggplot(train_lab_samp[which(train_lab_samp$test == 'MCV'),]) +
  aes(x=count,y=result,group=admissionid,colour=factor(label)) + geom_line()+ facet_wrap(~label)

ggplot(train_lab_samp[which(train_lab_samp$test == 'RDW'),]) +
  aes(x=count,y=result,group=admissionid,colour=factor(label)) + geom_line()+ facet_wrap(~label)

ggplot(train_lab_samp[which(train_lab_samp$test == 'PLT'),]) +
  aes(x=count,y=result,group=admissionid,colour=factor(label)) + geom_line()+ facet_wrap(~label)

ggplot(train_lab_samp[which(train_lab_samp$test == 'EOSINCNT'),]) +
  aes(x=count,y=result,group=admissionid,colour=factor(label)) + geom_line()+ facet_wrap(~label)

ggplot(train_lab_samp[which(train_lab_samp$test == 'MONOCNT'),]) +
  aes(x=count,y=result,group=admissionid,colour=factor(label)) + geom_line()+ facet_wrap(~label)

ggplot(train_lab_samp[which(train_lab_samp$test == 'BASOCNT'),]) +
  aes(x=count,y=result,group=admissionid,colour=factor(label)) + geom_line()+ facet_wrap(~label)
###useful

ggplot(train_lab_samp[which(train_lab_samp$test == 'LYMPCNT'),]) +
  aes(x=count,y=result,group=admissionid,colour=factor(label)) + geom_line()+ facet_wrap(~label)

ggplot(train_lab_samp[which(train_lab_samp$test == 'NEUTS'),]) +
  aes(x=count,y=result,group=admissionid,colour=factor(label)) + geom_line()+ facet_wrap(~label)

ggplot(train_lab_samp[which(train_lab_samp$test == 'MONOCNT'),]) +
  aes(x=count,y=result,group=admissionid,colour=factor(label)) + geom_line()+ facet_wrap(~label)

ggplot(train_lab_samp[which(train_lab_samp$test == 'CREAT'),]) +
  aes(x=count,y=result,group=admissionid,colour=factor(label)) + geom_line()+ facet_wrap(~label)
**useful
ggplot(train_lab_samp[which(train_lab_samp$test == 'UREA'),]) +
  aes(x=count,y=result,group=admissionid,colour=factor(label)) + geom_line()+ facet_wrap(~label)

ggplot(train_lab_samp[which(train_lab_samp$test == 'CRP'),]) +
  aes(x=count,y=result,group=admissionid,colour=factor(label)) + geom_line()+ facet_wrap(~label)

ggplot(train_lab_samp[which(train_lab_samp$test == 'BILI'),]) +
  aes(x=count,y=result,group=admissionid,colour=factor(label)) + geom_line()+ facet_wrap(~label)

ggplot(train_lab_samp[which(train_lab_samp$test == 'ALB'),]) +
  aes(x=count,y=result,group=admissionid,colour=factor(label)) + geom_line()+ facet_wrap(~label)

ggplot(train_lab_samp[which(train_lab_samp$test == 'ALP'),]) +
  aes(x=count,y=result,group=admissionid,colour=factor(label)) + geom_line()+ facet_wrap(~label)

#train_lab_samp = train_lab[1:5000,]
train_lab_samp = train_lab
clust.mod1<-clust(train_lab_samp, k = 6)

# --- logistic regression on scaled dataset
logist.mod1<-glm(label ~ . + age*. , data=train_modc2.df ,family=binomial)


# --- logistic regression with basic parameters
logist.mod2<-glm(label ~ age + gender + admission_type+outcome+no_prior_readm+
                   duration+total_no_of_tests + total_trend + age*no_prior_readm + age*duration +
                   age*total_no_of_tests + age*outcome + age*admission_type+ age:age+
                 total_devn_stats + 
                ALB_devn_stats   +     ALP_devn_stats    +    ALT_devn_stats   +    
                AMYLASE_devn_stats +   CAI_devn_stats   + CK_devn_stats     +    CL_devn_stats        +
                CREAT_devn_stats  +    GLUC_devn_stats + HB_devn_stats        +
                 LACTATE_devn_stats   + MCH_devn_stats  +       MCHC_devn_stats     +  MCV_devn_stats   +
                MG_devn_stats     + NEUTS_devn_stats    +  OSM_devn_stats       +
               PHOS_devn_stats        +    POT_devn_stats      +  RDW_devn_stats  +   TP_devn_stats  +
             TROPI_devn_stats     + URATE_devn_stats    +  UREA_devn_stats      +  WBC_devn_stats 
             +age*total_devn_stats + age*ALB_devn_stats + age*ALP_devn_stats + age*HB_devn_stats+
               age*MCHC_devn_stats + total_devn_stats*total_no_of_tests + total_devn_stats*duration  
             
             
,data=train_modc2, family=binomial)

summary(logist.mod2)
logist.srch1<-stepAIC(logist.mod2)
summary(logist.srch1)

m <- model.matrix(~label+age+gender+admission_type+outcome+no_prior_readm+total_no_of_tests +
                    total_trend + duration,data=train_modc2)

nn.mod1<-neuralnet(label~age       +                   genderM       +               
                     admission_typeOther       +    
                     admission_typePlanned     +    outcomeDied     +             
                     outcomeHome             +      outcomeOther      +           
                         no_prior_readm       +        
                     total_no_of_tests        +     total_trend +                 
                     duration   , data=m[,2:15],hidden=1,
          err.fct="ce", linear.output=FALSE, likelihood=TRUE,algorithm='backprop',
          learningrate=0.5)

predict.nn.mod1<-prediction(train_modc2,nn.mod1,list.glm=NULL)
                  
# ---  decision tree CART on unscaled dataset
cart.mod1<-rpart(label ~ ., data=train_modc2, method="class")

summary(cart.mod1)
print(cart.mod1)
plot(cart.mod1)

# ---  decision tree CART on unscaled dataset
cart.mod1<-rpart(label ~ age+gender+admission_type+outcome+
                   no_prior_readm+total_no_of_tests +
                   total_trend + total_devn_stats +
                 ALB_devn_stats   +    ALP_devn_stats  +    
                   ALT_devn_stats    +   AMYLASE_devn_stats + 
                   AST_devn_stats   +    BASOCNT_devn_stats  +
                   BILI_devn_stats   +   BILICON_devn_stats  +
                   CA_devn_stats     +   CAI_devn_stats      +
                   CAUNCOR_devn_stats +  CK_devn_stats       +
                   CL_devn_stats     +   CREAT_devn_stats   + 
                   CRP_devn_stats    +   EOSINCNT_devn_stats +
                   GGT_devn_stats    +   GLUC_devn_stats     +
                   HB_devn_stats     +   HCT_devn_stats      +
                   LACTATE_devn_stats +  LYMPCNT_devn_stats  +
                   MCH_devn_stats     +  MCHC_devn_stats     +
                   MCV_devn_stats    +   MG_devn_stats       +
                   MONOCNT_devn_stats +  NEUTS_devn_stats   + 
                   OSM_devn_stats    +   PHOS_devn_stats    + 
                   PLT_devn_stats   +    POT_devn_stats    +  
                   RDW_devn_stats    +   TP_devn_stats      + 
                   TROPI_devn_stats +    URATE_devn_stats  +  
                   UREA_devn_stats  +    WBC_devn_stats , data=train_modc2, method="class")

summary(cart.mod1)
print(cart.mod1)
plot(cart.mod1)

cart.mod1<-rpart(label ~ age+gender+admission_type+outcome+
                   no_prior_readm+total_no_of_tests +
                   total_trend + total_devn_stats 
                 , data=train_modc2, method="class")


                   
# ---  decision tree CART on scaled dataset
cart.mod1<-rpart(label ~ .  , data=train_modc2.df, method="class")

summary(cart.mod1)
print(cart.mod1)
plot(cart.mod1)
plotcp(cart.mod1)
post(cart.mod1, file = "cart_mod1.ps", title = " ")

set.seed(17)
# ---  random forest on unscaled dataset
rf.mod1<-randomForest(label ~ . + age*, data=train_modc2, method="class")
#label.f <- factor(train_modc2$label)

train_modc2_zerot<-train_modc2[which(train_modc2$total_no_of_tests==0),]
train_modc2_nzt.agegrp1<-train_modc2[which(train_modc2$total_no_of_tests!=0 &
                                           train_modc2$age <20),]
train_modc2_nzt.agegrp2<-train_modc2[which(train_modc2$total_no_of_tests!=0 &
                                           train_modc2$age >=20 & train_modc2$age <60),]

train_modc2_nzt.agegrp3<-train_modc2[which(train_modc2$total_no_of_tests!=0 &
                                           train_modc2$age >= 60),]




rf.zerot<-randomForest(label ~ age+gender+admission_type+outcome+
                   no_prior_readm, 
                   data=train_modc2_zerot)

rf.nzt.agegrp1<-randomForest(label ~ age+gender+admission_type+outcome+
                         no_prior_readm+total_no_of_tests +
                         total_trend + total_devn_stats +
                         ALB_devn_stats   +    ALP_devn_stats  +    
                         ALT_devn_stats    +   AMYLASE_devn_stats + 
                         AST_devn_stats   +    BASOCNT_devn_stats  +
                         BILI_devn_stats   +   BILICON_devn_stats  +
                         CA_devn_stats     +   CAI_devn_stats      +
                         CAUNCOR_devn_stats +  CK_devn_stats       +
                         CL_devn_stats     +   CREAT_devn_stats   + 
                         CRP_devn_stats    +   EOSINCNT_devn_stats +
                         GGT_devn_stats    +   GLUC_devn_stats     +
                         HB_devn_stats     +   HCT_devn_stats      +
                         LACTATE_devn_stats +  LYMPCNT_devn_stats  +
                         MCH_devn_stats     +  MCHC_devn_stats     +
                         MCV_devn_stats    +   MG_devn_stats       +
                         MONOCNT_devn_stats +  NEUTS_devn_stats   + 
                         OSM_devn_stats    +   PHOS_devn_stats    + 
                         PLT_devn_stats   +    POT_devn_stats    +  
                         RDW_devn_stats    +   TP_devn_stats      + 
                         TROPI_devn_stats +    URATE_devn_stats  +  
                         UREA_devn_stats  +    WBC_devn_stats, 
                       data=train_modc2_nzt.agegrp1)

rf.nzt.agegrp2<-randomForest(label ~ age+gender+admission_type+outcome+
                               no_prior_readm+total_no_of_tests +
                               total_trend + total_devn_stats +
                               ALB_devn_stats   +    ALP_devn_stats  +    
                               ALT_devn_stats    +   AMYLASE_devn_stats + 
                               AST_devn_stats   +    BASOCNT_devn_stats  +
                               BILI_devn_stats   +   BILICON_devn_stats  +
                               CA_devn_stats     +   CAI_devn_stats      +
                               CAUNCOR_devn_stats +  CK_devn_stats       +
                               CL_devn_stats     +   CREAT_devn_stats   + 
                               CRP_devn_stats    +   EOSINCNT_devn_stats +
                               GGT_devn_stats    +   GLUC_devn_stats     +
                               HB_devn_stats     +   HCT_devn_stats      +
                               LACTATE_devn_stats +  LYMPCNT_devn_stats  +
                               MCH_devn_stats     +  MCHC_devn_stats     +
                               MCV_devn_stats    +   MG_devn_stats       +
                               MONOCNT_devn_stats +  NEUTS_devn_stats   + 
                               OSM_devn_stats    +   PHOS_devn_stats    + 
                               PLT_devn_stats   +    POT_devn_stats    +  
                               RDW_devn_stats    +   TP_devn_stats      + 
                               TROPI_devn_stats +    URATE_devn_stats  +  
                               UREA_devn_stats  +    WBC_devn_stats, 
                             data=train_modc2_nzt.agegrp2)

rf.nzt.agegrp3<-randomForest(label ~ age+gender+admission_type+outcome+
                               no_prior_readm+total_no_of_tests +
                               total_trend + total_devn_stats +
                               ALB_devn_stats   +    ALP_devn_stats  +    
                               ALT_devn_stats    +   AMYLASE_devn_stats + 
                               AST_devn_stats   +    BASOCNT_devn_stats  +
                               BILI_devn_stats   +   BILICON_devn_stats  +
                               CA_devn_stats     +   CAI_devn_stats      +
                               CAUNCOR_devn_stats +  CK_devn_stats       +
                               CL_devn_stats     +   CREAT_devn_stats   + 
                               CRP_devn_stats    +   EOSINCNT_devn_stats +
                               GGT_devn_stats    +   GLUC_devn_stats     +
                               HB_devn_stats     +   HCT_devn_stats      +
                               LACTATE_devn_stats +  LYMPCNT_devn_stats  +
                               MCH_devn_stats     +  MCHC_devn_stats     +
                               MCV_devn_stats    +   MG_devn_stats       +
                               MONOCNT_devn_stats +  NEUTS_devn_stats   + 
                               OSM_devn_stats    +   PHOS_devn_stats    + 
                               PLT_devn_stats   +    POT_devn_stats    +  
                               RDW_devn_stats    +   TP_devn_stats      + 
                               TROPI_devn_stats +    URATE_devn_stats  +  
                               UREA_devn_stats  +    WBC_devn_stats, 
                             data=train_modc2_nzt.agegrp3)




logist.zerot<-glm(label ~ age+factor(gender)+factor(admission_type)+factor(outcome)+
                         no_prior_readm, 
                       data=train_modc2_zerot,family=binomial)
summary(logist.zerot)
predict.logist.zerot<-predict(logist.zerot,newdata=train_modc2_zerot,type="response")
length(predict.logist.zerot)

comp.logist.zerot<-cbind(train_modc2_zerot$label,predict.logist.zerot)
hist(predict.logist.zerot)
nodesize
ntree
summary(rf.mod1)

rf.gm.mod1<-randomForest(label ~ age+gender+admission_type+outcome+
                       no_prior_readm+total_no_of_tests +
                       total_trend + total_devn_stats +
                       total_trend*GLUC_devn_stats + total_trend*CRP_devn_stats +
                       total_trend*BASOCNT_devn_stats +
                       CA_devn_stats*CAUNCOR_devn_stats +
                       CAUNCOR_devn_stats *TP_devn_stats+
                       TP_devn_stats*ALB_devn_stats+
                       age*BASOCNT_devn_stats +
                       BASOCNT_devn_stats*ALB_devn_stats +
                       PLT_devn_stats*ALB_devn_stats+
                       EOSINCNT_devn_stats*ALB_devn_stats+
                       NEUTS_devn_stats*ALB_devn_stats+
                       ALB_devn_stats*HCT_devn_stats+
                       HB_devn_stats*HCT_devn_stats+
                       HB_devn_stats*MCHC_devn_stats+
                       MCHC_devn_stats*RDW_devn_stats+
                       MCH_devn_stats*MCHC_devn_stats+
                       MCH_devn_stats*MCV_devn_stats+
                       UREA_devn_stats*HB_devn_stats+
                       UREA_devn_stats*CREAT_devn_stats+
                       BILICON_devn_stats*BILI_devn_stats+
                       TROPI_devn_stats*LACTATE_devn_stats+
                       WBC_devn_stats*MONOCNT_devn_stats+
                       LYMPCNT_devn_stats*WBC_devn_stats+
                       total_no_of_tests*CAI_devn_stats+
                       total_no_of_tests*CL_devn_stats+
                       total_no_of_tests*PHOS_devn_stats+
total_no_of_tests*URATE_devn_stats+
  PHOS_devn_stats*MG_devn_stats+
  total_no_of_tests*OSM_devn_stats+
  POT_devn_stats+
  ALP_devn_stats+
  ALT_devn_stats+
  GGT_devn_stats+CK_devn_stats+AMYLASE_devn_stats+AST_devn_stats, data=train_modc2)


                       
          

train_modc2_zerot_x<-
  train_modc2_zerot[,c("age","gender","admission_type","outcome",
  "no_prior_readm","total_no_of_tests",
  "total_trend", "total_devn_stats",
  "ALB_devn_stats","ALP_devn_stats",   
  "ALT_devn_stats", "AMYLASE_devn_stats", 
  "AST_devn_stats", "BASOCNT_devn_stats",
  "BILI_devn_stats","BILICON_devn_stats",
  "CA_devn_stats","CAI_devn_stats",
  "CAUNCOR_devn_stats" ,  "CK_devn_stats",
  "CL_devn_stats"   ,   "CREAT_devn_stats"  , 
    "CRP_devn_stats"  ,   "EOSINCNT_devn_stats" ,
  "GGT_devn_stats"    ,   "GLUC_devn_stats" ,
    "HB_devn_stats"     ,   "HCT_devn_stats"    ,
  "LACTATE_devn_stats" ,  "LYMPCNT_devn_stats"  ,
    "MCH_devn_stats"     ,  "MCHC_devn_stats"   ,
  "MCV_devn_stats"    ,   "MG_devn_stats"       ,
    "MONOCNT_devn_stats" ,  "NEUTS_devn_stats"  , 
  "OSM_devn_stats"    ,   "PHOS_devn_stats"    ,
    "PLT_devn_stats"   ,    "POT_devn_stats"    ,  
  "RDW_devn_stats"    ,   "TP_devn_stats"      , 
    "TROPI_devn_stats" ,    "URATE_devn_stats"  ,  
  "UREA_devn_stats"  ,    "WBC_devn_stats")]

train_modc2_zerot_y<- train_modc2_zerot$label
rfcv.mod1<-rfcv(train_modc2_zerot_x, train_modc2_zerot_y,cv.fold=5,scale="log",step=0.5)

for (k in )
# -- 
nu = 2
trainK<-svm(label ~ age + gender + admission_type+outcome+no_prior_readm+
              duration+total_no_of_tests + total_trend + age*no_prior_readm + age*duration +
              age*total_no_of_tests + age*outcome + age*admission_type+ age:age+
              ALB_devn_stats   +     ALP_devn_stats    +    ALT_devn_stats   +    
              AMYLASE_devn_stats +   CAI_devn_stats   + CK_devn_stats     +    CL_devn_stats        +
              CREAT_devn_stats  +    GLUC_devn_stats + HB_devn_stats        +
              LACTATE_devn_stats   + MCH_devn_stats  +       MCHC_devn_stats     +  MCV_devn_stats   +
              MG_devn_stats     + NEUTS_devn_stats    +  OSM_devn_stats       +
              PHOS_devn_stats        +    POT_devn_stats      +  RDW_devn_stats  +   TP_devn_stats  +
              TROPI_devn_stats     + URATE_devn_stats    +  UREA_devn_stats      +  WBC_devn_stats  
            ,
              data = train_modc2,type="nu-classification",nu, kernel = "linear")
#              ALB_mean_value + ALP_mean_value + CAI_mean_value + HB_mean_value +
#              LACTATE_mean_value + MCHC_mean_value + NEUTS_mean_value + POT_mean_value +


print(trainK)
summary(trainK)
predK<-predict(trainK,xtest)

###################################################
# Test dataset: load 
###################################################
test_modc<-read.csv(file="test_mod_counts.csv")
nrow(test_modc)
head(test_modc)
tail(test_modc)
test_modc$duration<-as.Date(test_modc$discharge_date) -as.Date(test_modc$start_date)
# drop id columns
test_modc$total_trend = test_modc$ALB_trend + test_modc$ALP_trend + test_modc$ALT_trend + 
  test_modc$AMYLASE_trend + test_modc$CAI_trend +           
  test_modc$CK_trend + test_modc$NEUTS_trend + test_modc$OSM_trend + 
  test_modc$PHOS_trend+
  test_modc$TROPI_trend + test_modc$UREA_trend + test_modc$WBC_trend      

test_modc$total_devn_stats = test_modc$ALB_devn_stats   +    test_modc$ALP_devn_stats  +    
  test_modc$ALT_devn_stats    +   test_modc$AMYLASE_devn_stats + 
  test_modc$AST_devn_stats   +    test_modc$BASOCNT_devn_stats  +
  test_modc$BILI_devn_stats   +   test_modc$BILICON_devn_stats  +
  test_modc$CA_devn_stats     +   test_modc$CAI_devn_stats      +
  test_modc$CAUNCOR_devn_stats +  test_modc$CK_devn_stats       +
  test_modc$CL_devn_stats     +   test_modc$CREAT_devn_stats   + 
  test_modc$CRP_devn_stats    +   test_modc$EOSINCNT_devn_stats +
  test_modc$GGT_devn_stats    +   test_modc$GLUC_devn_stats     +
  test_modc$HB_devn_stats     +   test_modc$HCT_devn_stats      +
  test_modc$LACTATE_devn_stats +  test_modc$LYMPCNT_devn_stats  +
  test_modc$MCH_devn_stats     +  test_modc$MCHC_devn_stats     +
  test_modc$MCV_devn_stats    +   test_modc$MG_devn_stats       +
  test_modc$MONOCNT_devn_stats +  test_modc$NEUTS_devn_stats   + 
  test_modc$OSM_devn_stats    +   test_modc$PHOS_devn_stats    + 
  test_modc$PLT_devn_stats   +    test_modc$POT_devn_stats    +  
  test_modc$RDW_devn_stats    +   test_modc$TP_devn_stats      + 
  test_modc$TROPI_devn_stats +    test_modc$URATE_devn_stats  +  
  test_modc$UREA_devn_stats  +    test_modc$WBC_devn_stats    

test_modc2<- test_modc[,!(names(test_modc) %in% drops)]
test_modc2[which(test_modc2$age==0),]$age = 1

###################################################
# center and scale: test dataset
###################################################
test_modc2$age<-as.numeric(as.character(test_modc2$age))
test_modc2$gender<-as.numeric(test_modc2$gender)
test_modc2$admission_type<-as.numeric(test_modc2$admission_type)
test_modc2$outcome<-as.numeric(test_modc2$outcome)
test_modc2$duration<-as.numeric(test_modc2$duration)
tail(test_modc2)
test_modc2.scaled<-scale(test_modc2,center=TRUE,scale=TRUE)
test_modc2.df<-as.data.frame(test_modc2.scaled)


###################################################
# prediction (logistic regression): training accuracy - unscaled dataset
predict.ytrain<-predict(logist.mod2,newdata=train_modc2, type="response")
hist(predict.ytrain)
predict.ytrain_binary = numeric(length(predict.ytrain))
predict.ytrain_binary[which(predict.ytrain >= 0.45)] = 1
length(which(predict.ytrain_binary == train_modc2$label))/length(predict.ytrain)
## result: 0.599 very low
###################################################
# prediction (logistic regression): training accuracy - scaled dataset
predict.ytrain<-predict(logist.mod1,newdata=train_modc2.df,type="response")
hist(predict.ytrain)
predict.ytrain_binary = numeric(length(predict.ytrain))
predict.ytrain_binary[which(predict.ytrain > 0.45)] = 1
## result: 0.599 very low
length(which(predict.ytrain_binary == train_modc2$label))/length(predict.ytrain)
######################################################
# prediction (CART): training accuracy - unscaled dataset
predict.ytrain<-predict(cart.mod1,newdata=train_modc2,type="prob")[,2]
hist(predict.ytrain)
predict.ytrain_binary = numeric(length(predict.ytrain))
predict.ytrain_binary[which(predict.ytrain > 0.4)] = 1
length(which(predict.ytrain_binary == train_modc2$label))/length(predict.ytrain)
######################################################
# prediction (CART): training accuracy - scaled dataset
predict.ytrain<-predict(cart.mod1,data=train_modc2.df,type="prob")[,2]
hist(predict.ytrain)
predict.ytrain_binary = numeric(length(predict.ytrain))
predict.ytrain_binary[which(predict.ytrain > 0.45)] = 1
length(which(predict.ytrain_binary == train_modc2$label))/length(predict.ytrain)
######################################################
# prediction (RandomForest): training accuracy - unscaled dataset
predict.ytrain<-predict(rf.mod3,newdata=train_modc2)
hist(predict.train.final)
predict.ytrain_binary = numeric(length(predict.train.final))
predict.ytrain_binary[which(predict.ytrain > 0.45)] = 1
length(which(predict.ytrain_binary == train_modc2$label))/length(predict.ytrain)
#length(which(predict.ytrain == train_modc2$label))/length(predict.ytrain)
predict.train.final
####################
predict.ytrain.zerot<-predict(rf.zerot,newdata=train_modc2_zerot)
predict.ytrain.nzt.agegrp1<-predict(rf.nzt.agegrp1,newdata=train_modc2_nzt.agegrp1)
predict.ytrain.nzt.agegrp2<-predict(rf.nzt.agegrp2,newdata=train_modc2_nzt.agegrp2)
predict.ytrain.nzt.agegrp3<-predict(rf.nzt.agegrp3,newdata=train_modc2_nzt.agegrp3)
#predict.ytrain.zerot = cbind(predict.ytrain.zerot,train_modc2_zerot$seq_no)

predict.ytrain<-rbind(cbind(train_modc2_zerot$admissionid, predict.ytrain.zerot),
                      cbind(train_modc2_nzt.agegrp1$admissionid,predict.ytrain.nzt.agegrp1),
                      cbind(train_modc2_nzt.agegrp2$admissionid,predict.ytrain.nzt.agegrp2),
                      cbind(train_modc2_nzt.agegrp3$admissionid,predict.ytrain.nzt.agegrp3))
colnames(predict.ytrain) <- c("admissionid","prediction")
predict.ytrain.sorted<-predict.ytrain[order(as.numeric(attributes(predict.ytrain)$dimnames[[1]])),]
predict.ytrain.df<-data.frame(predict.ytrain.sorted)


head(predict.ytrain.nzt.agegrp1)
head(predict.ytrain.nzt.agegrp2)
head(predict.ytrain.nzt.agegrp3)
head(predict.ytrain.df)

#predict.ytrain<-predict(rf.gm.mod1,newdata=train_modc2)
hist(predict.ytrain.df$prediction)
predict.ytrain_binary = numeric(nrow(predict.ytrain.df))
predict.ytrain_binary[which(predict.ytrain.df$prediction > 0.45)] = 1

merge.ytrain<-merge(train_modc2,predict.ytrain.df,by="admissionid")

length(which(predict.ytrain_binary == train_modc2$label))/length(predict.ytrain_binary)

predict.train.final<-cbind(train_modc2$admissionid,predict.ytrain)
colnames(predict.train.final)<-c("id","Prediction")
tail(predict.final)
write.csv(predict.final,file="predict_train_final.csv")

######################################################
# prediction (logistic regression): test accuracy - unscaled dataset
predict.ytest<-predict(logist.mod2,newdata=test_modc2,type="response")
hist(predict.ytest)
######################################################
# prediction (logistic regression): test accuracy - scaled dataset
predict.ytest<-predict(logist.mod,newdata=test_modc2.df,type="response")
hist(predict.ytest)

######################################################
# prediction (CART): test accuracy - unscaled dataset
predict.ytest<-predict(cart.mod1,newdata=test_modc2,type="prob")[,2]
length(predict.ytest)
######################################################
# prediction (CART): test accuracy - scaled dataset
predict.ytest<-predict(cart.mod1,newdata=test_modc2.df,type="prob")[,2]

######################################################
# prediction (CART): test accuracy - unscaled dataset
predict.ytest<-predict(rf.mod3,newdata=test_modc2)

predict.ytest<-predict(rf.gm.mod1,newdata=test_modc2)


#### split and build two models based on zero tests or not

test_modc2_zerot<-test_modc2[which(test_modc2$total_no_of_tests==0),]
test_modc2_nzt.agegrp1<-test_modc2[which(test_modc2$total_no_of_tests!=0 &
                                           test_modc2$age <20),]
test_modc2_nzt.agegrp2<-test_modc2[which(test_modc2$total_no_of_tests!=0 &
                                           test_modc2$age >=20 & test_modc2$age <60),]

test_modc2_nzt.agegrp3<-test_modc2[which(test_modc2$total_no_of_tests!=0 &
                                           test_modc2$age >= 60),]


inc<-c(
"ALB_devn_stats","ALP_devn_stats",   
"ALT_devn_stats","AMYLASE_devn_stats",
"AST_devn_stats", "BASOCNT_devn_stats",
"BILI_devn_stats","BILICON_devn_stats",
"CA_devn_stats","CAI_devn_stats",
"CAUNCOR_devn_stats","CK_devn_stats",
"CL_devn_stats","CREAT_devn_stats",
"CRP_devn_stats","EOSINCNT_devn_stats",
"GGT_devn_stats"    ,  "GLUC_devn_stats" ,    
  "HB_devn_stats"    ,    "HCT_devn_stats"  ,    
  "LACTATE_devn_stats" ,  "LYMPCNT_devn_stats",  
  "MCH_devn_stats"     ,  "MCHC_devn_stats"   ,
  "MCV_devn_stats"    ,   "MG_devn_stats"      , 
  "MONOCNT_devn_stats" ,  "NEUTS_devn_stats"   ,
  "OSM_devn_stats"    ,  "PHOS_devn_stats"     ,
  "PLT_devn_stats"   ,   "POT_devn_stats"      ,
  "RDW_devn_stats"    ,   "TP_devn_stats"       ,
  "TROPI_devn_stats" ,   "URATE_devn_stats"   ,
  "UREA_devn_stats"  ,    "WBC_devn_stats","label")

train_modc2_gm<- train_modc[1:14873,(names(train_modc) %in% inc)]
head(train_modc2_gm)

m1<-minForest(train_modc2_gm,stat="BIC")
plot(m1)

cbind(m1@vertNames[m1@edges[,1]],m1@vertNames[m1@edges[,2]])

predict.ytest.zerot<-predict(rf.zerot,newdata=test_modc2_zerot)
logist.zerot<-glm(label ~ age+gender+admission_type+outcome+
                    no_prior_readm, 
                  data=train_modc2_zerot,family=binomial)
predict.ytest.zerot<-predict(logist.zerot,newdata=test_modc2_zerot,type="response")


predict.ytest.nzt.agegrp1<-predict(rf.nzt.agegrp1,newdata=test_modc2_nzt.agegrp1)
predict.ytest.nzt.agegrp2<-predict(rf.nzt.agegrp2,newdata=test_modc2_nzt.agegrp2)
predict.ytest.nzt.agegrp3<-predict(rf.nzt.agegrp3,newdata=test_modc2_nzt.agegrp3)
#predict.ytest.zerot = cbind(predict.ytest.zerot,test_modc2_zerot$seq_no)

predict.ytest<-rbind(cbind(test_modc2_zerot$admissionid, predict.ytest.zerot),
                      cbind(test_modc2_nzt.agegrp1$admissionid,predict.ytest.nzt.agegrp1),
                      cbind(test_modc2_nzt.agegrp2$admissionid,predict.ytest.nzt.agegrp2),
                      cbind(test_modc2_nzt.agegrp3$admissionid,predict.ytest.nzt.agegrp3))
colnames(predict.ytest) <- c("id","prediction")
predict.ytest.sorted<-predict.ytest[order(as.numeric(attributes(predict.ytest)$dimnames[[1]])),]
predict.ytest.df<-data.frame(predict.ytest.sorted)



hist(predict.ytrain.zerot)
hist(train_modc2_zerot$label)
plot(predict.ytrain.zerot,type="l")
lines(as.matrix(train_modc2$label))
comp.train<-cbind(predict.ytrain.df,as.matrix(train_modc2$label),
                  as.matrix(train_modc2$total_no_of_tests),as.matrix(train_modc2$age),
                  as.matrix(train_modc2$gender),as.matrix(train_modc2$outcome),
                  as.matrix(train_modc2$admission_type),
                  as.matrix(train_modc2$no_prior_readm))
write.csv(comp.train,"comp_train.csv")

######################################################
# add admissionids and create the output prediction file for submission
#predict.final<-cbind(test_modc$admissionid,predict.ytest)

colnames(predict.final)<-c("id","Prediction")
tail(predict.final)
write.csv(predict.final,file="predict_final.csv")
write.csv(predict.ytest.df,file="predict_final.csv")


#########
predict.prev <- read.csv("predict_final.csv")
head(predict.prev)
length(which(round(predict.final2[1:6354,2],1) != round(predict.final[1:6354,2],1)))
