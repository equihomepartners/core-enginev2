"""
Finance API router for the EQU IHOME SIM ENGINE v2.

This router handles finance-related API endpoints, including fees, cashflows, and waterfall.
"""

from typing import Dict, Any, List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends, Query, Path
from pydantic import BaseModel, Field

from src.engine.simulation_context import SimulationContext, get_simulation_context
from src.engine.orchestrator import get_orchestrator
from src.fee_engine.fee_engine import FeeEngine
from src.cashflow_aggregator.cashflow_aggregator import CashflowAggregator

# Create router
router = APIRouter(
    prefix="/finance",
    tags=["finance"],
)


# Pydantic models for request and response
class FeeCalculationRequest(BaseModel):
    """Request model for fee calculation."""

    simulation_id: str = Field(..., description="Simulation ID")

    # Optional fee engine parameters to override
    management_fee_rate: Optional[float] = Field(None, description="Management fee rate (0-1)")
    management_fee_basis: Optional[str] = Field(
        None,
        description="Basis for management fee calculation",
        enum=["committed_capital", "invested_capital", "net_asset_value"],
    )
    origination_fee_rate: Optional[float] = Field(None, description="Origination fee rate (0-1)")
    annual_fund_expenses: Optional[float] = Field(None, description="Annual fund expenses as percentage of fund size (0-1)")
    fixed_annual_expenses: Optional[float] = Field(None, description="Fixed annual expenses in dollars")
    expense_growth_rate: Optional[float] = Field(None, description="Annual growth rate for expenses (0-1)")
    acquisition_fee_rate: Optional[float] = Field(None, description="Acquisition fee rate (0-1)")
    disposition_fee_rate: Optional[float] = Field(None, description="Disposition fee rate (0-1)")
    setup_costs: Optional[float] = Field(None, description="One-time setup costs in dollars")


class FeeBreakdownItem(BaseModel):
    """Fee breakdown item model."""

    category: str = Field(..., description="Fee category")
    amount: float = Field(..., description="Fee amount")
    percentage: float = Field(..., description="Percentage of total fees")


class FeesByYearItem(BaseModel):
    """Fees by year item model."""

    year: int = Field(..., description="Year")
    management_fees: float = Field(..., description="Management fees")
    origination_fees: float = Field(..., description="Origination fees")
    fund_expenses: float = Field(..., description="Fund expenses")
    acquisition_fees: float = Field(..., description="Acquisition fees")
    disposition_fees: float = Field(..., description="Disposition fees")
    setup_costs: float = Field(..., description="Setup costs")
    total: float = Field(..., description="Total fees")


class FeeImpactItem(BaseModel):
    """Fee impact item model."""

    metric: str = Field(..., description="Performance metric")
    gross: float = Field(..., description="Gross value (before fees)")
    net: float = Field(..., description="Net value (after fees)")
    impact: float = Field(..., description="Impact of fees")


class FeeVisualization(BaseModel):
    """Fee visualization model."""

    fee_breakdown_chart: List[FeeBreakdownItem] = Field(..., description="Fee breakdown chart data")
    fees_by_year_chart: List[FeesByYearItem] = Field(..., description="Fees by year chart data")
    fee_impact_chart: List[FeeImpactItem] = Field(..., description="Fee impact chart data")
    fee_table: List[FeesByYearItem] = Field(..., description="Fee table data")


class FeeCalculationResponse(BaseModel):
    """Response model for fee calculation."""

    simulation_id: str = Field(..., description="Simulation ID")
    total_fees: Dict[str, float] = Field(..., description="Total fees by category")
    fee_impact: Dict[str, float] = Field(..., description="Impact of fees on fund performance")
    visualization: FeeVisualization = Field(..., description="Visualization data")


