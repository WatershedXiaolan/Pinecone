
from datetime import date
from datetime import timedelta
import calendar
import numpy as np
import scipy.stats
import time
import pickle
from yahoo_fin import stock_info as si
import pandas as pd


class Account:
    """
    This is the abstract account object.
    It allows set balance, check balance, withdraw, and
    make deposit.
    """

    def __init__(self, name, balance):
        self.name = name
        self._balance = balance
        self._restriction = None

    @property
    def restriction(self):
        """get restriction"""
        # print('Getting restrictions...')
        return self._restriction

    @restriction.setter
    def restriction(self, words):
        """set restriction"""
        # print('Setting restrictions...')
        self._restriction = words
        # print('restrictions: {}'.format(words))

    @property
    def balance(self):
        """get balance"""
        # print('Getting Balance...')
        # time.sleep(0.5)
        return self._balance

    @balance.setter
    def balance(self, value):
        """set balance"""
        self._balance = value

    def make_deposit(self, value):
        """make a deposite from account"""
        assert value > 0, 'Please make a positive deposit'
        # print('Making Deposit...')
        # time.sleep(0.5)
        self._balance += value
        self._balance = round(self._balance, 2)
        # print('You made a deposit of {0}. Current balance is {1}' \
        # .format(value, self._balance))

    def make_withdraw(self, value):
        """make a withdraw from account"""
        assert value > 0, 'Please make a positive withdraw'
        assert self._balance >= value, \
            "You don't have enough to make a valid withdraw"
        # print('Making Withdraw...')
        # time.sleep(0.5)
        self._balance -= value
        self._balance = round(self._balance, 2)
        # print('You made a withdraw of {0}. Current balance is {1}' \
        # .format(value, self._balance))


