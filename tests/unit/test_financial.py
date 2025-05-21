"""
Tests for the financial utilities module.
"""

import pytest
import numpy as np
from typing import List

from src.utils.financial import (
    npv,
    irr,
    xirr,
    equity_multiple,
    roi,
    payback_period,
    var,
    sharpe_ratio,
    max_drawdown,
)


def test_npv() -> None:
    """Test NPV calculation."""
    # Test case 1: Simple cash flows
    cashflows = [-100, 30, 40, 50]
    rate = 0.1
    expected = -100 + 30 / 1.1 + 40 / 1.1**2 + 50 / 1.1**3
    assert npv(rate, cashflows) == pytest.approx(expected)
    
    # Test case 2: Zero rate
    assert npv(0, cashflows) == pytest.approx(sum(cashflows))
    
    # Test case 3: Empty cash flows
    assert npv(0.1, []) == 0


def test_irr() -> None:
    """Test IRR calculation."""
    # Test case 1: Simple cash flows
    cashflows = [-100, 30, 40, 50]
    assert irr(cashflows) == pytest.approx(0.1066, abs=1e-4)
    
    # Test case 2: No solution
    assert irr([1, 2, 3]) is None
    
    # Test case 3: Empty cash flows
    assert irr([]) is None
    
    # Test case 4: All zeros
    assert irr([0, 0, 0]) is None
    
    # Test case 5: Negative IRR
    cashflows = [-100, 50, 40, 5]
    assert irr(cashflows) == pytest.approx(-0.0212, abs=1e-4)


def test_xirr() -> None:
    """Test XIRR calculation."""
    # Test case 1: Simple cash flows with irregular dates
    cashflows = [-100, 30, 40, 50]
    dates = [0, 0.5, 1.0, 1.5]
    assert xirr(cashflows, dates) == pytest.approx(0.2127, abs=1e-4)
    
    # Test case 2: No solution
    assert xirr([1, 2, 3], [0, 1, 2]) is None
    
    # Test case 3: Empty cash flows
    assert xirr([], []) is None
    
    # Test case 4: Mismatched lengths
    assert xirr([1, 2, 3], [0, 1]) is None
    
    # Test case 5: All zeros
    assert xirr([0, 0, 0], [0, 1, 2]) is None


def test_equity_multiple() -> None:
    """Test equity multiple calculation."""
    # Test case 1: Simple cash flows
    cashflows = [-100, 30, 40, 50]
    assert equity_multiple(cashflows) == pytest.approx(1.2)
    
    # Test case 2: No initial investment
    assert equity_multiple([0, 30, 40, 50]) is None
    
    # Test case 3: Positive initial investment
    assert equity_multiple([100, 30, 40, 50]) is None
    
    # Test case 4: Empty cash flows
    assert equity_multiple([]) is None
    
    # Test case 5: No returns
    assert equity_multiple([-100, 0, 0, 0]) == pytest.approx(0.0)


def test_roi() -> None:
    """Test ROI calculation."""
    # Test case 1: Simple cash flows
    cashflows = [-100, 30, 40, 50]
    assert roi(cashflows) == pytest.approx(0.2)
    
    # Test case 2: No initial investment
    assert roi([0, 30, 40, 50]) is None
    
    # Test case 3: Positive initial investment
    assert roi([100, 30, 40, 50]) is None
    
    # Test case 4: Empty cash flows
    assert roi([]) is None
    
    # Test case 5: Negative ROI
    assert roi([-100, 20, 30, 40]) == pytest.approx(-0.1)


def test_payback_period() -> None:
    """Test payback period calculation."""
    # Test case 1: Simple cash flows
    cashflows = [-100, 30, 40, 50]
    assert payback_period(cashflows) == pytest.approx(2.75)
    
    # Test case 2: No initial investment
    assert payback_period([0, 30, 40, 50]) is None
    
    # Test case 3: Positive initial investment
    assert payback_period([100, 30, 40, 50]) is None
    
    # Test case 4: Empty cash flows
    assert payback_period([]) is None
    
    # Test case 5: Never pays back
    assert payback_period([-100, 20, 20, 20]) is None
    
    # Test case 6: Pays back exactly
    cashflows = [-100, 50, 50]
    assert payback_period(cashflows) == pytest.approx(2.0)
    
    # Test case 7: Pays back in first period
    cashflows = [-100, 150, 50]
    assert payback_period(cashflows) == pytest.approx(1.0)


def test_var() -> None:
    """Test VaR calculation."""
    # Test case 1: Simple returns
    returns = [0.05, -0.02, 0.03, -0.01, 0.04]
    assert var(returns, 0.95) == pytest.approx(0.02)
    
    # Test case 2: Empty returns
    assert var([], 0.95) == 0.0
    
    # Test case 3: Different confidence level
    assert var(returns, 0.99) == pytest.approx(0.02)


def test_sharpe_ratio() -> None:
    """Test Sharpe ratio calculation."""
    # Test case 1: Simple returns
    returns = [0.05, -0.02, 0.03, -0.01, 0.04]
    risk_free_rate = 0.01
    expected = (np.mean(returns) - risk_free_rate) / np.std(returns, ddof=1)
    assert sharpe_ratio(returns, risk_free_rate) == pytest.approx(expected)
    
    # Test case 2: Empty returns
    assert sharpe_ratio([], 0.01) is None
    
    # Test case 3: Zero standard deviation
    assert sharpe_ratio([0.05, 0.05, 0.05], 0.01) is None


def test_max_drawdown() -> None:
    """Test maximum drawdown calculation."""
    # Test case 1: Simple values
    values = [100, 110, 105, 95, 100, 90, 95]
    assert max_drawdown(values) == pytest.approx(0.1818, abs=1e-4)
    
    # Test case 2: Empty values
    assert max_drawdown([]) == 0.0
    
    # Test case 3: Single value
    assert max_drawdown([100]) == 0.0
    
    # Test case 4: No drawdown
    assert max_drawdown([100, 110, 120, 130]) == 0.0
    
    # Test case 5: Continuous drawdown
    assert max_drawdown([100, 90, 80, 70]) == pytest.approx(0.3)
