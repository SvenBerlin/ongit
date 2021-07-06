# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 07:44:02 2020

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

import pandas as pd
import os as os
import glob as glob
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sn
sn.set()

class read_lambda:

    def __init__(self,path,title='',plot=False,save=False):
        self.path = os.path.abspath(path)
        self.title = title
        self.fname = 'plot_'+self.title+'.png'
        self.save = save
        self.plot = plot
        self.get_files()
        self.create_df()
        if self.plot or self.save:
            self.plot_lambda()

    def get_files(self):
        self.files = glob.glob(self.path+'/*.asc')
        if not self.title:
            self.title = self.files[0].split('\\')[-2]

    def create_df(self):
        self.df = pd.DataFrame()
        for file in self.files:
            temp = pd.read_csv(file,usecols=[0],skip_blank_lines=False)
            cname = temp.iloc[7,0]
            skiprows = temp[temp.iloc[:,0] == '#DATA'].index[0]+1
            index = temp.iloc[skiprows,0]

            temp = pd.DataFrame(data=pd.read_csv(file,skiprows=skiprows,sep='\t'))#,index_col=False))
            temp.reset_index(inplace=True)
            temp['#DATA'] = temp['#DATA'].apply(lambda x: float(x.replace(',','.')))
            temp['#DATA'] = temp['#DATA'].apply(lambda x: 10**-x*100)
            temp['index'] = temp['index'].apply(lambda x: int(float(x.replace(',','.'))))
            temp.set_index('index',inplace=True)
            temp[temp.iloc[:,0]>100]=100
            temp.rename(columns={'#DATA':cname},inplace=True)

            self.df = pd.concat([self.df,temp],axis=1)

    def plot_lambda(self,):
        if not self.plot:
            matplotlib.use('agg')
        else:
            matplotlib.use('Qt5Agg')
        mydpi=96
        fig,ax = plt.subplots(figsize=(1920/mydpi,1080/mydpi),dpi=mydpi)    
        for col in self.df.columns.tolist():
            ax.plot(self.df.index,self.df[col],label=col)
        ax.set_xlabel('Wellenlänge $\lambda$')
        ax.set_ylabel('Transmission %')
        ax.legend()
        ax.set_title(self.title)
        if self.save:
            fig.savefig(os.path.join(self.path,self.fname))

# path = r'H:\HOME\BERLIN USER\Bergmann, Sven Gerd\Private\Messungen\Aq_Filter'