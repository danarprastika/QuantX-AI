import { QuantXException } from './quantx.exception';

export class DomainException extends QuantXException {
  readonly code = 'DOMAIN_ERROR';
  readonly statusCode = 400;
}