import sys
#print(sys.path)
from src.acts import *
from src.aggregates import *
from src.get_prices import *
import pickle
from datetime import date
from src.plots import * 
from src.get_prices import get_static_prices
from src.helpers import prep_log_folder, merge_bank_logs, merge_gc_logs
import os, shutil

# get new price
prices = get_static_prices()

# clean log folder
folder = r'/Users/xiaolan/Documents/repos/FinProject/log/'
prep_log_folder(folder)


# initialize accounts and look-up tables
# create bank accounts
usbank_checking = BankAccount(name='US BANK CHECKING', balance=1860.63, interest_rate=0, month_fee=0)
usbank_checking.restriction = 'Balance should be > 1500, otherwise there would be a $6.95 monthly fee. Transfer out requires $3'
usbank_checking.min_amount = 1500

usbank_saving = BankAccount(name='US BANK SAVING', balance=1540.96, interest_rate=0.0001, month_fee=0)
usbank_saving.restriction = 'Balance should be > 1000, otherwise there would be a $4 monthly fee. Transfer out requires $3'
usbank_saving.min_amount = 1000

marcus_cd_4655 = BankAccount(name='MARCUS CD 4655', balance=10197.67, interest_rate=0.0235, month_fee=0)
marcus_cd_4655.add_alert((date(2020, 8, 27), 'Maturity date. Will be renewed for another 13 month. Need to update \
                                             interest rate and alert'))
marcus_cd_4655.restriction = "better not to withdraw before maturity"
marcus_cd_4655.min_amount = marcus_cd_4655.balance

marcus_cd_7222 = BankAccount(name='MARCUS CD 7222', balance=10202.21, interest_rate=0.0235, month_fee=0)
marcus_cd_7222.add_alert((date(2020, 8, 20), 'Maturity date. Will be renewed for another 13 month, Need to update \
                                             interest rate and alert'))
marcus_cd_7222.restriction = "better not to withdraw before maturity"
marcus_cd_7222.min_amount = marcus_cd_7222.balance

marcus_saving = BankAccount(name='MARCUS SAVING', balance=27316.43, interest_rate=0.0105, month_fee=0)
marcus_saving.min_amount = 0

chase_checking = BankAccount(name='CHASE CHECKING', balance=12350.88, interest_rate=0, month_fee=0)
chase_checking.restriction = 'Direct Deposits totaling $500 or more made to this account OR an average daily \
                               balance of $5,000 or more in any combination of qualifying linked deposits/investments, \
                               or minimum balance of $1500. Otherwise there will be a $12 monthly fee'
chase_checking.min_amount = 1500                               

chase_saving = BankAccount(name='CHASE SAVING', balance=2031.42, interest_rate=0.0001, month_fee=0)
chase_saving.restriction = 'There’s a $5 monthly service fee for a Chase Savings account, but the bank will waive this fee \
                            if at least one of the following conditions applies to you each statement cycle: \
                            you maintain at least a $300 minimum daily balance; \
                            you set up at least one repeat automatic transfer of $25 from a Chase checking account'
chase_saving.min_amount = 300

discover_saving = BankAccount(name='DISCOVER SAVING', balance=19087.32, interest_rate=0.0105, month_fee=0)

capital_one = BankAccount(name='CAPITAL ONE MONEY MARKET', balance=0.01, interest_rate=0.0105, month_fee=0)


betterment_cash = BankAccount(name='BETTERMENT CASH', balance=24.63, interest_rate=0.004, month_fee=0)

betterment_wealth = RoboAccount(name='BETTERMENT WEALTH', balance=46829.06, interest_rate=0.03, annual_pct_fee=0.0025)

wealthfront = RoboAccount(name='WEALTHFRONT', balance=16539.51, interest_rate=0.03, annual_pct_fee=0.0025)
wealthfront.restriction = 'First $15000 no management fee'
wealthfront.min_amount = 15000  

chase_invest_trade = BrokerAccount(name='CHASE YOU INVEST TRADE', balance=25575.52, interest_rate=0.015)
chase_invest_trade.restriction = '$75 account transfer fee for transfering stock out'

robinhood =  BrokerAccount(name='ROBINHOOD', balance=40167.72, interest_rate=0.03)
fidelity =  BrokerAccount(name='FIDELITY', balance=2365.40, interest_rate=0.03)


l_banks = [chase_checking, chase_saving, marcus_cd_4655, marcus_cd_7222, marcus_saving, usbank_checking, \
           usbank_saving, discover_saving, betterment_cash, capital_one]
l_brokers = [chase_invest_trade, robinhood, fidelity]
l_robos = [betterment_wealth, wealthfront]

d=date(2020,6,21)
balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)



