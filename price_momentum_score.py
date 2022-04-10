# %%
from tempfile import tempdir
import requests
import pandas as pd
import numpy as np
import os
import datetime
import re


def get_data(data_list):
    data_dict = {}
    for data in data_list:
        data_dict[data] = pd.read_csv('./data/' + data)
    return data_dict


class preprocess:
    def __init__(self, data):
        self.col = list(data.columns)
        self.data = self.parsing(data)

        self.time_ascend()

    def parsing(self, data):
        data = data.dropna(axis=0, how='any')
        data['Date'] = pd.to_datetime(data['Date'])
        for i in range(1, len(self.col)):
            if data[self.col[i]].dtypes == 'O':
                data[self.col[i]] = data[self.col[i]]\
                    .apply(lambda x: x.replace('$', '')).astype(float)
            else:
                pass
        return data

    def time_ascend(self):
        if self.data.Date[0] > self.data.Date[1]:
            self.data = self.data[::-1].reset_index(drop=True)
        else:
            pass


class strategies:
    def ranked_price_momentum(data: pd.DataFrame, col: str = 'Close/Last') -> pd.DataFrame:
        """ranking _summary_
        Yield higher percentage value as the value is cloaser to a highest peak from last 252 trading days.

        :param data: pre-processed price data
        :type data: pandas.DataFrame
        :return: dataframe with Date and ranked score
        :rtype: pandas.DataFrame
        """
        temp_data = pd.DataFrame(data.Date)
        temp_data['rank'] = (data[col].rolling(
            window=252).rank('max')-1)*100/251
        temp_data.dropna(axis=0, how='any', inplace=True)
        return temp_data

    def ranked_intraday_momentum(data):
        temp_data = pd.DataFrame(data.Date)
        temp_data['intra'] = \
            (data['Close/Last']- data['Open'])/(data['Low']-data['High'])*100
        temp_data['intra']= \
            (temp_data['intra'].rolling(window=252).rank('max')-1)*100/251
        temp_data.dropna(axis=0, how='any', inplace=True)
        return temp_data


# %%
if __name__ == "__main__":

    data_list = os.listdir('./data')
    data_dict = get_data(data_list)

    result1 = pd.DataFrame()
    result2 = pd.DataFrame()
    
    
    for i in data_list:
        ticker = i.replace('.csv', '')
        data_processed = preprocess(data_dict[i])
        rank_close = strategies.ranked_price_momentum(data_processed.data).rename({'rank': ticker}, axis=1)
        rank_intra = strategies.ranked_intraday_momentum(data_processed.data).rename({'intra': ticker}, axis=1)
        
        if len(result1) == 0:
            result1 = rank_close
        else:
            result1 = pd.merge(result1, rank_close, how='outer', on='Date')
        
        if len(result2) == 0:
            result2 = rank_intra
        else:
            result2 = pd.merge(result2, rank_intra, how='outer', on='Date')

    result1.to_csv('./result/Q2_result.csv', index=False)
    result2.to_csv('./result/Q3_result.csv', index=False)


# %%
