import sys
from src.acts import *
from src.aggregates import *
from src.get_prices import *
import pickle
from datetime import date
from src.plots import * 
from src.get_prices import get_static_prices
prices = get_static_prices()
import os, shutil
folder = r'/Users/xiaolan/Documents/repos/FinProject/log_cqm/'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    os.remove(file_path)

# initialize accounts and look-up tables
# create bank accounts
chase_checking = BankAccount(name='CHASE CHECKING', balance=2438.66, interest_rate=0, month_fee=0)
chase_checking.restriction = 'Direct Deposits totaling $500 or more made to this account OR an average daily \
                               balance of $5,000 or more in any combination of qualifying linked deposits/investments, \
                               or minimum balance of $1500. Otherwise there will be a $12 monthly fee'
chase_checking.min_amount = 1500  

chase_saving = BankAccount(name='CHASE SAVING', balance=355.65, interest_rate=0.0001, month_fee=0)
chase_saving.restriction = 'There’s a $5 monthly service fee for a Chase Savings account, but the bank will waive this fee \
                            if at least one of the following conditions applies to you each statement cycle: \
                            you maintain at least a $300 minimum daily balance; \
                            you set up at least one repeat automatic transfer of $25 from a Chase checking account'
chase_saving.min_amount = 300

discover_saving = BankAccount(name='DISCOVER SAVING', balance=6365.38, interest_rate=0.0055, month_fee=0)

citi_saving = BankAccount(name='CITI SAVING', balance=23482.73, interest_rate=0.007, month_fee=0)
citi_saving.restriction = 'The Citi Accelerate Savings account has a monthly fee of $4.50. \
                           The only way to waive the monthly fee is to maintain an average monthly balance of at least $500.'
citi_saving.min_amount = 500

citi_checking = BankAccount(name='CITI CHECKING', balance=10898.74, interest_rate=0.0003, month_fee=0)
citi_checking.restriction = 'Maintain a combined average monthly balance of $10,000+ in eligible linked deposit, \
                             retirement and investment accounts, otherwise $25'
citi_checking.min_amount = 10000

robinhood =  BrokerAccount(name='ROBINHOOD', balance=86134.60, interest_rate=0.03)

robinhood.add_ETF(ID='SPY', number=73, full_name='', expense_ratio=0.0009)
robinhood.add_ETF(ID='VTI', number=95, full_name='', expense_ratio=0.0004)
robinhood.add_ETF('VOO', 'SP 500', 57, expense_ratio=0.0003)
robinhood.add_bonds('BND', 'US Bond', 131, expense_ratio=0.00035)
robinhood.add_bonds('BNDX', 'International Bonds', 50, expense_ratio=0.0008)
robinhood.add_bonds('BAR', 'GraniteShares Gold Trust', 200, expense_ratio=0.0017)
robinhood.cash = 5625.55

fidelity_roth_ira = BrokerAccount(name='FIDELITY ROTH IRA', balance=12695.30, interest_rate=0.03)
fidelity_traditional = BrokerAccount(name='FIDELITY TRA IRA', balance=0.01, interest_rate=0.03)

l_banks = [chase_checking, chase_saving, discover_saving, citi_checking, citi_saving]
l_brokers = [robinhood]
l_robos = []


# -----------------------------
d=date(2020,11,15)

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances, dir_name=r'/Users/xiaolan/Documents/repos/FinProject/log_cqm')

#----------------------------------------------------------------- 
d=date(2020,11,30)
robinhood.buy_ETF('VOO', 10)
robinhood.balance = robinhood.get_balance(prices)
robinhood.cash = 2313.66

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances, dir_name=r'/Users/xiaolan/Documents/repos/FinProject/log_cqm')

#----------------------------------------------------------------- 
d=date(2020,12,14)
robinhood.buy_ETF('VOO', 6)
robinhood.balance = robinhood.get_balance(prices)
robinhood.cash = 307.17

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances, dir_name=r'/Users/xiaolan/Documents/repos/FinProject/log_cqm')