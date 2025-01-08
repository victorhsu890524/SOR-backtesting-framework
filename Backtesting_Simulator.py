#!/usr/bin/env python
# coding: utf-8

# In[8]:


import numpy as np
import pandas as pd

def generate_synthetic_data(n=1440, S0=100, mu=0.0002, sigma=0.002):
    # Timestamps
    timestamps = pd.date_range("2025-01-07", periods=n, freq='min')

    # Prices (Geometric Brownian Motion)
    dt = 1/n
    W = np.random.normal(0, np.sqrt(dt), n)
    mid_prices = np.zeros(n)
    mid_prices[0] = S0
    for t in range(1, n):
        mid_prices[t] = mid_prices[t-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * W[t])
    spread = np.random.uniform(0.01, 0.05, n)
    ask_prices = mid_prices + spread
    bid_prices = mid_prices - spread

    # Volumes (Lognormal)
    volumes = np.random.lognormal(mean=5, sigma=1, size=n).astype(int)

    # Synthetic data
    data = pd.DataFrame({
        "Timestamp": timestamps,
        "Bid Price": bid_prices,
        "Ask Price": ask_prices,
        "Mid Price": mid_prices,
        "Volume": volumes
    })

    return data

def execute_twap(data, total_qty=100000, interval=5, latency=1, side='buy'):
    # Time intervals & Order size
    num_intervals = len(data) // interval
    order_size = total_qty / num_intervals

    # Trades execution
    trades = []
    for i in range(num_intervals):
        order_index = i * interval
        execution_index = min(order_index + latency, len(data) - 1)
        order_row = data.iloc[order_index]
        execution_row = data.iloc[execution_index]
        
        if side == 'buy':
            order_price = order_row['Ask Price']
            execution_price = execution_row['Ask Price']
        elif side == 'sell':
            order_price = order_row['Bid Price']
            execution_price = execution_row['Bid Price']
            
        trades.append({
            "Order_Timestamp": order_row["Timestamp"],
            "Execution_Timestamp": execution_row["Timestamp"],
            "Order Price": order_price,
            "Execution Price": execution_price,
            "Quantity": order_size
        })

    executed_trades = pd.DataFrame(trades)

    return executed_trades

def calculate_vwap(data):
    vwap = (data["Mid Price"] * data["Volume"]).sum() / data["Volume"].sum()
    return vwap

def performance_metrics(data):
    # Execution cost
    executed_trades = execute_twap(data)
    avg_executed_price = executed_trades["Execution Price"].mean()
    vwap = calculate_vwap(data)    
    execution_cost = avg_executed_price - vwap

    # Slippage
    slippage = abs(executed_trades["Execution Price"] - executed_trades["Order Price"]).mean()

    return executed_trades, execution_cost, slippage

if __name__ == "__main__":
    data = generate_synthetic_data()
    executed_trades, execution_cost, slippage = performance_metrics(data)
    print(data.head())
    print(executed_trades.head())
    print(f"Execution Cost: {execution_cost:.6f}")
    print(f"Slippage: {slippage:.6f}")


# In[ ]:




