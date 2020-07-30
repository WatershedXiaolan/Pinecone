from src.get_prices import *


target = [['U.S. Total Stock Market', ['VTI', 'ITOT', 'SCHB'], 0.279], \
        ['U.S. Value Stocks - Large Cap', ['VTV', 'SCHV'], 0.074], \
        ['U.S. Value Stocks - Mid Cap', ['VOE', 'IWS'], 0.061], \
        ['U.S. Value Stocks - Small Cap', ['VBR', 'IWN'], 0.051], \
        ['International Developed Market', ['VEA', 'IEFA', 'SCHF'], 0.205], \
        ['International Emerging Market', ['VWO','IEMG'], 0.13], \
        ['U.S. Inflation-Protected Bonds', ['VTIP'], 0.013], \
        ['U.S. High Quality Bonds', ['AGG'], 0.02], \
        ['U.S. Municipal Bonds', ['MUB','TFI'], 0.073], \
        ['International Developed Market Bonds', ['BNDX'], 0.06], \
        ['International Emerging Market Bonds', ['EMB','VWOB'], 0.033]]

expensse_ratio = [['VTI' , 'ITOT', 'SCHB', 'VTV', 'SCHV', 'VOE' , \
                  'IWS' , 'VBR' , 'IWN' , 'VEA', 'IEFA', 'SCHF', \
                  'VWO' , 'IEMG', 'VTIP', 'AGG', 'MUB' , 'TFI' , \
                  'BNDX', 'EMB' , 'VWOB'], 
                 [0.03  , 0.03  , 0.03  , 0.04 , 0.04  ,  0.07 , \
                  0.24  , 0.07  , 0.24  , 0.05 , 0.07  ,  0.06 , \
                  0.10  , 0.13  , 0.05  , 0.04 , 0.07  ,  0.23 , \
                  0.08  , 0.39  , 0.25  ]]
    
prices = get_static_prices()

total = 45394
allocation = {}
for l in target:
    allocation[l[0]] = (round(total * l[2], 2), l[1][0], round(total * l[2], 2)/prices[l[1][0]])


