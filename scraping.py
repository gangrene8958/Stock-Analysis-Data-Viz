import requests
import pandas as pd
from io import StringIO



def get_incomestatement(ticker):
    url = f"https://stockanalysis.com/stocks/{ticker}/financials"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f" Error {response.status_code} loading {ticker}")
            return None
        else:
            htmlext = StringIO(response.text)
            df = pd.read_html(htmlext)[0]
            df.columns = df.columns.get_level_values(0)
            df = df.drop(df.columns[1], axis = 1)
            df.set_index(df.columns[0], inplace = True)
            df = df.T

            return df

    except Exception as e:
        print(f"There was a problem during the scraping: {e}")
        return None
    
def get_balancesheet(ticker):
    url = f"https://stockanalysis.com/stocks/{ticker}/financials/balance-sheet"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f" Error {response.status_code} loading {ticker}")
            return None
        else:
            htmlext = StringIO(response.text)
            df = pd.read_html(htmlext)[0]
            df.columns = df.columns.get_level_values(0)
            df.set_index(df.columns[0], inplace = True)
            df = df.drop(df.columns[0], axis = 1)
            df = df.T
            return df

    except Exception as e:
        print(f"There was a problem during the scraping: {e}")
        return None
    

def get_cashflowstatement(ticker):
    url = f"https://stockanalysis.com/stocks/{ticker}/financials/cash-flow-statement"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f" Error {response.status_code} loading {ticker}")
            return None
        else:
            htmlext = StringIO(response.text)
            df = pd.read_html(htmlext)[0]
            df.columns = df.columns.get_level_values(0)
            df.set_index(df.columns[0], inplace = True)
            df = df.drop(df.columns[0], axis = 1)
            df = df.T
            df = df.sort_index(ascending = False)


            return df

    except Exception as e:
        print(f"There was a problem during the scraping: {e}")
        return None
    
def numeric(series):
    try:
        return pd.to_numeric(series)
    except (ValueError, TypeError):
        return series
    

def ticker_info(ticker):
  IncomeStatement = get_incomestatement(ticker)
  BalanceSheet = get_balancesheet(ticker)
  CashFlowStatement = get_cashflowstatement(ticker)

  # Filter out None values before concatenating
  dataframes = [df for df in [IncomeStatement, BalanceSheet, CashFlowStatement] if df is not None]

  if not dataframes:
    print(f"Could not retrieve any financial data for {ticker}")
    return None


  df = pd.concat(dataframes, axis = 1)

  for i in df:
      df[i] = numeric(df[i])

  df = df.select_dtypes(exclude = 'object')

  index = map(lambda x: x.split()[1], list(df.index))

  df.index = index

  df = df.sort_index(ascending=True)
  return df