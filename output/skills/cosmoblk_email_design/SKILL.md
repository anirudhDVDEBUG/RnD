---
name: Email Design
description: |
  Design and build anti-slop marketing emails using six committed archetypes, brand-aware briefs, real imagery, and real footers. Outputs production-ready MJML/HTML compatible with any ESP (Nitrosend, Klaviyo, Mailchimp, ActiveCampaign) via MCP.
  
  Triggers:
  - "design an email"
  - "create email template"
  - "build an MJML email"
  - "email campaign"
  - "marketing email"
---

# Email Design Skill

Anti-slop email design — six committed archetypes, brand-aware briefs, real imagery, real footers. Works with any ESP via MCP (Nitrosend, Klaviyo, Mailchimp, ActiveCampaign).

## When to use

- "Design a welcome email for my SaaS product"
- "Create an MJML email template for a product launch"
- "Build a promotional email campaign with my brand colors"
- "Generate a newsletter email with real footer and unsubscribe links"
- "Design a transactional email for order confirmation"

## How to use

### 1. Gather the brand brief

Before designing, collect:
- **Brand name** and logo URL
- **Brand colors** (primary, secondary, accent)
- **Tone/voice** (e.g., professional, playful, minimal)
- **Footer details** (company address, social links, unsubscribe text)
- **Target ESP** (Nitrosend, Klaviyo, Mailchimp, ActiveCampaign, or generic)

### 2. Choose an archetype

Select from six email archetypes:

| Archetype | Use case |
|-----------|----------|
| **Welcome** | Onboarding new subscribers or customers |
| **Promotional** | Sales, discounts, limited-time offers |
| **Newsletter** | Recurring content digests and updates |
| **Transactional** | Order confirmations, receipts, shipping |
| **Re-engagement** | Win-back dormant subscribers |
| **Announcement** | Product launches, feature releases, events |

### 3. Build the email

1. **Define structure**: Use MJML components (`mj-section`, `mj-column`, `mj-text`, `mj-image`, `mj-button`) to lay out the email.
2. **Apply brand styling**: Inject brand colors, fonts, and logo into the MJML template.
3. **Add real content**: Use actual imagery URLs (not placeholders), real copy, and genuine footer with physical address and unsubscribe link.
4. **Anti-slop rules**:
   - No generic stock photo placeholders — use real or specified image URLs
   - No filler lorem ipsum — write actual copy matching the brand voice
   - Include a real, compliant footer (CAN-SPAM / GDPR)
   - Every CTA button must have a meaningful `href`

### 4. Output production-ready code

```mjml
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="Inter, Helvetica, Arial, sans-serif" />
      <mj-text font-size="16px" color="#333333" />
      <mj-button background-color="#YOUR_BRAND_COLOR" color="#ffffff" border-radius="6px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f4f4f4">
    <!-- Header with logo -->
    <mj-section background-color="#ffffff">
      <mj-column>
        <mj-image src="LOGO_URL" width="150px" />
      </mj-column>
    </mj-section>
    <!-- Main content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold">Your Headline Here</mj-text>
        <mj-text>Your body copy here.</mj-text>
        <mj-button href="https://your-cta-link.com">Call to Action</mj-button>
      </mj-column>
    </mj-section>
    <!-- Footer -->
    <mj-section background-color="#333333" padding="20px">
      <mj-column>
        <mj-text color="#999999" font-size="12px" align="center">
          Company Name · 123 Street, City, State ZIP
          <br/><a href="{{unsubscribe}}" style="color:#999999;">Unsubscribe</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
```

### 5. ESP delivery via MCP

If an MCP server is configured for an ESP (e.g., Nitrosend, Klaviyo, Mailchimp, ActiveCampaign), use the available MCP tools to:
- Create/update the email template in the ESP
- Set up the campaign with subject line and recipient list
- Schedule or send the email

Adapt merge tags to the target ESP:
- **Nitrosend**: `{{first_name}}`, `{{unsubscribe}}`
- **Klaviyo**: `{{ first_name }}`, `{% unsubscribe_url %}`
- **Mailchimp**: `*|FNAME|*`, `*|UNSUB|*`
- **ActiveCampaign**: `%FIRSTNAME%`, `%UNSUBSCRIBE%`

## References

- Source: [CosmoBlk/email-design](https://github.com/CosmoBlk/email-design) — Email design skill for Claude Code
- [MJML Documentation](https://mjml.io/documentation/) — The framework used for responsive email markup
