"""
Tranche router for the EQU IHOME SIM ENGINE v2.

This module provides API endpoints for tranche management.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field

from src.engine.simulation_context import get_simulation_context
from src.tranche_manager import TrancheType, PaymentFrequency, AmortizationSchedule

router = APIRouter(
    prefix="/tranches",
    tags=["tranches"],
    responses={404: {"description": "Not found"}},
)


class TrancheAllocationRule(BaseModel):
    """Tranche allocation rule model."""

    zone_allocations: Optional[Dict[str, float]] = Field(
        None,
        description="Target zone allocations for the tranche",
        example={"green": 0.5, "orange": 0.3, "red": 0.2},
    )
    ltv_constraints: Optional[Dict[str, float]] = Field(
        None,
        description="LTV constraints for the tranche",
        example={"min_ltv": 0.0, "max_ltv": 0.75},
    )


class TrancheWaterfallRule(BaseModel):
    """Tranche waterfall rule model."""

    hurdle_rate: Optional[float] = Field(
        None,
        description="Hurdle rate for the tranche (0-1)",
        ge=0,
        le=1,
        example=0.08,
    )
    carried_interest_rate: Optional[float] = Field(
        None,
        description="Carried interest rate for the tranche (0-1)",
        ge=0,
        le=1,
        example=0.2,
    )
    catch_up_rate: Optional[float] = Field(
        None,
        description="Catch-up rate for the tranche (0-1)",
        ge=0,
        le=1,
        example=0.5,
    )


class TrancheCreate(BaseModel):
    """Tranche creation model."""

    name: str = Field(..., description="Tranche name", example="Senior Debt")
    size: float = Field(..., description="Tranche size in dollars", example=70000000)
    priority: int = Field(
        ...,
        description="Payment priority (lower numbers get paid first)",
        ge=1,
        example=1,
    )
    type: str = Field(
        ...,
        description="Tranche type",
        example="senior_debt",
    )
    interest_rate: Optional[float] = Field(
        None,
        description="Interest rate for debt tranches (0-1)",
        ge=0,
        le=1,
        example=0.05,
    )
    target_return: Optional[float] = Field(
        None,
        description="Target return for the tranche (0-1)",
        ge=0,
        le=1,
        example=0.15,
    )
    payment_frequency: Optional[str] = Field(
        "quarterly",
        description="Payment frequency for the tranche",
        example="quarterly",
    )
    amortization: Optional[bool] = Field(
        False,
        description="Whether the tranche amortizes",
        example=False,
    )
    amortization_schedule: Optional[str] = Field(
        "interest_only",
        description="Amortization schedule type",
        example="interest_only",
    )
    term_years: Optional[float] = Field(
        None,
        description="Term in years",
        ge=0,
        example=5,
    )
    waterfall_rules: Optional[TrancheWaterfallRule] = Field(
        None,
        description="Waterfall rules for the tranche",
    )
    allocation_rules: Optional[TrancheAllocationRule] = Field(
        None,
        description="Allocation rules for the tranche",
    )


class TrancheResponse(BaseModel):
    """Tranche response model."""

    name: str = Field(..., description="Tranche name")
    type: str = Field(..., description="Tranche type")
    size: float = Field(..., description="Tranche size in dollars")
    priority: int = Field(..., description="Payment priority")
    interest_rate: Optional[float] = Field(None, description="Interest rate for debt tranches")
    target_return: Optional[float] = Field(None, description="Target return for the tranche")
    actual_return: Optional[float] = Field(None, description="Actual return achieved")
    irr: Optional[float] = Field(None, description="Internal rate of return")
    moic: Optional[float] = Field(None, description="Multiple on invested capital")
    total_payments: float = Field(..., description="Total payments made to the tranche")
    principal_payments: float = Field(..., description="Principal payments made to the tranche")
    interest_payments: float = Field(..., description="Interest payments made to the tranche")
    profit_share_payments: float = Field(..., description="Profit share payments made to the tranche")
    shortfall: float = Field(..., description="Shortfall amount (if any)")
    status: str = Field(..., description="Tranche status (e.g., 'paid', 'defaulted', 'active')")


class TrancheAllocationResponse(BaseModel):
    """Tranche allocation response model."""

    loan_id: str = Field(..., description="Loan ID")
    allocation_percentage: float = Field(..., description="Percentage of the loan allocated to this tranche")
    allocation_amount: float = Field(..., description="Amount of the loan allocated to this tranche")
    zone: str = Field(..., description="Zone of the loan")
    ltv: float = Field(..., description="LTV of the loan")


class TrancheCashflowResponse(BaseModel):
    """Tranche cashflow response model."""

    year: float = Field(..., description="Year")
    month: Optional[int] = Field(None, description="Month (if applicable)")
    quarter: Optional[int] = Field(None, description="Quarter (if applicable)")
    principal_payment: float = Field(..., description="Principal payment")
    interest_payment: float = Field(..., description="Interest payment")
    profit_share_payment: float = Field(..., description="Profit share payment")
    total_payment: float = Field(..., description="Total payment")
    remaining_principal: float = Field(..., description="Remaining principal")


class CoverageTestResponse(BaseModel):
    """Coverage test response model."""

    test_type: str = Field(..., description="Test type (e.g., 'overcollateralization', 'interest_coverage')")
    test_date: str = Field(..., description="Date of the test")
    year: float = Field(..., description="Year of the test")
    month: int = Field(..., description="Month of the test")
    threshold: float = Field(..., description="Test threshold")
    actual_value: float = Field(..., description="Actual value")
    passed: bool = Field(..., description="Whether the test passed")
    cure_deadline: Optional[str] = Field(None, description="Deadline to cure the test failure (if applicable)")
    cured: Optional[bool] = Field(None, description="Whether the test failure was cured (if applicable)")


class ReserveAccountResponse(BaseModel):
    """Reserve account response model."""

    year: float = Field(..., description="Year")
    month: int = Field(..., description="Month")
    balance: float = Field(..., description="Reserve account balance")
    target_balance: float = Field(..., description="Target reserve account balance")
    deposits: float = Field(..., description="Deposits to the reserve account")
    withdrawals: float = Field(..., description="Withdrawals from the reserve account")


@router.get("/", response_model=List[TrancheResponse])
async def get_tranches(
    simulation_id: str = Query(..., description="Simulation ID"),
) -> List[Dict[str, Any]]:
    """
    Get all tranches for a simulation.

    Args:
        simulation_id: Simulation ID

    Returns:
        List of tranches
    """
    context = get_simulation_context(simulation_id)
    if not context:
        raise HTTPException(status_code=404, detail="Simulation not found")

    if not hasattr(context, "tranches") or not context.tranches:
        raise HTTPException(status_code=404, detail="No tranches found for this simulation")

    return context.tranches.get("tranche_summary", [])


@router.get("/{tranche_name}/cashflows", response_model=List[TrancheCashflowResponse])
async def get_tranche_cashflows(
    tranche_name: str,
    simulation_id: str = Query(..., description="Simulation ID"),
) -> List[Dict[str, Any]]:
    """
    Get cashflows for a tranche.

    Args:
        tranche_name: Tranche name
        simulation_id: Simulation ID

    Returns:
        List of cashflows
    """
    context = get_simulation_context(simulation_id)
    if not context:
        raise HTTPException(status_code=404, detail="Simulation not found")

    if not hasattr(context, "tranches") or not context.tranches:
        raise HTTPException(status_code=404, detail="No tranches found for this simulation")

    tranche_cashflows = context.tranches.get("tranche_cashflows", {})
    if tranche_name not in tranche_cashflows:
        raise HTTPException(status_code=404, detail=f"Tranche {tranche_name} not found")

    return tranche_cashflows[tranche_name]


@router.get("/{tranche_name}/allocations", response_model=List[TrancheAllocationResponse])
async def get_tranche_allocations(
    tranche_name: str,
    simulation_id: str = Query(..., description="Simulation ID"),
) -> List[Dict[str, Any]]:
    """
    Get loan allocations for a tranche.

    Args:
        tranche_name: Tranche name
        simulation_id: Simulation ID

    Returns:
        List of loan allocations
    """
    context = get_simulation_context(simulation_id)
    if not context:
        raise HTTPException(status_code=404, detail="Simulation not found")

    if not hasattr(context, "tranches") or not context.tranches:
        raise HTTPException(status_code=404, detail="No tranches found for this simulation")

    tranche_allocations = context.tranches.get("tranche_allocations", {})
    if tranche_name not in tranche_allocations:
        raise HTTPException(status_code=404, detail=f"Tranche {tranche_name} not found")

    return tranche_allocations[tranche_name]


@router.get("/coverage-tests", response_model=List[CoverageTestResponse])
async def get_coverage_tests(
    simulation_id: str = Query(..., description="Simulation ID"),
    test_type: Optional[str] = Query(None, description="Test type (overcollateralization, interest_coverage)"),
) -> List[Dict[str, Any]]:
    """
    Get coverage test results.

    Args:
        simulation_id: Simulation ID
        test_type: Test type filter

    Returns:
        List of coverage test results
    """
    context = get_simulation_context(simulation_id)
    if not context:
        raise HTTPException(status_code=404, detail="Simulation not found")

    if not hasattr(context, "tranches") or not context.tranches:
        raise HTTPException(status_code=404, detail="No tranches found for this simulation")

    coverage_tests = context.tranches.get("coverage_tests", [])

    if test_type:
        coverage_tests = [test for test in coverage_tests if test.get("test_type") == test_type]

    return coverage_tests


@router.get("/reserve-account", response_model=List[ReserveAccountResponse])
async def get_reserve_account(
    simulation_id: str = Query(..., description="Simulation ID"),
) -> List[Dict[str, Any]]:
    """
    Get reserve account history.

    Args:
        simulation_id: Simulation ID

    Returns:
        Reserve account history
    """
    context = get_simulation_context(simulation_id)
    if not context:
        raise HTTPException(status_code=404, detail="Simulation not found")

    if not hasattr(context, "tranches") or not context.tranches:
        raise HTTPException(status_code=404, detail="No tranches found for this simulation")

    return context.tranches.get("reserve_account", [])


@router.get("/visualization/waterfall", response_model=List[Dict[str, Any]])
async def get_tranche_waterfall_visualization(
    simulation_id: str = Query(..., description="Simulation ID"),
) -> List[Dict[str, Any]]:
    """
    Get tranche waterfall visualization data.

    Args:
        simulation_id: Simulation ID

    Returns:
        Tranche waterfall visualization data
    """
    context = get_simulation_context(simulation_id)
    if not context:
        raise HTTPException(status_code=404, detail="Simulation not found")

    if not hasattr(context, "tranches") or not context.tranches:
        raise HTTPException(status_code=404, detail="No tranches found for this simulation")

    visualization = context.tranches.get("visualization", {})
    return visualization.get("tranche_waterfall_chart", [])


@router.get("/visualization/cashflow", response_model=Dict[str, List[Dict[str, Any]]])
async def get_tranche_cashflow_visualization(
    simulation_id: str = Query(..., description="Simulation ID"),
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get tranche cashflow visualization data.

    Args:
        simulation_id: Simulation ID

    Returns:
        Tranche cashflow visualization data
    """
    context = get_simulation_context(simulation_id)
    if not context:
        raise HTTPException(status_code=404, detail="Simulation not found")

    if not hasattr(context, "tranches") or not context.tranches:
        raise HTTPException(status_code=404, detail="No tranches found for this simulation")

    visualization = context.tranches.get("visualization", {})
    return visualization.get("tranche_cashflow_chart", {})


