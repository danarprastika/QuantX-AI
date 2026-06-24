# QuantX AI - Risk Management

## Overview

This document defines the risk management architecture for QuantX AI, including trading risk controls, position sizing, exposure limits, and risk monitoring systems.

## Risk Management Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Risk Management Layers                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│   │  Strategy    │  │   Position   │  │   Portfolio  │  │   Exchange   │ │
│   │  Risk        │  │   Risk       │  │   Risk       │  │   Risk       │ │
│   │              │  │              │  │              │  │              │ │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│          │                 │                 │                 │         │
│   ┌──────▼──────────────────────────────────────────────────────────┐    │
│   │                    Risk Engine                                  │    │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │    │
│   │  │  VaR     │  │  Exposure│  │  Limits  │  │  Alerts  │         │    │
│   │  │ Calculator│  │  Tracker │  │  Engine  │  │  System  │         │    │
│   │  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │    │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Trading    │  │   Strategy   │  │   Market     │  │   User       │ │
│  │   Service    │  │   Service    │  │   Service    │  │   Service    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

## Risk Categories

### 1. Market Risk
Risk of losses due to adverse market movements.

### 2. Credit Risk
Risk that counterparties (exchanges) fail to fulfill obligations.

### 3. Liquidity Risk
Risk of inability to enter/exit positions at desired prices.

### 4. Operational Risk
Risk of losses due to system failures, errors, or processes.

### 5. Model Risk
Risk that AI predictions are inaccurate or misleading.

### 6. Counterparty Risk
Risk from exchange operational issues or insolvency.

## Strategy-Level Risk Controls

### Position Size Limits
```python
def calculate_position_size(
    account_balance: Decimal,
    risk_limit_pct: Decimal,
) -> Decimal:
    """Calculate maximum position size."""
    return account_balance * (risk_limit_pct / 100)

# Default limits by tier
FREE_RISK_LIMIT = Decimal("100")  # $100 max per position
BASIC_RISK_LIMIT = Decimal("1000")  # $1000 max per position
PREMIUM_RISK_LIMIT = Decimal("10000")  # $10000 max per position
```

### Confidence-Based Position Sizing
```python
def size_position_by_confidence(
    base_size: Decimal,
    confidence: float,
    min_multiplier: float = 0.1,
    max_multiplier: float = 1.0,
) -> Decimal:
    """Adjust position size based on prediction confidence."""
    multiplier = min_multiplier + (confidence * (max_multiplier - min_multiplier))
    return base_size * Decimal(str(multiplier))
```

### Stop-Loss Implementation
```python
class StopLossCalculator:
    def calculate(
        self,
        entry_price: Decimal,
        side: Side,
        stop_loss_pct: Decimal,
    ) -> Decimal:
        """Calculate stop loss price."""
        if side == Side.BUY:
            return entry_price * (1 - stop_loss_pct / 100)
        return entry_price * (1 + stop_loss_pct / 100)
```

## Portfolio-Level Risk Controls

### Exposure Limits
| Tier | Max Concurrent Positions | Max Symbol Exposure | Max Daily Loss |
|------|-------------------------|---------------------|----------------|
| Free | 5 | 10% | $100 |
| Basic | 20 | 15% | $500 |
| Premium | 100 | 25% | $2000 |
| Enterprise | Unlimited | 50% | $10000 |

### Exposure Tracking
```python
class ExposureTracker:
    def get_user_exposure(self, user_id: UserId) -> ExposureReport:
        positions = position_repo.get_open_positions(user_id)
        total_value = sum(p.quantity * p.current_price for p in positions)
        symbol_exposure = {}
        for p in positions:
            symbol_exposure[p.symbol] = (
                symbol_exposure.get(p.symbol, 0) + p.quantity * p.current_price
            )
        
        return ExposureReport(
            total_exposure=total_value,
            symbol_exposure=symbol_exposure,
            exposure_pct=total_value / account_balance,
        )
```

### Daily Loss Limit
```python
async def check_daily_loss_limit(user_id: UserId) -> bool:
    """Check if user has exceeded daily loss limit."""
    tier = await user_repo.get_subscription_tier(user_id)
    daily_pnl = await portfolio_service.get_daily_pnl(user_id)
    
    return abs(daily_pnl) < get_tier_daily_limit(tier)
```

## VaR (Value at Risk) Implementation

### Historical VaR
```python
def calculate_historical_var(
    price_series: list[Decimal],
    confidence: float = 0.95,
    horizon: int = 1,
) -> Decimal:
    """Calculate historical Value at Risk."""
    returns = calculate_returns(price_series)
    var_threshold = int(len(returns) * (1 - confidence))
    var_value = sorted(returns)[var_threshold] * Decimal(str(horizon))
    return var_value
```

### Parametric VaR
```python
def calculate_parametric_var(
    portfolio_value: Decimal,
    volatility: float,
    confidence: float = 0.95,
    horizon: int = 1,
) -> Decimal:
    """Calculate parametric Value at Risk."""
    from scipy.stats import norm
    
    z_score = norm.ppf(confidence)
    var = portfolio_value * Decimal(str(volatility * z_score * (horizon ** 0.5)))
    return var
```

## Risk Monitoring

### Real-time Risk Checks
1. Pre-trade validation
2. Position size check
3. Exposure limit check
4. Daily loss check
5. Confidence threshold check