# create gift card 
nordstrom_digit = GiftCard(name='NORDSTROM 2819', balance=15.61, cat='Nordstrom')
nordstrom_digit.code = ('6182497601622819', '61857291')
target_green_chrismas = GiftCard(name='TARGET 664', balance=50, cat='Target')
target_green_chrismas.code = ('041220846991664', '28618712')
target_red_chrismas = GiftCard(name='TARGET 668', balance=50, cat='Target')
target_red_chrismas.code = ('041301393029668', '27986505')
target_green_chrismas2 = GiftCard(name='TARGET 668', balance=50, cat='Target')
target_green_chrismas2.code = ('041221081119334', '41344760')
target_santa = GiftCard(name='TARGET 292', balance=50, cat='Target')
target_santa.code = ('041301393682292', '04503278')
wholefood3pack = GiftCard(name='WHOLEFOOD 020899', balance=75, cat='Wholefoods')
wholefood50 = GiftCard(name='WHOLEFOOD 01225', balance=50, cat='Wholefoods')
wholefood50_2 = GiftCard(name='WHOLEFOOD 020613', balance=50, cat='Wholefoods')
wholefood100 = GiftCard(name='WHOLEFOOD 000351', balance=100, cat='Wholefoods')
wholefood_awe = GiftCard(name='WHOLEFOOD 0157', balance=34.44, cat='Wholefoods')
wholefood_awe.code = ('6362640259010157', '4703')
wholefood_scratch = GiftCard(name='WHOLEFOOD 7367', balance=50, cat='Wholefoods')
wholefood_scratch.code = ('6362642076097367', '4980')
kroger = GiftCard(name='KROGER 511', balance=100, cat='Kroger')
kroger.code = ('6006495903 356 024 511', '4223')
first_watch1 = GiftCard(name='FIRST WATCH 705', balance=25, cat='First Watch')
first_watch1.code = ('5896297503935502', '705')
first_watch2 = GiftCard(name='FIRST WATCH 655', balance=25, cat='First Watch')
first_watch2.code = ('5896297503935510', '655')
trader_joe = GiftCard(name='TRADER JOES', balance=10.16, cat='Trader Joes')
starbucks = GiftCard(name='STARBUCKS', balance=67.73)
airbnb1 = GiftCard(name='AIRBNB 904', balance=50, cat='Airbnb')
airbnb1.code = ('6039 5341 0081 3604 904', 'zl8uhfl6okix0')
airbnb2 = GiftCard(name='AIRBNB 852', balance=50, cat='Airbnb')
airbnb2.code = ('6039 5341 0081 5642 852', 'd7yvv7g0wcsff')
gamestop = GiftCard(name='GAMESTOP 382', balance=50, cat='Gamestop')
gamestop.code = ('6364 9110 0802 6539 382', '7037')
burger_king = GiftCard(name='BURGER KING', balance=10, cat='Burger King')
burger_king.code = ('6172656282110133', None)
cheese_cake_factory = GiftCard(name='CHEESE CAKE', balance=25, cat='Cheese Cake Factory')
cheese_cake_factory.code = ('6103359579424827', '64495067')
l_gc = [nordstrom_digit, target_green_chrismas, target_green_chrismas2, target_red_chrismas, target_santa, \
          wholefood3pack, wholefood50, wholefood50_2, wholefood100, wholefood_awe, wholefood_scratch, \
          kroger, first_watch1, first_watch2, trader_joe, starbucks, airbnb1, airbnb2, gamestop, burger_king, \
          cheese_cake_factory]

d = date(2020,6,21)
balances = output_balance_gc(l_gc, d=date(2020,6,21))
_ = write_balance(balances, filename='gc_balance.csv')


#-----------------------------------------------------------------
d=date(2020,6,22)
# usbank transfer out cost money. Pay from usbank first 
usbank_checking.make_withdraw(77.16) # pay usbank credit card
transfer(usbank_saving, usbank_checking, 500, factor=1)
transfer(chase_saving, chase_checking, 1700, factor=1)
balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')

#-----------------------------------------------------------------
d=date(2020,6,23)
chase_checking.make_withdraw(5.9) # pay CSP
chase_checking.make_withdraw(131.68) # pay Amex Hilton

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')
#-----------------------------------------------------------------
d=date(2020,6,24)
heb = GiftCard(name='HEB 1', balance=0, cat='Heb')
transfer(chase_checking, heb, 100, factor=1)
l_gc.append(heb)

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')

#-----------------------------------------------------------------
d=date(2020,6,25)
netflix = GiftCard(name='NETFLIX 1', balance=0, cat='Netflix')
transfer(chase_checking, netflix, 50, factor=1)
l_gc.append(netflix)

robinhood.d = d
robinhood.add_ETF(ID='SPY', number=60, full_name='', expense_ratio=0.0009)
robinhood.add_ETF(ID='VTI', number=56, full_name='', expense_ratio=0.0004)
robinhood.add_stocks(ID='MSFT', number=15, full_name='Microsoft')
robinhood.add_stocks(ID='AAPL', number=5, full_name='Apple')
robinhood.add_stocks(ID='XOM', number=105, full_name='ExxonMobil')
robinhood.add_stocks(ID='GOOGL', number=3, full_name='Google')
robinhood.add_stocks(ID='AMZN', number=1, full_name='Amazon')
robinhood.add_stocks(ID='BABA', number=5, full_name='Alibaba')
robinhood.add_stocks(ID='TSLA', number=1, full_name='Tesla')
robinhood.add_stocks(ID='FB', number=1, full_name='Facebsook')
robinhood.add_stocks(ID='MSFT', number=15, full_name='Microsoft')

#print(robinhood.get_etf_positions())
#print(robinhood.get_stock_positions())
#print(robinhood.get_bond_positions())

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')

