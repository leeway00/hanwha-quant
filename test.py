#%%
from price_momentum_score import *
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# %%
# 1. Get data from csv
## Use AAPL for testing

data_list = os.listdir('./data')
data_dict = get_data(data_list)
aapl = preprocess(data_dict['AAPL.csv']).data


# %%

# 2. Testing Intraday momentum
aapl['intra'] = (aapl['Close/Last']- aapl['Open'])/(aapl['High']-aapl['Low'])*100
aapl['intra2'] = (aapl['intra'].rolling(window=252).rank('max')-1)*100/251

aapl['pct']=aapl['Close/Last'].pct_change()
aapl['ret'] = aapl['pct'].shift(-1)
aapl = pd.merge(aapl, strategies.ranking(aapl), how='outer', on='Date')

#%%
# 3. Momentum Score

## 2 week MS
aapl['MS'] = 12*aapl['pct'] + 4*aapl['Close/Last'].pct_change(3)\
    + 2*aapl['Close/Last'].pct_change(6)+ aapl['Close/Last'].pct_change(12)

# Change window period of MS. 1 week
aapl['MS2'] = 6*aapl['pct'] + 2*aapl['Close/Last'].pct_change(3)\
    + aapl['Close/Last'].pct_change(6)

print(plt.scatter('MS2','ret', data=aapl))

# Rank by Momentum Score
aapl = pd.merge(aapl, strategies.ranking(aapl, 'MS').rename({'rank':'MS_rank'}, axis=1), how='outer', on='Date')
aapl = pd.merge(aapl, strategies.ranking(aapl, 'MS2').rename({'rank':'MS2_rank'}, axis=1), how='outer', on='Date')

# %%
aapl2 = aapl.dropna()
y = aapl2['ret']
x = aapl2[['rank','intra2','intra', 'MS', 'MS2', 'MS_rank', 'MS2_rank']]
x = sm.add_constant(x)

model = sm.OLS(y,x).fit()

print(model.summary())
print(plt.scatter(y, model.predict(x)))


# %%
# 4. Choosing Momentum score coefficient with OLS

aapl3 = aapl[['Date','ret','Close/Last']].copy()
for i in range(1,31):
    aapl3['pct'+str(i)] = aapl3['Close/Last'].pct_change(i)
    aapl3['pct'+str(i)+'_rank'] = \
        strategies.ranking(aapl3, 'pct'+str(i))['rank']

## OLS
aapl3 = aapl3.dropna().reset_index(drop=True)
y2 = aapl3['ret']
x2 = aapl3.drop(['Date','ret','Close/Last'], axis=1)
x2 = sm.add_constant(x2)

model2 = sm.OLS(y2, x2).fit()
print(plt.scatter(y2, model2.predict(x2)))

## Test with 2yrs sample
aapl_train = aapl3[aapl3['Date']<'2020-01-01']
aapl_test = aapl3[aapl3['Date']>'2020-01-01']

aapl_train = aapl_train.dropna().reset_index(drop=True)
y3 = aapl_train['ret']
x3 = aapl_train.drop(['Date','ret','Close/Last'], axis=1)
x3 = sm.add_constant(x3)
model3 = sm.OLS(y3, x3).fit()
plt.scatter(aapl_test['ret'], model3.predict(sm.add_constant(\
    aapl_test.drop(['Date','ret','Close/Last'], axis=1))))


# 5. aggregate all scores and test
for i in range(1,31):
    aapl['pct'+str(i)] = aapl['Close/Last'].pct_change(i)
    aapl['pct'+str(i)+'_rank'] = \
        strategies.ranking(aapl, 'pct'+str(i))['rank']

aapl3 = aapl.dropna().reset_index(drop=True)
y4 = aapl3['ret']
x4 = aapl3.drop(['Date','ret','Close/Last'], axis=1)
x4 = sm.add_constant(x4)

model4 = sm.OLS(y4, x4).fit()

plt.scatter(y4, model4.predict(x4))
# %%
aapl_train = aapl[aapl['Date']<'2020-01-01']
aapl_test = aapl[aapl['Date']>'2020-01-01']

aapl_train = aapl_train.dropna().reset_index(drop=True)
y5 = aapl_train['ret']
x5 = aapl_train.drop(['Date','ret','Close/Last'], axis=1)
x5 = sm.add_constant(x5)

model4_test = sm.OLS(y5, x5).fit()
plt.scatter(aapl_test['ret'], model4_test.predict(sm.add_constant(\
    aapl_test.drop(['Date','ret','Close/Last'], axis=1))))


# %%
# 6. As a single factor, 5 day momentum score
aapl['MS5'] = 0
for i in range(1,12,2):
    aapl['MS5'] += 5/i * aapl['Close/Last'].pct_change(i)
aapl['MS5_rank'] = strategies.ranking(aapl, 'MS5')['rank']

aapl6 = aapl.dropna()
y = aapl6['ret']
x = aapl6['MS5_rank']

model6 = sm.OLS(y,x).fit()
print(model6.summary())