@router.post("/fees/calculate", response_model=FeeCalculationResponse)
async def calculate_fees(
    request: FeeCalculationRequest,
    context: SimulationContext = Depends(get_simulation_context),
) -> Dict[str, Any]:
    """
    Calculate fees for a simulation.

    This endpoint calculates fees for a simulation, including management fees,
    origination fees, fund expenses, acquisition fees, and disposition fees.

    Args:
        request: Fee calculation request
        context: Simulation context

    Returns:
        Fee calculation response
    """
    # Get simulation ID
    simulation_id = request.simulation_id

    # Check if simulation exists
    if not context or context.run_id != simulation_id:
        raise HTTPException(
            status_code=404,
            detail=f"Simulation {simulation_id} not found",
        )

    # Override fee parameters if provided
    if request.management_fee_rate is not None:
        context.config.management_fee_rate = request.management_fee_rate

    if request.management_fee_basis is not None:
        context.config.management_fee_basis = request.management_fee_basis

    # Override fee engine parameters if provided
    fee_config = getattr(context.config, "fee_engine", {})

    if request.origination_fee_rate is not None:
        fee_config["origination_fee_rate"] = request.origination_fee_rate

    if request.annual_fund_expenses is not None:
        fee_config["annual_fund_expenses"] = request.annual_fund_expenses

    if request.fixed_annual_expenses is not None:
        fee_config["fixed_annual_expenses"] = request.fixed_annual_expenses

    if request.expense_growth_rate is not None:
        fee_config["expense_growth_rate"] = request.expense_growth_rate

    if request.acquisition_fee_rate is not None:
        fee_config["acquisition_fee_rate"] = request.acquisition_fee_rate

    if request.disposition_fee_rate is not None:
        fee_config["disposition_fee_rate"] = request.disposition_fee_rate

    if request.setup_costs is not None:
        fee_config["setup_costs"] = request.setup_costs

    # Update fee config
    context.config.fee_engine = fee_config

    # Create fee engine
    fee_engine = FeeEngine(context)

    # Calculate fees
    results = fee_engine.calculate_fees()

    # Create response
    response = {
        "simulation_id": simulation_id,
        "total_fees": results["total_fees"],
        "fee_impact": results["fee_impact"],
        "visualization": results["visualization"],
    }

    return response


@router.get("/fees/{simulation_id}", response_model=FeeCalculationResponse)
async def get_fees(
    simulation_id: str = Path(..., description="Simulation ID"),
    context: SimulationContext = Depends(get_simulation_context),
) -> Dict[str, Any]:
    """
    Get fee calculation results for a simulation.

    This endpoint retrieves fee calculation results for a simulation.

    Args:
        simulation_id: Simulation ID
        context: Simulation context

    Returns:
        Fee calculation response
    """
    # Check if simulation exists
    if not context or context.run_id != simulation_id:
        raise HTTPException(
            status_code=404,
            detail=f"Simulation {simulation_id} not found",
        )

    # Check if fee results exist
    if not hasattr(context, "fee_results") or not context.fee_results:
        raise HTTPException(
            status_code=404,
            detail=f"Fee results for simulation {simulation_id} not found",
        )

    # Get fee results
    results = context.fee_results

    # Create response
    response = {
        "simulation_id": simulation_id,
        "total_fees": results["total_fees"],
        "fee_impact": results["fee_impact"],
        "visualization": results["visualization"],
    }

    return response