#-----------------------------------------------------------------
d=date(2020,6,26)
# add two roth accounts
betterment_roth_ira = RoboAccount(name='BETTERMENT ROTH IRA', balance=3172.16, interest_rate=0.03, annual_pct_fee=0.0025)
betterment_traditional = RoboAccount(name='BETTERMENT TRA IRA', balance=2928.34, interest_rate=0.03, annual_pct_fee=0.0025)
betterment_traditional.add_alert((date(2020,6,28), 'Transfer to Roth'))
betterment_roth_ira.add_alert((date(2021,2,15), 'Need Form 8606 to report backdoor roth transfer'))
betterment_roth_ira.stock_ratio=0.9
betterment_traditional.stock_ratio=0.9
iras = [betterment_roth_ira, betterment_traditional]
# transfer to tranditional roth
transfer(chase_checking, betterment_traditional, 6000, factor=1)

# pay freedom card
chase_checking.make_withdraw(15.98)

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')
#-----------------------------------------------------------------
d=date(2020,6,28)

# update robinhood cash position 
robinhood.cash = 19834.60
# update fidelity position 
fidelity.add_ETF(ID='VTI', number=15, full_name='', expense_ratio=0.0009)
fidelity.add_MMF(ID='SPAXX', number=9.2, full_name='', expense_ratio=0.0042)
# update chase you invest trade
chase_invest_trade.add_MMF(ID='VMMXX', number=25165.33, full_name='', expense_ratio=0.0016)

betterment_wealth.stock_ratio = 0.8
wealthfront.stock_ratio = 0.8

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')
#-----------------------------------------------------------------
d=date(2020,6,29)
chase_checking.make_withdraw(39) # pay Amex Every Day
chase_checking.make_withdraw(63.89) # pay Amex Aspire
costco_1_1 = GiftCard(name='COSTCO 1-1', balance=0, cat='costco')
costco_1_2 = GiftCard(name='COSTCO 1-2', balance=0, cat='costco')
costco_2_1 = GiftCard(name='COSTCO 2-1', balance=0, cat='costco')
costco_3_1 = GiftCard(name='COSTCO 3-1', balance=0, cat='costco')
costco_3_2 = GiftCard(name='COSTCO 3-2', balance=0, cat='costco')
transfer(chase_checking, costco_1_1, 300, factor=1)
transfer(chase_checking, costco_1_2, 300, factor=1)
transfer(chase_checking, costco_2_1, 300, factor=1)
transfer(chase_checking, costco_3_1, 300, factor=1)
transfer(chase_checking, costco_3_2, 300, factor=1)
costco_1_1.make_withdraw(250)
l_gc += [costco_1_1, costco_1_2, costco_2_1, costco_3_1, costco_3_2]

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')
#----------------------------------------------------------------- 
d=date(2020,6,30)
# close usbank saving 
transfer(usbank_saving, usbank_checking, usbank_saving.balance, factor=1)
usbank_checking.make_withdraw(166.34) # pay usbank
# bought $200 amazon gift card
amazon = GiftCard(name='AMAZON', balance=0, cat='amazon')
transfer(chase_checking, amazon, 200, factor=1)
l_gc += [amazon]

#----------------------------------------------------------------- 
d=date(2020,7,1)
# buy and sell in chase you invest
chase_invest_trade.sell_MMF('VMMXX', 25165.33)
chase_invest_trade.add_bonds('BND', 'US Bond', 4, expense_ratio=0.00035)
# salary
chase_checking.make_deposit(3158.73)
# rent
chase_checking.make_withdraw(1124.04)

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')

#----------------------------------------------------------------- 
d=date(2020,7,2)
robinhood.add_ETF('VXUS', 'Vanguard Total International Market', 50, 0.0011) # buy international stock ETF
chase_invest_trade.buy_bonds('BND', 146) # buy us bond ETF
chase_invest_trade.add_bonds('BNDX', 'International Bonds', 100, expense_ratio=0.0008)

#----------------------------------------------------------------- 
d=date(2020,7,6)
usbank_checking.make_withdraw(55.56) # pay Amex Every Day
usbank_checking.make_withdraw(468.66) # pay Amex Aspire
chase_checking.make_withdraw(596.21) # pay Chase Freedom
chase_invest_trade.buy_bonds('BNDX', 50) # buy us bond ETF

#----------------------------------------------------------------- 
d=date(2020,7,7)
trader_joes1 = GiftCard(name='TRADER JOES 1', balance=0, cat='Trader Joes')
trader_joes2= GiftCard(name='TRADER JOES 2', balance=0, cat='Trader Joes')
l_gc += [trader_joes1, trader_joes2]
transfer(chase_checking, trader_joes1, 50, factor=1)
transfer(chase_checking, trader_joes2, 50, factor=1)
l_gc.append(heb)

#----------------------------------------------------------------- 
d=date(2020,7,8)
betterment_traditional.balance = 9112.36
transfer(betterment_traditional, betterment_roth_ira, 9112.36, factor=1)
robinhood.add_ETF('VOO', 'SP 500', 15, expense_ratio=0.0003)

names = get_all_broker_buy_names([robinhood, fidelity, chase_invest_trade])
# get static prices 
temp = [n for n in names if n not in prices.keys()]
if temp!=[]:
    print(temp)
    assert temp==[], 'Please update price list'
# get position


#----------------------------------------------------------------- 
d=date(2020,7,9)
transfer(marcus_saving, chase_checking, 20000)

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')

