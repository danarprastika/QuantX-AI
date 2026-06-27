import { QuantXException } from './quantx.exception';

export class InfrastructureException extends QuantXException {
  readonly code = 'INFRASTRUCTURE_ERROR';
  readonly statusCode = 503;
}