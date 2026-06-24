# QuantX AI - Telegram Architecture

## Overview

This document describes the Telegram bot integration architecture for QuantX AI, including message handling, conversation flows, state management, and user interaction patterns.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       Telegram Integration Layers                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│   │   Telegram   │  │   Message    │  │   Conversation│                │
│   │   Webhook    │  │   Handler    │  │   Manager    │                │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                 │
│          │                 │                 │                         │
│   ┌──────▼────────────────────────────────────────────────────────┐    │
│   │                    Handler Pipeline                              │    │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │    │
│   │  │ Command  │  │ Callback │  │ Message  │  │ State    │       │    │
│   │  │ Handler   │  │ Query    │  │ Handler   │  │ Handler   │       │    │
│   │  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │    │
│   └───────────────────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────────────────┤
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│   │   User       │  │   Strategy   │  │   Trading    │                 │
│   │   Service    │  │   Service    │  │   Service    │                 │
│   └──────────────┘  └──────────────┘  └──────────────┘                 │
└─────────────────────────────────────────────────────────────────────────┘
```

## Bot Configuration

### Bot Capabilities
- **Commands**: `/start`, `/help`, `/create`, `/list`, `/activate`, `/pause`
- **Inline Queries**: Symbol search, strategy lookup
- **Callback Queries**: Button interactions, confirmation dialogs
- **Message Types**: Text, images (charts), markdown formatting

### Bot Limits
| Limit | Value | Mitigation |
|-------|-------|------------|
| Message Rate | 30/second | Queue with priority |
| Caption Length | 1024 chars | Truncate with link |
| Inline Results | 50 | Paginate results |
| Webhook Timeout | 10s | Quick processing |

## Conversation Flows

### Strategy Creation Flow
```
User: /create_strategy
Bot: Select symbol (inline keyboard)
User: BTCUSDT
Bot: Select timeframe (inline keyboard)
User: 1h
Bot: Configure risk limit (input)
User: 100
Bot: Confirm creation (inline confirm/cancel)
User: Confirm
Bot: Strategy created successfully
```

### Strategy Management Flow
```
User: /list_strategies
Bot: [Strategy List with Status]
User: Selects strategy
Bot: [Strategy Details with Actions]
User: Clicks activate/pause
Bot: Action confirmed
```

### Position Monitoring Flow
```
User: /positions
Bot: [Open Positions Table]
User: /position BTCUSDT
Bot: [Position Details with P&L]
User: Automatic updates every 5 minutes
```

## State Management

### Finite State Machine
```python
class ConversationState(Enum):
    IDLE = "idle"
    SELECTING_SYMBOL = "selecting_symbol"
    SELECTING_TIMEFRAME = "selecting_timeframe"
    CONFIGURING_RISK = "configuring_risk"
    CONFIRMING_ACTION = "confirming_action"
```

### State Storage
- Redis with TTL (24 hours)
- Serialized FSM context
- Per-user state isolation
- Automatic cleanup

### State Recovery
- Load state on each message
- Graceful recovery on errors
- State expiration alerts
- Manual reset via `/reset` command

## Message Handlers

### Command Handler
```python
@dp.message(Command("create_strategy"))
async def create_strategy_command(
    message: Message,
    state: FSMContext,
) -> None:
    """Handle /create_strategy command."""
    user = await user_service.get_by_telegram_id(message.from_user.id)
    if not user:
        await message.answer("Please register with /start first")
        return
    
    await state.set_state(ConversationState.SELECTING_SYMBOL)
    await message.answer(
        "Select symbol:",
        reply_markup=create_symbol_keyboard(),
    )
```

### Callback Handler
```python
@dp.callback_query(
    CallbackData.filter(F.action == "activate_strategy")
)
async def activate_strategy_callback(
    callback: CallbackQuery,
    callback_data: CallbackData,
) -> None:
    """Handle strategy activation button."""
    strategy_id = callback_data.strategy_id
    await strategy_service.activate(strategy_id)
    await callback.answer("Strategy activated!", show_alert=True)