#----------------------------------------------------------------- 
d=date(2020,7,10)
robinhood.add_ETF('VXUS', 'International Stock', 50, expense_ratio=0.0008)
robinhood.buy_ETF('VXUS', 100)
# get detailed position ranked by details 
balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')
#----------------------------------------------------------------- 
d=date(2020,7,11)
uber_eats = GiftCard(name='UBER EATS', balance=0, cat='Uber Eats')
transfer(chase_checking, uber_eats, 24, factor=1.85)
l_gc += [uber_eats]
balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')
#----------------------------------------------------------------- 
d=date(2020,7,13)
robinhood.buy_ETF('VOO', 10)
costco_1_1.balances = 0
costco_1_2.make_withdraw(240) 
usbank_checking.make_withdraw(450) # tree trimming
chase_checking.make_withdraw(242.07) # pay chase freedom
transfer(chase_checking, chase_invest_trade, 20000)

chase_checking.make_withdraw(397.26) # pay Amex Aspire

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')


#----------------------------------------------------------------- 
d=date(2020,7,14)
robinhood.buy_ETF('VOO', 10)


#----------------------------------------------------------------- 
d=date(2020,7,15)
robinhood.add_stocks('LUV', 'Southwest Airline', 20)
robinhood.add_stocks('DAL', 'Delta Airline', 40)
chase_invest_trade.add_ETF('JETS', 'Airline ETF', 300, expense_ratio=0.006)

#update balance 
robinhood.balance = 69107.22
chase_invest_trade.balance = 45675.88
betterment_wealth.balances = 48628
wealthfront.balance = 17126.59

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')
#----------------------------------------------------------------- 
d=date(2020,7,16)
# update bank balance
chase_checking.balance = 10022.41
chase_saving.balance = 331.42
marcus_saving.balance = 7342.59
marcus_cd_4655.balance = 10217.10
marcus_cd_7222.balance = 10221.65
usbank_checking.balance = 2176.93
discover_saving.balance = 19104.04
# update robo balance
betterment_wealth.balance = 48415.25
wealthfront.balance = 17044.49
# update broker balance
chase_invest_trade.balance = 45580.90
robinhood.balance = 68380.74
fidelity.balance = 2448.95

chase_invest_trade.add_ETF('VOO', 'SP 500', 20, expense_ratio=0.0003)


balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')


#----------------------------------------------------------------- 
d=date(2020,7,17)
chase_checking.make_withdraw(403.07) # pay discover

#----------------------------------------------------------------- 
d=date(2020,7,19)
chase_checking.make_withdraw(120.57) # pay chase freedom

#----------------------------------------------------------------- 
d=date(2020,7,20)
yotta = BankAccount(name='YOTTA', balance=0, interest_rate=0.02, month_fee=0)
transfer(chase_checking, yotta, 5000, factor=1)
l_banks.append(yotta)

chase_checking.make_withdraw(1409) # pay Amex


balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')

#----------------------------------------------------------------- 
d=date(2020,7,24)
chase_checking.make_withdraw(93.02) # pay Discover

#----------------------------------------------------------------- 
d=date(2020,7,25)
chase_checking.make_withdraw(95.92) # pay usbank
chase_checking.make_withdraw(326.43) # pay freedom
chase_checking.make_withdraw(359.63) # pay hilton

#----------------------------------------------------------------- 
d=date(2020,7,28)
chase_checking.make_withdraw(537.04) # pay discover
chase_checking.make_withdraw(108.24) # pay freedom
chase_checking.make_withdraw(30.84) # pay target
chase_checking.make_withdraw(41.42) # pay target


#----------------------------------------------------------------- 
d=date(2020,7,29)
chase_checking.make_withdraw(616.05) # pay freedom

#----------------------------------------------------------------- 
d=date(2020,7,30)
chase_invest_trade.add_ETF('VEA', 'International Developed Market', 100, expense_ratio=0.0005)
chase_invest_trade.add_ETF('VWO', 'International Emerging Market', 70, expense_ratio=0.001)
chase_invest_trade.add_bonds('MUB', 'U.S. Municipal Bonds', 14, expense_ratio=0.0007)
chase_invest_trade.add_ETF('VBR', 'U.S. Value Stocks - Small Cap', 10, expense_ratio=0.0007)
chase_invest_trade.add_ETF('VTV', 'U.S. Value Stocks - Large Cap', 10, expense_ratio=0.0004)
chase_invest_trade.add_bonds('EMB', 'International Emerging Market Bonds', 5, expense_ratio=0.0039)
chase_invest_trade.add_bonds('AGG', 'U.S. High Quality Bonds', 4, expense_ratio=0.0004)
chase_invest_trade.add_bonds('VTIP', 'U.S. Inflation-Protected Bonds', 6, expense_ratio=0.0005)
transfer(discover_saving, chase_checking, 10000, factor=1)

 
balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')

#----------------------------------------------------------------- 
d=date(2020,7,31)
transfer(chase_checking, chase_invest_trade, 10000, factor=1)
chase_invest_trade.make_deposit(3158)
robinhood.sell_ETF('SPY', 15)
robinhood.add_ETF('JETS', 'Airline ETF', 300, expense_ratio=0.006)
chase_invest_trade.sell_ETF('JETS', 300)
#TODO: fix bug in balance mismatch

