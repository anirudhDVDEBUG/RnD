#!/usr/bin/env python3
"""
Overkill Demo: Enterprise-Grade Addition Service

Demonstrates the "overkill" Claude Code skill by over-engineering
the simple task of adding two numbers into a full enterprise architecture.
"""

from __future__ import annotations

import abc
import enum
import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Generic, Protocol, TypeVar

# ============================================================================
# SECTION 1: Enterprise Logging & Observability Infrastructure
# ============================================================================

class LogLevel(enum.Enum):
    """ISO-42069 compliant log level enumeration."""
    TRACE = 0
    DEBUG = 10
    INFO = 20
    WARN = 30
    ERROR = 40
    FATAL = 50
    APOCALYPTIC = 60  # For when addition fails


@dataclass(frozen=True)
class StructuredLogEntry:
    """Immutable, auditable log record with full traceability."""
    timestamp: str
    level: LogLevel
    message: str
    correlation_id: str
    component: str
    metadata: dict = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps({
            "timestamp": self.timestamp,
            "level": self.level.name,
            "message": self.message,
            "correlation_id": self.correlation_id,
            "component": self.component,
            "metadata": self.metadata,
        }, indent=2)


class EnterpriseLogger:
    """Production-grade structured logger for arithmetic operations."""

    def __init__(self, component: str, correlation_id: str | None = None):
        self._component = component
        self._correlation_id = correlation_id or str(uuid.uuid4())
        self._entries: list[StructuredLogEntry] = []

    def _log(self, level: LogLevel, message: str, **metadata: Any) -> None:
        entry = StructuredLogEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            level=level,
            message=message,
            correlation_id=self._correlation_id,
            component=self._component,
            metadata=metadata,
        )
        self._entries.append(entry)
        print(f"  [{level.name:>12}] [{self._component}] {message}")

    def trace(self, msg: str, **kw: Any) -> None: self._log(LogLevel.TRACE, msg, **kw)
    def debug(self, msg: str, **kw: Any) -> None: self._log(LogLevel.DEBUG, msg, **kw)
    def info(self, msg: str, **kw: Any) -> None: self._log(LogLevel.INFO, msg, **kw)
    def warn(self, msg: str, **kw: Any) -> None: self._log(LogLevel.WARN, msg, **kw)
    def error(self, msg: str, **kw: Any) -> None: self._log(LogLevel.ERROR, msg, **kw)

    def get_audit_trail(self) -> list[StructuredLogEntry]:
        return list(self._entries)


# ============================================================================
# SECTION 2: Configuration Management with Feature Flags
# ============================================================================

class FeatureFlag(enum.Enum):
    """Runtime-toggleable feature flags for the addition service."""
    ENABLE_OVERFLOW_PROTECTION = "enable_overflow_protection"
    ENABLE_AUDIT_LOGGING = "enable_audit_logging"
    ENABLE_METRICS_COLLECTION = "enable_metrics_collection"
    ENABLE_RETRY_ON_ADDITION_FAILURE = "enable_retry_on_addition_failure"
    ENABLE_RESULT_CACHING = "enable_result_caching"


@dataclass
class AdditionServiceConfiguration:
    """
    Centralized configuration for the Enterprise Addition Service.
    Supports environment-based overrides and runtime toggling.
    """
    max_operand_value: float = 1e308
    min_operand_value: float = -1e308
    max_retry_attempts: int = 3
    retry_backoff_base_ms: int = 100
    circuit_breaker_threshold: int = 5
    feature_flags: dict[str, bool] = field(default_factory=lambda: {
        FeatureFlag.ENABLE_OVERFLOW_PROTECTION.value: True,
        FeatureFlag.ENABLE_AUDIT_LOGGING.value: True,
        FeatureFlag.ENABLE_METRICS_COLLECTION.value: True,
        FeatureFlag.ENABLE_RETRY_ON_ADDITION_FAILURE.value: False,
        FeatureFlag.ENABLE_RESULT_CACHING.value: True,
    })

    def is_enabled(self, flag: FeatureFlag) -> bool:
        return self.feature_flags.get(flag.value, False)


# ============================================================================
# SECTION 3: Custom Exception Hierarchy
# ============================================================================

class AdditionDomainError(Exception):
    """Base exception for all addition-related domain errors."""
    def __init__(self, message: str, error_code: str, correlation_id: str = ""):
        super().__init__(message)
        self.error_code = error_code
        self.correlation_id = correlation_id


