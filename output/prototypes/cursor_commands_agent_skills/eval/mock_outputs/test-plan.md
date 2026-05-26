## Test Plan: auth/register.py

### Unit Tests

| # | Name | Input | Expected | Rationale |
|---|------|-------|----------|-----------|
| 1 | test_valid_registration | valid email + password | 201 + user object | Happy path |
| 2 | test_duplicate_email | existing email | 409 conflict | Uniqueness constraint |
| 3 | test_weak_password | "123" | 400 + error message | Password policy enforcement |
| 4 | test_missing_fields | empty body | 422 + validation errors | Input validation |

### Integration Tests

| # | Name | Setup | Steps | Expected |
|---|------|-------|-------|----------|
| 1 | test_db_persistence | empty users table | POST /register, then SELECT | Row exists with hashed password |
| 2 | test_welcome_email | mock SMTP | POST /register | Email queued to correct address |

### Edge Cases
- Unicode characters in name/email fields
- Extremely long input strings (>10 KB)
- Concurrent duplicate registrations (race condition)
- SQL reserved words in name field

### Coverage Estimate
Estimated 85% line coverage. Gaps: error-handling branches for database connection failures and SMTP timeouts.
