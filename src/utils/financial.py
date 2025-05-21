"""
Financial utilities module for the EQU IHOME SIM ENGINE v2.

This module provides financial calculation utilities such as IRR, XIRR, and NPV.
"""

import numpy as np
from scipy import optimize
from typing import List, Tuple, Optional, Union, Callable


def npv(rate: float, cashflows: List[float]) -> float:
    """
    Calculate the Net Present Value (NPV) of a series of cash flows.
    
    Args:
        rate: Discount rate (as a decimal, e.g., 0.05 for 5%)
        cashflows: List of cash flows, starting with the initial investment (negative)
        
    Returns:
        Net Present Value
        
    Example:
        >>> npv(0.1, [-100, 30, 40, 50])
        0.6863433748090816
    """
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(cashflows))


def irr(cashflows: List[float], guess: float = 0.1) -> Optional[float]:
    """
    Calculate the Internal Rate of Return (IRR) of a series of cash flows.
    
    Args:
        cashflows: List of cash flows, starting with the initial investment (negative)
        guess: Initial guess for the IRR
        
    Returns:
        Internal Rate of Return, or None if no solution is found
        
    Example:
        >>> irr([-100, 30, 40, 50])
        0.1066503793138814
    """
    if not cashflows or all(cf == 0 for cf in cashflows):
        return None
    
    if cashflows[0] > 0:
        # IRR calculation expects the first cash flow to be negative
        cashflows = [-cf for cf in cashflows]
    
    try:
        # Define the function to find the root of
        def f(r: float) -> float:
            return npv(r, cashflows)
        
        # Find the root using scipy's optimize.newton
        result = optimize.newton(f, guess, tol=1e-6, maxiter=1000)
        
        # Check if the result is valid
        if result <= -1:
            return None
        
        return result
    
    except (RuntimeError, ValueError):
        # Try with a different method if newton fails
        try:
            # Find the root using scipy's optimize.brentq
            result = optimize.brentq(f, -0.999, 1000, maxiter=1000)
            
            # Check if the result is valid
            if result <= -1:
                return None
            
            return result
        
        except (RuntimeError, ValueError):
            return None


def xirr(cashflows: List[float], dates: List[float], guess: float = 0.1) -> Optional[float]:
    """
    Calculate the Internal Rate of Return (IRR) of a series of cash flows occurring at irregular intervals.
    
    Args:
        cashflows: List of cash flows, starting with the initial investment (negative)
        dates: List of dates (in years) corresponding to each cash flow
        guess: Initial guess for the IRR
        
    Returns:
        Internal Rate of Return, or None if no solution is found
        
    Example:
        >>> xirr([-100, 30, 40, 50], [0, 0.5, 1.0, 1.5])
        0.2127016768241236
    """
    if not cashflows or len(cashflows) != len(dates) or all(cf == 0 for cf in cashflows):
        return None
    
    if cashflows[0] > 0:
        # IRR calculation expects the first cash flow to be negative
        cashflows = [-cf for cf in cashflows]
    
    try:
        # Define the function to find the root of
        def f(r: float) -> float:
            return sum(cf / (1 + r) ** t for cf, t in zip(cashflows, dates))
        
        # Find the root using scipy's optimize.newton
        result = optimize.newton(f, guess, tol=1e-6, maxiter=1000)
        
        # Check if the result is valid
        if result <= -1:
            return None
        
        return result
    
    except (RuntimeError, ValueError):
        # Try with a different method if newton fails
        try:
            # Find the root using scipy's optimize.brentq
            result = optimize.brentq(f, -0.999, 1000, maxiter=1000)
            
            # Check if the result is valid
            if result <= -1:
                return None
            
            return result
        
        except (RuntimeError, ValueError):
            return None