# Cashflow-related models
class CashflowCalculationRequest(BaseModel):
    """Request model for cashflow calculation."""

    simulation_id: str = Field(..., description="Simulation ID")

    # Optional cashflow aggregator parameters to override
    time_granularity: Optional[str] = Field(
        None,
        description="Time granularity for cashflow aggregation",
        enum=["daily", "monthly", "quarterly", "yearly"],
    )
    include_loan_level_cashflows: Optional[bool] = Field(
        None,
        description="Whether to include loan-level cashflows in the results",
    )
    include_fund_level_cashflows: Optional[bool] = Field(
        None,
        description="Whether to include fund-level cashflows in the results",
    )
    include_stakeholder_cashflows: Optional[bool] = Field(
        None,
        description="Whether to include stakeholder-level cashflows in the results",
    )
    simple_interest_rate: Optional[float] = Field(
        None,
        description="Simple interest rate for loans (0-1)",
    )
    origination_fee_rate: Optional[float] = Field(
        None,
        description="Origination fee rate (0-1)",
    )
    appreciation_share_method: Optional[str] = Field(
        None,
        description="Method for calculating appreciation share",
        enum=["pro_rata_ltv", "tiered", "fixed"],
    )
    distribution_frequency: Optional[str] = Field(
        None,
        description="Frequency of distributions to investors",
        enum=["monthly", "quarterly", "semi_annual", "annual"],
    )
    distribution_lag: Optional[int] = Field(
        None,
        description="Lag in months between cashflow receipt and distribution",
    )
    enable_parallel_processing: Optional[bool] = Field(
        None,
        description="Whether to enable parallel processing for loan-level cashflow calculations",
    )
    num_workers: Optional[int] = Field(
        None,
        description="Number of worker processes for parallel processing",
    )
    enable_scenario_analysis: Optional[bool] = Field(
        None,
        description="Whether to enable scenario analysis",
    )
    scenarios: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Scenarios for scenario analysis",
    )
    enable_sensitivity_analysis: Optional[bool] = Field(
        None,
        description="Whether to enable sensitivity analysis",
    )
    sensitivity_parameters: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Parameters to vary for sensitivity analysis",
    )
    enable_cashflow_metrics: Optional[bool] = Field(
        None,
        description="Whether to enable cashflow metrics calculation",
    )
    discount_rate: Optional[float] = Field(
        None,
        description="Discount rate for DCF calculations (0-1)",
    )
    enable_tax_impact_analysis: Optional[bool] = Field(
        None,
        description="Whether to enable tax impact analysis",
    )
    tax_rates: Optional[Dict[str, float]] = Field(
        None,
        description="Tax rates for different income types",
    )
    enable_reinvestment_modeling: Optional[bool] = Field(
        None,
        description="Whether to enable reinvestment modeling",
    )
    reinvestment_rate: Optional[float] = Field(
        None,
        description="Rate of return on reinvested cashflows (0-1)",
    )
    enable_liquidity_analysis: Optional[bool] = Field(
        None,
        description="Whether to enable liquidity analysis",
    )
    minimum_cash_reserve: Optional[float] = Field(
        None,
        description="Minimum cash reserve as percentage of fund size (0-1)",
    )
    enable_export: Optional[bool] = Field(
        None,
        description="Whether to enable export capabilities",
    )
    export_formats: Optional[List[str]] = Field(
        None,
        description="Export formats",
    )


class LoanLevelCashflow(BaseModel):
    """Loan-level cashflow model."""

    loan_id: str = Field(..., description="Loan ID")
    origination: Dict[str, Any] = Field(..., description="Origination cashflows")
    exit: Optional[Dict[str, Any]] = Field(None, description="Exit cashflows")


class FundLevelCashflow(BaseModel):
    """Fund-level cashflow model."""

    year: int = Field(..., description="Year")
    month: Optional[int] = Field(None, description="Month (if applicable)")
    quarter: Optional[int] = Field(None, description="Quarter (if applicable)")
    capital_calls: float = Field(..., description="Capital calls")
    loan_investments: float = Field(..., description="Loan investments")
    origination_fees: float = Field(..., description="Origination fees")
    principal_repayments: float = Field(..., description="Principal repayments")
    interest_income: float = Field(..., description="Interest income")
    appreciation_share: float = Field(..., description="Appreciation share")
    management_fees: float = Field(..., description="Management fees")
    fund_expenses: float = Field(..., description="Fund expenses")
    leverage_draws: float = Field(..., description="Leverage draws")
    leverage_repayments: float = Field(..., description="Leverage repayments")
    leverage_interest: float = Field(..., description="Leverage interest")
    distributions: float = Field(..., description="Distributions")
    net_cashflow: float = Field(..., description="Net cashflow")
    cumulative_cashflow: float = Field(..., description="Cumulative cashflow")