@router.get("/visualization/allocation", response_model=List[Dict[str, Any]])
async def get_tranche_allocation_visualization(
    simulation_id: str = Query(..., description="Simulation ID"),
) -> List[Dict[str, Any]]:
    """
    Get tranche allocation visualization data.

    Args:
        simulation_id: Simulation ID

    Returns:
        Tranche allocation visualization data
    """
    context = get_simulation_context(simulation_id)
    if not context:
        raise HTTPException(status_code=404, detail="Simulation not found")

    if not hasattr(context, "tranches") or not context.tranches:
        raise HTTPException(status_code=404, detail="No tranches found for this simulation")

    visualization = context.tranches.get("visualization", {})
    return visualization.get("tranche_allocation_chart", [])


@router.get("/visualization/performance", response_model=List[Dict[str, Any]])
async def get_tranche_performance_visualization(
    simulation_id: str = Query(..., description="Simulation ID"),
) -> List[Dict[str, Any]]:
    """
    Get tranche performance visualization data.

    Args:
        simulation_id: Simulation ID

    Returns:
        Tranche performance visualization data
    """
    context = get_simulation_context(simulation_id)
    if not context:
        raise HTTPException(status_code=404, detail="Simulation not found")

    if not hasattr(context, "tranches") or not context.tranches:
        raise HTTPException(status_code=404, detail="No tranches found for this simulation")

    visualization = context.tranches.get("visualization", {})
    return visualization.get("tranche_performance_chart", [])