class MoneyAccount(Account):
    """
    This is the money account abstract object.
    It allows set balance, check balance, withdraw, and
    make deposit. It should also allows a future forcast
    which takes interest and months
    for forcast, and return the estimated value forward.
    """
    def __init__(self, name, balance, interest_rate=0,
                 month_fee=0, annual_pct_fee=0.0, min_amount=0):
        Account.__init__(self, name, balance)
        self._month_fee = month_fee
        self._annual_pct_fee = annual_pct_fee
        self._interest_rate = interest_rate
        self._alert = {}
        self._min_amount = min_amount

    @property
    def monthly_fee(self):
        """get monthly fee"""
        # print('Getting monthly fee...')
        # time.sleep(0.5)
        return self._month_fee

    @monthly_fee.setter
    def monthly_fee(self, fee):
        """set monthly fee"""
        # print('Setting monthly fee...')
        # time.sleep(0.5)
        self._month_fee = fee
        # print('monthly fee is {}'.format(fee))

    @property
    def min_amount(self):
        """get minimum amount"""
        # print('Getting minimum amount...')
        # time.sleep(0.5)
        return self._min_amount

    @min_amount.setter
    def min_amount(self, m):
        """set minimum amount"""
        # print('Setting minimum amount...')
        # time.sleep(0.5)
        self._min_amount = m
        # print('minimum amount is {}'.format(m))

    def add_alert(self, alert):
        assert len(alert) == 2, 'please add a valid alert with len(alert=2)'
        assert isinstance(alert[0], date), 'please provide a date'
        self._alert[alert[0]] = alert[1]

    def get_alert(self, verbose=False):
        if verbose:
            for item in self._alert.items():
                print('{}: {}'.format(item[0], item[1]))
        return self._alert

    def remove_alert(self, key):
        if key in self._alert:
            temp = self._alert.pop(key)
            print('Alert removed: {}, {}'.format(key, temp))
        else:
            print('Nothing to remove')

    @property
    def annual_pct_fee(self):
        """get annual percentage fee"""
        # print('Getting annual percentage fee...')
        # time.sleep(0.5)
        return self._annual_pct_fee

    @annual_pct_fee.setter
    def annual_pct_fee(self, fee):
        """set annual percentage fee"""
        # print('Setting annual percentage fee...')
        # time.sleep(0.5)
        self._annual_pct_fee = fee
        # print('annual percentage fee is {}%'.format(fee*100))

    @property
    def interest_rate(self):
        """get interest rate"""
        # print('Getting interest rate...')
        # time.sleep(0.5)
        return self._interest_rate

    @interest_rate.setter
    def interest_rate(self, interest_rate):
        """set interest rate"""
        # print('Setting interest rate...')
        # time.sleep(0.5)
        self._interest_rate = interest_rate
        # print('interest rate. is {}%'.format(interest_rate*100))

    def allocable_mount(self):
        """get allocatable amount without violating minimum balance"""
        ret = round(self._balance - self._min_amount, 2)
        # print('Allocable amount is {}'.format(ret))
        return ret

    def forcast(self, interest_rate=None,
                months=0, verbose=True, d=date.today()):
        """
        return future values given current value, inttest rate and time period
        """
        if verbose:
            print('You have {0} as of {1}'.format(self._balance, d))
        if not interest_rate:
            interest_rate = self._interest_rate

        monthly_rate = interest_rate/12 + 1 - self._annual_pct_fee/12
        ret = round(self._balance*(monthly_rate)**months, 2)
        future_date = self.add_months(d, months)
        if verbose:
            # time.sleep(0.5)
            print("You will have {0} as of {1}".format(ret, future_date))
        return ret, future_date

    def forcast_guassian(self, mu_int=None, std_int=0, months=0,
                         verbose=True, d=date.today()):
        """
        forcast future value with uncertainty under gaussian process
        """
        if verbose:
            print('You have {0} as of {1}'.format(self._balance, d))
        if not mu_int:
            mu_int = self._interest_rate
        mu_int -= self._annual_pct_fee

        ints = np.random.normal(mu_int/12+1, std_int, months)
        ints[ints < 1] = 1
        ret = self._balance
        for i in ints:
            ret *= i
        ret = round(ret, 2)
        future_date = self.add_months(d, months)
        if verbose:
            # time.sleep(0.5)
            print("You will have {0} as of {1}".format(ret, future_date))
        return ret, future_date

    def forcast_monte_carlo(self, mu_int=0, std_int=0, months=0, num_run=1000,
                            verbose=False, d=date.today()):
        """run uncertainty forcast multiple times"""

        assert num_run >= 3, 'not enough data to give confidence interval'
        print('Running Monte Carlo for {} times'.format(num_run))
        if not mu_int:
            mu_int = self._interest_rate
        mu_int -= self._annual_pct_fee
        rets = [self.forcast_guassian(mu_int=mu_int, std_int=std_int,
                months=months, verbose=verbose)[0] for i in range(num_run)]
        m, m_d, m_u = self.mean_confidence_interval(rets, confidence=0.95)
        m, m_d, m_u = [round(i, 2) for i in [m, m_d, m_u]]
        h = round(m_u-m, 2)
        future_date = self.add_months(d, months)
        # time.sleep(0.5)
        print('You will have on average {0} as of {1}, \
              with a confidence interval of {2}'.format(m, future_date, h))
        return m, m_d, m_u

    @staticmethod
    def mean_confidence_interval(data, confidence=0.95):
        """calculate confidence interval"""
        assert isinstance(data, np.ndarray) or isinstance(data, list)
        a = 1.0 * np.array(data)
        n = len(a)
        assert n >= 3, 'not enough data to give confidence interval'
        m, se = np.mean(a), scipy.stats.sem(a)
        h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
        return m, m-h, m+h

    @staticmethod
    def add_months(sourcedate, months):
        """add months to current date"""
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month // 12
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year, month)[1])
        return date(year, month, day)


class BankAccount(MoneyAccount):
    def __init__(self, name, balance, interest_rate=0,
                 month_fee=0, min_amount=0):
        MoneyAccount.__init__(self, name, balance,
                              interest_rate=interest_rate,
                              min_amount=min_amount)
        self._month_fee = month_fee
        self._alert = {}

    @property
    def monthly_fee(self):
        """get monthly fee"""
        # print('Getting monthly fee...')
        # time.sleep(0.5)
        return self._month_fee

    @monthly_fee.setter
    def monthly_fee(self, fee):
        """set monthly fee"""
        # print('Setting monthly fee...')
        # time.sleep(0.5)
        self._month_fee = fee
        # print('monthly fee is {}'.format(fee))