class OperandValidationError(AdditionDomainError):
    """Raised when an operand fails validation checks."""
    def __init__(self, operand_name: str, value: Any, reason: str):
        super().__init__(
            f"Operand '{operand_name}' with value '{value}' failed validation: {reason}",
            error_code="ERR_OPERAND_VALIDATION_001",
        )
        self.operand_name = operand_name
        self.invalid_value = value


class ArithmeticOverflowError(AdditionDomainError):
    """Raised when the result would exceed safe numeric bounds."""
    def __init__(self, a: float, b: float):
        super().__init__(
            f"Addition of {a} + {b} would cause overflow",
            error_code="ERR_ARITHMETIC_OVERFLOW_002",
        )


class CircuitBreakerOpenError(AdditionDomainError):
    """Raised when the circuit breaker is open due to too many failures."""
    def __init__(self):
        super().__init__(
            "Circuit breaker is OPEN. Addition service is temporarily unavailable.",
            error_code="ERR_CIRCUIT_BREAKER_003",
        )


# ============================================================================
# SECTION 4: Value Objects & Domain Models
# ============================================================================

T = TypeVar("T")


@dataclass(frozen=True)
class Result(Generic[T]):
    """
    Railway-oriented programming Result monad for safe error propagation.
    Because exceptions are so 2005.
    """
    value: T | None
    error: AdditionDomainError | None
    success: bool

    @staticmethod
    def ok(value: T) -> "Result[T]":
        return Result(value=value, error=None, success=True)

    @staticmethod
    def fail(error: AdditionDomainError) -> "Result[T]":
        return Result(value=None, error=error, success=False)


@dataclass(frozen=True)
class ValidatedOperand:
    """An operand that has passed all validation gates."""
    value: float
    validated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    validation_checksum: str = ""

    def __post_init__(self):
        if not self.validation_checksum:
            object.__setattr__(self, "validation_checksum", str(hash(self.value)))


@dataclass(frozen=True)
class AdditionRequest:
    """Immutable value object representing a request to perform addition."""
    request_id: str
    operand_a: ValidatedOperand
    operand_b: ValidatedOperand
    requested_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    priority: str = "NORMAL"


@dataclass(frozen=True)
class AdditionResponse:
    """Immutable value object representing the result of an addition operation."""
    request_id: str
    result: float
    computed_at: str
    computation_time_ms: float
    strategy_used: str
    audit_trail_length: int


# ============================================================================
# SECTION 5: Strategy Pattern — Pluggable Addition Algorithms
# ============================================================================

class AdditionStrategy(Protocol):
    """Protocol for addition algorithm implementations."""
    def add(self, a: float, b: float) -> float: ...
    @property
    def name(self) -> str: ...


class NaiveAdditionStrategy:
    """The classic a + b. Simple. Elegant. Boring."""
    @property
    def name(self) -> str:
        return "NaiveAddition"

    def add(self, a: float, b: float) -> float:
        return a + b


class KahanSummationStrategy:
    """
    Kahan summation algorithm for numerically stable addition.
    Because floating-point errors in 2 + 2 are UNACCEPTABLE.
    """
    @property
    def name(self) -> str:
        return "KahanCompensatedSummation"

    def add(self, a: float, b: float) -> float:
        # Compensated summation for two numbers (yes, this is overkill)
        sum_val = a
        compensation = 0.0
        y = b - compensation
        t = sum_val + y
        compensation = (t - sum_val) - y
        return t


class BitManipulationAdditionStrategy:
    """
    Addition using bitwise operations. Because why use the + operator
    when you can simulate a half-adder in Python?
    Only works for integers. Falls back to naive for floats.
    """
    @property
    def name(self) -> str:
        return "BitwiseHalfAdderSimulation"

    def add(self, a: float, b: float) -> float:
        if a != int(a) or b != int(b):
            return a + b  # Shameful fallback
        a_int, b_int = int(a), int(b)
        # Handle negative numbers via Python's arbitrary precision
        while b_int != 0:
            carry = a_int & b_int
            a_int = a_int ^ b_int
            b_int = carry << 1
        return float(a_int)


# ============================================================================
# SECTION 6: Strategy Factory (Factory + Strategy = Double Pattern Points)
# ============================================================================

class AdditionStrategyFactory:
    """
    AbstractSingletonProxyFactoryBean... just kidding.
    But this IS a factory that produces strategies based on operand analysis.
    """

    @staticmethod
    def select_optimal_strategy(a: float, b: float, logger: EnterpriseLogger) -> AdditionStrategy:
        """Dynamically selects the best addition algorithm based on operand characteristics."""
        logger.debug(f"Analyzing operands for optimal strategy selection: a={a}, b={b}")

        # Use Kahan for very small or very large numbers
        if abs(a) > 1e15 or abs(b) > 1e15 or abs(a) < 1e-15 or abs(b) < 1e-15:
            logger.info("Selected KahanSummationStrategy for numeric stability")
            return KahanSummationStrategy()

        # Use bitwise for integers (because we can)
        if a == int(a) and b == int(b) and abs(a) < 2**31 and abs(b) < 2**31:
            logger.info("Selected BitManipulationAdditionStrategy for integer operands")
            return BitManipulationAdditionStrategy()

        logger.info("Selected NaiveAdditionStrategy (operands within safe bounds)")
        return NaiveAdditionStrategy()


# ============================================================================
# SECTION 7: Validation Pipeline
# ============================================================================

class OperandValidator:
    """Multi-stage validation pipeline for arithmetic operands."""

    def __init__(self, config: AdditionServiceConfiguration, logger: EnterpriseLogger):
        self._config = config
        self._logger = logger

    def validate(self, value: Any, name: str) -> Result[ValidatedOperand]:
        """Run the full validation pipeline on an operand."""
        self._logger.debug(f"Beginning validation pipeline for operand '{name}'")

        # Stage 1: Type check
        if not isinstance(value, (int, float)):
            return Result.fail(OperandValidationError(name, value, "Must be numeric"))

        numeric_value = float(value)

        # Stage 2: NaN check
        if numeric_value != numeric_value:  # NaN check without math.isnan
            return Result.fail(OperandValidationError(name, value, "NaN is not a valid operand"))

        # Stage 3: Infinity check
        if abs(numeric_value) == float("inf"):
            return Result.fail(OperandValidationError(name, value, "Infinity is not a valid operand"))

        # Stage 4: Bounds check
        if numeric_value > self._config.max_operand_value:
            return Result.fail(OperandValidationError(name, value, "Exceeds maximum allowed value"))
        if numeric_value < self._config.min_operand_value:
            return Result.fail(OperandValidationError(name, value, "Below minimum allowed value"))

        self._logger.info(f"Operand '{name}' passed all validation stages", value=numeric_value)
        return Result.ok(ValidatedOperand(value=numeric_value))


# ============================================================================
# SECTION 8: Circuit Breaker Pattern
# ============================================================================

class CircuitBreakerState(enum.Enum):
    CLOSED = "CLOSED"       # Normal operation
    OPEN = "OPEN"           # Rejecting requests
    HALF_OPEN = "HALF_OPEN" # Testing recovery


class CircuitBreaker:
    """
    Circuit breaker for the addition service.
    Because what if addition starts failing? You need to protect downstream systems.
    """

    def __init__(self, threshold: int, logger: EnterpriseLogger):
        self._threshold = threshold
        self._failure_count = 0
        self._state = CircuitBreakerState.CLOSED
        self._logger = logger

    @property
    def state(self) -> CircuitBreakerState:
        return self._state

    def record_success(self) -> None:
        self._failure_count = 0
        self._state = CircuitBreakerState.CLOSED
        self._logger.trace("Circuit breaker: success recorded, counter reset")

    def record_failure(self) -> None:
        self._failure_count += 1
        self._logger.warn(f"Circuit breaker: failure #{self._failure_count}/{self._threshold}")
        if self._failure_count >= self._threshold:
            self._state = CircuitBreakerState.OPEN
            self._logger.error("Circuit breaker OPENED - addition service suspended")

    def allow_request(self) -> bool:
        return self._state != CircuitBreakerState.OPEN


# ============================================================================
# SECTION 9: Metrics Collection
# ============================================================================