class StakeholderCashflow(BaseModel):
    """Stakeholder cashflow model."""

    year: int = Field(..., description="Year")
    month: Optional[int] = Field(None, description="Month (if applicable)")
    quarter: Optional[int] = Field(None, description="Quarter (if applicable)")
    capital_calls: float = Field(..., description="Capital calls")
    distributions: float = Field(..., description="Distributions")
    net_cashflow: float = Field(..., description="Net cashflow")
    cumulative_cashflow: float = Field(..., description="Cumulative cashflow")


class GPCashflow(BaseModel):
    """GP cashflow model."""

    year: int = Field(..., description="Year")
    month: Optional[int] = Field(None, description="Month (if applicable)")
    quarter: Optional[int] = Field(None, description="Quarter (if applicable)")
    capital_calls: float = Field(..., description="Capital calls")
    management_fees: float = Field(..., description="Management fees")
    origination_fees: float = Field(..., description="Origination fees")
    carried_interest: float = Field(..., description="Carried interest")
    distributions: float = Field(..., description="Distributions")
    net_cashflow: float = Field(..., description="Net cashflow")
    cumulative_cashflow: float = Field(..., description="Cumulative cashflow")


class CashflowWaterfallItem(BaseModel):
    """Cashflow waterfall item model."""

    category: str = Field(..., description="Cashflow category")
    amount: float = Field(..., description="Cashflow amount")


class CashflowByYearItem(BaseModel):
    """Cashflow by year item model."""

    year: int = Field(..., description="Year")
    inflows: float = Field(..., description="Total inflows")
    outflows: float = Field(..., description="Total outflows")
    net: float = Field(..., description="Net cashflow")


class CumulativeCashflowItem(BaseModel):
    """Cumulative cashflow item model."""

    year: int = Field(..., description="Year")
    cumulative_cashflow: float = Field(..., description="Cumulative cashflow")


class CashflowTableItem(BaseModel):
    """Cashflow table item model."""

    year: int = Field(..., description="Year")
    capital_calls: float = Field(..., description="Capital calls")
    loan_investments: float = Field(..., description="Loan investments")
    origination_fees: float = Field(..., description="Origination fees")
    principal_repayments: float = Field(..., description="Principal repayments")
    interest_income: float = Field(..., description="Interest income")
    appreciation_share: float = Field(..., description="Appreciation share")
    management_fees: float = Field(..., description="Management fees")
    fund_expenses: float = Field(..., description="Fund expenses")
    distributions: float = Field(..., description="Distributions")
    net_cashflow: float = Field(..., description="Net cashflow")
    cumulative_cashflow: float = Field(..., description="Cumulative cashflow")


class CashflowHeatmapItem(BaseModel):
    """Cashflow heatmap item model."""

    year: int = Field(..., description="Year")
    month: int = Field(..., description="Month")
    category: str = Field(..., description="Cashflow category")
    amount: float = Field(..., description="Cashflow amount")


class SankeyNode(BaseModel):
    """Sankey diagram node model."""

    id: str = Field(..., description="Node ID")
    name: str = Field(..., description="Node name")


class SankeyLink(BaseModel):
    """Sankey diagram link model."""

    source: str = Field(..., description="Source node ID")
    target: str = Field(..., description="Target node ID")
    value: float = Field(..., description="Link value")


class CashflowSankey(BaseModel):
    """Cashflow Sankey diagram model."""

    nodes: List[SankeyNode] = Field(..., description="Nodes in the Sankey diagram")
    links: List[SankeyLink] = Field(..., description="Links in the Sankey diagram")


class ScenarioComparisonItem(BaseModel):
    """Scenario comparison item model."""

    scenario: str = Field(..., description="Scenario name")
    metric: str = Field(..., description="Metric name")
    value: float = Field(..., description="Metric value")