def equity_multiple(cashflows: List[float]) -> Optional[float]:
    """
    Calculate the equity multiple of a series of cash flows.
    
    Args:
        cashflows: List of cash flows, starting with the initial investment (negative)
        
    Returns:
        Equity multiple, or None if the initial investment is zero
        
    Example:
        >>> equity_multiple([-100, 30, 40, 50])
        1.2
    """
    if not cashflows or cashflows[0] >= 0:
        return None
    
    initial_investment = abs(cashflows[0])
    total_returns = sum(cf for cf in cashflows[1:] if cf > 0)
    
    if initial_investment == 0:
        return None
    
    return total_returns / initial_investment


def roi(cashflows: List[float]) -> Optional[float]:
    """
    Calculate the Return on Investment (ROI) of a series of cash flows.
    
    Args:
        cashflows: List of cash flows, starting with the initial investment (negative)
        
    Returns:
        Return on Investment, or None if the initial investment is zero
        
    Example:
        >>> roi([-100, 30, 40, 50])
        0.2
    """
    if not cashflows or cashflows[0] >= 0:
        return None
    
    initial_investment = abs(cashflows[0])
    total_returns = sum(cashflows)
    
    if initial_investment == 0:
        return None
    
    return total_returns / initial_investment


def payback_period(cashflows: List[float]) -> Optional[float]:
    """
    Calculate the payback period of a series of cash flows.
    
    Args:
        cashflows: List of cash flows, starting with the initial investment (negative)
        
    Returns:
        Payback period in years, or None if the investment is never recovered
        
    Example:
        >>> payback_period([-100, 30, 40, 50])
        2.6
    """
    if not cashflows or cashflows[0] >= 0:
        return None
    
    initial_investment = abs(cashflows[0])
    cumulative = 0
    
    for i, cf in enumerate(cashflows[1:], 1):
        cumulative += cf
        
        if cumulative >= initial_investment:
            # Linear interpolation to find the exact payback period
            if i > 1 and cumulative > initial_investment:
                prev_cumulative = cumulative - cf
                fraction = (initial_investment - prev_cumulative) / cf
                return i - 1 + fraction
            
            return float(i)
    
    return None


def var(returns: List[float], confidence_level: float = 0.95) -> float:
    """
    Calculate the Value at Risk (VaR) of a series of returns.
    
    Args:
        returns: List of returns
        confidence_level: Confidence level (e.g., 0.95 for 95%)
        
    Returns:
        Value at Risk
        
    Example:
        >>> var([0.05, -0.02, 0.03, -0.01, 0.04], 0.95)
        0.02
    """
    if not returns:
        return 0.0
    
    return -np.percentile(returns, 100 * (1 - confidence_level))


def sharpe_ratio(returns: List[float], risk_free_rate: float = 0.0) -> Optional[float]:
    """
    Calculate the Sharpe ratio of a series of returns.
    
    Args:
        returns: List of returns
        risk_free_rate: Risk-free rate (as a decimal, e.g., 0.02 for 2%)
        
    Returns:
        Sharpe ratio, or None if the standard deviation is zero
        
    Example:
        >>> sharpe_ratio([0.05, -0.02, 0.03, -0.01, 0.04], 0.01)
        0.5
    """
    if not returns:
        return None
    
    mean_return = np.mean(returns)
    std_dev = np.std(returns, ddof=1)
    
    if std_dev == 0:
        return None
    
    return (mean_return - risk_free_rate) / std_dev


def max_drawdown(values: List[float]) -> float:
    """
    Calculate the maximum drawdown of a series of values.
    
    Args:
        values: List of values (e.g., portfolio values over time)
        
    Returns:
        Maximum drawdown as a positive decimal
        
    Example:
        >>> max_drawdown([100, 110, 105, 95, 100, 90, 95])
        0.18181818181818182
    """
    if not values or len(values) < 2:
        return 0.0
    
    max_so_far = values[0]
    max_drawdown_value = 0.0
    
    for value in values[1:]:
        if value > max_so_far:
            max_so_far = value
        else:
            drawdown = (max_so_far - value) / max_so_far
            max_drawdown_value = max(max_drawdown_value, drawdown)
    
    return max_drawdown_value
