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
    price_set = {'SPY': 316.84,
                 'VTI': 160.13,
                 'VOO': 290.31,
                 'date': str(date.today())}
    write_prices(r'/Users/xiaolan/Documents/repos/FinProject/ \
                 local_src/static_prices.json', price_set)     
                    
