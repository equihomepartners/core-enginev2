"""
Metrics module for the EQU IHOME SIM ENGINE v2.

This module provides utilities for exporting metrics to Prometheus.
"""

import os
import time
from typing import Dict, Any, Optional, Callable

import structlog
from prometheus_client import Counter, Gauge, Histogram, start_http_server

logger = structlog.get_logger(__name__)

# Metrics registry
_metrics: Dict[str, Any] = {}

# Flag to track if metrics server has been started
_metrics_server_started = False


def init_metrics() -> None:
    """Initialize metrics."""
    global _metrics
    
    # Runtime metrics
    _metrics["simulation_runs_total"] = Counter(
        "simulation_runs_total",
        "Total number of simulation runs",
        ["status"],
    )
    
    _metrics["simulation_runtime_seconds"] = Histogram(
        "simulation_runtime_seconds",
        "Simulation runtime in seconds",
        ["type"],
        buckets=(1, 5, 10, 30, 60, 120, 300, 600, 1800, 3600),
    )
    
    _metrics["active_simulations"] = Gauge(
        "active_simulations",
        "Number of active simulations",
    )
    
    _metrics["loans_generated_total"] = Counter(
        "loans_generated_total",
        "Total number of loans generated",
        ["zone"],
    )
    
    # Business metrics
    _metrics["irr_distribution"] = Histogram(
        "irr_distribution",
        "Distribution of IRR values",
        buckets=(-0.1, 0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4),
    )
    
    _metrics["equity_multiple_distribution"] = Histogram(
        "equity_multiple_distribution",
        "Distribution of equity multiple values",
        buckets=(0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 4.0, 5.0),
    )
    
    _metrics["var_95_distribution"] = Histogram(
        "var_95_distribution",
        "Distribution of VaR (95%) values",
        buckets=(0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.1, 0.15, 0.2, 0.3),
    )
    
    _metrics["guardrail_violations_total"] = Counter(
        "guardrail_violations_total",
        "Total number of guardrail violations",
        ["guardrail"],
    )
    
    _metrics["memory_usage_bytes"] = Gauge(
        "memory_usage_bytes",
        "Memory usage in bytes",
    )
    
    logger.info("Metrics initialized")


def start_metrics_server() -> None:
    """Start the Prometheus metrics server."""
    global _metrics_server_started
    
    if _metrics_server_started:
        return
    
    # Check if metrics are enabled
    if "ENABLE_PROMETHEUS" not in os.environ.get("SIM_FEATURES", "").split(","):
        logger.info("Prometheus metrics disabled")
        return
    
    # Initialize metrics if not already initialized
    if not _metrics:
        init_metrics()
    
    # Start the server
    port = int(os.environ.get("SIM_METRICS_PORT", "9090"))
    start_http_server(port)
    _metrics_server_started = True
    
    logger.info("Metrics server started", port=port)


def get_metric(name: str) -> Any:
    """
    Get a metric by name.
    
    Args:
        name: Metric name
        
    Returns:
        The metric object
        
    Raises:
        KeyError: If the metric does not exist
    """
    if not _metrics:
        init_metrics()
    
    return _metrics[name]


def increment_counter(name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
    """
    Increment a counter metric.
    
    Args:
        name: Metric name
        value: Value to increment by
        labels: Labels for the metric
    """
    if not _metrics:
        init_metrics()
    
    if name not in _metrics:
        logger.warning("Metric not found", name=name)
        return
    
    metric = _metrics[name]
    
    if labels:
        metric.labels(**labels).inc(value)
    else:
        metric.inc(value)


def set_gauge(name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
    """
    Set a gauge metric.
    
    Args:
        name: Metric name
        value: Value to set
        labels: Labels for the metric
    """
    if not _metrics:
        init_metrics()
    
    if name not in _metrics:
        logger.warning("Metric not found", name=name)
        return
    
    metric = _metrics[name]
    
    if labels:
        metric.labels(**labels).set(value)
    else:
        metric.set(value)


def observe_histogram(name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
    """
    Observe a histogram metric.
    
    Args:
        name: Metric name
        value: Value to observe
        labels: Labels for the metric
    """
    if not _metrics:
        init_metrics()
    
    if name not in _metrics:
        logger.warning("Metric not found", name=name)
        return
    
    metric = _metrics[name]
    
    if labels:
        metric.labels(**labels).observe(value)
    else:
        metric.observe(value)


def time_function(name: str, labels: Optional[Dict[str, str]] = None) -> Callable:
    """
    Decorator to time a function and record the duration in a histogram.
    
    Args:
        name: Metric name
        labels: Labels for the metric
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            observe_histogram(name, duration, labels)
            return result
        return wrapper
    return decorator
