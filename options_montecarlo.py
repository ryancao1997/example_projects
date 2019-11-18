import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd

# defines a function calculate the payoff given our variables
def montecarlo(libor,volatility, stock_price, a, c, p, long_run_volatility):
	estimated_price = stock_price
	day = 0
	random_variable = np.random.normal(0,1)
	random_variable_2 = np.random.normal(0,1)
	y = p*random_variable+math.sqrt(1-p**2)*random_variable_2
	volatility = volatility + c*math.sqrt((1/250)*abs(volatility))*y
	while day < 250:
		random_variable = np.random.normal(0,1)
		random_variable_2 = np.random.normal(0,1)
		if volatility < 0:
			volatility = abs(volatility)
		x = (libor-(0.5 * volatility**2))*(1/250)+(volatility*random_variable*math.sqrt(1/250))
		estimated_price = estimated_price*math.exp(x)
		y = p*random_variable+math.sqrt(1-p**2)*random_variable_2
		volatility = volatility + a*(long_run_volatility-volatility)*(1/250)+c*math.sqrt((1/250)*abs(volatility))*y
		day += 1
	return estimated_price

#defines variables
volatility = .20
long_run_volatility = .2
a = .95
c = .65
p = -.3
libor = .0125
index_level = 1065
strike_prices = [i*100 for i in range(1,21)]
estimated_stock_prices = []

#simulates 1000 paths
simulations = 0
sum_payoffs = 0
paths = 1000
while simulations<paths:
	estimated_stock_price = montecarlo(libor,volatility,index_level,a,c,p,long_run_volatility)
	estimated_stock_prices.append(estimated_stock_price)
	simulations += 1
rows = []
for strike_price in strike_prices:
	sum_payoffs = 0
	for estimated_stock_price in estimated_stock_prices:
		payoff = 0
		if (estimated_stock_price - strike_price) > 0:
			payoff = estimated_stock_price - strike_price
		sum_payoffs += payoff
	actual_payoff = sum_payoffs/paths
	price = actual_payoff*math.exp(-libor)
	rows.append([strike_price,price])
print(rows)
#writes csv outputfile
my_df = pd.DataFrame(rows)
print(my_df)
my_df.to_csv('prices.csv', index=False, header=False)

