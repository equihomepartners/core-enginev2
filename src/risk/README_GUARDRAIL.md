# Guardrail Monitor Module

The Guardrail Monitor module is a non-blocking guardrail system for the EQU IHOME SIM ENGINE v2. It monitors key risk metrics and ensures they stay within acceptable bounds, without stopping the simulation when guardrails are breached.

## Design Goals

| Goal | Explanation |
|------|-------------|
| Non-blocking | No `raise SimulationGuardrailError` that kills the run. The simulation always completes; guardrail outcomes are returned as a structured report. |
| Granular severity | INFO, WARN, FAIL. Only FAIL counts against IC policy, but it still just reports. |
| Single JSON report | The orchestrator stores one GuardrailReport object inside SimulationResult and pushes the same payload over WebSocket to the UI. |
| Prom & log hooks | Each breach increments Prometheus counters and emits a structured log line for ELK/Grafana. |
| MC compatibility | In Monte-Carlo mode, each path has its own report; aggregation layer can compute "% paths with FAIL". |

## Guardrail Catalogue

| ID | Rule | Severity on breach | Layer |
|----|------|-------------------|-------|
| LTV_STRESS_HIGH | Stress-LTV (−20%) > 90% | FAIL | Unit |
| ZONE_RED_WEIGHT | Red NAV share > 5% | FAIL | Zone/Port |
| LEVERAGE_UTIL | NAV util > cfg.max_nav_util | FAIL | Port |
| LIQUIDITY_BUFFER_LOW | Cash + undrawn < 4% NAV | FAIL | Port |
| VaR_99_LIMIT | VaR-99 > 15% NAV (MC only) | FAIL | Port |
| WAL_SOFT | WAL > 8 yrs | WARN | Port |
| PD_ZONE_ALERT | Zone default > 2× city avg | WARN | Zone |
| MC_LOW_PATHS | n_inner < cfg.min_paths | WARN | Run |
| INFO_SCHEMA_MISMATCH | Schema version drift | INFO | Run |

## Complete Guardrail Catalogue

### Property / Loan level

| # | Layer | Guardrail rule | Severity | Rationale |
|---|-------|---------------|----------|-----------|
| 1 | Unit | stress_LTV (−20% price dip) ≤ 90% | ERROR | Ensures adequate equity cushion even in stress. |
| 2 | Unit | principal ≤ loan_ticket_limit_zone | ERROR | No outsized single exposures in illiquid streets. |
| 3 | Unit | exit_month ≤ max_term_months (120) | ERROR | Contractual limit. |

### Zone (TLS) level

| # | Layer | Guardrail rule | Severity | Rationale |
|---|-------|---------------|----------|-----------|
| 4 | Zone | Zone NAV weight ≤ capital_limit_zone (e.g. Red ≤ 5%) | ERROR | Prevents concentration in high-risk areas. |
| 5 | Zone | default_rate_zone ≤ 2× city_avg_default | WARNING | Early signal of deteriorating credit pocket. |
| 6 | Zone | sigma_price_zone ≤ 3× city σ | WARNING | Flags data anomalies or speculative pockets. |

### Portfolio level – exposure & leverage

| # | Layer | Guardrail rule | Severity | Rationale |
|---|-------|---------------|----------|-----------|
| 7 | Port | Single suburb weight ≤ 10% NAV | ERROR | Diversification. |
| 8 | Port | Largest single loan weight ≤ 2% NAV | WARNING | Tail-risk outlier. |
| 9 | Port | NAV facility utilisation ≤ max_nav_util (cfg) | ERROR | Covenant breach prevention. |
| 10 | Port | Interest-coverage ratio (ICR) ≥ 1.25× | ERROR | Debt-service ability under base case. |

### Portfolio level – liquidity & duration

| # | Layer | Guardrail rule | Severity | Rationale |
|---|-------|---------------|----------|-----------|
| 11 | Port | Liquidity buffer (cash + undrawn) ≥ 4% NAV | ERROR | Working-capital safety. |
| 12 | Port | Weighted-Avg Life (WAL) ≤ 8 yrs unless wal_override=true | WARNING | Meets WM mandate for duration. |

### Portfolio level – market risk