#----------------------------------------------------------------- 
d=date(2020,8,3)
chase_checking.make_withdraw(18.07) # pay freedom
#----------------------------------------------------------------- 
d=date(2020,8,4)
chase_invest_trade.buy_bonds('EMB', 6)
chase_invest_trade.buy_bonds('MUB', 9)
chase_invest_trade.buy_bonds('AGG', 2)
chase_invest_trade.buy_bonds('VTIP', 3)
chase_invest_trade.buy_ETF('VWO', 42)
chase_invest_trade.buy_ETF('VEA', 91)
chase_invest_trade.buy_ETF('VBR', 7)
chase_invest_trade.add_ETF('VOE', 'U.S. Value Stocks - Mid Cap', 22, expense_ratio=0.0007)
chase_invest_trade.buy_ETF('VTV', 16)
chase_invest_trade.add_ETF('VTI', 'U.S. Total Stock Market', 50, expense_ratio=0.0003)
chase_invest_trade.sell_bonds('BNDX', 29)
chase_invest_trade.buy_ETF('VTI', 12)
transfer(marcus_saving, chase_checking, 7000, factor=1)
transfer(discover_saving, chase_checking, 8000, factor=1)
transfer(betterment_wealth, chase_checking, 20000, factor=1)

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')

#----------------------------------------------------------------- 
d=date(2020,8,5)
transfer(chase_checking, chase_invest_trade, 15000, factor=1)
chase_invest_trade.buy_bonds('EMB', 4)
chase_invest_trade.buy_bonds('MUB', 9)
chase_invest_trade.buy_bonds('AGG', 3)
chase_invest_trade.buy_bonds('VTIP', 4)
chase_invest_trade.buy_ETF('VTI', 25)
chase_invest_trade.buy_ETF('VTV', 11)
chase_invest_trade.buy_ETF('VOE', 9)
chase_invest_trade.buy_ETF('VBR', 7)
chase_invest_trade.buy_ETF('VEA', 72)
chase_invest_trade.buy_ETF('VWO', 43)
chase_invest_trade.buy_bonds('BND', 10)

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')

#----------------------------------------------------------------- 
d=date(2020,8,10)
transfer(chase_checking, chase_invest_trade, 20000, factor=1)

#----------------------------------------------------------------- 
d=date(2020,8,17)
chase_checking.make_withdraw(34.41) # pay discover
chase_checking.make_withdraw(173.18) # pay csp
chase_invest_trade.buy_bonds('EMB', 6)
chase_invest_trade.buy_bonds('MUB', 12)
chase_invest_trade.buy_bonds('AGG', 3)
chase_invest_trade.buy_bonds('VTIP', 5)
chase_invest_trade.buy_ETF('VTI', 33)
chase_invest_trade.buy_ETF('VTV', 14)
chase_invest_trade.buy_ETF('VOE', 12)
chase_invest_trade.buy_ETF('VBR', 9)
chase_invest_trade.buy_ETF('VEA', 97)
chase_invest_trade.buy_ETF('VWO', 59)
chase_invest_trade.buy_bonds('BND', 10)
chase_invest_trade.buy_bonds('BNDX', 21)

#----------------------------------------------------------------- 
d=date(2020,8,22)
chase_checking.make_withdraw(116.32) # pay freedom
chase_checking.make_withdraw(0.99) # pay csp

#----------------------------------------------------------------- 
d=date(2020,8,23)
chase_checking.make_withdraw(531.99) # pay discover
chase_checking.make_deposit(3158.74)
chase_checking.make_deposit(3158.74)

#----------------------------------------------------------------- 
d=date(2020,8,26)
chase_checking.make_withdraw(597.81) # pay amex
chase_checking.make_withdraw(28.90) # pay usbank

#----------------------------------------------------------------- 
d=date(2020,9,2)
chase_checking.make_withdraw(45.44) # pay chase

transfer(marcus_cd_4655, chase_checking, 10217.1, factor=1)
#----------------------------------------------------------------- 
d=date(2020,9,5)
chase_checking.make_withdraw(45.44) # pay chase

moomoo = BrokerAccount(name='MooMoo', balance=0, interest_rate=0.015)
moomoo.restriction = 'able to Da Xin'
transfer(chase_checking, moomoo, 1510, factor=1)
l_brokers.append(moomoo)
#----------------------------------------------------------------- 
d=date(2020,9,6)
chase_checking.make_withdraw(21.62) # pay discover
chase_checking.make_withdraw(36.92) # pay chase
chase_checking.make_withdraw(44.5) # pay citi
chase_checking.make_withdraw(181.34) # pay usbank
chase_checking.make_withdraw(51.92) # pay usbank


#----------------------------------------------------------------- 
d=date(2020,9,8)
robinhood.buy_ETF('JETS', 30)
transfer(chase_checking, robinhood, 1000, factor=1)

#----------------------------------------------------------------- 
d=date(2020,9,12)
nordstrom_digit = GiftCard(name='NORDSTROM 2359', balance=25.0, cat='Nordstrom')
nordstrom_digit.code = ('6168437045462359', '36425819')
nordstrom_digit.balance = 0

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')

#----------------------------------------------------------------- 
d=date(2020,9,13)
chase_checking.make_withdraw(1201.75) # pay west elm

