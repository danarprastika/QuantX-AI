"""Shared error types for QuantX AI."""


class QuantXError(Exception):
    """Base exception for all QuantX errors."""

    def __init__(self, message: str, code: str = "internal_error") -> None:
        self.code = code
        super().__init__(message)


class InfrastructureError(QuantXError):
    """Raised when infrastructure is unavailable."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="infrastructure_error")


class DomainError(QuantXError):
    """Raised for domain rule violations."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="domain_error")


class ValidationError(QuantXError):
    """Raised for validation failures."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="validation_error")


class ConfigurationError(QuantXError):
    """Raised for configuration errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message, code="configuration_error")