class CashflowVisualization(BaseModel):
    """Cashflow visualization model."""

    cashflow_waterfall_chart: List[CashflowWaterfallItem] = Field(..., description="Cashflow waterfall chart data")
    cashflow_by_year_chart: List[CashflowByYearItem] = Field(..., description="Cashflow by year chart data")
    cumulative_cashflow_chart: List[CumulativeCashflowItem] = Field(..., description="Cumulative cashflow chart data")
    cashflow_table: List[CashflowTableItem] = Field(..., description="Cashflow table data")
    cashflow_heatmap: Optional[List[CashflowHeatmapItem]] = Field(None, description="Cashflow heatmap data")
    cashflow_sankey: Optional[CashflowSankey] = Field(None, description="Cashflow Sankey diagram data")
    scenario_comparison_chart: Optional[List[ScenarioComparisonItem]] = Field(None, description="Scenario comparison chart data")


class FundLevelMetrics(BaseModel):
    """Fund-level metrics model."""

    irr: float = Field(..., description="Internal Rate of Return")
    moic: float = Field(..., description="Multiple on Invested Capital")
    tvpi: float = Field(..., description="Total Value to Paid-In")
    dpi: float = Field(..., description="Distributions to Paid-In")
    rvpi: float = Field(..., description="Residual Value to Paid-In")
    payback_period: float = Field(..., description="Payback period in years")
    cash_on_cash: float = Field(..., description="Cash-on-cash return")
    npv: float = Field(..., description="Net Present Value")
    profitability_index: float = Field(..., description="Profitability Index")
    cash_yield: float = Field(..., description="Cash yield")


class LPMetrics(BaseModel):
    """LP metrics model."""

    irr: float = Field(..., description="Internal Rate of Return")
    moic: float = Field(..., description="Multiple on Invested Capital")
    tvpi: float = Field(..., description="Total Value to Paid-In")
    dpi: float = Field(..., description="Distributions to Paid-In")
    rvpi: float = Field(..., description="Residual Value to Paid-In")
    payback_period: float = Field(..., description="Payback period in years")


class GPMetrics(BaseModel):
    """GP metrics model."""

    irr: float = Field(..., description="Internal Rate of Return")
    moic: float = Field(..., description="Multiple on Invested Capital")
    tvpi: float = Field(..., description="Total Value to Paid-In")
    dpi: float = Field(..., description="Distributions to Paid-In")
    rvpi: float = Field(..., description="Residual Value to Paid-In")
    payback_period: float = Field(..., description="Payback period in years")
    carried_interest: float = Field(..., description="Total carried interest")
    management_fees: float = Field(..., description="Total management fees")
    origination_fees: float = Field(..., description="Total origination fees")


class MetricsByYear(BaseModel):
    """Metrics by year model."""

    year: int = Field(..., description="Year")
    dpi: float = Field(..., description="Distributions to Paid-In")
    rvpi: float = Field(..., description="Residual Value to Paid-In")
    tvpi: float = Field(..., description="Total Value to Paid-In")
    irr: float = Field(..., description="Internal Rate of Return")
    cash_yield: float = Field(..., description="Cash yield")


class CashflowMetrics(BaseModel):
    """Cashflow metrics model."""

    fund_level_metrics: FundLevelMetrics = Field(..., description="Fund-level metrics")
    lp_metrics: LPMetrics = Field(..., description="LP metrics")
    gp_metrics: GPMetrics = Field(..., description="GP metrics")
    metrics_by_year: List[MetricsByYear] = Field(..., description="Metrics by year")


class ParameterVariation(BaseModel):
    """Parameter variation model."""

    parameter: str = Field(..., description="Parameter name")
    value: float = Field(..., description="Parameter value")
    metrics: Dict[str, float] = Field(..., description="Metrics for this parameter value")


class TornadoChartItem(BaseModel):
    """Tornado chart item model."""

    parameter: str = Field(..., description="Parameter name")
    low_value: float = Field(..., description="Low parameter value")
    high_value: float = Field(..., description="High parameter value")
    low_metric: float = Field(..., description="Metric value at low parameter value")
    high_metric: float = Field(..., description="Metric value at high parameter value")
    base_metric: float = Field(..., description="Metric value at base parameter value")
    metric_name: str = Field(..., description="Metric name")


