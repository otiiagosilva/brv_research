
import yfinance as yf
import pandas as pd
import numpy as np
import time
from colorama import Fore, Style

tickers = ['AAPL', 'AMZN', 'META', 'GOOGL', 'MSFT', 'TSLA', 'GOLD', '^NDX', '^BVSP', 'PBR-A']
period = '1d'
interval = '5m'
threshold = 0.3

def calculate_mfi(ticker, period, interval):
    data = yf.download(ticker, period=period, interval=interval)
    typical_price = (data['Close'] + data['High'] + data['Low']) / 3
    raw_money_flow = typical_price * data['Volume']
    money_flow_ratio = np.zeros_like(typical_price)

    for i in range(1, len(typical_price)):
        if raw_money_flow[i-1] == 0:
            money_flow_ratio[i] = 0
        elif typical_price[i] > typical_price[i-1]:
            money_flow_ratio[i] = raw_money_flow[i] / raw_money_flow[i-1]
        elif typical_price[i] < typical_price[i-1]:
            money_flow_ratio[i] = -raw_money_flow[i] / raw_money_flow[i-1]

    money_flow_ratio = np.clip(money_flow_ratio, -1, 1)
    money_flow = money_flow_ratio * raw_money_flow
    positive_money_flow = np.where(money_flow > 0, money_flow, 0)
    negative_money_flow = np.where(money_flow < 0, -money_flow, 0)
    positive_money_flow_sum = pd.Series(positive_money_flow).rolling(window=14).sum()
    negative_money_flow_sum = pd.Series(negative_money_flow).rolling(window=14).sum()
    money_flow_ratio = positive_money_flow_sum / negative_money_flow_sum
    mfi = 100 - (100 / (1 + money_flow_ratio))
    return mfi.iloc[-1]

while True:
    try:
        mfi_dict = {}
        for ticker in tickers:
            try:
                mfi = calculate_mfi(ticker, period, interval)
                mfi_dict[ticker] = mfi
            except Exception as e:
                print(f"No data found for {ticker}: {e}")
                continue

        if not mfi_dict:
            print("No data found for any ticker.")
            time.sleep(60)
            continue

        max_mfi = max(mfi_dict.values())
        max_mfi_ticker = [k for k, v in mfi_dict.items() if v == max_mfi][0]

        if max_mfi >= threshold:
            print(Fore.RED + f"{max_mfi_ticker} has the highest MFI of {max_mfi:.2f} - Potential BUY signal!" + Style.RESET_ALL)
        else:
            print(f"No ticker has an MFI greater than {threshold:.2f}")

        time.sleep(60)
    except KeyboardInterrupt:
        print("Execution interrupted by user.")
        break