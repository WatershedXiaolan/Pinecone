import json
from datetime import date

def write_prices(fn, data):
    with open(fn, 'w') as fp:
        json.dump(data, fp)

def read_prices(fn):
    with open(fn, 'r') as fp:
        data = json.load(fp)
    return data

if __name__ == '__main__':
    price_set = {'SPY'  : 316.84, \
                 'VTI'  : 160.13, \
                 'VOO'  : 290.31, \
                 'MSFT' : 215.13, \
                 'AAPL' : 383.42, \
                 'XOM'  : 42.95 , \
                 'GOOGL': 1512.9, \
                 'VTI'  : 160.13, \
                 'VOO'  : 290.31, \
                 'MSFT' : 215.13, \
                 'AAPL' : 383.42, \
                 'XOM'  : 42.95 , \
                 'GOOGL': 1512.9, \
                 'AMZN' : 3119.4, \
                 'BABA' : 261.81, \
                 'TSLA' : 1390.0, \
                 'FB'   : 244.20, \
                 'BND'  : 88.46 , \
                 'BNDX' : 57.82 , \
                 'VXUS' : 51.17 , \
                 'SPAXX': 1.0   , \
                 'VMMXX': 1.0   , \
                 'date' : str(date.today())}
    write_prices(r'/Users/xiaolan/Documents/repos/FinProject/local_src/static_prices.json', price_set)     
                    
