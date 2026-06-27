import { QuantXException } from './quantx.exception';

export class ValidationException extends QuantXException {
  readonly code = 'VALIDATION_ERROR';
  readonly statusCode = 400;
  readonly details: Array<{ field: string; issue: string }>;

  constructor(
    message: string,
    details: Array<{ field: string; issue: string }> = [],
    correlationId?: string,
  ) {
    super(message, correlationId);
    this.details = details;
  }
}