class SensitivityAnalysis(BaseModel):
    """Sensitivity analysis model."""

    parameter_variations: List[ParameterVariation] = Field(..., description="Parameter variations")
    tornado_chart: List[TornadoChartItem] = Field(..., description="Tornado chart data")


class ScenarioResult(BaseModel):
    """Scenario result model."""

    name: str = Field(..., description="Scenario name")
    description: str = Field(..., description="Scenario description")
    metrics: Dict[str, float] = Field(..., description="Metrics for this scenario")
    cashflows: List[Dict[str, float]] = Field(..., description="Cashflows for this scenario")


class ScenarioAnalysis(BaseModel):
    """Scenario analysis model."""

    scenarios: List[ScenarioResult] = Field(..., description="Scenario results")


class TaxCashflow(BaseModel):
    """Tax cashflow model."""

    year: int = Field(..., description="Year")
    net_cashflow: float = Field(..., description="Net cashflow")
    tax_amount: Optional[float] = Field(None, description="Tax amount")


class TaxMetrics(BaseModel):
    """Tax metrics model."""

    pre_tax_irr: float = Field(..., description="Pre-tax IRR")
    post_tax_irr: float = Field(..., description="Post-tax IRR")
    pre_tax_npv: float = Field(..., description="Pre-tax NPV")
    post_tax_npv: float = Field(..., description="Post-tax NPV")
    total_tax_amount: float = Field(..., description="Total tax amount")
    effective_tax_rate: float = Field(..., description="Effective tax rate")


class TaxImpactAnalysis(BaseModel):
    """Tax impact analysis model."""

    pre_tax_cashflows: List[TaxCashflow] = Field(..., description="Pre-tax cashflows by year")
    post_tax_cashflows: List[TaxCashflow] = Field(..., description="Post-tax cashflows by year")
    tax_metrics: TaxMetrics = Field(..., description="Tax metrics")


class CashReserve(BaseModel):
    """Cash reserve model."""

    year: int = Field(..., description="Year")
    month: int = Field(..., description="Month")
    cash_reserve: float = Field(..., description="Cash reserve")
    minimum_required: float = Field(..., description="Minimum required cash reserve")
    shortfall: float = Field(..., description="Shortfall (if any)")


class LiquidityMetrics(BaseModel):
    """Liquidity metrics model."""

    min_cash_reserve: float = Field(..., description="Minimum cash reserve")
    max_cash_reserve: float = Field(..., description="Maximum cash reserve")
    avg_cash_reserve: float = Field(..., description="Average cash reserve")
    num_shortfall_periods: int = Field(..., description="Number of periods with shortfall")
    max_shortfall: float = Field(..., description="Maximum shortfall")


class LiquidityAnalysis(BaseModel):
    """Liquidity analysis model."""

    cash_reserves: List[CashReserve] = Field(..., description="Cash reserves by year")
    liquidity_metrics: LiquidityMetrics = Field(..., description="Liquidity metrics")


class CashflowCalculationResponse(BaseModel):
    """Response model for cashflow calculation."""

    simulation_id: str = Field(..., description="Simulation ID")
    loan_level_cashflows: Optional[List[LoanLevelCashflow]] = Field(None, description="Loan-level cashflows")
    fund_level_cashflows: List[FundLevelCashflow] = Field(..., description="Fund-level cashflows")
    stakeholder_cashflows: Dict[str, List[Any]] = Field(..., description="Stakeholder cashflows")
    visualization: CashflowVisualization = Field(..., description="Visualization data")
    metrics: Optional[CashflowMetrics] = Field(None, description="Cashflow metrics")
    sensitivity_analysis: Optional[SensitivityAnalysis] = Field(None, description="Sensitivity analysis results")
    scenario_analysis: Optional[ScenarioAnalysis] = Field(None, description="Scenario analysis results")
    tax_impact: Optional[TaxImpactAnalysis] = Field(None, description="Tax impact analysis results")
    liquidity_analysis: Optional[LiquidityAnalysis] = Field(None, description="Liquidity analysis results")


