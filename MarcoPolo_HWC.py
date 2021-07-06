# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 08:55:31 2018

@author: sbergmann

Copyright@Hach Lange GmbH 

Programm to read several HWC files from 2100Q(MarcoPolo), evaluation in
Excel based on selected TestTypes
"""

import pandas as pd
import os as os
import os.path
import glob
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.mlab as mlab
from matplotlib.gridspec import GridSpec
from matplotlib.dates import DateFormatter
import numpy as np
import shutil
import devdata as dv

def read_csv(path, years=None):
    '''
    Create pandas DataFrame of all given HWC files
    
    Parameter
    ------
    path: absolute path of mainfolder that holds subfolders containing the 
    HWC files.
    
    returns:
        
    df: plane DataFrame of all HWC files
    
    df_list: list of DataFrames for every HWC file
    '''         
    df = pd.DataFrame()
    # initialize count for purpose of feedback during processing through all files
    count = 1

    files = glob.glob(path+'\\*.txt')
    if years != None:
        files = [x for x in files if (x.split('_')[-1][:2] in str(years))] # for reduced list
#    files = files [:10]
    for file in files:
        print(str(count)+'/'+str(len(files))+' files: '+file.split('\\')[-1])
        count += 1
        try:
            blocks = pd.read_csv(file,usecols=[0], header=None).iloc[:,0]
            blocks = blocks[blocks.str.contains('\[')].index.tolist()
            
            general = pd.read_csv(file, skiprows = blocks[0]+2, nrows = blocks[1]-4,
                                     index_col = False, header = None)
            general = general.drop_duplicates(subset=[0],keep = 'last').reset_index(drop=True)
            hardware = pd.read_csv(file, skiprows = blocks[1]+2, nrows =(blocks[2]-blocks[1]-2))
            hardware['Block'] = 'Hardware'
            fi = pd.read_csv(file, skiprows = blocks[2]+3, nrows =(blocks[3]-blocks[2]-2))
            fi['Block'] = 'Fi'
            confdata = pd.read_csv(file, skiprows = blocks[3]+4 )
            confdata['Block'] = 'ConfData'
            
            temp = pd.concat([hardware,fi,confdata])
            temp = pd.concat([pd.DataFrame(columns = general[0]),temp ], axis=1)
            
            # re-organize HeadData into df_dat
            for i in range(len(general)):
                temp.iloc[:,i] = general.loc[i,1]
            # concat current file with main DataFrame df
            df = pd.concat([df,temp], ignore_index = True)
        except:
            pass
    try:
        df['DateTime'] = pd.to_datetime(df['DateTime'])
    except:
        pass
    return df
            
def print_MP_graphs(df,output, df2=None, sorter=None):

#    poi = [p for p in df['#VAAxxx'].unique().tolist() if type(p) is str]
#    poi = [p for p in df['#VAAxxx'].drop_duplicates(keep='last').tolist() if type(p) is str]
    
#    lastDev = [elm for elm in df.DeviceNumber.unique() if type(elm) is str][-1]
#    poi = pd.DataFrame({'#VAAxxx':df[df.DeviceNumber == lastDev]['#VAAxxx'].unique()})

#    poi = pd.read_hdf('sorter.h5').iloc[:,0].tolist()
    poi = sorter
                        
    types = [typ for typ in df.LightSourceType.unique().tolist() if typ in ['EPA','ISO']]
    mydpi=96
    labelCounter = (len(str(len(poi)))+1)*"0"
    for i,pruef in enumerate(poi):
        try:
            sc = pruef.split('_')[-1]
            title = pruef.split('_')[0]
        except:
            sc = '1'
            title = pruef
            pass
        temp = df[df['#VAAxxx']==pruef].reset_index(drop=True)
        if df2 is not None:
            temp2 = df2[df2['#VAAxxx']==pruef].reset_index(drop=True)
            temp2 = temp2[pd.notnull(temp2['actVal'])]
            temp2.sort_values(by='DateTime', inplace=True,)
            temp2.reset_index(drop=True,inplace=True)
                            
        fig = plt.figure(figsize=(1920/mydpi,1080/mydpi),dpi=mydpi)
        gs = GridSpec(4,4)#
        ax =fig.add_subplot(gs[1:4,0:4])
        hist = fig.add_subplot(gs[0,0:4])
        
        if len(temp) != len(temp[~pd.notnull(temp['actVal'])]):
                        
            temp = temp[pd.notnull(temp['actVal'])]
            temp.sort_values(by='DateTime', inplace=True,)
            temp.reset_index(drop=True,inplace=True)
            
            temp['NominalVersion']=pd.to_numeric(temp['NominalVersion'])
            latestVersion = temp[temp['NominalVersion']==max(temp['NominalVersion'])].iloc[0]        
            nomVal = [float(latestVersion['NomVal'])]*len(temp)  
            lbound = [float(latestVersion['loTol'])]*len(temp)
            ubound = [float(latestVersion['upTol'])]*len(temp)
            nomVal = [float(latestVersion['NomVal'])]*len(temp)           

            ax.plot(temp['DateTime'],lbound, 'k--', label='lo lim' )
            ax.plot(temp['DateTime'],ubound, 'k--', label='up lim' )
            ax.plot(temp['DateTime'],nomVal, 'm--', label='NomVal' )              
            
            mean_line = [temp['actVal'].mean()]*len(temp)
            plus_std3 = [mean_line[0]+(temp['actVal'].std()*3)]*len(temp)
            minus_std3 = [mean_line[0]-(temp['actVal'].std()*3)]*len(temp)
            plus_std5 = [mean_line[0]+(temp['actVal'].std()*5)]*len(temp)
            minus_std5 = [mean_line[0]-(temp['actVal'].std()*5)]*len(temp)            

            ax.plot(temp['DateTime'],mean_line, 'r--', label='mean' )
            ax.plot(temp['DateTime'],plus_std3, 'g--', label='+3s')
            ax.plot(temp['DateTime'],minus_std3, 'g--', label='-3s')
            ax.plot(temp['DateTime'],plus_std5, 'b--', label='-5s')
            ax.plot(temp['DateTime'],minus_std5, 'b--', label='-5s')
            
        else:
            y = pd.Series([1,0], index=['OK','NOK'])
            temp['actVal'] = temp['InspectionResult'].map(y)
        kwargs = dict(bins=10, alpha=0.5, histtype='stepfilled',edgecolor='none')    
        for typ in types:
            ax.scatter(x=temp[temp['LightSourceType']==typ]['DateTime'].dt.to_pydatetime(),
                       y=temp[temp['LightSourceType']==typ]['actVal'],
                       s=5, label=typ, alpha=.5)
            #Histplot
            hist.hist(list(temp[temp['LightSourceType']==typ]['actVal']),
                    weights=list(np.ones_like(temp[temp['LightSourceType']==typ]['actVal'])/float(len(temp))),
                    label=typ, **kwargs)
        
        if df2 is not None:
            ax.scatter(x=temp2['DateTime'].dt.to_pydatetime(),
                       y=temp2['actVal'],
                       c = 'r',s=5, label=typ, alpha=.5)
            hist.hist(list(temp2[temp2['LightSourceType']==typ]['actVal']),
                    weights=list(np.ones_like(temp2[temp2['LightSourceType']==typ]['actVal'])/float(len(temp2))),
                    label='BG26', **kwargs)
        hist.set_ylabel('probability')
        hist.set_title(title)
        hist.legend()
        plt.setp(ax.xaxis.get_majorticklabels(),'rotation', 90)
        
        ax.grid(b=True)
        ax.set_xlabel('Date')
        ax.set_ylabel(sc)
        
        ax.legend()
        plt.tight_layout()
        plt.savefig(output+'\\'+(labelCounter+str(i))[-3:]+'_'+pruef+'.png')
        plt.close(fig)


def SortValuesByList(df, sorter=None, sub = 'DeviceNumber', by='#VAAxxx'):
    
    if sorter is None:
        file = open('sorter.txt','r')
        sorter = file.readlines()
    sorterIndex = dict(zip(sorter,range(len(sorter))))
    df['sorter']=df[by].map(sorterIndex)
    df.sort_values([sub,'sorter'],inplace=True)
    df.drop('sorter', 1, inplace = True)
    df.reset_index(drop=True, inplace=True)
    return df                           
                 
def extract_raw(path_in,path_out):
    
#    path_out=dv.kon.montagetest[dv.kon.montagetest['Dateityp']==r'marcopolo_Fi'][r'Montageordner']   
    files = [glob.glob(subfolder[0] + '\\*.txt')[-1] for subfolder in os.walk(path_in) if glob.glob(subfolder[0] + '\\*.txt')]
    count = 0
    for file in files:
        print('Parsing file '+str(count+1)+'/'+str(len(files))+': '+os.path.basename(file))
#        path_out = file+'\\'+file.split('\\')[-1]
        out = path_out+'\\'+os.path.basename(file)
        shutil.copy(file,out)
        (dformatstr ,zieldformatdatei)=dv._read._marcoPolo2100Q._marcoPolo2100Q_parseto_dformat(out,dformatcsvbehalten=True)
        with open(out, 'w') as f:
            for item in dformatstr:
                f.write("%s\n" % item)
        count = count +1
    print('----- all files parsed -----')
    
    
# MAIN    
"""
mainfolder - enter the mainfolder that stores all subfolders holding 
HWC-files
"""   
# main folder of all devices
path = os.path.abspath(r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\lab\Marco Polo\9_Optics\Produktionsdaten\HW Files from 2019-1 to 2019-4-9\parsedQis')
# selection of TestTypes that should be evaluated ('all' if every TestType is wanted)
output = r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\lab\Marco Polo\9_Optics\Produktionsdaten\HW Files from 2019-1 to 2019-4-9\Auswertung'
#df, df_list = read_csv(mainfolder)
path = r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\lab\Marco Polo\9_Optics\Produktionsdaten\Auswertung_2100Qis_komplett\2100Qis.h5'
df = pd.read_hdf(path)
df = read_csv(path, 5)
h5_path = r'H:\WORKGROUP\R&D Projects\PUBLICGROUP\lab\Marco Polo\9_Optics\Produktionsdaten\HW Files from 2019-1 to 2019-4-9\Qis.h5'
df = pd.read_pickle(h5_path)
df = pd.concat([df,pd.read_pickle(pickle_path)])    
df = pd.concat([pd.read_pickle(pickle_path),df]) 
df = pd.concat([pd.read_hdf(h5_path),df]) 
df = pd.concat([df,pd.read_hdf(h5_path)]) 
#pd.to_pickle(df,output+'\\2100Qis.pkl')
dfGood2.to_hdf(output+'\\good.h5', key='dfGood2', mode='w')
dfQis.to_hdf(h5_path, key='dfQis', mode='w')
df = pd.read_hdf(h5_path)
sub = df[df['DeviceNumber'].isin(df['DeviceNumber'].unique()[0:10].tolist())]
sub['DateTime'] = pd.to_datetime(sub['DateTime'])
    
df.DateTime = pd.to_datetime(df.DateTime, errors='coerce',) 
df.drop(df.index[df.DateTime.isnull()], inplace=True)
df.sort_values(by='DateTime', inplace=True)
df.reset_index(drop=True, inplace=True)

lst = df.DeviceNumber.unique().tolist()[:10]
df_sub = pd.DataFrame()#
for elm in lst:
    df_sub = pd.concat([df_sub, df[df.DeviceNumber==elm]])  
fig, ax = plt.subplots()
ax.plot(df_sub[df_sub['#VAAxxx']=='180DegAdjPotiPreset'].DateTime,df_sub[df_sub['#VAAxxx']=='180DegAdjPotiPreset'].actVal)

# rotate and align the tick labels so they look better
fig.autofmt_xdate()

# use a more precise date string for the x axis locations in the
# toolbar
ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
ax.set_title('fig.autofmt_xdate fixes the labels')

plt.plot(df[df['#VAAxxx']=='10NtuReadTurb_NTU'].DateTime,df[df['#VAAxxx']=='10NtuReadTurb_NTU'].actVal)

for elm in list(df['#VAAxxx'].unique()):
                   plt.plot(df[df['#VAAxxx']==elm].DateTime,df[df['#VAAxxx']==elm].actVal)
                            
 h =df[(df['#VAAxxx']=='180DegAdjPotiPreset') & (df['actVal']> 80)]
           
lst = df[(df['#VAAxxx']=='20NtuAdjPotiL190Deg_V') & (df['actVal'] > 1.5)]['DeviceNumber'].unique().tolist()
lst2 = df_good[(df_good['#VAAxxx']=='100NtuCalTurb_NTU') & (df_good['actVal'] < 54)]['DeviceNumber'].unique().tolist()           

                        
#sorter = df2['#VAAxxx'].unique().tolist()
sorter.to_hdf('sorter.h5',key='sorter',mode='w')
sorter = pd.DataFrame({'#VAAxxx':sorter})
sorter = '''LidDetection 
Keyboard
LcdContrast
LcdBacklight
Sound
StandByMode
RAM
Flash
ModulConnect
Temperature_C
BattPowerNoLoad_V
BattPowerLocalLoad_V
BattPowerModulLoad_V
ExternalPower_V
AnalogPowerOffPos_V
AnalogPowerOffNeg_V
AnalogPowerOnPos_V
AnalogPowerOnNeg_V
LampOff180Deg_V
LampOff90DegPoti0_V
LampOn180Deg_V
LampOn90DegPoti0_V
LampOn90DegFilterPoti0_V
LampOn90DegPoti99_V
LampOnOffDiff_V
180DegOnOffDiff_V
90DegOnOffDiff_V
90DegPoti0Poti99Diff_V
90DegFilterVoltQuot
180DegAdjPotiSensorValue_V
180DegAdjPotiPreset
RtcTimer
RtcAlarm
800NtuAdjPotiL090Deg_V
800NtuAdjPotiL0
800NtuDarkL0180Deg_mV
800NtuDarkL090Deg_mV
800NtuCal180Deg_V
800NtuCal90Deg_V
800NtuCalRatio
800NtuCalTurb_NTU
800NtuCalTurbMinMaxRange_NTU
100NtuCal180Deg_V
100NtuCal90Deg_V
100NtuCalRatio
100NtuCalTurb_NTU
100NtuCalTurbMinMaxRange_NTU
20NtuAdjPotiL190Deg_V
20NtuAdjPotiL1
20NtuAdjMinVoltL090Deg_V
20NtuAdjL1Low180Deg_V
20NtuAdjL1Low90Deg_V
20NtuAdjL1High180Deg_V
20NtuAdjL1High90Deg_V
20NtuAdjL1Factor
20NtuAdjL1Offset_V
20NtuDarkL190Deg_mV
20NtuCal180Deg_V
20NtuCal90Deg_V
20NtuCalRatio
20NtuCalTurb_NTU
20NtuCalTurbMinMaxRange_NTU
1NtuAdjPotiL290Deg_V
1NtuAdjPotiL2
1NtuAdjMinVoltL190Deg_V
1NtuAdjL2High90Deg_V
1NtuAdjL2High90DegFilter_V
1NtuAdjL2Low90Deg_V
1NtuAdjL2Low90DegFilter_V
1NtuAdjL2TurbL1_NTU
1NtuAdjL2TurbL2_NTU
1NtuAdjL2TurbFactor
1NtuAdjL2Factor
1NtuAdjL2Offset_V
1NtuDarkL290Deg_mV
1NtuRead180Deg_V
1NtuRead90Deg_V
1NtuReadRatio
1NtuReadTurb_NTU
1NtuReadTurbMinMaxRange_NTU
WaterNtuRead180Deg_V
WaterNtuRead90Deg_V
WaterNtuReadRatio
WaterNtuReadTurb_NTU
WaterNtuReadTurbMinMaxRange_NTU
10NtuRead180Deg_V
10NtuRead90Deg_V
10NtuReadRatio
10NtuReadTurb_NTU
10NtuReadTurbMinMaxRange_NTU
e1
e2
e3
e4
a0
a1
a2
a3'''.split()



#mydpi=96
##try:
##    sc = pruef.split('_')[-1]
##    title = pruef.split('_')[0]
##except:
##    sc = '1'
##    title = pruef
##    pass
#pruef = '180DegAdjPotiPreset'
#fig, ax = plt.subplots(1,1,figsize=(1920/mydpi,1080/mydpi),dpi=mydpi)
#ax.set_xlabel('Time')
#ax.set_ylabel('1')
#ax.set_title(pruef)
#
##temp = df[df['#VAAxxx']==pruef].reset_index(drop=True)
#
##try:
###    temp.sort_values(by='DateTime', inplace=True,)
##except TypeError:
##    pass
##temp.reset_index(drop=True,inplace=True)
#
#mean_line = [h['actVal'].mean()]*len(h)
#plus_std3 = [mean_line[0]+(h['actVal'].std()*3)]*len(h)
#minus_std3 = [mean_line[0]-(h['actVal'].std()*3)]*len(h)
#plus_std5 = [mean_line[0]+(h['actVal'].std()*5)]*len(h)
#minus_std5 = [mean_line[0]-(h['actVal'].std()*5)]*len(h)
#if not np.isnan(h['loTol'].iloc[0]):
#    lbound = [float(h['loTol'].iloc[0])]*len(h)
#    ubound = [float(h['upTol'].iloc[0])]*len(h)
#    ax.plot(h['DateTime'],lbound, 'k--', label='up lim' )
#    ax.plot(h['DateTime'],ubound, 'k--', label='lo lim' )
##    
##ax.plot(h['DateTime'],mean_line, 'r--', label='mean' )
#ax.plot(h['DateTime'],plus_std3, 'g--', label='+3s')
#ax.plot(h['DateTime'],minus_std3, 'g--', label='-3s')
#ax.plot(h['DateTime'],plus_std5, 'b--', label='-5s')
#ax.plot(h['DateTime'],minus_std5, 'b--', label='-5s')
#
#
#ax.scatter(h['DateTime'].dt.to_pydatetime(),h['actVal'], s=5, label='2100Q')
#ax.scatter(h3['DateTime'].dt.to_pydatetime(),h3['actVal'], s=5, label='2100Qis')
#
#plt.setp(ax.xaxis.get_majorticklabels(),'rotation', 90)
#
#ax.grid(b=True)
#plt.legend()
#plt.tight_layout()
#plt.savefig(output+'\\'+pruef+'.png')
#plt.close(fig)









#def print_MP_graphs(df,output):
#
#    poi = [p for p in df['#VAAxxx'].unique().tolist() if type(p) is str]
#
#    mydpi=96
#    for pruef in poi:
#        try:
#            sc = pruef.split('_')[-1]
#            title = pruef.split('_')[0]
#        except:
#            sc = '1'
#            title = pruef
#            pass
#        fig, ax = plt.subplots(1,1,figsize=(1920/mydpi,1080/mydpi),dpi=mydpi)
#        ax.set_xlabel('Device')
#        ax.set_ylabel(sc)
#        ax.set_title(title)
#        
#        temp = df[df['#VAAxxx']==pruef].reset_index(drop=True)        
#        try:
#            temp.sort_values(by='DateTime', inplace=True,)
#        except TypeError:
#            pass
#        temp.reset_index(drop=True,inplace=True)
#        
#        if len(temp) != len(temp[~np.notnull(temp['actVal'])]):
#            temp = temp[temp[np.notnull(temp['actVal'])]]
#            temp.reset_index(drop=True,inplace=True)
#        else:
#            y = pd.Series([1,0], index=['OK','NOK'])
#            temp['actVal'] = temp['InspectionResult'].map(y)
#        
##        if not np.isnan(temp['loTol'][0]):
#        if len(temp[pd.notnull(temp['loTol'])])!=0:
#            lbound = [temp[pd.notnull(temp['loTol'])]['loTol'].iloc[0]]*len(temp)
#            ubound = [temp[pd.notnull(temp['upTol'])]['upTol'].iloc[0]]*len(temp)
##            lbound = [float(temp['loTol'][0])]*len(temp)
##            ubound = [float(temp['upTol'][0])]*len(temp)
#            ax.plot(temp['DateTime'],lbound, 'k--', label='up lim' )
#            ax.plot(temp['DateTime'],ubound, 'k--', label='lo lim' )
#        
##        if not np.isnan(temp['actVal'][0]):
#        if not np.isnan(temp['actVal'][0]):
#            mean_line = [temp['actVal'].mean()]*len(temp)
#            plus_std3 = [mean_line[0]+(temp['actVal'].std()*3)]*len(temp)
#            minus_std3 = [mean_line[0]-(temp['actVal'].std()*3)]*len(temp)
#            plus_std5 = [mean_line[0]+(temp['actVal'].std()*5)]*len(temp)
#            minus_std5 = [mean_line[0]-(temp['actVal'].std()*5)]*len(temp)
#            
#            ax.plot(temp['DateTime'],mean_line, 'r--', label='mean' )
#            ax.plot(temp['DateTime'],plus_std3, 'g--', label='+3s')
#            ax.plot(temp['DateTime'],minus_std3, 'g--', label='-3s')
#            ax.plot(temp['DateTime'],plus_std5, 'b--', label='-5s')
#            ax.plot(temp['DateTime'],minus_std5, 'b--', label='-5s')
#        else:
##            y = pd.Series([1,0], index=['OK','NOK'])
##            temp['actVal'] = temp['InspectionResult'].map(y) 
#            if len(temp[temp['actVal'] != 'NaN']) == 0:
#                y = pd.Series([1,0], index=['OK','NOK'])
#                temp['actVal'] = temp['InspectionResult'].map(y)
#                
#            else:
#                temp = temp[pd.notnull(temp['actVal'])]
#                temp.sort_values(by='DateTime', inplace=True,)
#                temp.reset_index(drop=True,inplace=True)
#                
#            
##        ax.plot(temp['DateTime'],temp['actVal'], linewidth=.5)
#        for typ in ['EPA','ISO']:
#            ax.scatter(x=temp[temp['LightSourceType']==typ]['DateTime'].dt.to_pydatetime(),
#                       y=temp[temp['LightSourceType']==typ]['actVal'],
#                       s=5, label=typ)
#        plt.setp(ax.xaxis.get_majorticklabels(),'rotation', 90)
#        
#        ax.grid(b=True)
#        plt.legend()
#        plt.tight_layout()
#        plt.savefig(output+'\\'+pruef+'.png')
#        plt.close(fig)






















#def print_MP_graphs(df=None,df2=None,output=None):
#
#    poi = [p for p in df['#VAAxxx'].unique().tolist() if type(p) is str]
#
#    mydpi=96
#    for pruef in poi:
#        try:
#            sc = pruef.split('_')[-1]
#            title = pruef.split('_')[0]
#        except:
#            sc = '1'
#            title = pruef
#            pass
#        fig, ax = plt.subplots(1,1,figsize=(1920/mydpi,1080/mydpi),dpi=mydpi)
#        ax.set_xlabel('Device')
#        ax.set_ylabel(sc)
#        ax.set_title(title)
#        
#        temp = df[df['#VAAxxx']==pruef].reset_index(drop=True)        
#        try:
#            temp.sort_values(by='DateTime', inplace=True,)
#        except TypeError:
#            pass
#        temp.reset_index(drop=True,inplace=True)
#        
#        if df2 is not None:
#            temp2 = df2[df2['#VAAxxx']==pruef].reset_index(drop=True)
#            try:
#                temp2.sort_values(by='DateTime', inplace=True,)
#            except TypeError:
#                pass
#            temp2.reset_index(drop=True,inplace=True)
#        
#
#        if not np.isnan(temp['loTol'][0]):
#            lbound = [float(temp['loTol'][0])]*len(temp)
#            ubound = [float(temp['upTol'][0])]*len(temp)
#            ax.plot(temp['DateTime'],lbound, 'k--', label='up lim' )
#            ax.plot(temp['DateTime'],ubound, 'k--', label='lo lim' )
#        
#        if not np.isnan(temp['actVal'][0]):
#            mean_line = [temp['actVal'].mean()]*len(temp)
#            plus_std3 = [mean_line[0]+(temp['actVal'].std()*3)]*len(temp)
#            minus_std3 = [mean_line[0]-(temp['actVal'].std()*3)]*len(temp)
#            plus_std5 = [mean_line[0]+(temp['actVal'].std()*5)]*len(temp)
#            minus_std5 = [mean_line[0]-(temp['actVal'].std()*5)]*len(temp)
#            
#            ax.plot(temp['DateTime'],mean_line, 'r--', label='mean' )
#            ax.plot(temp['DateTime'],plus_std3, 'g--', label='+3s')
#            ax.plot(temp['DateTime'],minus_std3, 'g--', label='-3s')
#            ax.plot(temp['DateTime'],plus_std5, 'b--', label='-5s')
#            ax.plot(temp['DateTime'],minus_std5, 'b--', label='-5s')
#        else:
##            y = pd.Series([1,0], index=['OK','NOK'])
##            temp['actVal'] = temp['InspectionResult'].map(y) 
#            if len(temp[temp['actVal'] != 'NaN']) == 0:
#                y = pd.Series([1,0], index=['OK','NOK'])
#                temp['actVal'] = temp['InspectionResult'].map(y)
#                if df2 is not None:
#                    if len(temp2[temp['actVal'] != 'NaN']) == 0:
#                        y = pd.Series([1,0], index=['OK','NOK'])
#                        temp2['actVal'] = temp2['InspectionResult'].map(y)
#            else:
#                temp = temp[pd.notnull(temp['actVal'])]
#                temp.sort_values(by='DateTime', inplace=True,)
#                temp.reset_index(drop=True,inplace=True)
#                if df2 is not None:
#                    temp2 = temp2[pd.notnull(temp2['actVal'])]
#                    temp2.sort_values(by='DateTime', inplace=True,)
#                    temp2.reset_index(drop=True,inplace=True)
#            
##        ax.plot(temp['DateTime'],temp['actVal'], linewidth=.5)
#        ax.scatter(x=temp['DateTime'].dt.to_pydatetime(),y=temp['actVal'], s=5, label=df.iloc[0].LightSourceType)
#        if df2 is not None:
#            ax.scatter(x=temp2['DateTime'].dt.to_pydatetime(),y=temp2['actVal'], s=5, label=df2.iloc[0].LightSourceType)
#        plt.setp(ax.xaxis.get_majorticklabels(),'rotation', 90)
#        
#        ax.grid(b=True)
#        plt.legend()
#        plt.tight_layout()
#        plt.savefig(output+'\\'+pruef+'.png')
#        plt.close(fig)