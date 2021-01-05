import os, shutil
import pandas as pd


def h():
    print('h')

def prep_log_folder(folder):
    """
    move the existing log files to cache for final merge
    and clean up the directory
    """
    filenames = ['gc_balance.csv', 'balances.csv']
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


def merge_bank_logs(balances, cache_file='./log/balances_cache.csv', save_file='./log/balances.csv'):
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
    existing = pd.read_csv(cache_file)
    merged = pd.concat([existing, balances], axis=0, sort=False).fillna(0).reset_index(drop=True)
    merged = reorg(merged)
    merged.drop_duplicates(subset=['Date'], keep='last', inplace=True)
    os.remove(cache_file)
    merged.to_csv(save_file)
    print('file saved in ', save_file)


def reorg(df_merge):
    """clean up unnecessary columns and reorder them to have the statistics always at the end"""


    df_merge.drop(columns=['Unnamed: 0'], axis=1, inplace=True)

    df_merge['Date'] = pd.to_datetime(df_merge['Date'])

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

    return df_merge
