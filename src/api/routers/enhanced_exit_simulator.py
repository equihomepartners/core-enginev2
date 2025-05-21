"""
Enhanced exit simulator API router for the EQU IHOME SIM ENGINE v2.

This module provides API endpoints for the enhanced exit simulator.
"""

from typing import Dict, Any, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from src.engine.simulation_context import SimulationContext
from src.exit_simulator.enhanced_exit_simulator import (
    simulate_enhanced_exits,
    get_enhanced_exit_summary,
)

# In-memory storage for simulations
from src.api.routers.portfolio import simulations

router = APIRouter(
    prefix="/api/v1/simulations",
    tags=["enhanced-exit-simulator"],
)


class EnhancedExitVisualizationResponse(BaseModel):
    """Enhanced exit visualization response model."""
    # Base visualization
    exit_timing_chart: List[Dict[str, Any]] = Field(
        ..., description="Exit timing distribution chart"
    )
    exit_type_chart: List[Dict[str, Any]] = Field(
        ..., description="Exit type distribution chart"
    )
    cumulative_exits_chart: List[Dict[str, Any]] = Field(
        ..., description="Cumulative exits chart"
    )
    exit_roi_chart: List[Dict[str, Any]] = Field(
        ..., description="Exit ROI distribution chart"
    )
    exit_type_roi_chart: List[Dict[str, Any]] = Field(
        ..., description="Exit type ROI chart"
    )
    exit_summary: Dict[str, Any] = Field(
        ..., description="Exit summary"
    )
    exit_value_by_year_chart: List[Dict[str, Any]] = Field(
        ..., description="Exit value by year chart"
    )
    exit_count_by_year_chart: List[Dict[str, Any]] = Field(
        ..., description="Exit count by year chart"
    )

    # Cohort visualizations
    cohort_visualizations: Dict[str, Any] = Field(
        {}, description="Cohort analysis visualizations"
    )

    # Risk visualizations
    risk_visualizations: Dict[str, Any] = Field(
        {}, description="Risk metrics visualizations"
    )

    # Machine learning visualizations
    ml_visualizations: Dict[str, Any] = Field(
        {}, description="Machine learning visualizations"
    )

    # Economic visualizations
    economic_visualizations: Dict[str, Any] = Field(
        {}, description="Economic scenario visualizations"
    )

    # Geospatial visualizations
    geospatial_visualizations: Dict[str, Any] = Field(
        {}, description="Geospatial visualizations"
    )

    # Comparative visualizations
    comparative_visualizations: Dict[str, Any] = Field(
        {}, description="Comparative visualizations"
    )


class EnhancedExitStatisticsResponse(BaseModel):
    """Enhanced exit statistics response model."""
    # Base statistics
    avg_exit_year: float = Field(
        ..., description="Average exit year"
    )
    avg_roi: float = Field(
        ..., description="Average ROI"
    )
    avg_annualized_roi: float = Field(
        ..., description="Average annualized ROI"
    )
    exit_type_distribution: Dict[str, float] = Field(
        ..., description="Exit type distribution"
    )
    exit_timing_distribution: Dict[str, int] = Field(
        ..., description="Exit timing distribution"
    )
    exit_roi_distribution: Dict[str, int] = Field(
        ..., description="Exit ROI distribution"
    )
    exit_type_roi: Dict[str, Dict[str, Any]] = Field(
        ..., description="Exit type ROI"
    )
    exit_value_total: float = Field(
        ..., description="Total exit value"
    )
    appreciation_share_total: float = Field(
        ..., description="Total appreciation share"
    )
    total_return: float = Field(
        ..., description="Total return"
    )
    total_roi: float = Field(
        ..., description="Total ROI"
    )
    annualized_roi: float = Field(
        ..., description="Annualized ROI"
    )

    # Comparison to base
    comparison_to_base: Optional[Dict[str, Any]] = Field(
        None, description="Comparison to base exit statistics"
    )

    # Cohort analysis
    cohort_analysis: Dict[str, Any] = Field(
        {}, description="Cohort analysis"
    )

    # Cohort analysis summary
    cohort_analysis_summary: Dict[str, Any] = Field(
        {}, description="Cohort analysis summary"
    )

    # Risk metrics
    risk_metrics: Dict[str, Any] = Field(
        {}, description="Risk metrics"
    )

    # Machine learning insights
    ml_insights: Dict[str, Any] = Field(
        {}, description="Machine learning insights"
    )


