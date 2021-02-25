# IMPORTS 
import talib
import yfinance as yf

# TESTING CANDLESTICK PATTERN ANALYSIS WITH YFINANCE + TA-LIB 

# Download Data Frame of asset index
data = yf.download("GME", start="2020-12-01", end="2021-01-27")

# Get Morning star pattern analysis
morning_stars = talib.CDLMORNINGSTAR(data['Open'], data['High'], data['Low'], data['Close'])
# Get Engulfing pattern analysis
engulfing = talib.CDLENGULFING(data['Open'], data['High'], data['Low'], data['Close'])
# Get moment indicator 
momentum = talib.ADX(data['High'], data['Low'], data['Close'], timeperiod=20)
# Get Evening star pattern analysis 
evening_stars = talib.CDLEVENINGSTAR(data['Open'], data['High'], data['Low'], data['Close'])
# Get Relative Strength Index Indicator
relative_strength = talib.RSI(data['Close'], timeperiod=14)
# Get Exponetial Moving Average Indicator
exp_moving_avg = talib.EMA(data['Close'], timeperiod=20)

# Assign analysis and indicator vals to Data Frame with titles
data['Morning_star'] = morning_stars
data['Engulfing'] = engulfing 
data['Momentum'] = momentum
data['EMA'] = exp_moving_avg 
data['RSI'] = relative_strength 
data['Evening_star'] = evening_stars

# Print data frame
print(data) 

# Break down data frame by respective analysis/indicator
engulfing_days = data[data["Engulfing"] != 0]
morning_star_flips = data[data["Morning_star"] != 0]
evening_star_flips = data[data["Evening_star"] != 0]

# Print data frame for engulfing days analysis
print("Engulfing days \n")
print(engulfing_days)

# Print data frame for morning star analysis
print("Morning star flips \n")
print(morning_star_flips)

# Print data frame for evening star analysis 
print("Evening star flips \n")
print(evening_star_flips)

