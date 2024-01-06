#!/usr/bin/env python
# coding: utf-8

# In[1]:


import yfinance as yf
import pandas as pd
import numpy as np


# In[2]:


vix_df = yf.download('^VIX')


# In[4]:


vix_df['MA'] = vix_df.Close.rolling('30D').mean()


# In[5]:


vix_df


# In[6]:


vix_df_filtered = vix_df[vix_df.Close > 1.5* vix_df.MA]


# In[7]:


vix_df_filtered


# In[13]:


series = pd.Series(vix_df_filtered.index).diff() / np.timedelta64(1, 'D') >=30


# In[19]:


series[0] = True


# In[22]:


series.value_counts()


# In[23]:


signals = vix_df_filtered[series.values]


# In[29]:


sp500_df = yf.download('^GSPC', start = '1990-01-01')


# In[30]:


from pandas.tseries.offsets import DateOffset


# In[38]:


returns = []

for i in range(len(signals)):
    subdf = sp500_df[(sp500_df.index >= signals.index[i]) &
                     (sp500_df.index <= signals.index[i] + DateOffset(months=6))]
    returns.append((subdf.Close.pct_change()+1).prod())


# In[40]:


pd.Series(returns) -1


# In[43]:


(pd.Series(returns)-1).plot(kind='bar')

