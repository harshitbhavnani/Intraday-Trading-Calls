import yfinance as yf
import pandas as pd
import numpy as np
import time

counter = 1

symbols = ['RELIANCE.NS', 'HDFCBANK.NS', 'HINDUNILVR.NS', 'ITC.NS', 'BHARTIARTL.NS', 'ICICIBANK.NS', 'TATAMOTORS.NS', 'TATASTEEL.NS',
           'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJAJFINSV.NS', 'BPCL.NS', 'CIPLA.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'GAIL.NS', 'GRASIM.NS',
           'HCLTECH.NS', 'HDFC.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDPETRO.NS', 'INFY.NS', 'IOC.NS', 'IRB.NS', 'JSWSTEEL.NS',
           'KOTAKBANK.NS', 'LT.NS', 'LUPIN.NS', 'M&M.NS', 'MARUTI.NS', 'NTPC.NS', 'ONGC.NS', 'POWERGRID.NS', 'PNB.NS', 'RCOM.NS',
           'SBIN.NS', 'SUNPHARMA.NS', 'TCS.NS', 'WIPRO.NS', 'ZEEL.NS', 'ADANIPORTS.NS', 'ASIANPAINT.NS', 'AUROPHARMA.NS', 'BAJFINANCE.NS',
           'BEL.NS', 'BHEL.NS', 'CESC.NS', 'COALINDIA.NS', 'DLF.NS', 'GODREJCP.NS', 'GODREJIND.NS', 'HAVELLS.NS', 'HINDZINC.NS', 'IDBI.NS',
           'IDEA.NS', 'INDUSINDBK.NS', 'ITDCEM.NS', 'JINDALSTEL.NS', 'JPASSOCIAT.NS', 'KTKBANK.NS', 'L&TFH.NS', 'LICHSGFIN.NS', 'NMDC.NS',
           'OIL.NS', 'PETRONET.NS', 'PFC.NS', 'RCOM.NS', 'RECLTD.NS', 'RPOWER.NS', 'SAIL.NS', 'SBIN.NS', 'SIEMENS.NS', 'SUNTV.NS',
           'BANDHANBNK.NS', 'ULTRACEMCO.NS', 'DIVISLAB.NS', 'AARTIIND.NS', 'BATAINDIA.NS', 'CEATLTD.NS', 'TITAN.NS', 'BANKBARODA.NS',
           'ESCORTS.NS', 'DISHTV.NS', 'APOLLOHOSP.NS', 'ADANIPOWER.NS', 'BANKINDIA.NS', 'TECHM.NS', 'IBULHSGFIN.NS', 'AMBUJACEM.NS',
           'ASHOKLEY.NS', 'YESBANK.NS', 'DABUR.NS', 'ABBOTINDIA.NS', 'CANBK.NS', 'EXIDEIND.NS', 'BOSCHLTD.NS', 'BALKRISIND.NS',
           'AARTIDRUGS.NS', 'FEDERALBNK.NS', 'CHOLAFIN.NS', 'CUMMINSIND.NS', 'ADANIENT.NS', 'UPL.NS', 'CENTURYTEX.NS', 'APOLLOTYRE.NS']

def get_stock_data(symbol):
    stock_data = yf.Ticker(symbol).history(period="1d", interval="1m")
    return stock_data

def analyze_stock_data(data):

    # Calculate Simple Moving Average (SMA) with a window of 50
    data['SMA_50'] = data['Close'].rolling(window=50).mean()

    # Calculate Exponential Moving Average (EMA) with a window of 50
    data['EMA_50'] = data['Close'].ewm(span=50, adjust=False).mean()

    # Calculate Bollinger Bands
    data['Upper_Band'] = data['SMA_50'] + 2 * data['Close'].rolling(window=50).std()
    data['Lower_Band'] = data['SMA_50'] - 2 * data['Close'].rolling(window=50).std()
    
    # Calculate the relative strength index (RSI)
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # Check if the RSI is below 30 and if the current price is below the lower Bollinger Band
    if (data['RSI'].iloc[-1] < 30) and (data['Close'].iloc[-1] < data['Lower_Band'].iloc[-1]):
        return 'BUY'
    # Check if the RSI is above 70 and if the current price is above the upper Bollinger Band
    elif (data['RSI'].iloc[-1] > 70) and (data['Close'].iloc[-1] > data['Upper_Band'].iloc[-1]):
        return 'SELL'
    else:
        return 'HOLD'

if __name__ == '__main__':
    while True:
        for symbol in symbols:
            data = get_stock_data(symbol)
            if data is not None:
              signal = analyze_stock_data(data)
              if signal != 'HOLD':
                print("Symbol: {}, Signal: {}, RSI: {:.2f}".format(symbol, signal, data['RSI'].iloc[-1]))
            else:
              print("Unable to retrieve data for symbol: {}".format(symbol))
        print(counter,' Iteration(s) finished at ',time.strftime("%H:%M:%S", time.localtime()),'\n')
        counter = counter + 1
        time.sleep(900)
