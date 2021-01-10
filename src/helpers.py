import os, shutil
import pandas as pd


def h():
    print('h')

def prep_log_folder(folder):
    """
    move the existing log files to cache for final merge
    and clean up the directory
    """
    filenames = ['gc_balance.csv', 'balances.csv', 'retire_balances.csv']
    for filename in filenames:
        file_path = os.path.join(folder, filename)
        # copy balance file if one exist
        try:
            p = file_path.split('.')
            p.insert(-1, '_cache.')
            p = ''.join(p)
            shutil.copyfile(file_path, p)
            os.remove(file_path)
        except:
            pass
            
    print('cleaned log folder!')

def remove_cache(folder):
    filenames = ['gc_balance_cache.csv', 'balances_cache.csv', 'retire_balances_cache.csv']
    for filename in filenames:
        file_path = os.path.join(folder, filename)
        try:
            os.remove(file_path)
        except:
            pass
    
    print('removed all cache!')


    

def merge_bank_logs(balances, cache_file='./log/balances_cache.csv', save_file='./log/balances.csv'):
    """
    merge current balance with the existing balance sheets
    """
    merge_logs(balances, cache_file, save_file)

def merge_retirement_logs(balances, cache_file='./log/retire_balances_cache.csv', save_file='./log/retire_balances.csv'):
    """
    merge current balance with the existing balance sheets
    """
    merge_logs(balances, cache_file, save_file)    

def merge_gc_logs(balances, cache_file='./log/gc_balance_cache.csv', save_file='./log/gc_balance.csv'):
    """
    merge current balance with the existing balance sheets
    """
    merge_logs(balances, cache_file, save_file)

def merge_logs(balances, cache_file, save_file):
    """
    merge current balance with the existing balance sheets
    """
    balances.Date = pd.to_datetime(balances.Date)

    if os.path.exists(cache_file):
        existing = pd.read_csv(cache_file)
        existing.Date = pd.to_datetime(existing.Date)
        
        # only keep record before current
        # existing = existing[existing.Date<balances.Date.values[0]]

        merged = pd.concat([existing, balances], axis=0, sort=False).fillna(0).reset_index(drop=True)

        #os.remove(cache_file)
    else:
        merged = balances

    merged = reorg(merged)
    merged.drop_duplicates(subset=['Date'], keep='last', inplace=True)    
    merged.to_csv(save_file)
    merged.to_csv(cache_file)

    print('file saved in ', save_file)


def reorg(df_merge):
    """clean up unnecessary columns and reorder them to have the statistics always at the end"""

    # drop trailing columns
    df_merge.drop(columns=[n for n in df_merge if 'unname' in n.lower()], axis=1, inplace=True)

    df_merge['Date'] = pd.to_datetime(df_merge['Date'])

    # reorder columns
    if 'Date'  in df_merge.columns:
        names = ['Date']
        cols = [n for n in df_merge.columns if n not in names]
        cols = names + cols
        df_merge = df_merge[cols]

    if 'Sum' in df_merge.columns:
        names = ['Cash', 'Stock', 'Bond', 'Sum', 'S/(S+B) ratio']
        cols = [n for n in df_merge.columns if n not in names]
        cols += names
        df_merge = df_merge[cols]

    # sort rows by date
    df_merge = df_merge.sort_values(by=['Date'], ascending=False).reset_index(drop=True)
    

    # sort columns by the most recent balances 
    if 'Sum' in df_merge.columns:  
        names = ['Cash', 'Stock', 'Bond', 'Sum', 'S/(S+B) ratio']
    else:
        names = []
    accts = [n for n in df_merge.columns if n not in names+['Date']]
    balances = sorted([(df_merge.loc[0, n], n) for n in accts], reverse=True)
    col_orders = [temp[1] for temp in balances]
    col_orders = ['Date'] + col_orders + names
    df_merge = df_merge[col_orders]


    return df_merge