class EnhancedExitScenarioRequest(BaseModel):
    """Enhanced exit scenario request model."""
    # Base exit parameters
    base_exit_rate: float = Field(
        0.1, description="Base annual exit probability"
    )
    time_factor: float = Field(
        0.4, description="Weight for time-based exit probability"
    )
    price_factor: float = Field(
        0.6, description="Weight for price-based exit probability"
    )
    min_hold_period: float = Field(
        1.0, description="Minimum holding period in years"
    )
    max_hold_period: float = Field(
        10.0, description="Maximum holding period in years"
    )
    sale_weight: float = Field(
        0.6, description="Base weight for sale exits"
    )
    refinance_weight: float = Field(
        0.3, description="Base weight for refinance exits"
    )
    default_weight: float = Field(
        0.1, description="Base weight for default exits"
    )
    appreciation_share: float = Field(
        0.2, description="Fund's share of appreciation"
    )

    # Behavioral model parameters
    refinance_interest_rate_sensitivity: float = Field(
        2.0, description="How sensitive refinancing is to interest rate changes"
    )
    sale_appreciation_sensitivity: float = Field(
        1.5, description="How sensitive sales are to appreciation"
    )
    life_event_probability: float = Field(
        0.05, description="Annual probability of life events triggering exits"
    )
    behavioral_correlation: float = Field(
        0.3, description="Correlation in exit decisions (herd behavior)"
    )

    # Economic model parameters
    recession_default_multiplier: float = Field(
        2.5, description="How much recessions increase defaults"
    )
    inflation_refinance_multiplier: float = Field(
        1.8, description="How inflation affects refinancing"
    )
    employment_sensitivity: float = Field(
        1.2, description="How employment affects exits"
    )
    migration_sensitivity: float = Field(
        0.8, description="How population migration affects exits"
    )

    # Regulatory and tax parameters
    regulatory_compliance_cost: float = Field(
        0.01, description="Compliance cost as percentage of loan"
    )
    tax_efficiency_factor: float = Field(
        0.9, description="Tax efficiency factor (1.0 = fully efficient)"
    )

    # Cohort analysis parameters
    vintage_segmentation: bool = Field(
        True, description="Whether to segment by vintage"
    )
    ltv_segmentation: bool = Field(
        True, description="Whether to segment by LTV"
    )
    zone_segmentation: bool = Field(
        True, description="Whether to segment by zone"
    )

    # Risk metrics parameters
    var_confidence_level: float = Field(
        0.95, description="Confidence level for Value-at-Risk"
    )
    stress_test_severity: float = Field(
        0.3, description="Severity of stress tests (0-1)"
    )
    tail_risk_threshold: float = Field(
        0.05, description="Threshold for tail risk events"
    )

    # Machine learning parameters
    use_ml_models: bool = Field(
        True, description="Whether to use machine learning models"
    )
    feature_importance_threshold: float = Field(
        0.05, description="Threshold for important features"
    )
    anomaly_detection_threshold: float = Field(
        3.0, description="Standard deviations for anomaly detection"
    )


@router.get("/{simulation_id}/enhanced-exits")
async def get_enhanced_exits(simulation_id: str) -> Dict[str, Any]:
    """
    Get enhanced exit simulation results.

    Args:
        simulation_id: Simulation ID

    Returns:
        Enhanced exit simulation results
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has enhanced exit data
    if "enhanced_exits" not in simulation:
        raise HTTPException(status_code=404, detail="Enhanced exit data not found")

    return simulation["enhanced_exits"]


@router.get("/{simulation_id}/enhanced-exits/visualization", response_model=EnhancedExitVisualizationResponse)
async def get_enhanced_exit_visualization(simulation_id: str) -> EnhancedExitVisualizationResponse:
    """
    Get enhanced visualization data for exits.

    Args:
        simulation_id: Simulation ID

    Returns:
        Enhanced visualization data
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has enhanced exit visualization data
    if "enhanced_exits" not in simulation or "visualization" not in simulation["enhanced_exits"]:
        raise HTTPException(status_code=404, detail="Enhanced exit visualization data not found")

    return EnhancedExitVisualizationResponse(**simulation["enhanced_exits"]["visualization"])