class RoboAccount(MoneyAccount):
    def __init__(self, name, balance, interest_rate=0,
                 annual_pct_fee=0.0, min_amount=0):
        MoneyAccount.__init__(self, name, balance,
                              interest_rate=interest_rate,
                              min_amount=min_amount)
        self._annual_pct_fee = annual_pct_fee
        self._alert = {}
        self._stock_ratio = 0.5

    @property
    def annual_pct_fee(self):
        """get annual percentage fee"""
        return self._annual_pct_fee

    @annual_pct_fee.setter
    def annual_pct_fee(self, fee):
        """set annual percentage fee"""
        self._annual_pct_fee = fee

    @property
    def stock_ratio(self):
        """get stock ratio"""
        return self._stock_ratio

    @stock_ratio.setter
    def stock_ratio(self, r):
        """set stock ratio"""
        self._stock_ratio = r


class BrokerAccount(MoneyAccount):
    def __init__(self, name, balance,
                 interest_rate=0, min_amount=0, d=date.today()):
        MoneyAccount.__init__(self, name, balance,
                              interest_rate=interest_rate,
                              min_amount=min_amount)
        self._alert = {}
        self._stocks = {}
        self._etfs = {}
        self._bonds = {}
        self._mmf = {}
        self._d = d
        self._cash = self.balance

    def get_balance(self, prices):
        """only for broker acct
        calculate current balance from all positions"""
        blc = 0
        blc += sum([prices[k]*v[1] for k, v in self.get_stocks().items()])
        blc += sum([prices[k]*v[1] for k, v in self.get_ETF().items()])
        blc += sum([prices[k]*v[1] for k, v in self.get_bonds().items()])
        blc += sum([prices[k]*v[1] for k, v in self.get_MMF().items()])
        blc += self._cash
        return blc

    def get_past_balance(self,
                         d,
                         h_prices_path=('/Users/xiaolan/Documents'
                                        '/repos/FinProject/local_src'
                                        '/historical_prices.csv')):

        """
        only for broker acct
        calculate past balance from all positions
        given a historical price sheet
        TODO: if the price at a certain date is not available, update the date 
        """
        # proposed order

        # 1. get historical price
        # 2. get all tickers
        # 3. go through the historical price.
        # 3-1. if price not available: get price and update price list
        # 4. calculate balance
        # 5. update price set if needed

        h_prices = pd.read_csv(h_prices_path)

        blc = 0
        prices = h_prices[h_prices.date == d.strftime("%Y-%m-%d")]
        available_tickers = prices.ticker.tolist()
        num_h_prices_entries = h_prices.shape[0]

        for ticker, params in self.get_MMF().items():
            position = params[1]
            blc += position

        for get_p in [self.get_stocks,
                      self.get_ETF,
                      self.get_bonds]:

            for ticker, params in get_p().items():
                position = params[1]
                if position != 0:
                    if ticker in available_tickers:
                        price = prices[prices.ticker == ticker].price.values[0]
                    else:
                        # TODO: add read price and update
                        # historical price database
                        dateback = 0
                        while True:
                            try:
                                new_price = si.get_data(ticker.lower(),
                                                        start_date=d+timedelta(days=0-dateback),
                                                        end_date=d+timedelta(days=1-dateback)
                                                        )
                                break
                            except KeyError:
                                dateback += 1

                        new_price['price'] = (new_price['open']
                                              + new_price['close'])/2
                        new_price = new_price[['ticker', 'price']] \
                            .reset_index().rename(columns={'index': 'date'})
                        new_price.date = d.strftime("%Y-%m-%d")
                        h_prices = pd.concat([h_prices, new_price], axis=0,
                                             sort=False).fillna(0).reset_index(drop=True)

                        price = new_price.price.values[0]

                    blc += position * price

        if num_h_prices_entries != h_prices.shape[0]:
            h_prices.to_csv(h_prices_path, index=False)
        blc += self._cash
        return round(blc, 2)

    def make_deposit(self, value):
        """adapt from base class
        add fund to the cash part"""
        assert value > 0, 'Please make a positive deposit'
        self._balance += value
        self._balance = round(self._balance, 2)
        self._cash += value
        self._cash = round(self._cash, 2)

    def make_withdraw(self, value):
        """adapt from base class
        withdraw fund from the cash part"""
        assert value > 0, 'Please make a positive withdraw'
        assert self._cash >= value, \
               "You don't have enough to make a valid withdraw"
        assert self._balance >= value, \
               "You don't have enough to make a valid withdraw"

        self._balance -= value
        self._balance = round(self._balance, 2)
        self._cash -= value
        self._cash = round(self._cash, 2)

    @property
    def d(self):
        return self._d

    @d.setter
    def d(self, d):
        self._d = d

    @property
    def cash(self):
        return self._cash

    @cash.setter
    def cash(self, cash):
        self._cash = cash

    def get_all_names(self):
        l_stocks = list(self.get_stocks().keys())
        l_ETF = list(self.get_ETF().keys())
        l_MMF = list(self.get_MMF().keys())
        l_bonds = list(self.get_bonds().keys())
        return l_stocks + l_ETF + l_MMF + l_bonds

    def add_stocks(self, ID, full_name, number):
        """
        NOTE: this method will NOT update cash position
        if want to update cash, please use buy_stocks following
        this function, and set number=0 in this function
        """
        self._stocks[ID] = (full_name, number)

    def get_stocks(self):
        return self._stocks

    def buy_stocks(self, ID, number):
        assert ID in self._stocks, 'please use add_stocks instead'
        self._stocks[ID] = (self._stocks[ID][0], self._stocks[ID][1]+number)

    def sell_stocks(self, ID, number):
        assert ID in self._stocks, 'please purchase stock first'
        current = self._stocks[ID][1]
        assert current >= number, 'not enough stocks to sell'
        self._stocks[ID] = (self._stocks[ID][0], self._stocks[ID][1]-number)

    def add_ETF(self, ID, full_name, number, expense_ratio):
        self._etfs[ID] = (full_name, number, expense_ratio)

    def get_ETF(self):
        return self._etfs

    def buy_ETF(self, ID, number):
        assert ID in self._etfs, 'please use add_stocks instead'
        self._etfs[ID] = (self._etfs[ID][0], self._etfs[ID][1]+number,
                          self._etfs[ID][2])

    def sell_ETF(self, ID, number):
        assert ID in self._etfs, 'please purchase stock first'
        current = self._etfs[ID][1]
        assert current >= number, 'not enough stocks to sell'
        self._etfs[ID] = (self._etfs[ID][0], self._etfs[ID][1]-number,
                          self._etfs[ID][2])

    def buy_sell_auto(self, code, number, price, category, action):
        """
        Base function for buying or selling anything.
        categories = ['ETF', 'Stock', 'MMF', 'Bond']
        It will:
        1. update inventories by adding <number> of entity
        2. read the current or historical price when this transaction happens
        3. update cash -= number * price
        """

        # 0. check if category and action are supported
        assert category in ['ETF', 'Stock', 'MMF', 'Bond'], \
            'please provide a valid category. \
             ETF, Stock, MMF and Bond are supported.'
        assert action in ['buy', 'sell'], \
            'please provide a valid action. \
             buy and sell are supported.'
        # 1. update inventory
        switcher = {
            'ETF_buy': self.buy_ETF,
            'Stock_buy': self.buy_stocks,
            'MMF_buy': self.buy_MMF,
            'Bond_buy': self.buy_bonds,
            'ETF_sell': self.sell_ETF,
            'Stock_sell': self.sell_stocks,
            'MMF_sell': self.sell_MMF,
            'Bond_sell': self.sell_bonds
        }

        trans_function = switcher.get(category+'_'+action, '')
        trans_function(code, number)

        # 2. read the current price.
        # price = si.get_live_price(code.lower())
        if action == 'sell':
            price *= -1

        # 3. update cash -= number * price
        self.cash -= price * number

    def buy_ETF_auto(self, code, number, price):
        self.buy_sell_auto(code, number, price, category='ETF', action='buy')

    def buy_stock_auto(self, code, number, price):
        self.buy_sell_auto(code, number, price, category='Stock', action='buy')

    def buy_MMF_auto(self, code, number, price):
        self.buy_sell_auto(code, number, price, category='MMF', action='buy')

    def buy_bond_auto(self, code, number, price):
        self.buy_sell_auto(code, number, price, category='Bond', action='buy')

    def sell_ETF_auto(self, code, number, price):
        self.buy_sell_auto(code, number, price, category='ETF', action='sell')

    def sell_stock_auto(self, code, number, price):
        self.buy_sell_auto(code, number, price, category='Stock', action='sell')

    def sell_MMF_auto(self, code, number, price):
        self.buy_sell_auto(code, number, price, category='MMF', action='sell')

    def sell_bond_auto(self, code, number, price):
        self.buy_sell_auto(code, number, price, category='Bond', action='sell')

    def add_MMF(self, ID, full_name, number, expense_ratio):
        self._mmf[ID] = (full_name, number, expense_ratio)

    def get_MMF(self):
        return self._mmf

    def buy_MMF(self, ID, number):
        assert ID in self._mmf, 'please use add_stocks instead'
        self._mmf[ID] = (self._mmf[ID][0],
                         self._mmf[ID][1]+number,
                         self._mmf[ID][2])

    def sell_MMF(self, ID, number):
        assert ID in self._mmf, 'please purchase stock first'
        current = self._mmf[ID][1]
        assert current >= number, 'not enough stocks to sell'
        self._mmf[ID] = (self._mmf[ID][0],
                         self._mmf[ID][1]-number, self._mmf[ID][2])

    def add_bonds(self, ID, full_name, number, expense_ratio):
        self._bonds[ID] = (full_name, number, expense_ratio)

    def get_bonds(self):
        return self._bonds

    def buy_bonds(self, ID, number):
        assert ID in self._bonds, 'please use add_stocks instead'
        self._bonds[ID] = (self._bonds[ID][0],
                           self._bonds[ID][1]+number,
                           self._bonds[ID][2])

    def sell_bonds(self, ID, number):
        assert ID in self._bonds, 'please purchase stock first'
        current = self._bonds[ID][1]
        assert current >= number, 'not enough stocks to sell'
        self._bonds[ID] = (self._bonds[ID][0],
                           self._bonds[ID][1]-number,
                           self._bonds[ID][2])

    def get_position(self, ID):
        """
        return total amount of a stock/etf/bond
        and its pct position in porfolio
        """
        assert ID in self._stocks or ID in self._etfs or ID in self._bonds
        merged = self._stocks.update(self._bonds).update(self._etfs)
        number = merged[ID][1]
        price = self.get_price(ID, self._d)
        amount = price * number
        return amount, round(amount/self._balance, 2)

    def get_stock_positions(self):
        IDs = self._stocks.keys()
        prices = [self.get_price(id, self._d) for id in IDs]
        numbers = [self._stocks[id][1] for id in IDs]
        amount = sum([i*j for i, j in zip(prices, numbers)])
        return amount

    def get_etf_positions(self):
        IDs = self._etfs.keys()
        prices = [self.get_price(id, self._d) for id in IDs]
        numbers = [self._etfs[id][1] for id in IDs]
        amount = sum([i*j for i, j in zip(prices, numbers)])
        return amount

    def get_bond_positions(self):
        IDs = self._bonds.keys()
        prices = [self.get_price(id, self._d) for id in IDs]
        numbers = [self._bonds[id][1] for id in IDs]
        amount = sum([i*j for i, j in zip(prices, numbers)])
        return amount

    def get_relative_position(self, amount):
        return round(amount/self._balance, 2)

    def get_total_asset(self):
        stocks = self.get_stock_positions()
        bonds = self.get_etf_positions()
        etfs = self.get_bond_positions()
        return stocks+bonds+etfs

    @staticmethod
    def get_price(ID, d):
        # from yahoo_fin import stock_info as si
        import yfinance as yf
        # get live price of Apple
        # return si.get_live_price(ID)
        tickerData = yf.Ticker(ID)
        tickerDf = tickerData.history(period='1d',
                                      start=d,
                                      end=d+timedelta(days=1))
        return tickerDf.Close.iloc[0]


