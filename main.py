import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os, sys
from collections import defaultdict
from urllib.request import urlopen
import json
import matplotlib.pyplot as plt
import random
import plotly.express as px
import plotly.graph_objects as go



# import the file

vote=pd.read_csv('LS_2.0.csv')

vote[vote.SYMBOL.isnull()==True]['NAME'].unique() #Identifying the null entries in the data

'''
Cleaning up the Assets and Liabilities columns
'''
def value_cleaner(x):
    try:
        str_temp = (x.split('Rs')[1].split('\n')[0].strip())
        str_temp_2 = ''
        for i in str_temp.split(","):
            str_temp_2 = str_temp_2+i
        return str_temp_2
    except:
        x = 0
        return x
vote['ASSETS'] = vote['ASSETS'].apply((value_cleaner))
vote['LIABILITIES'] = vote['LIABILITIES'].apply((value_cleaner))

# Renaming the columns
vote.rename(columns={"CRIMINAL\nCASES": "CRIMINAL CASES", "GENERAL\nVOTES": "GENERAL VOTES", "POSTAL\nVOTES": "POSTAL VOTES","TOTAL\nVOTES": "TOTAL VOTES","OVER TOTAL ELECTORS \nIN CONSTITUENCY": "OVER TOTAL ELECTORS IN CONSTITUENCY","OVER TOTAL VOTES POLLED \nIN CONSTITUENCY": "OVER TOTAL VOTES POLLED IN CONSTITUENCY"}, inplace=True)

vote['ASSETS']=pd.to_numeric(vote['ASSETS'])
vote['LIABILITIES']=pd.to_numeric(vote['LIABILITIES'])
vote['CRIMINAL CASES'].replace({np.NaN:0})
vote['CRIMINAL CASES'] = pd.to_numeric(vote['CRIMINAL CASES'], errors='coerce').fillna(0).astype(np.int64)


def show_contestants_gender_ratio():
	vote_gndr=vote[vote['PARTY']!='NOTA']
	gndr_overall=vote_gndr.groupby('GENDER').apply(lambda x:x['NAME'].count()).reset_index(name='Counts')
	gndr_overall['Category']='Overall Gender Ratio'
	winners=vote_gndr[vote_gndr['WINNER']==1]
	gndr_winner=winners.groupby('GENDER').apply(lambda x:x['NAME'].count()).reset_index(name='Counts')
	gndr_winner['Category']='Winning Gender Ratio'
	gndr_overl_win=pd.concat([gndr_winner,gndr_overall])
	fig = px.bar(gndr_overl_win, x='GENDER', y='Counts',color='Category', barmode='group')
	fig.update_layout(title_text='Participation vs Win Counts analysis for the Genders',template='plotly_dark')
	fig.show()

def politician_education():
	ed_valid=vote[vote['PARTY']!="NOTA"]
	ed_cnt=ed_valid.groupby('EDUCATION').apply(lambda x:x['PARTY'].count()).reset_index(name='Counts')
	fig = go.Figure(data=[go.Pie(labels=ed_cnt['EDUCATION'], values=ed_cnt['Counts'], pull=[0.1, 0.2, 0, 0.1, 0.2, 0,0.1, 0.2, 0,0.1, 0.2, 0.1])])
	fig.update_layout(title_text='Overall Education Qualification of all the Nominees',template='plotly_dark')
	fig.show()
	ed_won=ed_valid[ed_valid['WINNER']==1]
	ed_win_cnt=ed_won.groupby('EDUCATION').apply(lambda x:x['PARTY'].count()).reset_index(name='Counts')
	fig2 = go.Figure(data=[go.Pie(labels=ed_win_cnt['EDUCATION'], values=ed_win_cnt['Counts'], pull=[0.1, 0.2, 0, 0.1, 0.2, 0,0.1, 0.1, 0.2,0, 0.1, 0.2],title='Education Qualification of the Winners')])
	fig2.update_layout(title_text='Education Qualification of the Winners',template='plotly_dark')
	fig2.show()



def politician_oopsy():
	ed_valid=vote[vote['PARTY']!="NOTA"]
	crim_cnt=ed_valid.groupby('CRIMINAL CASES').apply(lambda x:x['NAME'].count()).reset_index(name='Counts')
	fig = px.bar(crim_cnt, x='CRIMINAL CASES',y='Counts', barmode='group')
	fig.update_layout(title_text='Criminal Cases Counts Distribution among the politicians',template='plotly_dark')
	fig.show()

def politicain_age_distribution():
	ed_valid=vote[vote['PARTY']!="NOTA"]
	age_cnt=ed_valid.groupby(['AGE','GENDER']).apply(lambda x:x['NAME'].count()).reset_index(name='Counts')
	fig = px.bar(age_cnt, x='AGE',y='Counts', barmode='group')
	fig.update_layout(title_text='Age Counts Distribution among the politicians',template='plotly_dark')
	fig.show()


show_contestants_gender_ratio()
politician_oopsy()
politician_education()
politicain_age_distribution()