@router.post("/cashflows/calculate", response_model=CashflowCalculationResponse)
async def calculate_cashflows(
    request: CashflowCalculationRequest,
    context: SimulationContext = Depends(get_simulation_context),
) -> Dict[str, Any]:
    """
    Calculate cashflows for a simulation.

    This endpoint calculates cashflows for a simulation, including loan-level cashflows,
    fund-level cashflows, and stakeholder cashflows.

    Args:
        request: Cashflow calculation request
        context: Simulation context

    Returns:
        Cashflow calculation response
    """
    # Get simulation ID
    simulation_id = request.simulation_id

    # Check if simulation exists
    if not context or context.run_id != simulation_id:
        raise HTTPException(
            status_code=404,
            detail=f"Simulation {simulation_id} not found",
        )

    # Override cashflow parameters if provided
    cashflow_config = getattr(context.config, "cashflow_aggregator", {})

    # Basic parameters
    if request.time_granularity is not None:
        cashflow_config["time_granularity"] = request.time_granularity

    if request.include_loan_level_cashflows is not None:
        cashflow_config["include_loan_level_cashflows"] = request.include_loan_level_cashflows

    if request.include_fund_level_cashflows is not None:
        cashflow_config["include_fund_level_cashflows"] = request.include_fund_level_cashflows

    if request.include_stakeholder_cashflows is not None:
        cashflow_config["include_stakeholder_cashflows"] = request.include_stakeholder_cashflows

    if request.simple_interest_rate is not None:
        cashflow_config["simple_interest_rate"] = request.simple_interest_rate

    if request.origination_fee_rate is not None:
        cashflow_config["origination_fee_rate"] = request.origination_fee_rate

    if request.appreciation_share_method is not None:
        cashflow_config["appreciation_share_method"] = request.appreciation_share_method

    if request.distribution_frequency is not None:
        cashflow_config["distribution_frequency"] = request.distribution_frequency

    if request.distribution_lag is not None:
        cashflow_config["distribution_lag"] = request.distribution_lag

    # Parallel processing parameters
    if request.enable_parallel_processing is not None:
        cashflow_config["enable_parallel_processing"] = request.enable_parallel_processing

    if request.num_workers is not None:
        cashflow_config["num_workers"] = request.num_workers

    # Scenario analysis parameters
    if request.enable_scenario_analysis is not None:
        cashflow_config["enable_scenario_analysis"] = request.enable_scenario_analysis

    if request.scenarios is not None:
        cashflow_config["scenarios"] = request.scenarios

    # Sensitivity analysis parameters
    if request.enable_sensitivity_analysis is not None:
        cashflow_config["enable_sensitivity_analysis"] = request.enable_sensitivity_analysis

    if request.sensitivity_parameters is not None:
        cashflow_config["sensitivity_parameters"] = request.sensitivity_parameters

    # Cashflow metrics parameters
    if request.enable_cashflow_metrics is not None:
        cashflow_config["enable_cashflow_metrics"] = request.enable_cashflow_metrics

    if request.discount_rate is not None:
        cashflow_config["discount_rate"] = request.discount_rate

    # Tax impact analysis parameters
    if request.enable_tax_impact_analysis is not None:
        cashflow_config["enable_tax_impact_analysis"] = request.enable_tax_impact_analysis

    if request.tax_rates is not None:
        cashflow_config["tax_rates"] = request.tax_rates

    # Reinvestment modeling parameters
    if request.enable_reinvestment_modeling is not None:
        cashflow_config["enable_reinvestment_modeling"] = request.enable_reinvestment_modeling

    if request.reinvestment_rate is not None:
        cashflow_config["reinvestment_rate"] = request.reinvestment_rate

    # Liquidity analysis parameters
    if request.enable_liquidity_analysis is not None:
        cashflow_config["enable_liquidity_analysis"] = request.enable_liquidity_analysis

    if request.minimum_cash_reserve is not None:
        cashflow_config["minimum_cash_reserve"] = request.minimum_cash_reserve

    # Export parameters
    if request.enable_export is not None:
        cashflow_config["enable_export"] = request.enable_export

    if request.export_formats is not None:
        cashflow_config["export_formats"] = request.export_formats

    # Update cashflow config
    context.config.cashflow_aggregator = cashflow_config

    # Create cashflow aggregator
    aggregator = CashflowAggregator(context)

    # Run cashflow aggregator
    aggregator.run()

    # Get cashflow results
    results = context.cashflows

    # Create response
    response = {
        "simulation_id": simulation_id,
        "loan_level_cashflows": results["loan_level_cashflows"] if cashflow_config.get("include_loan_level_cashflows", True) else None,
        "fund_level_cashflows": results["fund_level_cashflows"],
        "stakeholder_cashflows": results["stakeholder_cashflows"],
        "visualization": results["visualization"],
    }

    # Add metrics if available
    if "metrics" in results and cashflow_config.get("enable_cashflow_metrics", True):
        response["metrics"] = results["metrics"]

    # Add sensitivity analysis results if available
    if "sensitivity_analysis" in results and cashflow_config.get("enable_sensitivity_analysis", False):
        response["sensitivity_analysis"] = results["sensitivity_analysis"]

    # Add scenario analysis results if available
    if "scenario_analysis" in results and cashflow_config.get("enable_scenario_analysis", False):
        response["scenario_analysis"] = results["scenario_analysis"]

    # Add tax impact analysis results if available
    if "tax_impact" in results and cashflow_config.get("enable_tax_impact_analysis", False):
        response["tax_impact"] = results["tax_impact"]

    # Add liquidity analysis results if available
    if "liquidity_analysis" in results and cashflow_config.get("enable_liquidity_analysis", True):
        response["liquidity_analysis"] = results["liquidity_analysis"]

    return response