```

### Message Handler
```python
@dp.message(StateFilter(ConversationState.CONFIGURING_RISK))
async def configure_risk_handler(
    message: Message,
    state: FSMContext,
) -> None:
    """Handle risk limit input."""
    try:
        risk_limit = Decimal(message.text)
        if not (0 < risk_limit <= 10000):
            raise ValidationError("Risk limit must be between 0 and 10000")
        
        await state.update_data(risk_limit=risk_limit)
        await state.set_state(ConversationState.CONFIRMING_ACTION)
        await message.answer(
            f"Confirm risk limit: ${risk_limit}",
            reply_markup=confirm_keyboard(),
        )
    except ValidationError as e:
        await message.answer(f"Invalid input: {e}")
```

## Message Types

### Text Messages
- Command responses
- Status updates
- Error messages
- Help content

### Media Messages
- Chart images (P&L, equity curve)
- PDF reports
- TradingView-style charts

### Interactive Messages
- Inline keyboards
- Reply keyboards
- Force reply prompts

## Notification System

### Notification Types
| Type | Trigger | Priority |
|------|---------|----------|
| Position Opened | Position opened | High |
| Position Closed | Position closed | High |
| Order Filled | Order execution | High |
| Prediction | New prediction | Medium |
| Risk Alert | Risk limit hit | Critical |

### Message Batching
- Group notifications by user
- 30-second batching window
- Priority-based ordering
- Deduplication of similar events

### Rate Limiting
- Max 10 messages/user/minute
- Queue overflow triggers summary
- User-configurable quiet hours
- Emergency alerts bypass limits

## Security Architecture

### Authentication Flow
```
Telegram Message
      ↓
Telegram ID → User Service
      ↓
User Found? → Yes → Authorized
      ↓ No
Register Flow
      ↓
User Created → Authorized
```

### Input Validation
- All user input validated
- XSS prevention in markdown
- Numeric input range checking
- Symbol whitelist validation

### Rate Limiting
- Per-user message limits
- Per-command cooldowns
- Spam detection
- Automatic ban for abuse

## Error Handling

### Bot Error Categories
| Category | Handling |
|----------|----------|
| Invalid Input | Prompt user for correction |
| Network Error | Retry with exponential backoff |
| Service Error | Generic error message, alert ops |
| Rate Limit | Queue message, inform user |

### Fallback Behaviors
- Degraded to text-only on media failures
- Cache responses for common queries
- Graceful degradation on service outages
- Manual intervention escalation

## Performance Requirements

### Response Time Targets
| Operation | Target | SLA |
|-----------|--------|-----|
| Command Response | <1s | <2s |
| Callback Response | <500ms | <1s |
| Media Generation | <1.5s | <3s |
| Notification | <100ms | <200ms |

### Scalability Targets
- 10,000 concurrent users
- 100 messages/second peak
- 1M messages/day capacity

## Integration Points

### Service Integration
| Service | Integration Method |
|---------|-------------------|
| User Auth | REST API (user validation) |
| Strategy | REST API + Events |
| Trading | REST API + Events |
| Portfolio | REST API |
| Notification | Internal queue |

### Event Subscriptions
```python
EVENT_SUBSCRIPTIONS = {
    'prediction_generated': send_prediction_notification,
    'position_opened': send_position_notification,
    'position_closed': send_pnl_notification,
    'order_filled': send_execution_notification,
}
```

## Testing Strategy

### Unit Testing
- Handler logic testing
- State transition testing
- Input validation testing

### Integration Testing
- Mock Telegram API
- Real bot in test environment
- Webhook endpoint testing

### E2E Testing
- Full conversation flows
- Multi-user scenarios
- Error recovery testing

## Monitoring & Observability

### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Handler Latency | Processing time | >2s |
| Error Rate | Failed handlers | >1% |
| Message Queue | Pending messages | >1000 |
| Active Sessions | Concurrent users | >10k |

### Logs
- Message ID for tracing
- User ID (not personal info)
- Handler execution time
- Error stack traces

## Related Documents
- [20_TELEGRAM_ARCHITECTURE.md](20_TELEGRAM_ARCHITECTURE.md)
- [07_SERVICE_BOUNDARIES.md](07_SERVICE_BOUNDARIES.md)
- [26_EVENT_SYSTEM.md](26_EVENT_SYSTEM.md)
- [31_OBSERVABILITY.md](31_OBSERVABILITY.md)

---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Phase: Core Architecture*