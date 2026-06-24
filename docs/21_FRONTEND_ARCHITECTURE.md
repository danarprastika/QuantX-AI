---
status: Approved
owner: Frontend Team
version: 1.0.0
last_updated: 2026-06-24
source_of_truth: docs/21_FRONTEND_ARCHITECTURE.md
depends_on:
  - docs/02_SYSTEM_ARCHITECTURE.md
  - docs/11_API_SPECIFICATION.md
  - docs/22_BACKEND_ARCHITECTURE.md
  - docs/27_CONFIGURATION.md
related_documents:
  - docs/02_SYSTEM_ARCHITECTURE.md
  - docs/11_API_SPECIFICATION.md
  - docs/22_BACKEND_ARCHITECTURE.md
  - docs/27_CONFIGURATION.md
---
# QuantX AI - Frontend Architecture

## Overview

This document describes the frontend architecture for QuantX AI's web-based dashboard. The frontend provides a comprehensive trading interface for strategy management, portfolio monitoring, and analytics visualization.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Frontend Architecture                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│   │   Browser    │  │   CDN/Edge   │  │   Load       │                 │
│   │              │  │   Cache      │  │   Balancer   │                 │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                 │
│          │                 │                 │                         │
│   ┌──────▼───────────────────────────────────────────────────────────┐ │
│   │                    Next.js Application                              │ │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │ │
│   │  │  Pages   │  │  React   │  │  Redux/  │  │  API     │          │ │
│   │  │          │  │ Components │  │ Zustand  │  │  Client  │          │ │
│   │  └──────────┘  └──────────┘  └──────────┘  └──────────┘          │ │
│   └────────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────────┤
│                        Backend API Layer                                  │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   FastAPI    │  │   GraphQL    │  │   WebSocket  │  │   REST       │ │
│  │   Endpoints  │  │   Endpoint   │  │   Streams    │  │   Client    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Core Framework
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript 5.x
- **Runtime**: Node.js 20.x LTS

### UI Libraries
- **Component Library**: Radix UI primitives
- **Styling**: Tailwind CSS 3.x
- **Charts**: TradingView Lightweight Charts
- **Tables**: TanStack Table
- **Forms**: React Hook Form + Zod

### State Management
- **Global State**: Zustand (lightweight alternative to Redux)
- **Server State**: TanStack Query (React Query)
- **URL State**: Next.js URL state management

### Build & Deployment
- **Bundler**: Turbopack (Next.js default)
- **Package Manager**: pnpm 9.x
- **Testing**: Jest + React Testing Library
- **Linting**: ESLint + Prettier

## Application Structure

```
web/
├── app/                    # App Router pages
│   ├── api/               # API routes (edge)
│   ├── (auth)/            # Auth layouts
│   ├── strategies/        # Strategy pages
│   ├── positions/         # Position pages
│   ├── analytics/         # Analytics pages
│   └── layout.tsx         # Root layout
│
├── components/            # React components
│   ├── ui/               # Generic UI primitives
│   ├── trading/          # Trading-specific components
│   ├── charts/           # Chart components
│   └── layout/           # Layout components
│
├── lib/                   # Utility libraries
│   ├── api/              # API client
│   ├── auth/             # Auth utilities
│   ├── trading/          # Trading helpers
│   └── utils/            # General utilities
│
├── store/                 # Zustand stores
│   ├── strategy-store.ts
│   ├── position-store.ts
│   └── user-store.ts
│
├── hooks/                 # Custom React hooks
│   ├── use-strategy.ts
│   ├── use-position.ts
│   └── use-websocket.ts
│
├── types/                 # TypeScript types
│   ├── api.ts
│   ├── domain.ts
│   └── trading.ts
│
└── public/                # Static assets
    ├── icons/
    └── images/
```

## Page Architecture

### Authentication Pages
- `/login` - User login
- `/register` - User registration
- `/callback` - OAuth callback
- `/reset-password` - Password reset

### Dashboard Pages
- `/dashboard` - Main dashboard overview
- `/strategies` - Strategy list and management
- `/positions` - Position monitoring
- `/analytics` - Performance analytics
- `/settings` - User configuration

### Feature Pages
- `/strategies/create` - Strategy creation wizard
- `/strategies/[id]` - Strategy detail view
- `/positions/[symbol]` - Position detail view
- `/analytics/backtest` - Backtesting interface
- `/analytics/reports` - Generated reports

## Component Architecture

### Presentational Components
```typescript
interface StrategyCardProps {
  strategy: StrategyDTO;
  onActivate: (id: string) => void;
  onPause: (id: string) => void;
}

const StrategyCard: React.FC<StrategyCardProps> = ({ 
  strategy, 
  onActivate, 
  onPause 
}) => { ... };
```

### Container Components
```typescript
const StrategyListContainer: React.FC = () => {
  const { data: strategies } = useStrategies();
  const { mutate: activateStrategy } = useActivateStrategy();
  
  return <StrategyList strategies={strategies} />;
};
```

### UI Component Patterns
- Compound component pattern for complex UI
- Render props for flexible composition
- Custom hooks for reusable logic
- Context for theme and auth state

## State Management

