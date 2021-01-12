
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
from os import listdir


def sum_balance(accts):
    """get the current summation of balance given a list of accounts"""
    ret = 0
    for act in accts:
        ret += act.balance
    ret = round(ret, 2)
    print('Your current summation of balance is {}'.format(ret))
    return ret


def sum_allocable_balance(accts):
    """
    get the current summation of allocable
    balance given a list of accounts
    """
    ret = 0
    for acct in accts:
        ret += acct.allocable_mount()
    ret = round(ret, 2)
    print('Your current summation of allocable balance is {}'.format(ret))
    return ret


def output_balance(l_brokers, l_robos, l_banks, prices, d=date.today()):
    """get the current balance as a DataFrame, given a list of accounts"""

    # update brokers' balance
    for broke in l_brokers:
        broke.balance = broke.get_balance(prices)

    # gather balance of each account
    accts = l_brokers+l_robos+l_banks
    balances = {}
    for acct in accts:
        balances[act.name] = round(acct.balance, 2)
    balances = pd.DataFrame(balances.items()).T
    balances.columns = balances.iloc[0]
    balances.drop(balances.index[0], inplace=True)
    balances.insert(0, "Date", d)
    balances.reset_index(drop=True, inplace=True)

    # get positions and stats
    tot_stock_amt, tot_etf_amt, tot_bond_amt, tot_mmf_amt, tot_cash_amt = \
        get_positions(prices, l_brokers, l_robos, l_banks)

    # get summation and other stats
    balances['Sum'] = round(balances.iloc[:, 1:].sum(axis=1), 2)
    balances['Cash'] = round(tot_cash_amt + tot_mmf_amt, 2)
    balances['Stock'] = round(tot_stock_amt + tot_etf_amt, 2)
    balances['Bond'] = round(tot_bond_amt, 2)
    balances['S/(S+B) ratio'] = round((tot_etf_amt+tot_stock_amt)
                                      / (tot_etf_amt
                                         + tot_stock_amt
                                         + tot_bond_amt), 2)

    # merge results and arrange order
    names = ['Cash', 'Stock', 'Bond', 'Sum', 'S/(S+B) ratio']

    cols = [n for n in balances.columns if n not in names]
    cols += names
    balances = balances[cols]
    return balances


def output_balance_gc(accts, d=date.today()):
    """get the current balance as a DataFrame, given a list of accounts"""

    # gather balance of each account
    balances = {}
    for acct in accts:
        balances[acct.name] = round(acct.balance, 2)
    balances = pd.DataFrame(balances.items()).T
    balances.columns = balances.iloc[0]
    balances.drop(balances.index[0], inplace=True)
    balances.insert(0, "Date", d)
    balances.reset_index(drop=True, inplace=True)

    return balances


def write_balance_gc(acct,
                     dir_name=r'/Users/xiaolan/Documents/repos/FinProject/log',
                     filename='balances.csv'):
    """
    write balance to csv file.
    The current/Users/xiaolan/Documents/repos/FinProject/scripts
    """

    f = path.join(dir_name, filename)
    if path.exists(f):
        df_old = pd.read_csv(f)
        df_merge = df_old.append(acct, sort=False).reset_index(drop=True)
        df_merge.drop(columns=['Unnamed: 0'], axis=1, inplace=True)
        df_merge.to_csv(f)
        return df_merge
    else:
        acct.to_csv(f)
        return acct


def write_balance(acct,
                  dir_name=r'/Users/xiaolan/Documents/repos/FinProject/log',
                  filename='balances.csv'):
    """
    write balance to csv file
    The current/Users/xiaolan/Documents/repos/FinProject/scripts
    """
    f = path.join(dir_name, filename)
    if path.exists(f):
        df_old = pd.read_csv(f)
        df_merge = df_old.append(acct, sort=False).reset_index(drop=True)
        df_merge.drop(columns=['Unnamed: 0'], axis=1, inplace=True)
        if 'Sum' in df_merge.columns:
            names = ['Cash', 'Stock', 'Bond', 'Sum', 'S/(S+B) ratio']
            cols = [n for n in df_merge.columns if n not in names]
            cols += names
            df_merge = df_merge[cols]

        df_merge.to_csv(f)
        return df_merge
    else:
        acct.to_csv(f)
        return acct


def get_all_cb(l_cards):
    """credit card specific method"""

    all_df = []
    for card in l_cards:
        df = pd.DataFrame(card.get_cat()).T
        df['card_name'] = card.name
        all_df.append(df)
    all_df = pd.concat(all_df, axis=0).reset_index().reset_index().\
        drop(columns=['level_0'])
    all_df.columns = ['category',
                      'pct',
                      'cb_type',
                      'start_date',
                      'expire_date',
                      'card_name']
    all_df = all_df[(all_df.start_date <= date.today())
                    & (all_df.expire_date >= date.today())]
    all_df['pct_cash'] = all_df[['pct', 'cb_type']] \
        .apply(lambda x: convert2cash(x[1], x[0]), axis=1)
    all_df.sort_values(by=['category', 'pct_cash'],
                       ascending=[True, False],
                       inplace=True)
    all_df = all_df[['category',
                     'card_name',
                     'pct_cash',
                     'pct',
                     'cb_type',
                     'start_date',
                     'expire_date']]  # reorder
    return all_df


def get_highest_cb_each_cat(l_cards):
    """credit card specific method"""
    all_df = get_all_cb(l_cards)
    idx = all_df.groupby('category')['pct_cash'].idxmax()
    return all_df.loc[idx]


def convert2cash(t, v):
    """credit card specific method"""
    available_type = {'UR':  1.5,
                      'MR':  1.5,
                      'HHP': 0.4,
                      'TYP': 1.5,
                      'cash': 1.0}
    assert t in available_type, 'This type is not supported'
    return v*available_type[t]


def get_all_alerts(accts):
    alerts = []
    for card in accts:
        alert = card.get_alert()
        if alert != {}:
            for key, value in alert.items():
                alerts.append((card.name, key, value))

    df = pd.DataFrame(alerts, columns=['Name', 'Date', 'Alert']) \
        .sort_values(by='Date')
    return df


def get_latest_alerts(accts):
    df = get_all_alerts(accts)
    if df.shape[0] == 0:
        print('No alert available')
    else:
        return df.iloc[0]


def get_all_account(accts):
    temp = []
    for c in accts:
        temp.append((c.name, c.balance))
    return pd.DataFrame(temp, columns=['Name', 'Position']) \
        .sort_values(by='Position', ascending=False)


def get_all_restrictions(accts):
    temp = []
    for acct in accts:
        if acct.restriction:
            temp.append((acct.name, acct.restriction))
    return pd.DataFrame(temp, columns=['Name', 'Restriction']) \
        .sort_values(by='Name', ascending=False)


def get_all_annual_fee(l_cards):
    """credit card specific method"""
    temp = []
    for card in l_cards:
        if card.annual_fee != 0:
            temp.append((card.name, card.annual_fee))
    return pd.DataFrame(temp, columns=['Name', 'Annual Fee']) \
        .sort_values(by='Annual Fee', ascending=False)


def No_ftf(l_cards):
    """credit card specific method"""
    temp = []
    for c in l_cards:
        if not c._ftf:
            temp.append(c.name)
    return temp


def get_all_membership(l_cards):
    """credit card specific method"""
    temp = []
    for c in l_cards:
        temp2 = c.get_reimburse()
        for k in temp2:
            temp.append((c.name, k, temp2[k][0], temp2[k][1]))
    return pd.DataFrame(temp,
                        columns=['Name', 'Type', 'Balance', 'Expire']) \
        .sort_values(by='Expire')


def get_all_other_benefits(l_cards):
    """credit card specific method"""
    temp = []
    for card in l_cards:
        if c.benefit != '':
            temp.append((c.name, c.benefit))
    return pd.DataFrame(temp, columns=['Name', 'Benefit']) \
        .sort_values(by='Name', ascending=False)


def get_gc_balance_by_cat(l_gc):
    """gift card specific method"""
    ret = {}
    for c in l_gc:
        if c.cat not in ret:
            ret[c.cat] = c.balance
        else:
            ret[c.cat] += c.balance
    ret = pd.DataFrame(ret.items(), columns=['cat', 'balance']) \
        .sort_values('balance', ascending=False).reset_index(drop=True)
    return ret


def get_all_broker_buy_names(l_brokers):
    """get all stock names from all broker account"""
    stocks = []
    for b in l_brokers:
        stocks += b.get_all_names()
    return list(set(stocks))


def get_positions(prices, l_brokers, l_robos, l_banks):
    # get position
    """
    gether all accounts, return cash, mmf, stock, etf and bond balances
    """
    tot_stock_amt = 0
    tot_etf_amt = 0
    tot_bond_amt = 0
    tot_mmf_amt = 0
    tot_cash_amt = 0

    for b in l_brokers:
        tot_stock_amt += sum([prices[k]*v[1]
                              for k, v in b.get_stocks().items()])
        tot_etf_amt += sum([prices[k]*v[1] for k, v in b.get_ETF().items()])
        tot_bond_amt += sum([prices[k]*v[1] for k, v in b.get_bonds().items()])
        tot_mmf_amt += sum([prices[k]*v[1] for k, v in b.get_MMF().items()])
        tot_cash_amt += b.cash

    for b in l_robos:
        tot_etf_amt += b.balance*b.stock_ratio
        tot_bond_amt += b.balance*(1-b.stock_ratio)

    for b in l_banks:
        tot_cash_amt += b.balance

    return tot_stock_amt, tot_etf_amt, tot_bond_amt, tot_mmf_amt, tot_cash_amt


def save_pkl_files(l_banks=[], l_brokers=[], l_robos=[], l_gcs=[]):
    for b in l_banks:
        save_object(b, 'saved_objs/banks/'+b.name+'.pkl')
    for b in l_brokers:
        save_object(b, 'saved_objs/brokers/'+b.name+'.pkl')
    for b in l_robos:
        save_object(b, 'saved_objs/robos/'+b.name+'.pkl')
    for b in l_gcs:
        save_object(b, 'saved_objs/gcs/'+b.name+'.pkl')


def load_pkl_files():
    bank_files = [f for f in listdir('saved_objs/banks/')
                  if path.isfile(path.join('saved_objs/banks/', f))]
    brokers_files = [f for f in listdir('saved_objs/brokers/')
                     if path.isfile(path.join('saved_objs/brokers/', f))]
    gcs_files = [f for f in listdir('saved_objs/gcs/')
                 if path.isfile(path.join('saved_objs/gcs/', f))]
    robos_files = [f for f in listdir('saved_objs/robos/')
                   if path.isfile(path.join('saved_objs/robos/', f))]

    l_banks = []
    l_gcs = []
    l_brokers = []
    l_robos = []

    for f in bank_files:
        l_banks.append(load_object(path.join('saved_objs/banks/', f)))
    for f in brokers_files:
        l_brokers.append(load_object(path.join('saved_objs/brokers/', f)))
    for f in gcs_files:
        l_gcs.append(load_object(path.join('saved_objs/gcs/', f)))
    for f in robos_files:
        l_robos.append(load_object(path.join('saved_objs/robos/', f)))
    return l_banks, l_brokers, l_gcs, l_robos


def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def load_object(filename):
    with open(filename, 'rb') as input:
        ret = pickle.load(input)
    return ret
