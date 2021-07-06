# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 09:29:48 2018

@author: sbergmann

Copyright@Sven Bergmann
"""
'''
Beobachte Preisentwicklung eines Artikels

Programm dient zur Überwachung verschiedener Artikel auf Amazon

Parameter
---------

fname: string
    Name der hdf5 Datei die die alle Informationen über die getrackten Artikel enthält
'''


import pandas as pd
import os.path
import matplotlib.pyplot as plt


def _load(fname='amzTrack.h5',links=None,article=None, vis=False):
    if os.path.isfile(fname) is True:
        df = pd.read_hdf(fname, 'df')
        try:
            df = _check(df=df,links=links,article=article,vis=vis,fname=fname)
        except:
            print('HTTPError: Service Unavailable - Please try checking later again.')
            pass
    else:
        print('Log file doesn\' exist yet, new file will be created')
        df = _new_logger(fname)        
    return df

def _check(df=None,links=None,article=None, vis=False, fname='amzTrack.h5'):
    if df is None:
        df = _new_logger()        
    if links is None:
        links = df['Link'].unique().tolist()
    for link in links:
        data = pd.read_html(link)
        h = pd.DataFrame({'Article':[''.join([x+' ' for x in data[1].iloc[0,1].split()[2:]])],
                          'Link':link,
                          'DateTime':[pd.Timestamp.now()],
                          'Currency':[data[0].iloc[0,1].split()[0]],
                          'Price':[float(data[0].iloc[0,1].split()[1].replace(',','.'))]})
        _stats(df=h)
        df = pd.concat([df,h])
    if vis is True:
        _vis(df,article)
    df = _save(df=df,fname=fname)
    return df

def _add(df=None,links=None,fname='amzTrack.h5'):
    df = _check(df=df,links=links,fname=fname)
    return df

def _save(df=None,fname=None):
    df.to_hdf(fname, key='df', mode='w')
    print('File saved as '+fname)

def _del(df=None,article=None,fname='amzTrack.h5'):
    df=df[~df['Article'].str.contains(article)]
    _save(df,fname)
    return df

def _vis(df=None, article=None):
    if article == None:
        articles = df['Article'].unique()
    else:
        articles = list(df['Article'][df['Article'].str.contains(article)].unique())
    
    mydpi=96
    for article in articles:
        fig, ax = plt.subplots(1,1,figsize=(1920/mydpi,1080/mydpi),dpi=mydpi)
        ax.set_xlabel('Date')
        ax.set_ylabel('Price ('+df['Currency'][df['Article']==article].iloc[0]+')')
        ax.set_title(article[0:10])
        ax.plot(df['DateTime'][df['Article']==article].tolist(),df['Price'][df['Article']==article].tolist())
        plt.grid()

def _stats(df=None):
    articles = df['Article'].unique().tolist()
    for article in articles:
        temp = df['Price'][df['Article']==article]
        try:
            if temp.iloc[-1]<temp.iloc[-2]:
                print(article[:10]+' droped %.0f%% günstiger geworden' % ((temp.iloc[-2]-temp.iloc[-1])/temp.iloc[-2]*100))
        except:
            pass

def _new_logger(fname='amzTrack.h5'):
    df = pd.DataFrame(columns='Article Link DateTime Currency Price'.split())
    _save(df,fname)
    return df


if __name__ == "__main__":
    main(path_to_watch, 'VRFY_LXG445')        
df = _load()




#fname = 'amzTrack.h5'
#new_links = ['https://www.amazon.de/Cloud-EX2-Ultra-Spielkonsolen-WDBVBZ0080JCH-EESN/dp/B01BIGSRLS/ref=sr_1_1?ie=UTF8&qid=1544099912&sr=8-1&keywords=home+cloud']
#article = 'Cloud'

#df = _add(df,new_links,fname)
#df = _load(fname,links=None,article=None, vis=True)
#df = _check(df)



#import pandas as pd
#import requests
#from bs4 import BeautifulSoup
#from tabulate import tabulate
#
#res = requests.get(links[0])
#soup = BeautifulSoup(res.content,'lxml')
#table = soup.find_all('table')[0] 
#df = pd.read_html(str(soup))
#print( tabulate(df[0], headers='keys', tablefmt='psql') )

    
#df = _add(df,new_links)
#df = _del(df,article)
#_vis(df)
#_save(df)






#import pandas as pd
#import os.path
#import matplotlib.pyplot as plt
#
#### TBD
## statistics (mean), trend...
## graphial visualization
#
#def _check(df,links=None):
#    if links == None:
#        links = df['Link'].unique().tolist()
#    for link in links:
#        data = pd.read_html(link)
#        h = pd.DataFrame({'Article':[''.join([x+' ' for x in data[1].iloc[0,1].split()[2:]])],
#                          'Link':link,
#                          'DateTime':[pd.Timestamp.now()],
#                          'Currency':[data[0].iloc[0,1].split()[0]],
#                          'Price':[float(data[0].iloc[0,1].split()[1].replace(',','.'))]})
#        _stats(h)
#        df = pd.concat([df,h])
#    return df
#
#def _add(df,links):
#    df = _check(df,links)
#    return df
#
#def _save(df):
#    df.to_hdf(fname, key='df', mode='w')
#
#def _load(fname):
#    if os.path.isfile(fname) == True:
#        df = pd.read_hdf(fname, 'df')
##        links = df['Link'].unique().tolist()
#    else:
#        print('File does not exist')
#    return df#, links
#
#def _del(df,article):
#    df=df[~df['Article'].str.contains(article)]    
#    return df
#
#def _vis(df, article=None):
#    if article == None:
#        articles = df['Article'].unique()
#    else:
#        articles = list(df['Article'][df['Article'].str.contains(article)].unique())
#    
#    mydpi=96
#    for article in articles:
#        fig, ax = plt.subplots(1,1,figsize=(1920/mydpi,1080/mydpi),dpi=mydpi)
#        ax.set_xlabel('Date')
#        ax.set_ylabel('Price ('+df['Currency'][df['Article']==article].iloc[0]+')')
##        ax.set_title(article[0:10])
#        ax.plot(df['DateTime'][df['Article']==article].tolist(),df['Price'][df['Article']==article].tolist())
#        plt.grid()
#
#def _stats(df):
#    articles = df['Article'].unique().tolist()
#    for article in articles:
#        temp = df['Price'][df['Article']==article]
#        try:
#            if temp.iloc[-1]<temp.iloc[-2]:
#                print(article[:10]+' ist %.0f%% günstiger geworden' % ((temp.iloc[-2]-temp.iloc[-1])/temp.iloc[-2]*100))
#        except:
#            pass
#
#def _new_logger():
#    df = pd.DataFrame(columns='Article Link DateTime Currency Price'.split())
#    return df
#        
#fname = 'amzTrack.h5'
##new_links = ['https://www.amazon.de/Cloud-EX2-Ultra-Spielkonsolen-WDBVBZ0080JCH-EESN/dp/B01BIGSRLS/ref=sr_1_1?ie=UTF8&qid=1544099912&sr=8-1&keywords=home+cloud']
##article = 'Cloud'
#df = _load(fname)
#df = _check(df)
#    
##df = _add(df,new_links)
##df = _del(df,article)
##_vis(df)
##_save(df)







### Funktionsfähing
#fname = 'amzTrack.h5'
#if not os.path.isfile(fname):
#    df = pd.DataFrame(columns='Article Link DateTime Currency Price'.split())
#    links = ['https://www.amazon.de/Xiaomi-Saugroboter-Staubsager-Kehrmaschine-Wischfunktion/dp/B0799KQRSR/ref=sr_1_4?ie=UTF8&qid=1544083947&sr=8-4&keywords=Xiaomi+Xiaomi+roborock+S50',]
#else:
#    df = pd.read_hdf(fname, 'df')
#    links = df['Link'].unique()
##    links = ['https://www.amazon.de/Xiaomi-Saugroboter-Staubsager-Kehrmaschine-Wischfunktion/dp/B0799KQRSR/ref=sr_1_4?ie=UTF8&qid=1544083947&sr=8-4&keywords=Xiaomi+Xiaomi+roborock+S50',]
#
#for link in links:
#    data = pd.read_html(link)
#    h = pd.DataFrame({'Article':[''.join([x+' ' for x in data[1].iloc[0,1].split()[2:]])],
#                      'Link':link,
#                      'DateTime':[pd.Timestamp.now()],
#                      'Currency':[data[0].iloc[0,1].split()[0]],
#                      'Price':[data[0].iloc[0,1].split()[1]]})
#    df = pd.concat([df,h])
#
#df.to_hdf(fname, key='df', mode='w')