### Zustand Store Pattern
```typescript
interface StrategyStore {
  strategies: StrategyDTO[];
  activeStrategy: StrategyDTO | null;
  loading: boolean;
  error: string | null;
  
  fetchStrategies: () => Promise<void>;
  createStrategy: (data: StrategyCreate) => Promise<void>;
  updateStrategy: (id: string, data: StrategyUpdate) => Promise<void>;
}

export const useStrategyStore = create<StrategyStore>()((set, get) => ({
  strategies: [],
  activeStrategy: null,
  loading: false,
  error: null,
  
  fetchStrategies: async () => {
    set({ loading: true });
    const strategies = await api.getStrategies();
    set({ strategies, loading: false });
  },
}));
```

### React Query Pattern
```typescript
const useStrategy = (id: string) => {
  return useQuery({
    queryKey: ['strategy', id],
    queryFn: () => api.getStrategy(id),
    staleTime: 1000 * 60 * 5, // 5 minutes
    cacheTime: 1000 * 60 * 10, // 10 minutes
  });
};

const useCreateStrategy = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: api.createStrategy,
    onSuccess: () => {
      queryClient.invalidateQueries(['strategies']);
    },
  });
};
```

## API Integration

### API Client Configuration
```typescript
const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 10000,
});

apiClient.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### Request/Response Types
```typescript
interface StrategyDTO {
  id: string;
  name: string;
  symbol: string;
  timeframe: Timeframe;
  status: StrategyStatus;
  config: StrategyConfig;
  createdAt: string;
  performance?: PerformanceMetrics;
}

interface StrategyCreate {
  name: string;
  symbol: string;
  timeframe: Timeframe;
  config: StrategyConfig;
}
```

## WebSocket Integration

### Real-time Updates
```typescript
const usePositionStream = (symbol: string) => {
  const { data, error } = useWebSocket<PositionUpdate>(
    `${WS_URL}/positions/${symbol}`
  );
  
  return { position: data, error };
};
```

### Connection Management
- Auto-reconnect with exponential backoff
- Ping/pong health checks
- Message queuing during disconnect
- Connection status indicator

## Security Architecture

### Authentication Flow
```
1. User navigates to /login
2. Redirect to OAuth provider
3. Callback with JWT token
4. Store encrypted in HttpOnly cookie
5. Attach to API requests
6. Refresh token before expiry
```

### Authorization
- Role-based access control (RBAC)
- Route-level protection
- API-level permission checks
- UI element visibility based on permissions

### CSRF Protection
- SameSite cookies
- CSRF tokens for mutations
- Origin header validation

## Performance Optimization

### Bundle Optimization
- Code splitting by route
- Tree shaking unused code
- Dynamic imports for heavy components
- Font optimization

### Runtime Optimization
- React.memo for expensive components
- useMemo/useCallback for derived state
- Virtualized lists for large datasets
- Image optimization with next/image

### Caching Strategy
| Type | Strategy | TTL |
|------|----------|-----|
| API Responses | React Query cache | 5 minutes |
| Static Assets | CDN | 1 year |
| Charts | In-memory cache | Session |
| User Preferences | LocalStorage | Persistent |

## Responsive Design

### Breakpoints
```css
sm: 640px   /* Mobile */
md: 768px   /* Tablet */
lg: 1024px  /* Desktop */
xl: 1280px  /* Large desktop */
```

### Mobile-First Approach
- Touch-friendly interactions
- Simplified navigation on mobile
- Chart responsive resizing
- Offline state handling

## Testing Strategy

### Unit Testing
- Component rendering tests
- Hook logic tests
- Utility function tests

### Integration Testing
- API integration tests
- State management tests
- WebSocket handling tests

### E2E Testing
- Playwright for browser testing
- User journey tests
- Cross-browser compatibility

## Deployment Architecture

### Vercel Deployment
- Automatic deployments from main branch
- Preview deployments for PRs
- Edge functions for API routes
- Image optimization at edge

### Environment Variables
```
NEXT_PUBLIC_API_URL=https://api.quantx.ai
NEXT_PUBLIC_WS_URL=wss://api.quantx.ai/ws
NEXT_PUBLIC_TELEGRAM_BOT=@quantx_bot
```

## Related Documents
- [02_SYSTEM_ARCHITECTURE.md](02_SYSTEM_ARCHITECTURE.md)
- [11_API_SPECIFICATION.md](11_API_SPECIFICATION.md)
- [22_BACKEND_ARCHITECTURE.md](22_BACKEND_ARCHITECTURE.md)
- [27_CONFIGURATION.md](27_CONFIGURATION.md)
---
*Document Version: 1.0.0*
*Created: 2026-06-24*
*Last Updated: 2026-06-24*
*Status: Approved*
*Owner: Frontend Team*
*Source of Truth: docs/21_FRONTEND_ARCHITECTURE.md*
*Depends On: 02_SYSTEM_ARCHITECTURE.md, 11_API_SPECIFICATION.md, 22_BACKEND_ARCHITECTURE.md, 27_CONFIGURATION.md*
*Related Documents: 02_SYSTEM_ARCHITECTURE.md, 11_API_SPECIFICATION.md, 22_BACKEND_ARCHITECTURE.md, 27_CONFIGURATION.md*
*Phase: Core Architecture*
