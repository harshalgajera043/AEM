
# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
from fbprophet import Prophet

# Load your time series dataset
# Assuming the data has a 'Date' column and a 'Inventory_Valuation' column
data = pd.read_csv('daily_inventory_valuation.csv', parse_dates=['Date'], index_col='Date')

# Plot the data to visualize the time series
plt.figure(figsize=(10, 6))
plt.plot(data['Inventory_Valuation'])
plt.title('Daily Inventory Valuation Over Time')
plt.xlabel('Date')
plt.ylabel('Inventory Valuation')
plt.show()

# Split the data into training and testing sets
train_size = int(len(data) * 0.8)
train, test = data['Inventory_Valuation'][:train_size], data['Inventory_Valuation'][train_size:]

# --- SARIMA Model ---
# Seasonal ARIMA model
# p: number of lag observations (AR term), d: degree of differencing, q: size of moving average window
# P, D, Q are the seasonal components with 's' being the seasonality period
sarima_model = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 7))  # Adjust based on seasonality
sarima_model_fit = sarima_model.fit()

# Forecast the future values using SARIMA
sarima_forecast = sarima_model_fit.forecast(steps=len(test))

# Evaluate SARIMA model
sarima_error = mean_squared_error(test, sarima_forecast)
print(f'SARIMA Mean Squared Error: {sarima_error}')

# Plot SARIMA forecast vs actual values
plt.figure(figsize=(10, 6))
plt.plot(test.index, test, label='Actual Inventory Valuation')
plt.plot(test.index, sarima_forecast, label='SARIMA Forecasted', color='red')
plt.title('SARIMA Forecast vs Actual Inventory Valuation')
plt.xlabel('Date')
plt.ylabel('Inventory Valuation')
plt.legend()
plt.show()

# --- Prophet Model ---
# Preparing data for Prophet (requires a 'ds' and 'y' column for Date and Value)
prophet_data = data.reset_index().rename(columns={'Date': 'ds', 'Inventory_Valuation': 'y'})

# Create a Prophet model
prophet_model = Prophet(daily_seasonality=True)
prophet_model.fit(prophet_data[['ds', 'y']][:train_size])

# Forecast future values using Prophet
future = prophet_model.make_future_dataframe(periods=len(test), freq='D')
forecast = prophet_model.predict(future)

# Evaluate Prophet model
prophet_forecast = forecast['yhat'][train_size:].values
prophet_error = mean_squared_error(test, prophet_forecast)
print(f'Prophet Mean Squared Error: {prophet_error}')

# Plot Prophet forecast vs actual values
plt.figure(figsize=(10, 6))
plt.plot(test.index, test, label='Actual Inventory Valuation')
plt.plot(test.index, prophet_forecast, label='Prophet Forecasted', color='green')
plt.title('Prophet Forecast vs Actual Inventory Valuation')
plt.xlabel('Date')
plt.ylabel('Inventory Valuation')
plt.legend()
plt.show()

# Prophet future forecast (e.g., next 30 days)
future_forecast = prophet_model.predict(prophet_model.make_future_dataframe(periods=30, freq='D'))
print('Future Prophet Forecasted Inventory Valuation:')
print(future_forecast[['ds', 'yhat']].tail(30))
