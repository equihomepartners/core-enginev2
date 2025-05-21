#!/usr/bin/env python3
"""
Main entry point for the EQU IHOME SIM ENGINE v2.

This module provides a command-line interface for running simulations and
viewing results.
"""

import json
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

import typer
from rich.console import Console
from rich.table import Table

from src.config.config_loader import load_config
from src.utils.logging_setup import setup_logging

app = typer.Typer(help="EQU IHOME SIM ENGINE v2")
console = Console()


@app.command()
def run(
    config_path: str = typer.Option(
        ..., "--config", "-c", help="Path to the simulation configuration JSON file"
    ),
    output_path: Optional[str] = typer.Option(
        None, "--output", "-o", help="Path to save the simulation results"
    ),
    seed: Optional[int] = typer.Option(
        None, "--seed", "-s", help="Random seed for reproducibility"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose logging"
    ),
) -> None:
    """
    Run a simulation using the provided configuration.
    """
    setup_logging(verbose=verbose)
    
    try:
        # Load and validate configuration
        config = load_config(config_path)
        
        # TODO: Implement simulation engine
        # For now, just return a placeholder result
        simulation_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        result = {
            "simulation_id": simulation_id,
            "run_timestamp": timestamp,
            "config": config,
            "metrics": {
                "irr": 0.12,
                "equity_multiple": 1.5,
                "roi": 0.5,
                "payback_period": 4.2,
                "var_95": 0.08,
                "var_99": 0.12,
                "sharpe_ratio": 1.2,
                "max_drawdown": 0.15,
            },
            "cashflows": [
                {
                    "year": 0,
                    "inflow": 0,
                    "outflow": 100000000,
                    "net": -100000000,
                    "cumulative": -100000000,
                },
                {
                    "year": 1,
                    "inflow": 5000000,
                    "outflow": 2000000,
                    "net": 3000000,
                    "cumulative": -97000000,
                },
                # Additional years would be included here
                {
                    "year": 10,
                    "inflow": 150000000,
                    "outflow": 0,
                    "net": 150000000,
                    "cumulative": 50000000,
                },
            ],
        }
        
        # Save results if output path is provided
        if output_path:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w") as f:
                json.dump(result, f, indent=2)
            console.print(f"Results saved to [bold]{output_path}[/bold]")
        
        # Save latest results
        latest_file = Path("results/latest.json")
        latest_file.parent.mkdir(parents=True, exist_ok=True)
        with open(latest_file, "w") as f:
            json.dump(result, f, indent=2)
        
        # Display summary
        display_summary(result)
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)


@app.command()
def results(
    result_path: str = typer.Argument(
        "results/latest.json", help="Path to the simulation results JSON file"
    )
) -> None:
    """
    Display simulation results.
    """
    try:
        # Load results
        with open(result_path, "r") as f:
            result = json.load(f)
        
        # Display summary
        display_summary(result)
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)


def display_summary(result: Dict[str, Any]) -> None:
    """
    Display a summary of the simulation results.
    
    Args:
        result: Simulation results dictionary
    """
    console.print("\n[bold]Simulation Summary[/bold]")
    console.print(f"Simulation ID: {result['simulation_id']}")
    console.print(f"Run Timestamp: {result['run_timestamp']}")
    
    # Display metrics
    console.print("\n[bold]Key Metrics[/bold]")
    metrics_table = Table(show_header=True, header_style="bold")
    metrics_table.add_column("Metric")
    metrics_table.add_column("Value")
    
    for metric, value in result["metrics"].items():
        metrics_table.add_row(
            metric.replace("_", " ").title(),
            f"{value:.2%}" if metric in ["irr", "roi", "var_95", "var_99", "max_drawdown"] else f"{value:.2f}"
        )
    
    console.print(metrics_table)
    
    # Display cashflows
    console.print("\n[bold]Cash Flows[/bold]")
    cashflow_table = Table(show_header=True, header_style="bold")
    cashflow_table.add_column("Year")
    cashflow_table.add_column("Inflow")
    cashflow_table.add_column("Outflow")
    cashflow_table.add_column("Net")
    cashflow_table.add_column("Cumulative")
    
    for cf in result["cashflows"]:
        cashflow_table.add_row(
            str(cf["year"]),
            f"${cf['inflow']:,.0f}",
            f"${cf['outflow']:,.0f}",
            f"${cf['net']:,.0f}",
            f"${cf['cumulative']:,.0f}"
        )
    
    console.print(cashflow_table)


if __name__ == "__main__":
    app()