### Risk Alerts
| Alert Type | Trigger | Action |
|------------|---------|--------|
| Exposure Warning | >80% portfolio | Notify user |
| Daily Loss Warning | >50% daily limit | Pause strategies |
| Model Accuracy Drop | <60% for 1h | Disable model |
| Exchange Downtime | >30s outage | Failover |

### Risk Alert Implementation
```python
class RiskAlertSystem:
    def check_and_alert(
        self,
        user_id: UserId,
        proposed_trade: TradeProposal,
    ) -> RiskCheckResult:
        """Check all risk limits before trade."""
        exposure = self.exposure_tracker.get_user_exposure(user_id)
        daily_loss = self.loss_tracker.get_daily_loss(user_id)
        confidence = self.confidence_checker.get_latest(
            user_id, proposed_trade.symbol
        )
        
        violations = []
        if exposure.exposure_pct > get_tier_limit(user_id):
            violations.append("EXPOSURE_LIMIT")
        if daily_loss > get_tier_daily_limit(user_id):
            violations.append("DAILY_LOSS_LIMIT")
        if confidence < proposed_trade.min_confidence:
            violations.append("LOW_CONFIDENCE")
        
        return RiskCheckResult(
            allowed=len(violations) == 0,
            violations=violations,
        )
```

## Exchange Risk Controls

### Rate Limit Risk
- Queue overflow handling
- Request prioritization (orders first)
- Exponential backoff
- Circuit breaker on limit hits

### Exchange Health Checks
```python
class ExchangeHealthMonitor:
    async def check_health(self, exchange: str) -> HealthStatus:
        try:
            status = await exchange_client.get_system_status()
            return HealthStatus.HEALTHY
        except Exception as e:
            if self.error_count[exchange] > 5:
                return HealthStatus.UNHEALTHY
            self.error_count[exchange] += 1
            return HealthStatus.DEGRADED
```

### Exchange Failover
- Primary → Secondary → Tertiary
- Automatic failover on health check failure
- Manual override for known issues
- Alert on failover events

## Model Risk Controls

### Model Validation
```python
class ModelRiskValidator:
    def validate_prediction(
        self,
        prediction: Prediction,
        market_conditions: MarketConditions,
    ) -> ValidationResult:
        """Validate prediction against market conditions."""
        # Check volatility
        if market_conditions.volatility > self.thresholds.high_volatility:
            return ValidationResult(
                approved=False,
                reason="High volatility exceeds model confidence"
            )
        
        # Check confidence
        if prediction.confidence < self.thresholds.min_confidence:
            return ValidationResult(
                approved=False,
                reason="Low confidence"
            )
        
        return ValidationResult(approved=True)
```

### Confidence Calibration
- Temperature scaling for probabilities
- Platt scaling for calibration
- Confidence bands for uncertainty
- Model ensemble disagreement monitoring

## Operational Risk Controls

### System Redundancy
- Active-passive service deployment
- Database replication
- Exchange redundancy
- Backup exchange connections

### Process Controls
- Manual approval for large trades
- Two-person rule for admin actions
- Change management for model updates
- Deployment validation gates

## Risk Metrics

### Key Risk Indicators (KRIs)

| Metric | Description | Warning Threshold | Critical Threshold |
|--------|-------------|-------------------|-------------------|
| Portfolio Exposure | % of account in positions | 80% | 95% |
| Daily Loss | Loss vs daily limit | 50% | 100% |
| Model Accuracy | Prediction accuracy | <60% | <50% |
| Exchange Latency | Order execution time | >50ms | >100ms |
| Position Count | Open positions | Tier limit | Tier limit |

### Risk Dashboards
- Real-time exposure tracking
- Daily P&L monitoring
- Model performance metrics
- Exchange health status

## Risk Configuration

### Per-User Risk Settings
```python
class UserRiskConfig:
    max_position_size: Decimal
    max_concurrent_positions: int
    daily_loss_limit: Decimal
    max_symbol_exposure: Decimal
    confidence_threshold: float
    auto_pause_on_loss: bool
    
    @classmethod
    def from_tier(cls, tier: SubscriptionTier) -> 'UserRiskConfig':
        return cls(
            max_position_size=DEFAULT_LIMITS[tier].position,
            max_concurrent_positions=DEFAULT_LIMITS[tier].positions,
            daily_loss_limit=DEFAULT_LIMITS[tier].daily_loss,
            ...
        )
```

### Global Risk Settings
- System-wide position caps
- Emergency stop thresholds
- Model fallback thresholds
- Exchange blackout lists

## Risk Testing

### Stress Testing
- Market crash scenarios
- Flash crash protection
- Exchange outage scenarios
- Model failure scenarios

### Backtesting Risk Controls
- Walk-forward analysis
- Monte Carlo simulations
- Stress period testing
- Validation against historical data

## Incident Response

### Risk Breach Procedures
1. Identify breach type
2. Assess impact
3. Execute mitigation
4. Notify stakeholders
5. Document incident
6. Update prevention

### Emergency Stop
- Manual kill switch
- Automatic on critical breach
- Graceful position closure
- User notification

## Related Documents
- [07_SERVICE_BOUNDARIES.md](07_SERVICE_BOUNDARIES.md)
- [15_SECURITY.md](15_SECURITY.md)
- [47_OPERATIONS_RUNBOOK.md](47_OPERATIONS_RUNBOOK.md)

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Phase: Infrastructure*