import pandas as pd 
import matplotlib.pyplot as plt 
import yfinance as yf 

from datetime import datetime, timedelta 

class Run: 

    def __init__(self): 

        self.log_df = pd.read_csv('Dataset/Log/log.csv') 
        self.start_date = '2021-01-01' 
        self.stock_list = self.log_df['Stock'].to_list() 
        self.stock_qty = self.log_df['Qty'].to_list() 

    def make_portfolio(self): 

        df = yf.download([stock + ".NS" for stock in self.stock_list], start = self.start_date, end = datetime.today(), auto_adjust = True)['Close']
        
        daily_index = pd.date_range(self.start_date, datetime.today(), freq = 'D')
        df_filled = df.reindex(daily_index, method = 'ffill').dropna()
        

        for stock, qty in zip(self.stock_list, self.stock_qty):
            print(stock, qty)
            df_filled[stock + '.NS'] = df_filled[stock + '.NS'] * qty  

        df_filled['Pf_Value'] = df_filled.sum(axis = 1) 
        df_filled['Pf_Value_Pct'] = df_filled['Pf_Value'] / df_filled['Pf_Value'].iloc[0] 
        df_filled['Pf_Value_Pct_100'] = df_filled['Pf_Value_Pct'] * 100 

        # print(df_filled.tail())

        print(df_filled.info())
        df_filled.to_csv('Dataset/main_pf.csv')  
    


if __name__ == "__main__": 

    run = Run() 

    run.make_portfolio()  


