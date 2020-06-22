
from datetime import date
import calendar
import numpy as np
import scipy.stats
import time
import pickle
import pandas as pd
import os.path
from os import path

def sum_balance(l):
    """get the current summation of balance given a list of accounts"""
    ret = 0
    for act in l:
        ret += act.balance
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
        a[act.name] = act.balance
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