@router.get("/{simulation_id}/enhanced-exits/statistics", response_model=EnhancedExitStatisticsResponse)
async def get_enhanced_exit_statistics(simulation_id: str) -> EnhancedExitStatisticsResponse:
    """
    Get enhanced statistics for exits.

    Args:
        simulation_id: Simulation ID

    Returns:
        Enhanced statistics data
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has enhanced exit statistics data
    if "enhanced_exits" not in simulation or "statistics" not in simulation["enhanced_exits"]:
        raise HTTPException(status_code=404, detail="Enhanced exit statistics data not found")

    return EnhancedExitStatisticsResponse(**simulation["enhanced_exits"]["statistics"])


@router.post("/{simulation_id}/enhanced-exits/scenario")
async def run_enhanced_exit_scenario(
    simulation_id: str,
    request: EnhancedExitScenarioRequest
) -> Dict[str, Any]:
    """
    Run an enhanced exit scenario with custom parameters.

    Args:
        simulation_id: Simulation ID
        request: Enhanced exit scenario request

    Returns:
        Enhanced exit scenario results
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has a context
    if "context" not in simulation:
        raise HTTPException(status_code=400, detail="Simulation context not found")

    # Get simulation context
    context = simulation["context"]

    # Update context with scenario parameters
    # Base exit parameters
    context.config.exit_simulator = {
        "base_exit_rate": request.base_exit_rate,
        "time_factor": request.time_factor,
        "price_factor": request.price_factor,
        "min_hold_period": request.min_hold_period,
        "max_hold_period": request.max_hold_period,
        "sale_weight": request.sale_weight,
        "refinance_weight": request.refinance_weight,
        "default_weight": request.default_weight,
        "appreciation_share": request.appreciation_share,
    }

    # Enhanced exit parameters
    context.config.enhanced_exit_simulator = {
        # Behavioral model parameters
        "refinance_interest_rate_sensitivity": request.refinance_interest_rate_sensitivity,
        "sale_appreciation_sensitivity": request.sale_appreciation_sensitivity,
        "life_event_probability": request.life_event_probability,
        "behavioral_correlation": request.behavioral_correlation,

        # Economic model parameters
        "recession_default_multiplier": request.recession_default_multiplier,
        "inflation_refinance_multiplier": request.inflation_refinance_multiplier,
        "employment_sensitivity": request.employment_sensitivity,
        "migration_sensitivity": request.migration_sensitivity,

        # Regulatory and tax parameters
        "regulatory_compliance_cost": request.regulatory_compliance_cost,
        "tax_efficiency_factor": request.tax_efficiency_factor,

        # Cohort analysis parameters
        "vintage_segmentation": request.vintage_segmentation,
        "ltv_segmentation": request.ltv_segmentation,
        "zone_segmentation": request.zone_segmentation,

        # Risk metrics parameters
        "var_confidence_level": request.var_confidence_level,
        "stress_test_severity": request.stress_test_severity,
        "tail_risk_threshold": request.tail_risk_threshold,

        # Machine learning parameters
        "use_ml_models": request.use_ml_models,
        "feature_importance_threshold": request.feature_importance_threshold,
        "anomaly_detection_threshold": request.anomaly_detection_threshold,
    }

    # Run enhanced exit simulation
    try:
        await simulate_enhanced_exits(context)

        # Get enhanced exit summary
        summary = await get_enhanced_exit_summary(context)

        # Update simulation data
        simulation["enhanced_exits"] = summary

        return summary

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