class GiftCard(Account):
    def __init__(self, name, balance, cat=None):
        Account.__init__(self, name, balance)
        self._expiration = date(2100, 1, 1)
        self._code = None
        self.cat = cat

    @property
    def expiration(self):
        """get expiration date"""
        # print('Getting expiration date...')
        # time.sleep(0.5)
        # print('Expiration date is {}.{}.{}'.format(self._expiration.year, \
        #    self._expiration.month, self._expiration.day))
        return self._expiration

    @expiration.setter
    def expiration(self, d):
        """set expiration date"""
        assert isinstance(d, date), \
               'Please provide a valid date format: date(year, month, day)'
        # print('Setting expiration...')
        # time.sleep(0.5)
        self._expiration = d
        # print('Expiration date set to {}.{}.{}'. \
        # format(d.year, d.month, d.day))

    @property
    def code(self):
        """get access code"""
        return self._code

    @code.setter
    def code(self, c):
        """set access code"""
        self._code = c


class CreditCard:
    """
    This is the credit card account object.
    """
    def __init__(self, name, balance=0):
        self.name = name
        self._balance = balance
        self._restriction = None
        self._category = {}
        self._alert = {}
        self._annual_fee = 0
        self._benefit = ''
        self._ftf = True
        self._membership = []
        self._reimburse = {}

    @property
    def restriction(self):
        """get restriction"""
        # print('Getting restrictions...')
        return self._restriction

    @restriction.setter
    def restriction(self, words):
        """set restriction"""
        # print('Setting restrictions...')
        self._restriction = words

    @property
    def annual_fee(self):
        """get annual fee"""
        return self._annual_fee

    @annual_fee.setter
    def annual_fee(self, fee):
        """set annual fee"""
        self._annual_fee = fee

    @property
    def benefit(self):
        """get benefit"""
        return self._benefit

    @benefit.setter
    def benefit(self, b):
        """set benefit"""
        self._benefit = b

    @property
    def ftf(self):
        """get foreign transaction fee (boolen)"""
        return self._ftf

    @ftf.setter
    def ftf(self, b):
        """set foreign transaction fee (boolen)"""
        self._ftf = b

    def add_cat(self, cat, pct=0, type_='cash',
                expire=date(2999, 1, 1), start=date(1000, 1, 1)):
        """add cash back category"""
        self._category[cat] = (pct, type_, start, expire)

    def get_cat(self, c=None):
        """return cash back categories"""
        if not c:
            return self._category
        else:
            return self._category[c]

    def add_reimburse(self, name, balance=0, expire=date(2999, 1, 1)):
        self._reimburse[name] = (balance, expire)

    def get_reimburse(self):
        return self._reimburse

    def withdraw_from_reimburse(self, name, v):
        assert name in self._reimburse, "This category is not available"
        balance, expire = self._reimburse[name]
        assert balance >= v, "Not enough balance"
        assert expire >= date.today(), "benefit expired"
        self._reimburse = (balance-v, expire)

    def delete_reimburse(self, name):
        assert name in self._reimburse, "item not available"
        self._reimburse.pop(name)

    def add_membership(self, m):
        """add available membership"""
        self._membership.append(m)

    def get_membership(self, c=None):
        """return available membership"""
        return self._membership

    def remove_expired_cat(self):
        for key, value in self._category.items():
            if value[2] < date.today():  # expired
                self._category.pop(key)
        return self._category

    def add_alert(self, *awargs):
        for key, value in awargs:
            self._alert[key] = value

    def get_alert(self):
        return self._alert

    def print_alert(self, latest=False):
        if len(self._alert) == 0:
            print("No alert available")
        else:
            if latest:
                key = min(self._alert)
                print('Most recent alert: {}, {}'.format(key,
                                                         self._alert[key]))
            else:
                for key, value in self._alert.items():
                    print('Alert: {}, {}'.format(key, value))


def transfer(out_acct, in_acct, amount, factor=1):
    """perform transfer from one account to another. """
    out_acct.make_withdraw(amount)
    in_acct.make_deposit(amount*factor)
    log = 'Made a tranfer from {} to {} at a value of {}'.format(out_acct.name,
                                                                 in_acct.name,
                                                                 amount)
