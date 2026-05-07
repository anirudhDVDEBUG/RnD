// Six committed email archetypes from the CosmoBlk email-design skill.
// Each archetype defines structure, tone guidance, and default sections.

const ARCHETYPES = {
  welcome: {
    name: "Welcome",
    description: "Onboarding new subscribers or customers",
    sections: ["hero_image", "headline", "body", "cta", "footer"],
    defaults: {
      headline: "Welcome aboard, {{first_name}}!",
      body: "We're thrilled to have you. Here's what to expect next.",
      cta_text: "Get Started",
      cta_href: "https://example.com/get-started",
    },
  },
  promotional: {
    name: "Promotional",
    description: "Sales, discounts, limited-time offers",
    sections: ["hero_image", "headline", "offer_badge", "body", "cta", "footer"],
    defaults: {
      headline: "Don't miss out — {{offer_percent}}% off everything",
      body: "For a limited time, save on our entire collection. Use code {{promo_code}} at checkout.",
      cta_text: "Shop Now",
      cta_href: "https://example.com/shop",
    },
  },
  newsletter: {
    name: "Newsletter",
    description: "Recurring content digests and updates",
    sections: ["logo_header", "intro", "article_cards", "footer"],
    defaults: {
      headline: "This week at {{brand_name}}",
      body: "Here's a round-up of what we've been working on.",
      cta_text: "Read More",
      cta_href: "https://example.com/blog",
    },
  },
  transactional: {
    name: "Transactional",
    description: "Order confirmations, receipts, shipping",
    sections: ["logo_header", "headline", "order_summary", "body", "footer"],
    defaults: {
      headline: "Your order is confirmed",
      body: "Thanks for your purchase, {{first_name}}. Here's your receipt.",
      cta_text: "Track Order",
      cta_href: "https://example.com/orders/{{order_id}}",
    },
  },
  reengagement: {
    name: "Re-engagement",
    description: "Win-back dormant subscribers",
    sections: ["hero_image", "headline", "body", "cta", "footer"],
    defaults: {
      headline: "We miss you, {{first_name}}",
      body: "It's been a while! Come back and see what's new.",
      cta_text: "Come Back",
      cta_href: "https://example.com/welcome-back",
    },
  },
  announcement: {
    name: "Announcement",
    description: "Product launches, feature releases, events",
    sections: ["hero_image", "headline", "body", "feature_list", "cta", "footer"],
    defaults: {
      headline: "Introducing {{feature_name}}",
      body: "We've been building something special, and it's finally here.",
      cta_text: "Learn More",
      cta_href: "https://example.com/launch",
    },
  },
};

// ESP-specific merge tag mappings
const ESP_TAGS = {
  nitrosend: { first_name: "{{first_name}}", unsubscribe: "{{unsubscribe}}" },
  klaviyo: { first_name: "{{ first_name }}", unsubscribe: "{% unsubscribe_url %}" },
  mailchimp: { first_name: "*|FNAME|*", unsubscribe: "*|UNSUB|*" },
  activecampaign: { first_name: "%FIRSTNAME%", unsubscribe: "%UNSUBSCRIBE%" },
  generic: { first_name: "{{first_name}}", unsubscribe: "{{unsubscribe}}" },
};

module.exports = { ARCHETYPES, ESP_TAGS };
