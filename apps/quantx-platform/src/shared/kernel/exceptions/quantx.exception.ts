export abstract class QuantXException extends Error {
  abstract readonly code: string;
  abstract readonly statusCode: number;
  readonly correlationId: string;
  readonly timestamp: string;

  constructor(
    message: string,
    correlationId?: string,
  ) {
    super(message);
    this.correlationId = correlationId ?? crypto.randomUUID();
    this.timestamp = new Date().toISOString();
    Error.captureStackTrace(this, this.constructor);
  }
}