@dataclass
class AdditionMetrics:
    """Prometheus-style metrics (without Prometheus, because that's a dependency)."""
    total_requests: int = 0
    successful_additions: int = 0
    failed_additions: int = 0
    total_computation_time_ms: float = 0.0
    strategy_usage: dict[str, int] = field(default_factory=dict)

    def record_success(self, strategy_name: str, time_ms: float) -> None:
        self.total_requests += 1
        self.successful_additions += 1
        self.total_computation_time_ms += time_ms
        self.strategy_usage[strategy_name] = self.strategy_usage.get(strategy_name, 0) + 1

    def record_failure(self) -> None:
        self.total_requests += 1
        self.failed_additions += 1

    def to_report(self) -> str:
        avg_time = (self.total_computation_time_ms / self.total_requests
                    if self.total_requests > 0 else 0)
        lines = [
            "=== Addition Service Metrics Report ===",
            f"  Total requests:       {self.total_requests}",
            f"  Successful additions: {self.successful_additions}",
            f"  Failed additions:     {self.failed_additions}",
            f"  Avg computation time: {avg_time:.4f} ms",
            f"  Strategy breakdown:   {json.dumps(self.strategy_usage)}",
        ]
        return "\n".join(lines)


# ============================================================================
# SECTION 10: The Enterprise Addition Service (Facade Pattern)
# ============================================================================

class EnterpriseAdditionService:
    """
    Enterprise-grade, production-ready addition service.

    Features:
    - Pluggable addition strategies (Strategy Pattern)
    - Dynamic strategy selection (Factory Pattern)
    - Input validation pipeline
    - Circuit breaker for fault tolerance
    - Structured logging with correlation IDs
    - Metrics collection
    - Result monad for error handling
    - Feature flags for runtime configuration

    All for the humble task of adding two numbers.
    """

    def __init__(self, config: AdditionServiceConfiguration | None = None):
        self._config = config or AdditionServiceConfiguration()
        self._metrics = AdditionMetrics()
        self._correlation_id = str(uuid.uuid4())
        self._logger = EnterpriseLogger("AdditionService", self._correlation_id)
        self._validator = OperandValidator(self._config, self._logger)
        self._circuit_breaker = CircuitBreaker(
            self._config.circuit_breaker_threshold, self._logger
        )
        self._logger.info("EnterpriseAdditionService initialized",
                         config=str(self._config))

    def add(self, a: Any, b: Any) -> Result[AdditionResponse]:
        """
        Perform enterprise-grade addition of two numbers.

        This method orchestrates the full addition pipeline:
        1. Circuit breaker check
        2. Operand validation
        3. Strategy selection
        4. Computation with timing
        5. Metrics recording
        6. Response construction

        Args:
            a: The first operand (will be validated)
            b: The second operand (will be validated)

        Returns:
            Result[AdditionResponse]: A Result monad containing either
            the successful response or a domain error.
        """
        request_id = str(uuid.uuid4())[:8]
        self._logger.info(f"--- Addition Request [{request_id}] ---")
        start_time = time.perf_counter()

        # Step 1: Circuit breaker gate
        if not self._circuit_breaker.allow_request():
            self._metrics.record_failure()
            return Result.fail(CircuitBreakerOpenError())

        # Step 2: Validate operands
        self._logger.debug("Entering validation pipeline")
        result_a = self._validator.validate(a, "operand_a")
        if not result_a.success:
            self._circuit_breaker.record_failure()
            self._metrics.record_failure()
            return Result.fail(result_a.error)

        result_b = self._validator.validate(b, "operand_b")
        if not result_b.success:
            self._circuit_breaker.record_failure()
            self._metrics.record_failure()
            return Result.fail(result_b.error)

        validated_a = result_a.value
        validated_b = result_b.value

        # Step 3: Build addition request
        request = AdditionRequest(
            request_id=request_id,
            operand_a=validated_a,
            operand_b=validated_b,
        )
        self._logger.debug(f"AdditionRequest constructed: {request}")

        # Step 4: Select optimal strategy
        strategy = AdditionStrategyFactory.select_optimal_strategy(
            validated_a.value, validated_b.value, self._logger
        )

        # Step 5: Execute addition with timing
        self._logger.info(f"Executing addition: {validated_a.value} + {validated_b.value}")
        compute_start = time.perf_counter()
        result_value = strategy.add(validated_a.value, validated_b.value)
        compute_end = time.perf_counter()
        computation_time_ms = (compute_end - compute_start) * 1000

        # Step 6: Overflow protection
        if self._config.is_enabled(FeatureFlag.ENABLE_OVERFLOW_PROTECTION):
            if abs(result_value) == float("inf"):
                self._circuit_breaker.record_failure()
                self._metrics.record_failure()
                return Result.fail(ArithmeticOverflowError(validated_a.value, validated_b.value))

        # Step 7: Record metrics
        self._circuit_breaker.record_success()
        self._metrics.record_success(strategy.name, computation_time_ms)

        # Step 8: Construct response
        response = AdditionResponse(
            request_id=request_id,
            result=result_value,
            computed_at=datetime.now(timezone.utc).isoformat(),
            computation_time_ms=computation_time_ms,
            strategy_used=strategy.name,
            audit_trail_length=len(self._logger.get_audit_trail()),
        )

        self._logger.info(
            f"Addition complete: {validated_a.value} + {validated_b.value} = {result_value}",
            strategy=strategy.name,
            time_ms=computation_time_ms,
        )

        return Result.ok(response)

    def get_metrics_report(self) -> str:
        return self._metrics.to_report()