#----------------------------------------------------------------- 
d=date(2020,9,16)
chase_checking.make_withdraw(50.25) # pay usbank


#----------------------------------------------------------------- 
d=date(2020,9,19)
chase_checking.make_withdraw(103.93) # pay amex
chase_checking.make_withdraw(18.96) # pay csp

#----------------------------------------------------------------- 
d=date(2020,9,24)
chase_checking.make_withdraw(6.24) # pay amex
nordstrom_digit = GiftCard(name='NORDSTROM 3178', balance=25.0, cat='Nordstrom')
nordstrom_digit.code = ('6168437062723178', '54470555')
nordstrom_digit.balance = 0

#----------------------------------------------------------------- 
d=date(2020,9,28)
chase_checking.make_withdraw(60.85) # pay chase freedom
nordstrom_digit = GiftCard(name='NORDSTROM 3178', balance=25.0, cat='Nordstrom')
nordstrom_digit.code = ('6168437069088110', '19599515')
nordstrom_digit.balance = 16.32

#----------------------------------------------------------------- 
d=date(2020,10,11)
chase_checking.make_withdraw(36.69) # pay discover
chase_checking.make_withdraw(42.80) # pay freedom
chase_checking.make_withdraw(192.79) # pay hilton
chase_checking.make_withdraw(12.98) # pay citi double cash
chase_checking.make_withdraw(96.67) # pay usbank

#----------------------------------------------------------------- 
d=date(2020,10,17)
nordstrom_digit = GiftCard(name='NORDSTROM 3178', balance=100.0, cat='Nordstrom')
nordstrom_digit.code = ('6168 4371 0333 4795', '44793051')
# gc by categories

#----------------------------------------------------------------- 
d=date(2020,10,24)
chase_checking.make_withdraw(50.25) # pay usbank
chase_checking.make_withdraw(5.22) # pay freedom
chase_checking.make_withdraw(79.99) # pay amex white
chase_checking.make_withdraw(307.0) # pay citi double cash
chase_checking.make_withdraw(73.88) # pay amex hilton

#----------------------------------------------------------------- 
d=date(2020,11,8)
chase_checking.make_withdraw(85.28) # pay usbank
chase_checking.make_withdraw(129.82) # pay freedom
chase_checking.make_withdraw(89.91) # pay discover
chase_checking.make_withdraw(4.99) # pay amex hilton

#----------------------------------------------------------------- 
# balance correction day
d=date(2020,11,14)

# balances
chase_checking.balance = 28614.64
chase_saving.balance = 331.42
marcus_cd_7222.balance = 10269.37
marcus_saving.balance = 355.45
usbank_checking.balance = 1791.38
discover_saving.balance = 1122.16
betterment_cash.balance = 24.66
yotta.balance = 5035.34
robinhood.balance = 86134.6
chase_invest_trade.balance = 95864.27

# interest
capital_one.interest_rate = 0.004
yotta.interest_rate = 0.005
betterment_cash.interest_rate = 0.004
marcus_saving.interest_rate = 0.006
marcus_cd_7222.interest_rate = 0.007
discover_saving.interest_rate = 0.0055

# robinhood stocks
robinhood.sell_stocks("AAPL", 5)
robinhood.buy_stocks("BABA", 3)
robinhood.buy_stocks("LUV", 10)
robinhood.buy_stocks("DAL", 10)
robinhood.buy_stocks("TSLA", 4)
robinhood.sell_ETF("JETS", 30)

# chase stock 
chase_invest_trade.buy_ETF("VTI", 0.47)
chase_invest_trade.buy_ETF("VEA", 1.98)
chase_invest_trade.buy_ETF("VWO", 2.17)
chase_invest_trade.buy_ETF("VTV", 0.35)
chase_invest_trade.buy_ETF("VOE", 0.27)
chase_invest_trade.sell_ETF("VOO", 20)
chase_invest_trade.buy_ETF("VBR", 0.19)

chase_invest_trade.sell_bonds("BND", 8.91)
chase_invest_trade.buy_bonds("BNDX", 0.46)
chase_invest_trade.buy_bonds("MUB", 0.25)
chase_invest_trade.buy_bonds("EMB", 0.22)
chase_invest_trade.buy_bonds("AGG", 0.07)

# robo advisor 
betterment_wealth.balance = 32042.59
wealthfront.balance = 18684.10

# broker account, reset cash and balance
robinhood.cash = 2993.83
robinhood.balance = robinhood.get_balance(prices)
chase_invest_trade.cash = 154.89
chase_invest_trade.balance = chase_invest_trade.get_balance(prices)

# pay card 
chase_checking.make_withdraw(155.25) # pay usbank
chase_checking.make_withdraw(19.88) # pay discover

# transfer
transfer(betterment_wealth, chase_checking, 20000, factor=1)
transfer(chase_checking, chase_invest_trade, 20000, factor=1)

# transfer to cqm
chase_checking.make_withdraw(887.0)


balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')

#----------------------------------------------------------------- 
d=date(2020,11,17)
robinhood.add_ETF(ID='LIT', number=50, full_name='Lithum ETF', expense_ratio=0.0075)

fidelity_roth_ira = BrokerAccount(name='FIDELITY ROTH IRA', balance=0, interest_rate=0.03)
fidelity_traditional = BrokerAccount(name='FIDELITY TRA IRA', balance=0, interest_rate=0.03)