@router.get("/visualization/coverage-tests", response_model=Dict[str, List[Dict[str, Any]]])
async def get_coverage_test_visualization(
    simulation_id: str = Query(..., description="Simulation ID"),
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get coverage test visualization data.

    Args:
        simulation_id: Simulation ID

    Returns:
        Coverage test visualization data
    """
    context = get_simulation_context(simulation_id)
    if not context:
        raise HTTPException(status_code=404, detail="Simulation not found")

    if not hasattr(context, "tranches") or not context.tranches:
        raise HTTPException(status_code=404, detail="No tranches found for this simulation")

    visualization = context.tranches.get("visualization", {})
    return visualization.get("coverage_test_chart", {})


@router.get("/visualization/reserve-account", response_model=List[Dict[str, Any]])
async def get_reserve_account_visualization(
    simulation_id: str = Query(..., description="Simulation ID"),
) -> List[Dict[str, Any]]:
    """
    Get reserve account visualization data.

    Args:
        simulation_id: Simulation ID

    Returns:
        Reserve account visualization data
    """
    context = get_simulation_context(simulation_id)
    if not context:
        raise HTTPException(status_code=404, detail="Simulation not found")

    if not hasattr(context, "tranches") or not context.tranches:
        raise HTTPException(status_code=404, detail="No tranches found for this simulation")

    visualization = context.tranches.get("visualization", {})
    return visualization.get("reserve_account_chart", [])
