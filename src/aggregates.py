
from datetime import date
import calendar
import numpy as np
import scipy.stats
import time
import pickle
import pandas as pd
import os.path
from os import path
import pandas as pd

def sum_balance(l):
    """get the current summation of balance given a list of accounts"""
    ret = 0
    for act in l:
        ret += act.balance
    ret = round(ret, 2)
    print('Your current summation of balance is {}'.format(ret))
    return ret

def sum_allocable_balance(l):
    """get the current summation of allocable balance given a list of accounts"""
    ret = 0
    for act in l:
        ret += act.allocable_mount()
    ret = round(ret, 2)
    print('Your current summation of allocable balance is {}'.format(ret))
    return ret

def output_balance(l, d=date.today()):
    """get the current balance as a DataFrame, given a list of accounts"""
    a = {}
    for act in l:
        a[act.name] = round(act.balance,2)
    b  = pd.DataFrame(a.items()).T
    b.columns = b.iloc[0]
    b.drop(b.index[0], inplace=True)
    b.insert(0, "Date", d)
    b.reset_index(drop=True, inplace=True)
    return b

def write_balance(b, dir_name=r'/Users/xiaolan/Documents/repos/FinProject/log', filename='balances.csv'):
    """write balance to csv file. The current/Users/xiaolan/Documents/repos/FinProject/scripts """
    f = path.join(dir_name, filename)
    if path.exists(f):
        df_old = pd.read_csv(f)
        df_merge = df_old.append(b, sort=False).reset_index(drop=True)
        df_merge.drop(columns=['Unnamed: 0'], axis=1, inplace=True)
        df_merge.to_csv(f)
        return df_merge
    else:
        b.to_csv(f)
        return b

def get_all_cb(l_cards):
    all_df = []
    for card in l_cards:
        df = pd.DataFrame(card.get_cat()).T
        df['card_name'] = card.name
        all_df.append(df)
    all_df = pd.concat(all_df, axis=0).reset_index().reset_index().drop(columns=['level_0'])
    all_df.columns = ['category', 'pct', 'cb_type', 'start_date', 'expire_date', 'card_name']
    all_df = all_df[(all_df.start_date <= date.today()) & (all_df.expire_date >= date.today())]
    all_df['pct_cash'] = all_df[['pct', 'cb_type']].apply(lambda x: convert2cash(x[1], x[0]), axis=1)
    all_df.sort_values(by=['category', 'pct_cash'], ascending=[True, False], inplace=True)
    all_df = all_df[['category', 'card_name', 'pct_cash', 'pct', 'cb_type', 'start_date', 'expire_date']] # reorder
    return all_df

def get_highest_cb_each_cat(l_card):
    all_df =  get_all_cb(l_card)
    idx = all_df.groupby('category')['pct_cash'].idxmax()
    return all_df.loc[idx]

def convert2cash(t, v):
    available_type = {'UR':  1.5, \
                      'MR':  1.5, \
                      'HHP': 0.4, \
                      'TYP': 1.5, \
                      'cash':1.0}
    assert t in available_type, 'This type is not supported'
    return v*available_type[t]

def get_all_alerts(l_cards):
    alerts = []
    for card in l_cards:
        alert = card.get_alert()
        if alert!={}:
            for key, value in alert.items():
                alerts.append((card.name, key, value))
    
    df = pd.DataFrame(alerts, columns=['Name', 'Date', 'Alert']).sort_values(by='Date')
    return df


def get_latest_alerts(l_cards):
    df = get_all_alerts(l_cards)
    if df.shape[0]==0:
        print('No alert available')
    else:
        return df.iloc[0]

def get_all_account(l_cards):
    temp = []
    for c in l_cards:
        temp.append((c.name, c.balance))
    return pd.DataFrame(temp, columns=['Name', 'Position']).sort_values(by='Position',ascending=False)

def get_all_restrictions(l_cards):
    temp = []
    for c in l_cards:
        if c.restriction:
            temp.append((c.name, c.restriction))
    return pd.DataFrame(temp, columns=['Name', 'Restriction']).sort_values(by='Name',ascending=False)

def get_all_annual_fee(l_cards):
    temp = []
    for c in l_cards:
        if c.annual_fee != 0:
            temp.append((c.name, c.annual_fee))
    return pd.DataFrame(temp, columns=['Name', 'Annual Fee']).sort_values(by='Annual Fee',ascending=False)   

def No_ftf(l_cards):
    temp = []
    for c in l_cards:
        if not c._ftf:
            temp.append(c.name)
    return temp

def get_all_membership(l_cards):
    temp = []
    for c in l_cards:
        temp2 = c.get_reimburse()
        for k in temp2:
            temp.append((c.name, k, temp2[k][0], temp2[k][1]))
    return pd.DataFrame(temp, columns=['Name', 'Type', 'Balance', 'Expire']).sort_values(by='Expire')  

def get_all_other_benefits(l_cards):
    temp = []
    for c in l_cards:
        if c.benefit != '':
            temp.append((c.name, c.benefit))
    return pd.DataFrame(temp, columns=['Name', 'Benefit']).sort_values(by='Name',ascending=False)

# get all account and positions

#TODO: cash and stock position and profiles

#TODO: get all expiration date for gift card 

#TODO：get porfolio report (add pie chart)

#TODO: read me file or sphinx documentation