#----------------------------------------------------------------- 
d=date(2020,11,23)
chase_checking.make_withdraw(205.65) # pay discover

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')

#----------------------------------------------------------------- 
d=date(2020,11,24)
robinhood.sell_stocks("DAL", 30)
robinhood.sell_stocks("LUV", 20)
robinhood.buy_ETF('LIT', 30)

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')

#----------------------------------------------------------------- 
d=date(2020,11,27)
chase_checking.make_withdraw(31.37) # pay chase

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')


#----------------------------------------------------------------- 
d=date(2020,11,29)
chase_checking.make_withdraw(200.81) # pay citi

bbb1 = GiftCard(name='BED BATH AND BEYOND 5144', balance=145.0, cat='bbb')
bbb1.code = ('6189988221855144', '41433819')

bbb1 = GiftCard(name='BED BATH AND BEYOND 5144', balance=105.0, cat='bbb')
bbb1.code = ('6189988221949802', '60488080')

robinhood.balance = robinhood.get_balance(prices)
robinhood.cash = 1050.3



chase_invest_trade.balance = chase_invest_trade.get_balance(prices)
chase_invest_trade.cash = 20154.3

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')


#----------------------------------------------------------------- 
d=date(2020,11,30)
chase_invest_trade.buy_bonds('BND', 49)
chase_invest_trade.balance = chase_invest_trade.get_balance(prices)
chase_invest_trade.cash = 15822.8

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')

#----------------------------------------------------------------- 
d=date(2020,12,5)
chase_checking.make_withdraw(686.44) # pay chase
usbank_checking.make_withdraw(85.28) # pay usbank
usbank_checking.make_withdraw(7.99) # pay amex
chase_checking.make_withdraw(415.69) # pay discover

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')

#----------------------------------------------------------------- 
d=date(2020,12,7)

chase_invest_trade.buy_ETF('VTI', 3)
chase_invest_trade.buy_ETF('VTV', 1)
chase_invest_trade.buy_ETF('VOE', 1)
chase_invest_trade.buy_ETF('VBR', 1)
chase_invest_trade.buy_ETF('VEA', 9)
chase_invest_trade.buy_ETF('VWO', 5)
chase_invest_trade.buy_bonds('VTIP', 1)
chase_invest_trade.buy_bonds('MUB', 1)
chase_invest_trade.buy_bonds('BNDX', 2)
chase_invest_trade.buy_bonds('EMB', 1)

chase_invest_trade.balance = chase_invest_trade.get_balance(prices)
chase_invest_trade.cash = 13921.99

transfer(chase_checking, usbank_checking, 2000, factor=1)

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')



#----------------------------------------------------------------- 
d=date(2020,12,7)
transfer(chase_checking, usbank_checking, 500, factor=1)

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')


#----------------------------------------------------------------- 
d=date(2020,12,10)

madewell = GiftCard(name='MADEWELL', balance=25.0, cat='madewell')
madewell.code = ('6006493863022456087', '5700')

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')


#----------------------------------------------------------------- 
d=date(2020,12,12)

chase_checking.make_withdraw(61.65) # pay chase
chase_checking.make_withdraw(18.0) # pay seed
chase_checking.make_withdraw(50.25) # pay usbank
chase_checking.make_withdraw(211.85) # pay discover
chase_checking.make_withdraw(5.44) # pay citi

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')


#----------------------------------------------------------------- 
d=date(2020,12,15)

usbank_checking.make_withdraw(2528.0) # special contribution

#----------------------------------------------------------------- 
d=date(2020,12,18)

chase_checking.make_withdraw(20.57) # pay chase

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')

#----------------------------------------------------------------- 
d=date(2020,12,21)

# banks
chase_checking.balance = 30415.26
marcus_saving.balance = 355.61
marcus_cd_7222.balance = 10275.26
usbank_checking.balance = 184.01
discover_saving.balance = 1122.67
yotta.balance = 5060.88

# brokers balance 
chase_invest_trade.cash = 13921.99
chase_invest_trade.balance = chase_invest_trade.get_balance(prices)
chase_invest_trade.sell_bonds('EMB', 22.22-21.29)

robinhood.cash = 1149.78
robinhood.balance = robinhood.get_balance(prices)

fidelity.cash = 0.0
fidelity.balance = fidelity.get_balance(prices)
fidelity.buy_MMF('SPAXX', 29.81-9.2)

moomoo.cash = 1602.41

# robot balance
betterment_wealth.balance = 12700.48
wealthfront.balance = 19545.24

transfer(chase_checking, fidelity, 10000, factor=1)
fidelity.add_bonds('FXNAX', 'US Bond', 322.061, expense_ratio=0.00025)


balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')

#----------------------------------------------------------------- 
d=date(2020,12,21)
robinhood.buy_stocks('BABA', 3)
transfer(chase_checking, robinhood, 2000, factor=1)

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')


#----------------------------------------------------------------- 
d=date(2020,12,26)
chase_checking.make_withdraw(124.43) # pay discover
chase_checking.make_withdraw(11.7) # pay citi

balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')

#----------------------------------------------------------------- 
d=date(2020,12,28)
chase_invest_trade.sell_bonds('BND', 50)
chase_invest_trade.sell_bonds('BNDX', 20)