| # | Layer | Guardrail rule | Severity | Rationale |
|---|-------|---------------|----------|-----------|
| 13 | Port | VaR-99 ≤ 15% NAV | ERROR (MC mode) | Institutional risk limit. |
| 14 | Port | CVaR-99 ≤ 20% NAV | ERROR (MC mode) | Extreme-tail containment. |

### Performance & mandate

| # | Layer | Guardrail rule | Severity | Rationale |
|---|-------|---------------|----------|-----------|
| 15 | Port | Net-IRR P5 ≥ hurdle (8%) – 250 bp | WARNING | Alerts PM that downside paths near hurdle. |
| 16 | Port | Hurdle-clear probability ≥ 70% | ERROR (MC) | Ensures carry realistically attainable. |

### Model / process

| # | Layer | Guardrail rule | Severity | Rationale |
|---|-------|---------------|----------|-----------|
| 17 | Run | Config JSON schema version == engine schema version | ERROR | Prevents mismatched param sets. |
| 18 | Run | Monte-Carlo inner paths ≥ min_paths (500) | WARNING | Statistical quality. |
| 19 | Run | Seed reproducibility check (rerun hash) | INFO | Ensures deterministic results. |

## GuardrailMonitor Interface & Flow

The GuardrailMonitor class provides a simple interface for evaluating guardrails:

```python
class GuardrailMonitor:
    def __init__(self, context: SimulationContext):
        """Initialize the guardrail monitor."""
        self.context = context
        self.config = context.config
        self.websocket_manager = get_websocket_manager()
        
        # Get guardrail configuration
        self.guardrail_config = self.config.get("guardrails", {})
        
        # Initialize report
        self.report = GuardrailReport(simulation_id=context.run_id)
        
        # Track checked guardrails
        self.checked_guardrails: Set[str] = set()
    
    async def evaluate_guardrails(self) -> GuardrailReport:
        """Evaluate all guardrails."""
        # Evaluate property/loan level guardrails
        await self._evaluate_loan_guardrails(metrics)
        
        # Evaluate zone level guardrails
        await self._evaluate_zone_guardrails(metrics)
        
        # Evaluate portfolio level guardrails
        await self._evaluate_portfolio_guardrails(metrics)
        
        # Evaluate model/process guardrails
        await self._evaluate_model_guardrails(metrics)
        
        # Store report in context
        self.context.guardrail_report = self.report
        
        return self.report
```

## Breach and GuardrailReport Models

```python
@dataclass
class Breach:
    code: str
    severity: Severity
    message: str
    value: float | None
    threshold: float | None
    unit: str | None
    layer: str | None

@dataclass
class GuardrailReport:
    breaches: list[Breach]
    simulation_id: str | None = None

    @property
    def worst_level(self) -> Severity:
        if any(b.severity == Severity.FAIL for b in self.breaches):
            return Severity.FAIL
        if any(b.severity == Severity.WARN for b in self.breaches):
            return Severity.WARN
        return Severity.INFO
```

## Orchestrator & WebSocket Integration

The GuardrailMonitor is integrated with the orchestrator and WebSocket manager:

```python
# In orchestrator.py
report = guardrail_monitor.evaluate(portfolio_metrics)
sim_result = SimulationResult(loans, cash, metrics, guardrails=report)

# Push non-blocking status to live dashboard
ws_manager.broadcast({
    "run_id": ctx.run_id,
    "guardrail_level": report.worst_level,
    "breaches": [b.__dict__ for b in report.breaches]
})
```

In Monte Carlo mode, the aggregation layer can compute:

```python
fail_rate = sum(r.worst_level=='FAIL' for r in mc_reports)/len(mc_reports)
```

## API Endpoints

The Guardrail Monitor module provides the following API endpoints:

- `POST /guardrail/evaluate`: Evaluate guardrails for a simulation
- `GET /guardrail/{simulation_id}`: Get guardrail report for a simulation

## Usage

```python
# Create guardrail monitor
guardrail_monitor = GuardrailMonitor(context)

# Evaluate guardrails
report = await guardrail_monitor.evaluate_guardrails()

# Check for breaches
if report.worst_level == Severity.FAIL:
    print("Guardrail breaches detected!")
    for breach in report.breaches:
        if breach.severity == Severity.FAIL:
            print(f"FAIL: {breach.message}")
```
