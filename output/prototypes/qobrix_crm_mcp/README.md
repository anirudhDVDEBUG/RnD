# Qobrix CRM MCP Server

**Read-only MCP server giving Claude access to 42 tools across 13 real-estate CRM entity groups (contacts, properties, leads, listings, opportunities, tasks, etc.), with all fields mapped to RESO Data Dictionary 2.0 canonical names.**

## Headline Result

```
$ bash run.sh

  PROPERTY SEARCH — Dubai Marina, under $2M
  ListingId | Type      | Beds | Price (USD)  | Status | Location
  prop-101  | Apartment | 2    | $1,500,000   | Active | Dubai Marina

  DEAL PIPELINE — Opportunities in Negotiation stage
  OppId   | Contact         | Value       | Probability | Expected Close
  opp-301 | Sarah Al-Rashid | $1,450,000  | 70%         | 2026-05-30
```

One `npm install && bash run.sh` — no API keys needed for the demo.

## Next Steps

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install, configure, connect to Claude in 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, RESO mapping, limitations
- **[Source repo](https://github.com/sharpsir-group/qobrix-crm-mcp)** — Full 42-tool server
