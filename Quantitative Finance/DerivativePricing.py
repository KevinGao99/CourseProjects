import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from Binomial.binomial_pricing import OptionTrade, Binomial
from BlackScholes.black_scholes import BlackScholes
from MonteCarlo.monte_carlo_pricing import GbmModel, OptionTradePayoffPricer, MonteCarloEngineSimulator, Configuration, OptionTrade as MO

# Binomial Model to price American options
# Call
# delta
Underlying = np.arange(90, 131, .01)
Strike = 100
t = 1.0
r = 0.05
sigma = 0.25
option_type = 'C'
exercise_type = 'A'
def binomial_pricing(underlying, strike, risk_free_rate, volatility, time_to_maturity, option_type, exercise_type):
    trade = OptionTrade(underlying, strike, risk_free_rate, volatility, time_to_maturity,
                        option_type, exercise_type)
    binomial = Binomial(trade)
    price = binomial.price(5)
    return price
Binomial_American_Call_Price = np.asarray([binomial_pricing(underlying, Strike, r, sigma, t, option_type, exercise_type) for underlying in Underlying]) 
Binomial_American_Call_Delta = np.diff(Binomial_American_Call_Price) / np.diff(Underlying)
plt.plot(Underlying[1:], Binomial_American_Call_Delta)
plt.title('American Call Delta')
plt.xlabel('Underlying_Price')
plt.ylabel('Delta')

# gamma
Binomial_American_Call_Gamma = np.diff(Binomial_American_Call_Delta) / np.diff(Underlying[1:])
plt.plot(Underlying[2:], Binomial_American_Call_Gamma)
plt.title('American Call Gamma')
plt.xlabel('Underlying_Price')
plt.ylabel('Gamma')

# theta (at the money)
t = np.arange(0.01, 1.01, .01)
Binomial_American_Call_Price = np.asarray([binomial_pricing(100, Strike, r, sigma, time_to_maturity, option_type, exercise_type) for time_to_maturity in t])
Binomial_American_Call_Theta = np.diff(Binomial_American_Call_Price) / np.diff(t)
plt.plot(t[1:], Binomial_American_Call_Theta)
plt.title('American Call Theta')
plt.xlabel('Time_to_Maturity')
plt.ylabel('Theta')

# Asian Equity Option: Monte Carlo
# Delta
Underlying = np.arange(90, 131, .01)
strike = 100
risk_free_rate = 0.05
volatility = 0.25
time_to_maturity = 1

configuration = Configuration(16, 252 * time_to_maturity)

def monte_carlo_pricing(underlying, strike, risk_free_rate, volatility, time_to_maturity,
                        option_type = 'AC', barrier = None):
    trade = MO(underlying, strike, risk_free_rate, volatility, time_to_maturity,
                        option_type, barrier)
    model = GbmModel(configuration)
    trade_pricer = OptionTradePayoffPricer()
    simulator = MonteCarloEngineSimulator(configuration, model)
    price = simulator.simulate(trade, trade_pricer)
    return price

Monte_Carlo_Asian_Call_Price = np.asarray([monte_carlo_pricing(underlying, strike, risk_free_rate, volatility, time_to_maturity) for underlying in Underlying])
Monte_Carlo_Asian_Call_Delta = np.diff(Monte_Carlo_Asian_Call_Price) / np.diff(Underlying)
plt.plot(Underlying[1:], Monte_Carlo_Asian_Call_Delta)
plt.title('Asian Call Delta')
plt.xlabel('Underlying_Price')
plt.ylabel('Delta')

# Gamma
Monte_Carlo_Asian_Call_Gamma = np.diff(Monte_Carlo_Asian_Call_Delta) / np.diff(Underlying[1:])
plt.plot(Underlying[2:], Monte_Carlo_Asian_Call_Gamma)
plt.title('Asian Call Gamma')
plt.xlabel('Underlying_Price')
plt.ylabel('Gamma')