chase_invest_trade.buy_ETF('VTI', 4)
chase_invest_trade.buy_ETF('VEA', 14.3)
chase_invest_trade.buy_ETF('VTV', 2)
chase_invest_trade.buy_ETF('VOE', 1)
chase_invest_trade.buy_ETF('VBR', 1)
chase_invest_trade.buy_ETF('VWO', 7)
chase_invest_trade.buy_bonds('VTIP', 1)
chase_invest_trade.buy_bonds('MUB', 2)
chase_invest_trade.buy_bonds('EMB', 1)
robinhood.buy_stocks('BABA', 5)

fidelity.buy_bonds('FXNAX', 362.03)

etrade =  BrokerAccount(name='E_TRADER', balance=0, interest_rate=0.03)
l_brokers.append(etrade)
transfer(chase_checking, etrade, 15000, factor=1)

chase_invest_trade.cash = 16949
fidelity.balance = fidelity.get_balance(prices)
robinhood.balance = robinhood.get_balance(prices)
chase_invest_trade.balance = chase_invest_trade.get_balance(prices)

transfer(chase_invest_trade, chase_checking, 10000, factor=1)


balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')

#----------------------------------------------------------------- 
d=date(2020,12,28)
robinhood.sell_ETF('VTI', 56)
robinhood.balance = robinhood.get_balance(prices)


balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')

#----------------------------------------------------------------- 
d=date(2021,1,1)
chase_checking.make_withdraw(13.38) # pay discover
chase_checking.make_withdraw(67.83) # pay united chase
transfer(chase_checking, fidelity_traditional, 6000, factor=1)
chase_checking.make_deposit(3517.36)

robinhood.cash = 12409.01
robinhood.balance = robinhood.get_balance(prices)

chase_invest_trade.cash = 6956.18
chase_invest_trade.balance = chase_invest_trade.get_balance(prices)

fidelity.cash = 1541.55
fidelity.balance = fidelity.get_balance(prices)


balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')

#----------------------------------------------------------------- 
d=date(2021,1,4)
etrade.add_ETF(ID='SPY', number=5, full_name='', expense_ratio=0.0009)
etrade.cash = 13132.59
etrade.balance = etrade.get_balance(prices)
chase_checking.make_withdraw(17.64)


balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
_ = write_balance(balances)
balances = output_balance_gc(l_gc, d=d)
_ = write_balance(balances, filename='gc_balance.csv')


#----------------------------------------------------------------- 
d=date(2021,1,5)
robinhood.add_stocks('CRM', 'Saleforce', 20)
etrade.buy_ETF('SPY', 5)
robinhood.cash = 8019.21
etrade.cash = 11276.99
robinhood.balance = robinhood.get_balance(prices)
etrade.balance = etrade.get_balance(prices)


#----------------------------------------------------------------- 
d=date(2021,1,6)
etrade.buy_ETF('SPY', 5)
etrade.cash = 9369.0
etrade.balance = etrade.get_balance(prices)



#----------------------------------------------------------------- 
d=date(2021,1,7)
etrade.buy_ETF('SPY', 5)
etrade.cash = 7511.31
etrade.balance = etrade.get_balance(prices)

# correct balance
chase_checking.balance = 10813.97
chase_checking.make_withdraw(176.13) # pay united
chase_checking.make_withdraw(17.30) # pay discover
chase_checking.make_withdraw(62.51) # pay usbank

chase_invest_trade.buy_ETF('VTI', 127.97-127.47)
chase_invest_trade.buy_bonds('BND', 161.13-160.09)
chase_invest_trade.buy_ETF('VWO', 229.53-228.17)
chase_invest_trade.buy_bonds('BNDX', 124.91-124.46)
chase_invest_trade.buy_ETF('VTV', 54.7-54.35)
chase_invest_trade.buy_ETF('VOE', 45.55-45.27)
chase_invest_trade.buy_ETF('VBR', 35.4-35.19)
chase_invest_trade.buy_bonds('MUB', 47.4-47.25)
chase_invest_trade.buy_bonds('EMB', 22.37-22.29)
chase_invest_trade.buy_bonds('AGG', 12.10-12.07)

chase_invest_trade.balance = chase_invest_trade.get_balance(prices)
robinhood.balance = robinhood.get_balance(prices)

fidelity.buy_bonds('FXNAX', 684.344-684.09)
fidelity.balance = fidelity.get_balance(prices)

etrade.balance = etrade.get_balance(prices)


balances = output_balance(l_brokers, l_robos, l_banks, prices, d=d)
merge_bank_logs(balances)
balances = output_balance_gc(l_gc, d=d)
merge_gc_logs(balances)



# 策略
#1. 往etrade里面转6000
#2. robinhood买600 VTI 5天
#3. etrader买600 SPY 5天

# buy BNDX in fidelity 

# gc by categories 

# act restrictions
# act expiration
# alert
# cat 
# annual fee

# sell chase MMF and fidelity MMF



# todo: add show growth
# todo: add cash reserve (buying power)
# todo: add IRS and 401K account 
# todo: add webull
# todo: sell all SPY and buy VOO
# todo: see what's going on with ira
# todo: see beveldere pop up correct or not 
# todo: see if I received costco card
print('Done')