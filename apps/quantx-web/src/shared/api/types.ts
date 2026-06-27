export interface HealthResponse {
  status: string;
  timestamp: string;
}

export interface MarketSignal {
  id: string;
  symbol: string;
  signalType: string;
  confidence: number;
  classification: string;
  createdAt: string;
  createdBy: string;
}

export interface Portfolio {
  id: string;
  userId: string;
  name: string;
  totalValue: number;
  classification: string;
  createdAt: string;
  createdBy: string;
}