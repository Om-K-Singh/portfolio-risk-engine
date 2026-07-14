import numpy as np
from data import Portfolio, Position
from abc import ABC, abstractmethod

class RiskModel:
    def __init__(self, portfolio: Portfolio, confidence: float = 0.95, horizon: int = 1):
        self.portfolio = portfolio
        self.confidence = confidence
        self.horizon = horizon
    
    @abstractmethod
    def calculate(self):
        pass
        
class MonteCarlo(RiskModel):
    def __init__(self, n_simulations: int = 10000):
        pass
    
class Parametric(RiskModel):
    def __init__(self):
        pass

class Historic(RiskModel):
    def __init__(self):
        pass
