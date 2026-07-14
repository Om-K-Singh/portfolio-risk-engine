import yfinance as yf
import pandas as pd

class Position:

    '''
    Tracks a specific security in a portfolio: price history, returns, and the
    quantity currently held.
        
    Attributes
    ----------
    ticker: str
        Ticker for the specific security
    lookback: str
        Lookback period for yfinance data download
    quantity: float
        Amount of one particular security owned
    price_data: pandas.Series
        Closing price data spanning time defined with lookback
    returns: pandas.Series
        Percent change between succesive trading days
    stock_price: float
        Most recent closing price for the security
    value: float
        Total value of the position (quantity multiplied by stock_price)
    
    Methods
    ----------
    set_lookback(lookback)
        Updates lookback period and re-downloads price data
    refresh()
        Re-downloads data from yfinance with current attributes
    modify_quantity(amount)
        Adjusts quantity held by the given amount (positive or negative)
    '''

    def __init__(self, ticker: str, quantity: float = 1, lookback: str = "252d"):
        self.ticker = ticker
        self.quantity = quantity
        self.lookback = lookback
    
        # Refresh is called here so that data can be loaded to calculate self.returns

        self.refresh()

    def set_lookback(self, lookback: str):
        
        '''
        Updates the lookback period and re-downloads price data.

        Parameters
        ----------
        lookback : str
            New lookback period string to pass to yfinance (e.g. "252d").
        '''
        
        self.lookback = lookback
        self.refresh()

    def refresh(self):
        
        '''
        (Re)downloads price data and recomputes returns using the current
        ticker and lookback period.
        '''
        
        data = yf.download(tickers=[self.ticker], period=self.lookback, auto_adjust=True)
        if data is None or data.empty:
            raise ValueError(f"No data returned for ticker '{self.ticker}'")
        
        # Handles edge case that yfinance returns None -> should functionally never happen
        
        self.price_data = data["Close"][self.ticker]                
        self.returns = self.price_data.pct_change().dropna()

    def modify_quantity(self, amount: float):
        
        '''
        Modifies the quantity of stock in a particular position.
        
        Parameters
        ----------
        amount: float
            Amount to add to the current position. Negative values reduce the
            position.
        '''
        
        self.quantity += amount

    @property
    def stock_price(self):
        return self.price_data.iloc[-1]
    
    @property
    def value(self):
        return self.stock_price * self.quantity

class Portfolio:
    
    '''
    Tracks a portfolio, which is a collection of Position objects.
    
    Attributes
    ----------
    positions: list of Position
        A specific position that is part of the portfolio
    lookback: str
        Lookback period applied to every position in the portfolio
    value: float
        The total value of the portfolio
    returns: pandas.DataFrame
        A matrix of the returns of each Position in the portfolio. Columns
        are labelled by ticker and rows are labelled by date.
    weights: pandas.Series
        A vector that contains the relative dollar value weights of each
        position
    portfolio_returns: pandas.Series
        Daily returns of the portfolio as a whole, computed as the weighted sum
        of individual position returns.
        
    Methods
    ----------
    add_position(ticker, quantity)
        Adds a new position, or tops up quantity if the ticker is already held
    remove_position(ticker)
        Removes a position from the portfolio
    set_lookback(lookback)
        Updates the lookback period for the portfolio and every position in it

    '''
    
    def __init__(self, positions=None, lookback: str = "252d"):
        self.positions = positions or []    # Allows for initialising portfolio with no objects
        self.lookback = lookback
    
    def add_position(self, ticker: str, quantity: float = 1):

        '''
        Adds a position to the portfolio. If the ticker is already held,
        tops up its quantity instead of creating a duplicate. New positions
        are constructed using the portfolio's current lookback period.

        Parameters
        ----------
        ticker: str
            Ticker of the security to add.
        quantity: float
            Quantity to add. If the ticker is new, this is the starting
            quantity; if it already exists, this is added to the existing quantity.
        '''

        existing = next((position for position in self.positions if position.ticker == ticker), None)
        if existing:
            existing.modify_quantity(quantity)
        else:
            self.positions.append(Position(ticker, quantity, self.lookback))

    def remove_position(self, ticker: str):
        
        '''
        Removes a specific position from the portfolio.
        
        Parameters
        ----------
        ticker: str
            The ticker of the security you want to remove from your portfolio.
        '''
        
        self.positions = [
            position for position in self.positions
            if position.ticker != ticker
        ]
        
    def set_lookback(self, lookback: str):

        '''
        Updates the lookback period for the portfolio and propagates it to
        every position currently held.

        Parameters
        ----------
        lookback: str
            New lookback period string to pass to yfinance (e.g. "252d").
        '''

        self.lookback = lookback
        for position in self.positions:
            position.set_lookback(lookback)

    @property
    def value(self):
        return sum(position.value
                   for position in self.positions
        )
    
    @property
    def returns(self):
        return pd.concat(
            [position.returns.rename(position.ticker) for position in self.positions],
            axis=1,
            join="inner"
        )
        
    @property
    def weights(self):
        return pd.Series(
            {position.ticker: position.value / self.value for position in self.positions}
        )
    
    @property
    def portfolio_returns(self):
        return self.returns @ self.weights
    
# Test case

portfolio = Portfolio()
portfolio.add_position("AAPL")
print(portfolio.value)