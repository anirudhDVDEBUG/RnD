---
name: overkill
description: |
  Over-engineer any coding task to the extreme. Takes simple requests and produces maximally robust, enterprise-grade, over-engineered implementations with exhaustive error handling, abstractions, design patterns, and documentation.
  Triggers: over-engineer, overkill, enterprise-grade, maximum robustness, go overboard
---

# Overkill — Over-Engineer Everything

A Claude Code skill that takes any coding task and deliberately over-engineers the solution to an absurd degree. Instead of simple, minimal implementations, Overkill produces enterprise-grade, maximally abstracted, pattern-heavy code.

## When to use

- "Over-engineer this for me"
- "Go overkill on this implementation"
- "Make this enterprise-grade"
- "Give me the most robust version possible"
- "Apply every design pattern you know to this"

## How to use

1. **Identify the task**: Take the user's simple coding request (e.g., "add two numbers", "read a file", "make a TODO app").
2. **Apply maximum over-engineering**: Transform the solution using as many of the following as contextually applicable:
   - **Design patterns**: Factory, Strategy, Observer, Builder, Singleton, Adapter, Decorator, Command, etc.
   - **Abstraction layers**: Interfaces, abstract base classes, dependency injection, inversion of control.
   - **Error handling**: Exhaustive try/catch blocks, custom exception hierarchies, retry logic with exponential backoff, circuit breakers.
   - **Configuration**: Environment-based config, feature flags, runtime toggleable options.
   - **Logging & observability**: Structured logging at every level (debug, info, warn, error), metrics collection stubs, tracing spans.
   - **Validation**: Input validation, schema validation, runtime type checking, assertion guards.
   - **Documentation**: JSDoc/docstrings on every method, README generation, inline comments explaining "why" for trivial operations.
   - **Testing**: Unit tests, integration tests, edge-case tests, property-based test stubs.
   - **Type safety**: Full generic types, branded types, discriminated unions, exhaustiveness checks.
3. **Maintain functionality**: Despite the over-engineering, the code must still work correctly and solve the original problem.
4. **Add a humorous touch**: Include comments or naming that acknowledge the absurdity (e.g., `AbstractSingletonProxyFactoryBean`, `EnterpriseFizzBuzzStrategy`).
5. **Deliver the result**: Present the over-engineered solution with a brief note on what patterns and principles were applied.

## Guidelines

- The over-engineering should be **fun and educational** — it showcases design patterns and best practices taken to their logical extreme.
- Always ensure the code **compiles/runs correctly** despite the complexity.
- Match the language and framework the user is working in.
- If no language is specified, default to TypeScript for maximum type-level over-engineering potential.
- Scale the over-engineering to the simplicity of the task — the simpler the request, the more absurdly over-engineered the response.

## References

- Source: [claude-overkill](https://github.com/santiago-vargas-de-kruijf/claude-overkill)
