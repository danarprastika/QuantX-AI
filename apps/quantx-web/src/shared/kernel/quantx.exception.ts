export class QuantXException extends Error {
  code: string;
  statusCode: number;
  correlationId: string;
  timestamp: string;

  constructor(
    code: string,
    message: string,
    correlationId?: string,
    statusCode: number = 500
  ) {
    super(message);
    this.code = code;
    this.statusCode = statusCode;
    this.correlationId = correlationId ?? crypto.randomUUID();
    this.timestamp = new Date().toISOString();
    this.name = 'QuantXException';
  }
}