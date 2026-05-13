---
name: buy-me-a-car
description: |
  End-to-end used car buying assistant — multi-site research, mass dealer outreach, OTD negotiation with 50-state fee data, CARFAX analysis, and decision tracking.
  TRIGGER when: user mentions buying a used car, car shopping, dealer negotiation, OTD price, CARFAX review, vehicle comparison, or dealer outreach.
  DO NOT TRIGGER when: user is discussing car maintenance, repair, insurance, or new car purchases unrelated to negotiation.
---

# buy-me-a-car

Claude Code skill for end-to-end used car buying: multi-site research, mass dealer outreach, OTD negotiation with 50-state fee data, CARFAX analysis, and decision tracking.

## When to use

- "Help me find a used car under $25k"
- "Negotiate the OTD price with this dealer"
- "Analyze this CARFAX report for red flags"
- "Compare these used car listings across sites"
- "Draft outreach emails to dealers for a 2022 Civic"

## How to use

### 1. Research & Search

Gather the user's requirements (budget, make/model preferences, mileage, location radius) and search across listing sites (Autotrader, Cars.com, CarGurus, Facebook Marketplace, Craigslist) to compile a candidate list.

- Normalize listings into a comparison table: year, make, model, trim, mileage, asking price, dealer/private, location, listing URL.
- Flag deals rated "great" or "good" by aggregator pricing tools.

### 2. CARFAX / History Analysis

When the user provides a CARFAX or vehicle history report:

- Summarize ownership history, accident records, service regularity, and title status.
- Flag red flags: salvage/rebuilt title, frame damage, odometer discrepancies, flood damage, excessive owners.
- Provide a risk rating: **Green** (clean), **Yellow** (minor concerns), **Red** (significant risk).

### 3. OTD Price Calculation

Calculate the realistic out-the-door (OTD) price using 50-state fee data:

- **Base price** (negotiated)
- **Sales tax** (state + local rates)
- **Title & registration fees** (state-specific)
- **Doc fee** (state caps where applicable)
- **Common dealer add-ons** to watch for and decline (e.g., nitrogen tires, VIN etching, fabric protection)

Present a breakdown so the user knows exactly what to expect.

### 4. Dealer Outreach

Draft professional outreach messages for mass dealer contact:

- Introduce the buyer and specific vehicle of interest (stock number if available).
- Request the best OTD price including all fees.
- Keep tone firm but polite; mention competing offers when applicable.
- Generate templates for email, text, and phone scripts.

### 5. Negotiation Strategy

- Anchor offers using market data (KBB, Edmunds, NADA values).
- Suggest counter-offer amounts based on listing age, market days, and comparable sales.
- Advise on walk-away price thresholds.
- Track negotiation rounds in a decision log.

### 6. Decision Tracking

Maintain a structured decision tracker:

| Vehicle | Asking | Our Offer | Counter | OTD Est. | Status | Notes |
|---------|--------|-----------|---------|----------|--------|-------|
| 2022 Civic EX | $24,500 | $22,000 | $23,200 | $25,100 | Pending | Clean CARFAX |

Update as negotiations progress. Recommend a final pick based on value, condition, and total cost.

## References

- Source repository: [DaizeDong/buy-me-a-car](https://github.com/DaizeDong/buy-me-a-car)
- Topics: car-buying, negotiation, dealer outreach, CARFAX, claude-skill
