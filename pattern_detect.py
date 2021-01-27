import talib
import yfinance as yf
data = yf.download("GME", start="2020-01-01", end="2021-01-27")

morning_stars = talib.CDLMORNINGSTAR(data['Open'], data['High'], data['Low'], data['Close'])

engulfing = talib.CDLENGULFING(data['Open'], data['High'], data['Low'], data['Close'])

momentum = talib.ADX(data['High'], data['Low'], data['Close'], timeperiod=20)

evening_stars = talib.CDLEVENINGSTAR(data['Open'], data['High'], data['Low'], data['Close'])

relative_strength = talib.RSI(data['Close'], timeperiod=14)

exp_moving_avg = talib.EMA(data['Close'], timeperiod=20)

data['Morning_star'] = morning_stars
data['Engulfing'] = engulfing 
data['Momentum'] = momentum
data['EMA'] = exp_moving_avg 
data['RSI'] = relative_strength 
data['Evening_star'] = evening_stars

print(data) 


engulfing_days = data[data["Engulfing"] != 0]
morning_star_flips = data[data["Morning_star"] != 0]
evening_star_flips = data[data["Evening_star"] != 0]

print("Engulfing days \n")
print(engulfing_days)
print("Morning star flips \n")
print(morning_star_flips)
print("Evening star flips \n")
print(evening_star_flips)

