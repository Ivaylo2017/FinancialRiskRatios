import pandas as pd
import numpy as np
import pandas_datareader.data as web
from datetime import date

class RiskRatios():

	def __init__(self, symbol): 
		#Validate if user is enetring an actual symbols
		self.symbol = symbol
		self.start = date(2017,1,1)
		self.stop = date.today()
		self.data = self.get_data()
		self.returns = self.get_returns()
		self.covariance = self.get_covariance()
		self.beta = self.get_beta()
		self.alpha = self.get_alpha()

	def get_data(self):
		portfolio = ["SPY", self.symbol]
		rawdata = pd.DataFrame()
		for ticker in portfolio:
			rawdata[ticker] = web.DataReader(ticker, "google", self.start, self.stop)["Close"]
		#print("\n",rawdata.head(),"\n")
		return rawdata

	def get_returns(self):
		returns = np.log(self.data/self.data.shift(1))
		returns = returns.dropna() #Built-in function to remove NaN values from DataFrame
		#print(returns.head())
		return returns

	def get_covariance(self):
		covariance = np.cov(self.returns.SPY, self.returns[self.symbol])
		return covariance

	def get_beta(self):
		beta = self.covariance[0,1]/np.var(self.returns.SPY)
		return beta

	def get_alpha(self):
		alpha = np.mean(self.returns[self.symbol]) - (self.beta*np.mean(self.returns.SPY))
		return alpha

	def get_r_squared(self):
		corr_coefficient = self.alpha + (self.beta*self.returns.SPY)
		square_correlation = np.sum(np.power(corr_coefficient-self.returns.SPY, 2))
		sum_of_squares = self.covariance[0,0]*(len(self.returns) - 1)
		r_squared = 1 - square_correlation / sum_of_squares          
		#print("R", r_squared)           #The higher the R more confident we can be in the beta
		return r_squared

def main():
	TMPL = '''
	Stock: %s
	Beta: %s
	Alpha: %s
	R Squared: %s
	'''
	stock_symbol = input("Please enter a stock symbol: ")
	b = RiskRatios(stock_symbol)
	alpha = b.get_alpha()*252 #To annualize alpha using 252 trading days in the year
	print(TMPL % (stock_symbol, b.get_beta(), alpha, b.get_r_squared()))


if __name__ == "__main__":
	main()



#b = RiskRatios("AAPL")
# b.get_data()
# b.get_returns()