# Theta (at the money)
t = np.arange(0.01, 1.01, .01)
Monte_Carlo_Asian_Call_Price = np.asarray([monte_carlo_pricing(100, strike, risk_free_rate, volatility, time_to_maturity) for time_to_maturity in t])
Monte_Carlo_Asian_Call_Theta = np.diff(Monte_Carlo_Asian_Call_Price) / np.diff(t)
plt.plot(t[1:], Monte_Carlo_Asian_Call_Theta)
plt.title('Asian Call Theta')
plt.xlabel('Time_to_Maturity')
plt.ylabel('Theta')

# Barrier Up and In Call Option: Monte Carlo
# Delta
option_type = 'BuiC'
Underlying = np.arange(90, 131, .01)
strike = 100
risk_free_rate = 0.05
volatility = 0.25
time_to_maturity = 1
Barrier_Up_and_In_Call_Price = np.asarray([monte_carlo_pricing(underlying, strike, risk_free_rate, volatility, time_to_maturity, option_type, barrier = 1.5 * underlying) for underlying in Underlying])
Barrier_Up_and_In_Call_Delta = np.diff(Barrier_Up_and_In_Call_Price) / np.diff(Underlying)
plt.plot(Underlying[1:], Barrier_Up_and_In_Call_Delta)
plt.title('Barrier Up and In Call Delta')
plt.xlabel('Underlying_Price')
plt.ylabel('Delta')

# Gamma
Barrier_Up_and_In_Call_Gamma = np.diff(Barrier_Up_and_In_Call_Delta) / np.diff(Underlying[1:])
plt.plot(Underlying[2:], Barrier_Up_and_In_Call_Gamma)
plt.title('Barrier Up and In Call Gamma')
plt.xlabel('Underlying_Price')
plt.ylabel('Gamma')

# Theta (at the money)
t = np.arange(0.01, 1.01, .01)
Barrier_Up_and_In_Call_Price = np.asarray([monte_carlo_pricing(100, strike, risk_free_rate, volatility, time_to_maturity, option_type, barrier = 1.5 * 100) for time_to_maturity in t])
Barrier_Up_and_In_Call_Theta = np.diff(Barrier_Up_and_In_Call_Price) / np.diff(t)
plt.plot(t[1:], Barrier_Up_and_In_Call_Theta)
plt.title('Barrier Up and In Call Theta')
plt.xlabel('Time_to_Maturity')
plt.ylabel('Theta')

# Barrier Up and Out Call Option: Monte Carlo
# Delta
option_type = 'BuoC'
Underlying = np.arange(90, 131, .01)
strike = 100
risk_free_rate = 0.05
volatility = 0.25
time_to_maturity = 1
Barrier_Up_and_Out_Call_Price = np.asarray([monte_carlo_pricing(underlying, strike, risk_free_rate, volatility, time_to_maturity, option_type, barrier = 1.5 * underlying) for underlying in Underlying])
Barrier_Up_and_Out_Call_Delta = np.diff(Barrier_Up_and_Out_Call_Price) / np.diff(Underlying)
plt.plot(Underlying[1:], Barrier_Up_and_Out_Call_Delta)
plt.title('Barrier Up and Out Call Delta')
plt.xlabel('Underlying_Price')
plt.ylabel('Delta')

# Gamma
Barrier_Up_and_Out_Call_Gamma = np.diff(Barrier_Up_and_Out_Call_Delta) / np.diff(Underlying[1:])
plt.plot(Underlying[2:], Barrier_Up_and_Out_Call_Gamma)
plt.plot('Barrier Up and Out Call Gamma')
plt.xlabel('Underlying_Price')
plt.ylabel('Gamma')

# Theta (at the money)
t = np.arange(0.01, 1.01, .01)
Barrier_Up_and_Out_Call_Price = np.asarray([monte_carlo_pricing(100, strike, risk_free_rate, volatility, time_to_maturity, option_type, barrier = 1.5 * 100) for time_to_maturity in t])
Barrier_Up_and_Out_Call_Theta = np.diff(Barrier_Up_and_Out_Call_Price) / np.diff(t)
plt.plot(t[1:], Barrier_Up_and_Out_Call_Theta)
plt.title('Barrier Up and Out Call Theta')
plt.xlabel('Time_to_Maturity')
plt.ylabel('Theta')