# ============================================================================
# SECTION 11: Demo Runner
# ============================================================================

def print_banner() -> None:
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   ⚙️  ENTERPRISE ADDITION SERVICE v2.0.0-OVERKILL               ║
║                                                                  ║
║   "Because a + b deserves a 400-line architecture"               ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def run_demo() -> None:
    """Execute the full enterprise addition demo."""
    print_banner()

    service = EnterpriseAdditionService()

    # --- Demo 1: Simple integer addition ---
    print("\n" + "=" * 60)
    print("  DEMO 1: Add 2 + 3 (integer path → bitwise strategy)")
    print("=" * 60)
    result = service.add(2, 3)
    if result.success:
        r = result.value
        print(f"\n  ✅ Result: {r.result}")
        print(f"     Strategy: {r.strategy_used}")
        print(f"     Time: {r.computation_time_ms:.4f} ms")
        print(f"     Audit entries: {r.audit_trail_length}")

    # --- Demo 2: Float addition ---
    print("\n" + "=" * 60)
    print("  DEMO 2: Add 3.14 + 2.72 (float path → naive strategy)")
    print("=" * 60)
    result = service.add(3.14, 2.72)
    if result.success:
        r = result.value
        print(f"\n  ✅ Result: {r.result}")
        print(f"     Strategy: {r.strategy_used}")
        print(f"     Time: {r.computation_time_ms:.4f} ms")

    # --- Demo 3: Large numbers ---
    print("\n" + "=" * 60)
    print("  DEMO 3: Add 1e16 + 1.0 (large number → Kahan strategy)")
    print("=" * 60)
    result = service.add(1e16, 1.0)
    if result.success:
        r = result.value
        print(f"\n  ✅ Result: {r.result}")
        print(f"     Strategy: {r.strategy_used}")
        print(f"     Time: {r.computation_time_ms:.4f} ms")

    # --- Demo 4: Validation failure ---
    print("\n" + "=" * 60)
    print('  DEMO 4: Add "hello" + 5 (validation failure)')
    print("=" * 60)
    result = service.add("hello", 5)
    if not result.success:
        print(f"\n  ❌ Error: {result.error}")
        print(f"     Code: {result.error.error_code}")

    # --- Demo 5: Negative numbers ---
    print("\n" + "=" * 60)
    print("  DEMO 5: Add -42 + 42 (should equal zero)")
    print("=" * 60)
    result = service.add(-42, 42)
    if result.success:
        r = result.value
        print(f"\n  ✅ Result: {r.result}")
        print(f"     Strategy: {r.strategy_used}")

    # --- Metrics Report ---
    print("\n" + "=" * 60)
    print(service.get_metrics_report())
    print("=" * 60)

    # --- Pattern Summary ---
    print("""
╔══════════════════════════════════════════════════════════════════╗
║  Patterns & Principles Applied:                                  ║
║                                                                  ║
║  ✓ Strategy Pattern (3 addition algorithms)                      ║
║  ✓ Factory Pattern (dynamic strategy selection)                  ║
║  ✓ Result Monad (railway-oriented error handling)                ║
║  ✓ Circuit Breaker (fault tolerance)                             ║
║  ✓ Value Objects (immutable domain models)                       ║
║  ✓ Validation Pipeline (4-stage operand validation)              ║
║  ✓ Structured Logging (correlation IDs, levels)                  ║
║  ✓ Feature Flags (runtime configuration)                         ║
║  ✓ Metrics Collection (Prometheus-style)                         ║
║  ✓ Custom Exception Hierarchy                                    ║
║  ✓ Protocol-based typing (structural subtyping)                  ║
║  ✓ Facade Pattern (service orchestration)                        ║
║                                                                  ║
║  Lines of code to add two numbers: ~400                          ║
║  Lines actually needed: 1  (a + b)                               ║
║  Over-engineering factor: 400x                                   ║
╚══════════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    run_demo()
