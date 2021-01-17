import sys
from src.account import *
from src.aggregates import *
from src.get_prices import *
import pickle
from datetime import timedelta
from datetime import date
from src.plots import *
from src.get_prices import get_static_prices
from src.helpers import prep_log_folder, merge_bank_logs_no_cache, \
                        merge_retirement_logs, remove_cache
import os
import shutil
"""
# get new price
prices = get_static_prices()
h_prices = pd.read_csv(('/Users/xiaolan/Documents'
                        '/repos/FinProject/local_src'
                        '/historical_prices.csv'))
"""
today = date(2020, 6, 1)

robinhood = BrokerAccount(name='ROBINHOOD', balance=10000, interest_rate=0.03)
robinhood.add_stocks(ID='AAPL', number=0, full_name='APPLE')
robinhood.buy_stock_auto('AAPL', 5, 120)
robinhood.add_ETF(ID='SPY', number=0, full_name='SPY', expense_ratio=0.0002)
robinhood.buy_ETF_auto('SPY', 10, 100)

l_brokers = [robinhood]
l_robos = []
l_banks = []

balances = output_balance_with_history_price(l_brokers,
                                             l_robos,
                                             l_banks,
                                             d=today)

merged_balance = merge_bank_logs_no_cache(balances)

today = date(2020, 6, 15)
robinhood.buy_stock_auto('AAPL', 5, 110)
balances = output_balance_with_history_price(l_brokers,
                                             l_robos,
                                             l_banks,
                                             d=today)

merged_balance = merge_bank_logs_no_cache(balances, merged_balance)

merged_balance.to_csv(('/Users/xiaolan/Documents'
                       '/repos/FinProject/log'
                       '/balance_banks.csv'), index=False)
