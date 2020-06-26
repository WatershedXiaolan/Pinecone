
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

def get_available_categories(l_cards):
    all_df = []
    for card in l_cards:
        df = pd.DataFrame(card.get_cat()).T
        df['card_name'] = card.name
        all_df.append(df)
    all_df = pd.concat(all_df, axis=0).reset_index().reset_index().drop(columns=['level_0'])
    all_df.columns = ['category', 'pct', 'cb_type', 'start_date', 'expire_date', 'card_name']
    all_df = all_df[(all_df.start_date >= date.today()) & (all_df.expire_date <= date.today())]
    all_df.sort_values(by=['category', 'pct'], ascending=[True, False], inplace=True)
    return all_df


def get_all_alerts(l_card):
    alerts = []
    for card in l_card:
        alert = card.get_alert()
        if alert!={}:
            for key, value in alert.items():
                alerts.append((card.name, key, value))
    
    df = pd.DataFrame(alerts, columns=['Name', 'Date', 'Alert']).sort_values(by='Date')
    return df


def get_latest_alerts(l_card):
    df = get_all_alerts(l_card)
    if df.shape[0]==0:
        print('No alert available')
    else:
        return df.iloc[0]


#TODO: get the highest in each categories

#TODO: get cards belong to a category, not expired, cash and type


#TODO: broker class

#TODO: cash and stock position and profiles

#TODO: get all expiration date for gift card 

#TODO：get porfolio report (add pie chart)



