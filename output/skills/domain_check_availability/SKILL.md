---
name: Domain Check Availability
description: |
  Check domain name availability across 7 registrars and 52 TLDs using the digmyname.com API.
  Triggers: "check domain", "domain availability", "is this domain available", "find available domains", "search domain name"
---

# Domain Check Availability

Check domain name availability from Claude Code. Queries the digmyname.com API to check availability across 7 registrars and 52 TLDs.

## When to use

- "Check if example.com is available"
- "Find available domains for my project name"
- "Is mydomain.io taken?"
- "Search domain availability across multiple TLDs"
- "Check domain name options for a new startup"

## How to use

1. **Check a single domain:**
   Use the digmyname.com API to check availability:
   ```bash
   curl -s "https://api.digmyname.com/check?domain=example.com"
   ```

2. **Check multiple TLDs for a name:**
   Query the API with just the name to get availability across supported TLDs:
   ```bash
   curl -s "https://api.digmyname.com/check?domain=example&tlds=com,net,io,dev,ai,co,org"
   ```

3. **Parse the response:**
   The API returns JSON with availability status and registrar pricing. Present results in a clear table format showing:
   - Domain name
   - Availability status (available/taken)
   - Registrar options and pricing (when available)

4. **Supported TLDs include:**
   52 TLDs across popular extensions (.com, .net, .org, .io, .dev, .ai, .co, .app, .xyz, and more).

5. **Supported registrars:**
   7 registrars are compared for pricing and availability.

## Tips

- Check multiple variations of a name at once to find the best available option.
- Consider newer TLDs like .dev, .ai, or .io if .com is taken.
- The API is free and requires no authentication.

## References

- Source: [seomarlboro/domain-check-skills](https://github.com/seomarlboro/domain-check-skills)
- API: [digmyname.com](https://digmyname.com)
