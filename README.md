Implementation Approach 

1.	Synthetic Data Generation:
•	Generate synthetic data for one day in minute-level intervals.
•	Price data (bid, ask, mid prices) is generated using geometric Brownian motion for simulation, with a random spread is added to mid prices to calculate bid and ask prices.
•	Volume data is generated using log-normal distribution.

2.	TWAP Execution Logic:
•	The total order quantity is divided equally over specified intervals (5 minutes).
•	At each interval, an order is placed and executed with a fixed latency (1 minute).
•	Support Buy and sell operations with the ask and bid prices, respectively.

3.	Performance Metrics:
•	VWAP: Calculated as the ratio of price-volume product to total volume.
•	Execution Cost: Calculated as the difference between the average executed price and VWAP.
•	Slippage: Calculated as the average absolute difference between the executed price and the order price.

4.	Further Enhancements:
•	Incorporate multi-venue execution capabilities to simulate real-world market fragmentation.
•	Consider 1st and 2nd layer order book depth for more accurate slippage calculation.
•	Implement adaptive order sizing based on market volatility and liquidity for VWAP strategy
•	Include dynamic latency adjustments to reflect varying network and exchange conditions.
