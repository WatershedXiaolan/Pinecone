import sys
from src.acts import *
from src.aggregates import *
from src.get_prices import *
import pickle
from datetime import date
from src.plots import * 
from src.get_prices import get_static_prices
from src.helpers import prep_log_folder, merge_bank_logs, merge_gc_logs, merge_retirement_logs, remove_cache
import os, shutil

# get new price
prices = get_static_prices()

# clean log folder
folder = r'/Users/xiaolan/Documents/repos/FinProject/log_example/'
prep_log_folder(folder)

# initialize data hosting structure
l_banks, l_robos, l_brokers = [], [], []

# create a bank account
a_bank = BankAccount(name='I AM A BANK', balance=100, interest_rate=0.01, month_fee=10)
l_banks.append(a_bank)

# create a robo advisor account
a_robo = RoboAccount(name='I AM A ROBO', balance=100, interest_rate=0.03, annual_pct_fee=0.0025)
a_robo.stock_ratio=0.9
l_robos.append(a_robo)

# create a robo advisor account
a_broker = BrokerAccount(name='I AM A BROKER', balance=100, interest_rate=0.015)
l_brokers.append(a_broker)

# -------
# beginning of transaction
d=date(2021,1,1)

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
merge_bank_logs(balances, cache_file='./log_example/balances_cache.csv', save_file='./log_example/balances.csv')


# -------
# beginning of transaction
d=date(2021,1,2)
a_bank.make_deposit(100)

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
merge_bank_logs(balances, cache_file='./log_example/balances_cache.csv', save_file='./log_example/balances.csv')

# -------
# beginning of transaction
d=date(2021,1,3)
a_bank.make_deposit(101)

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
merge_bank_logs(balances, cache_file='./log_example/balances_cache.csv', save_file='./log_example/balances.csv')

# -------
# beginning of transaction
d=date(2021,1,4)
a_bank.make_deposit(200)


balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
merge_bank_logs(balances, cache_file='./log_example/balances_cache.csv', save_file='./log_example/balances.csv')




remove_cache(folder)

# if inside: replace
# if not: add or insert into the right place
# dont remove the cache
# remove cache at the very end of the scripts

# existing 1: replace 1 and add 2;
# existing 1 and 3: replace 1, insert 2 and add 3 

