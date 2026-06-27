import { QuantXException } from './quantx.exception';

export class ApplicationException extends QuantXException {
  readonly code = 'APPLICATION_ERROR';
  readonly statusCode = 500;
}