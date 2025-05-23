"""
Performance Reporter module for the EQU IHOME SIM ENGINE v2.

This module is responsible for generating comprehensive performance reports for the simulation,
including KPI tables, zone allocation reports, cash flow visualizations, risk metric reports,
and export capabilities.
"""

from src.performance_reporter.performance_reporter import PerformanceReporter, ReportFormat

__all__ = ["PerformanceReporter", "ReportFormat", "generate_performance_report"]


async def generate_performance_report(context):
    """
    Generate a comprehensive performance report for the simulation.

    This function is the entry point for the performance reporter module.
    It creates a PerformanceReporter instance and calls the appropriate methods.

    Args:
        context: Simulation context

    Returns:
        Dictionary containing the performance report
    """
    # Create performance reporter
    reporter = PerformanceReporter(context)

    # Generate report
    report = await reporter.generate_report()

    # Store report in context
    context.performance_report = report

    return report