import ccxt
import pandas as pd
import ta
import requests
import time

WEBHOOK_URL = "ใส่ Discord Webhook URL ตรงนี้"
SYMBOL = "BTC/USDT"
TIMEFRAME = "15m"
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70

def send_discord(msg):
    requests.post(WEBHOOK_URL, json={"content": msg})

def get_rsi():
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(SYMBOL, TIMEFRAME, limit=100)
    df = pd.DataFrame(ohlcv, columns=["time","open","high","low","close","volume"])
    df["rsi"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()
    return round(df["rsi"].iloc[-1], 2)

last_signal = None

while True:
    try:
        rsi = get_rsi()
        print(f"RSI: {rsi}")
        if rsi < RSI_OVERSOLD and last_signal != "oversold":
            send_discord(f"🟢 **RSI Oversold!**\n{SYMBOL} | 15m\nRSI = {rsi}\nโอกาสเติมของ!")
            last_signal = "oversold"
        elif rsi > RSI_OVERBOUGHT and last_signal != "overbought":
            send_discord(f"🔴 **RSI Overbought!**\n{SYMBOL} | 15m\nRSI = {rsi}\nระวังแรงขาย!")
            last_signal = "overbought"
        elif RSI_OVERSOLD < rsi < RSI_OVERBOUGHT:
            last_signal = None
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(60)
  
https://discord.com/api/webhooks/1513571106508902401/nZH8Ya8FEYMtFCmVmr6qa4WuKkdG8GC15kzZm-oqwlxZ8dZPek2FAjRD79yAwKbQuWZ7
