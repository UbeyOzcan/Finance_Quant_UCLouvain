# -*- coding: utf-8 -*-
"""
Created on Sun Feb 27 22:26:00 2022

@author: ozcan
"""

import pandas_datareader as web
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def Markovitz(A, start, end,  Nsim, rf) :
    n = len(A)
    portfolio_returns = []
    portfolio_volatilities = []
    sharpe_ratio = []
    w = np.zeros((Nsim, n))
    pf_data = pd.DataFrame()
    
    for x in A:
        pf_data[x] = web.DataReader(x, data_source = 'yahoo', start = start, end = end)['Adj Close']
        
    log_returns = np.log(pf_data/pf_data.shift(1)).dropna()
    
    for i in np.arange(Nsim):
        weights = np.array(np.random.random(n))
        weights = weights/np.sum(weights)
        portfolio_returns.append(np.sum(weights * log_returns.mean()) * 250)
        portfolio_volatilities.append(np.sqrt(np.dot(weights.T,np.dot(log_returns.cov() * 250, weights))))
        sharpe_ratio.append((portfolio_returns[i] - np.array(rf))/portfolio_volatilities[i])
        w[i,:] = weights
    
    portfolios = pd.DataFrame({A[0] : w[:,0], A[1] : w[:,1], A[2] : w[:,2],
                               'Return': portfolio_returns, 'Volatility':portfolio_volatilities, 
                              'sharpe_ratio' : sharpe_ratio})
    
    output = {"Price" : pf_data,
              "logR" : log_returns,
              "Ptf" : portfolios
        }
    
    return(output)
    
#test = Markovitz(["AAPL", "TSLA", "AMZN", "GOOGL", "FB", "MSFT", "SONY"],
#                 '01-01-2021', '31-12-2021',
#                 1000,
#                 0.01)


#P = test["Price"]

#P.plot()
#plt.legend(loc='upper right')