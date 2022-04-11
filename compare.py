#%%
import numpy as np
import pandas as pd
from price_momentum_score import *
import matplotlib.pyplot as plt
import statsmodels.api as sm
    
# %%
def price_score_plot(data, ticker):
    fig, axs = plt.subplots(4, 1, figsize=(12, 10))
    axs[0].plot(data.Date, data['Close/Last'], color='black')
    axs[0].set_xlabel('Price')
    axs[1].plot(data.Date, data['daily_ret'], color='black')
    axs[1].set_xlabel('daily return')
    axs[2].bar(data.Date, data['score1'], color='red')
    axs[2].set_xlabel('ranked price momentum')
    axs[3].bar(data.Date, data['score2'], color='blue')
    axs[3].set_xlabel('ranked intraday momentum')
    fig.suptitle(ticker)
    fig.tight_layout()
    plt.savefig('./result/images2021/'+ticker+'.png')
    plt.show()
    
# %%
class OLS_tools:
    def ols_result(data, ticker):
        y = data.daily_ret
        x1 = data.score1
        x2 = data.score2
        model1 = sm.OLS(y,x1).fit()
        model2 = sm.OLS(y,x2).fit()
        return (model1.rsquared, model2.rsquared)


    def yearly_res(data, ticker):
        res = pd.DataFrame()
        for i in range(2013, 2023):
            yearly_data = data[data.Date.dt.year == i]
            res_temp = OLS_tools.ols_result(yearly_data, ticker)
            res = pd.concat([res, \
                pd.DataFrame({'Date': i, 'score1': res_temp[0], 'score2': res_temp[1]}, index = [i-2013])], axis=0)
        return res

    def plot(data, ticker):
        fig = plt.figure(figsize=(12, 3))
        fig.suptitle(ticker)
        plt.plot(data.Date, data.score1, label='ranked price momentum')
        plt.plot(data.Date, data.score2, label='ranked intraday momentum')
        plt.legend()
        fig.tight_layout()
        plt.savefig('./result/images_OLS/'+ticker+'.png')
        plt.show()
    
    
#%%
if __name__=='__main__':
    data_list = os.listdir('./data')
    data_dict = get_data(data_list)
    score1 = pd.read_csv('./result/Q2_result.csv').astype({'Date':'datetime64[ns]'})
    score2 = pd.read_csv('./result/Q3_result.csv').astype({'Date':'datetime64[ns]'})
    for i in data_list:
        ticker = i.replace('.csv', '')
        data_dict[i] = preprocess(data_dict[i]).data
        data_dict[i] = pd.merge(data_dict[i], \
            score1[['Date', ticker]].rename({ticker:'score1'}, axis=1), \
                how='outer', on='Date')
        data_dict[i] = pd.merge(data_dict[i], \
            score2[['Date', ticker]].rename({ticker:'score2'}, axis=1), \
                how='outer', on='Date')
        data_dict[i]['daily_ret'] = data_dict[i]['Close/Last'].pct_change(1).shift(-1)
        data_dict[i] = data_dict[i].dropna()
        
    
    ols_res = pd.DataFrame()
    for i in data_list:
        ticker = i.replace('.csv', '')
        temp = data_dict[i][data_dict[i].Date > '2021-01-01']
        # price_score_plot(temp, ticker)
        
        OLS_tools.plot(OLS_tools.yearly_res(data_dict[i], ticker), ticker)


# %%
