<!-- Project-specific CLAUDE.md customizations -->
## Project-Specific Guidelines

This is a sample e-commerce project using the cc-boilerplate synchronization system.

- Use TypeScript for all new code
- Follow React Hooks patterns for frontend components
- API calls use fetch with async/await
- All monetary amounts use Decimal.js for precision
- Database queries use Prisma ORM

## Domain-Specific Rules

### Payment Processing

- All payment code requires PCI compliance review
- Use Stripe API v3 for payment processing
- Log all payment events for audit trail
- Never store raw credit card data

### User Data Handling

- All PII must be encrypted at rest
- GDPR compliance required for EU users
- User sessions expire after 24 hours
- Password minimum 12 characters with complexity

### API Design

- Use RESTful conventions
- Version all APIs (e.g., /api/v1/)
- Rate limiting: 1000 requests/hour per user
- Always return consistent error format:

  ```json
  {
    "error": {
      "code": "VALIDATION_ERROR",
      "message": "Invalid email format",
      "details": {}
    }
  }
  ```

### Testing Requirements

- Unit test coverage minimum 80%
- Integration tests for all payment flows
- E2E tests for critical user journeys
- Performance tests for checkout process

### Deployment Rules

- Blue/green deployments only
- Database migrations run separately
- Feature flags for major changes
- Rollback plan required for each release
