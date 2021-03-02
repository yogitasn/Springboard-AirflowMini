#pylint: disable = line-too-long, too-many-lines, no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order

import yfinance as yf
from datetime import timedelta,date,datetime
import pandas as pd
from scripts.config import DATAPATH
from airflow.utils.dates import days_ago


class YfinanceStock():

    """
     Function to download stock data for tsla and apple using yfinance library

    """
    @staticmethod
    def download_stock_data(**kwargs):
        print("Downloading stock data for {}".format(kwargs['symbolType']))
        
       # start_date = date.today()-timedelta(days=2)

        execution_date=kwargs['ds']
        print(execution_date)

        start_date = datetime.strptime(execution_date, '%Y-%m-%d')
       
        print("Start_date: {}".format(start_date))
        
        end_date = start_date + timedelta(days=1)

        print("End_date: {}".format(end_date))
        
        todays_date=start_date.strftime('%Y-%m-%d')

        print(todays_date)
        
        tsla_df = yf.download(kwargs['symbolType'], start=start_date, end=end_date, interval='1m')
        
        tsla_df.to_csv("{}/{}/data_{}.csv".format(DATAPATH,execution_date,kwargs['symbolType']),header=True)

    
def main():
    YfinanceStock.download_stock_data()


if __name__ == "__main__":
    main()