@router.get("/cashflows/{simulation_id}", response_model=CashflowCalculationResponse)
async def get_cashflows(
    simulation_id: str = Path(..., description="Simulation ID"),
    context: SimulationContext = Depends(get_simulation_context),
) -> Dict[str, Any]:
    """
    Get cashflow calculation results for a simulation.

    This endpoint retrieves cashflow calculation results for a simulation.

    Args:
        simulation_id: Simulation ID
        context: Simulation context

    Returns:
        Cashflow calculation response
    """
    # Check if simulation exists
    if not context or context.run_id != simulation_id:
        raise HTTPException(
            status_code=404,
            detail=f"Simulation {simulation_id} not found",
        )

    # Check if cashflow results exist
    if not hasattr(context, "cashflows") or not context.cashflows:
        raise HTTPException(
            status_code=404,
            detail=f"Cashflow results for simulation {simulation_id} not found",
        )

    # Get cashflow results
    results = context.cashflows

    # Get cashflow config
    cashflow_config = getattr(context.config, "cashflow_aggregator", {})

    # Create response
    response = {
        "simulation_id": simulation_id,
        "loan_level_cashflows": results["loan_level_cashflows"] if cashflow_config.get("include_loan_level_cashflows", True) else None,
        "fund_level_cashflows": results["fund_level_cashflows"],
        "stakeholder_cashflows": results["stakeholder_cashflows"],
        "visualization": results["visualization"],
    }

    # Add metrics if available
    if "metrics" in results and cashflow_config.get("enable_cashflow_metrics", True):
        response["metrics"] = results["metrics"]

    # Add sensitivity analysis results if available
    if "sensitivity_analysis" in results and cashflow_config.get("enable_sensitivity_analysis", False):
        response["sensitivity_analysis"] = results["sensitivity_analysis"]

    # Add scenario analysis results if available
    if "scenario_analysis" in results and cashflow_config.get("enable_scenario_analysis", False):
        response["scenario_analysis"] = results["scenario_analysis"]

    # Add tax impact analysis results if available
    if "tax_impact" in results and cashflow_config.get("enable_tax_impact_analysis", False):
        response["tax_impact"] = results["tax_impact"]

    # Add liquidity analysis results if available
    if "liquidity_analysis" in results and cashflow_config.get("enable_liquidity_analysis", True):
        response["liquidity_analysis"] = results["liquidity_analysis"]

    return response