---
name: small_business_ops
description: |
  Small business operations assistant using Claude connectors for QuickBooks, Xero, Stripe, PayPal, Square, HubSpot, and Gmail. Provides pre-built workflows for weekly business tasks.
  
  Triggers: small business automation, Monday brief, invoice chase, close month, payroll planning, CRM maintenance, Friday brief, quarterly review, complaint handling, campaign management, call list generation
---

# Small Business Ops

A skill for small business owners to run weekly operational workflows using Claude's MCP connectors to their business stack.

## When to use

- "Generate my Monday brief with open invoices and this week's priorities"
- "Chase outstanding invoices older than 30 days"
- "Help me close the month and reconcile accounts"
- "Run CRM maintenance and flag stale leads"
- "Create my Friday brief summarizing this week's revenue and next week's plan"

## How to use

### Prerequisites

Ensure you have MCP connectors configured for your business tools (any combination of):
- **Accounting**: QuickBooks, Xero
- **Payments**: Stripe, PayPal, Square
- **CRM**: HubSpot
- **Email**: Gmail

### Core Workflows

1. **Monday Brief** — Pull open invoices, upcoming payments, calendar items, and top CRM opportunities into a single prioritized action list for the week.

2. **Invoice Chase** — Identify overdue invoices from your accounting connector, draft follow-up emails via Gmail, and log contact attempts in your CRM.

3. **Close Month** — Reconcile transactions across payment processors and accounting software, flag discrepancies, and generate a summary P&L snapshot.

4. **Plan Payroll** — Pull hours/contractor invoices, calculate totals, and prepare payment runs.

5. **Call List** — Query CRM for leads/customers needing follow-up, rank by priority, and output a structured call sheet.

6. **Handle Complaint** — Draft a response to a customer complaint using order history from your payment processor and prior communications.

7. **Run Campaign** — Plan and draft a marketing campaign using CRM segments and email templates.

8. **Friday Brief** — Summarize the week's revenue, new customers, resolved issues, and set up next week's priorities.

9. **Quarterly Review** — Aggregate 3 months of financial data, CRM growth metrics, and campaign performance into a board-ready summary.

10. **CRM Maintenance** — Deduplicate contacts, update deal stages, and archive dead leads.

### Steps

1. Tell Claude which workflow you want to run (e.g., "Run my Monday brief")
2. Claude will query your connected tools via MCP connectors
3. Review the generated output — approve actions like sending emails or updating records
4. Optionally schedule recurring workflows using `/schedule`

### Customization

Add a `CLAUDE.md` in your project with business-specific context:
```markdown
# My Business Context
- Business: [Your business name and type]
- Invoice terms: Net 30
- Key accounts: [List VIP customers]
- Payroll schedule: Bi-weekly, Friday
- Revenue targets: [Monthly/quarterly goals]
```

## References

- Source video: https://www.youtube.com/watch?v=GXq7mi1UQQ4
- Small Business Skills Guide: https://brad-b.kit.com/bb4f80fd45
