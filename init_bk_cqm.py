import sys
from src.acts import *
from src.aggregates import *
from src.get_prices import *
import pickle
from datetime import date
from src.plots import * 
from src.get_prices import get_static_prices

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

citi_saving = BankAccount(name='CITI SAVING', balance=23482.73, interest_rate=0.0001, month_fee=0)
citi_saving.restriction = 'There’s a $5 monthly service fee for a Chase Savings account, but the bank will waive this fee \
                            if at least one of the following conditions applies to you each statement cycle: \
                            you maintain at least a $300 minimum daily balance; \
                            you set up at least one repeat automatic transfer of $25 from a Chase checking account'
citi_saving.min_amount = 300

citi_checking = BankAccount(name='CITI CHECKING', balance=10898.74, interest_rate=0.0001, month_fee=0)
citi_checking.restriction = 'There’s a $5 monthly service fee for a Chase Savings account, but the bank will waive this fee \
                            if at least one of the following conditions applies to you each statement cycle: \
                            you maintain at least a $300 minimum daily balance; \
                            you set up at least one repeat automatic transfer of $25 from a Chase checking account'
citi_checking.min_amount = 300