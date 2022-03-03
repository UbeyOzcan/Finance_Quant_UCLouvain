import streamlit as st
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from Calculator import Markovitz

def homepage():
    st.write("""
        # Markovitz efficient frontier 
        ### This application has been developped to compute efficient frontier using Markovitz Modern Portfolio Theory ###
        #""")
        

def main():
    page = st.sidebar.selectbox(
        "Select a Page",
        [
            "Homepage", 
            "Data analysis",
            "Efficient Frontier"
        ]
    )
    
    

    if page == "Homepage":
        homepage()
    
    elif page == "Data analysis":
        st.write("# Stocks prices and return analysis")
        T = ["AAPL", "TSLA", "AMZN", "GOOGL", "FB", "MSFT", "SONY"]
        tickers = st.sidebar.multiselect("Choose assets", T)
        start = st.sidebar.date_input("Choose starting date", datetime.date(2019, 7, 6))
        end = st.sidebar.date_input("Choose ending date", datetime.date(2019, 7, 6))
        Nsim = st.sidebar.number_input('Insert number of simulation',value = 10000,
                                       min_value = 5000, max_value = 20000, step = 10000)
        rf = st.sidebar.number_input("Enter free risk rate")
        run = st.sidebar.button("Run !")
        asset = st.multiselect('Which asset do you want to analyze ?', tickers)
        st.write('You selected:', asset)
        if start > end:
            st.warning('Please choose a starting date more recent than ending date')
        
        else :
            if run:
                data = Markovitz(tickers, start, end, Nsim, rf)
                price = data["Price"]
                st.line_chart(price[asset])
                
                logR = data["logR"]
                st.line_chart(logR[asset])
    
    else:
        st.write("# Efficient frontier computation")
        T = ["AAPL", "TSLA", "AMZN", "GOOGL", "FB", "MSFT", "SONY"]
        tickers = st.sidebar.multiselect("Choose assets", T)
        start = st.sidebar.date_input("Choose starting date", datetime.date(2019, 7, 6))
        end = st.sidebar.date_input("Choose ending date", datetime.date(2019, 7, 6))
        Nsim = st.sidebar.number_input('Insert number of simulation',value = 10000,
                                       min_value = 5000, max_value = 20000, step = 10000)
        rf = st.sidebar.number_input("Enter free risk rate")
        run2 = st.sidebar.button("Run !")
        if start > end:
            st.warning('Please choose a starting date more recent than ending date')
            
            
        if run2:
            
            data = Markovitz(tickers, start, end, Nsim, rf)
            st.write("# Efficient frontier")
            Portfolio = data["Ptf"]
            index = Portfolio["sharpe_ratio"].idxmax()
            result = pd.DataFrame(Portfolio.iloc[index])
            result.columns = ['MaxSR']
            
            index2 = Portfolio["Volatility"].idxmin()
            result2 = pd.DataFrame(Portfolio.iloc[index2])
            result2.columns = ['MinVol']
            
            final = result.join(result2)
            st.dataframe(final)
            
            vol_maxsr = final.at["Volatility", "MaxSR"]
            ret_maxsr = final.at["Return", "MaxSR"]
            
            vol_minvol = final.at["Volatility", "MinVol"]
            ret_minvol = final.at["Return", "MinVol"]
            
            x2 = [0, float(vol_maxsr)]
            y2 = [rf, float(ret_maxsr)]
            slope, intercept = np.polyfit(x2,y2,1)
            
            range = np.arange(0,vol_maxsr + 0.05, 0.001)
            rangey = slope * range + intercept

            fig, ax = plt.subplots()
            ax.scatter(x = Portfolio["Volatility"], y = Portfolio["Return"], c = Portfolio["sharpe_ratio"])
            ax.scatter(vol_maxsr, ret_maxsr, c = "red")
            ax.scatter(vol_minvol, ret_minvol, c = "yellow")
            ax.scatter(0, rf, c = "black")
            ax.plot(range, rangey)
            st.pyplot(fig)
        
        

if __name__ == "__main__":
    main()

        


    
    

        
        
        
    