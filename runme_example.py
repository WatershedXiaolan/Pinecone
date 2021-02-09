import sys
from src.account import *
from src.aggregates import *
from src.get_prices import *
import pickle
from datetime import timedelta
from datetime import date
#from src.plots import *
from src.get_prices import get_static_prices
from src.helpers import merge_bank_logs_no_cache
from src.helpers import merge_retirement_logs
from src.helpers import remove_cache
from src.helpers import prep_log_folder
import os
import shutil

# initialize accounts and look-up tables
merged_balance = None
h_prices_path = './log_example/historical_prices.csv'

# create accounts
pinecone_checking = BankAccount(
    name='PINECONE BANK CHECKING',
    balance=10000,
    interest_rate=0.01,
    month_fee=0)
pinecone_broker = BrokerAccount(
    name='PINECONE BROKER',
    balance=10000)
pinecone_robo = RoboAccount(
    name='PINECONE ROBO',
    balance=10000,
    interest_rate=0.05,
    annual_pct_fee=0.0025)
pinecone_broker.stock_ratio = 0.8
# add accounts into lists
l_banks = [pinecone_checking]
l_brokers = [pinecone_broker]
l_robos = [pinecone_robo]

# -----------------------------------------------------------------------------
#                            BEGIN TRANSACTIONS
# -----------------------------------------------------------------------------
today = date(2021, 1, 1)
print(today.strftime("%Y-%m-%d"))

# output balance
balances = output_balance_with_history_price(l_brokers,
                                             l_robos,
                                             l_banks,
                                             d=today,
                                             h_prices_path=h_prices_path)

merged_balance = merge_bank_logs_no_cache(balances)

# ---------------------------TRANSACTION DIVIDER-------------------------------
today = date(2021, 1, 2)
print(today.strftime("%Y-%m-%d"))

# transaction
transfer(pinecone_checking, pinecone_broker, 1000)

# output balance
balances = output_balance_with_history_price(l_brokers,
                                             l_robos,
                                             l_banks,
                                             d=today,
                                             h_prices_path=h_prices_path)

merged_balance = merge_bank_logs_no_cache(balances, merged_balance)

# ---------------------------TRANSACTION DIVIDER-------------------------------
today = date(2021, 1, 3)
print(today.strftime("%Y-%m-%d"))

# transaction
pinecone_broker.add_ETF('SPY', 'SP500', 0, 0.0002)
pinecone_broker.buy_ETF_auto('SPY', 10, 300)

# output balance
balances = output_balance_with_history_price(l_brokers,
                                             l_robos,
                                             l_banks,
                                             d=today,
                                             h_prices_path=h_prices_path)

merged_balance = merge_bank_logs_no_cache(balances, merged_balance)

# -----------------------------------------------------------------------------
#                            BEGIN TRANSACTIONS
# -----------------------------------------------------------------------------

merged_balance.to_csv(('./log_example/balance_banks.csv'), index=False)
