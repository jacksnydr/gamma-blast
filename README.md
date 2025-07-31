# gamma-blast
This project implements and backtests an automated trading strategy known as the "Gamma Blast", designed to exploit sharp directional moves in 0DTE (zero days to expiration) index options—particularly on major indices like SPX and SPY.

The strategy leverages the concept of high gamma exposure near expiry, identifying breakout opportunities from low-volatility, range-bound price action during the trading day. It focuses on high-probability option plays that offer 2:1 and 3:1 risk-to-reward setups, triggered by late-day momentum and straddle price structure breaks.

🔍 Strategy Logic
1. Monitor intraday price action from 9:30 AM to 2:30 PM.

2. If the price range (high − low) is less than 1%, proceed.

3. Identify the at-the-money (ATM) straddle and monitor its price structure.

4. Wait for a descending structure breakout to the upside on the straddle chart.

5. Confirm price direction on the main index:
  - If trending up, buy ATM/OTM call options.
  - If trending down, buy ATM/OTM put options.

6. Enter trade with:
  - 3x take profit
  - 1x stop loss (based on option premium)

The strategy is designed to capitalize on sharp gamma-fueled moves often seen in the final hour of expiry-day trading.
