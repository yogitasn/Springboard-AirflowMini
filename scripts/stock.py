#pylint: disable = line-too-long, too-many-lines, no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order

import yfinance as yf
from datetime import timedelta,date,datetime
import pandas as pd
from scripts.config import FnDATAPATH

class stockData():

    """
     Function to read dataframe and execute query on the TSLA and AAPL stock data

    """
    @staticmethod
    def execute_query(**kwargs):
        print("Execute a query on the Apple stock finance dataframe and display the results")
        
        execution_date=kwargs['ds']
        print(execution_date)
              
        df_aapl=pd.read_csv("{}/finance_data/{}/data_aapl.csv".format(FnDATAPATH,execution_date))

        print(df_aapl.query('Volume < 500000'))

        print("---------------------------------------------------------------------")

        print("Execute a query on the TSLA stock finance dataframe and display the results")
              
        df_tsla=pd.read_csv("{}/finance_data/{}/data_tsla.csv".format(FnDATAPATH,execution_date))

        print(df_tsla.query('Volume < 300000'))

    
def main():
    stockData.execute_query()


if __name__ == "__main__":
    main()