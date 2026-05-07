const mjml2html = require("mjml");
const { ARCHETYPES, ESP_TAGS } = require("./archetypes");

/**
 * Build a production-ready MJML email from a brand brief and archetype.
 *
 * @param {object} opts
 * @param {string} opts.archetype - One of: welcome, promotional, newsletter, transactional, reengagement, announcement
 * @param {object} opts.brand - Brand brief (name, logo_url, primary_color, secondary_color, accent_color, font_family, address)
 * @param {object} [opts.content] - Override default headline, body, cta_text, cta_href
 * @param {string} [opts.esp] - Target ESP: nitrosend, klaviyo, mailchimp, activecampaign, generic
 * @returns {{ mjml: string, html: string, errors: Array }}
 */
function buildEmail(opts) {
  const {
    archetype = "welcome",
    brand = {},
    content = {},
    esp = "generic",
  } = opts;

  const arch = ARCHETYPES[archetype];
  if (!arch) {
    throw new Error(`Unknown archetype "${archetype}". Choose from: ${Object.keys(ARCHETYPES).join(", ")}`);
  }

  const tags = ESP_TAGS[esp] || ESP_TAGS.generic;

  // Merge defaults with overrides
  const c = { ...arch.defaults, ...content };

  // Replace merge-tag placeholders with ESP-specific tags
  const resolve = (str) =>
    str
      .replace(/\{\{first_name\}\}/g, tags.first_name)
      .replace(/\{\{unsubscribe\}\}/g, tags.unsubscribe);

  const brandName = brand.name || "Acme Co";
  const logoUrl = brand.logo_url || "https://placehold.co/150x50/333/white?text=" + encodeURIComponent(brandName);
  const primaryColor = brand.primary_color || "#2563eb";
  const secondaryColor = brand.secondary_color || "#1e40af";
  const fontFamily = brand.font_family || "Inter, Helvetica, Arial, sans-serif";
  const address = brand.address || `${brandName} · 123 Main St, San Francisco, CA 94105`;

  // Build MJML sections based on archetype
  const heroSection = arch.sections.includes("hero_image")
    ? `
    <mj-section padding="0">
      <mj-column>
        <mj-image src="https://placehold.co/600x250/${primaryColor.replace("#", "")}/${secondaryColor.replace("#", "")}?text=${encodeURIComponent(arch.name + "+Email")}" alt="${arch.name} hero" fluid-on-mobile="true" />
      </mj-column>
    </mj-section>`
    : "";

  const offerBadge = arch.sections.includes("offer_badge")
    ? `
        <mj-text align="center" font-size="14px" color="#ffffff" padding="8px 16px"
          background-color="${primaryColor}" border-radius="20px" width="auto">
          LIMITED TIME OFFER
        </mj-text>`
    : "";

  const featureList = arch.sections.includes("feature_list")
    ? `
        <mj-text font-size="15px" color="#555555" line-height="1.6">
          &#8226; Faster performance across the board<br/>
          &#8226; Brand-new dashboard with real-time analytics<br/>
          &#8226; Seamless integrations with your favourite tools
        </mj-text>`
    : "";

  const articleCards = arch.sections.includes("article_cards")
    ? `
    <mj-section background-color="#ffffff" padding="10px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#333333" padding-bottom="4px">Latest from the blog</mj-text>
        <mj-divider border-color="#e5e7eb" border-width="1px" />
        <mj-text font-size="15px" color="#555555" line-height="1.5" padding-top="8px">
          <strong>How we redesigned our onboarding</strong><br/>
          A deep-dive into the UX decisions behind our new user flow.
        </mj-text>
        <mj-divider border-color="#e5e7eb" border-width="1px" />
        <mj-text font-size="15px" color="#555555" line-height="1.5" padding-top="8px">
          <strong>Q2 product roadmap</strong><br/>
          Everything we're shipping in the next quarter.
        </mj-text>
      </mj-column>
    </mj-section>`
    : "";

  const orderSummary = arch.sections.includes("order_summary")
    ? `
        <mj-table font-size="14px" color="#555555" padding="0 0 16px 0">
          <tr style="border-bottom:1px solid #e5e7eb;text-align:left;">
            <th style="padding:8px 0;">Item</th>
            <th style="padding:8px 0;">Qty</th>
            <th style="padding:8px 0;text-align:right;">Price</th>
          </tr>
          <tr style="border-bottom:1px solid #e5e7eb;">
            <td style="padding:8px 0;">Widget Pro</td>
            <td style="padding:8px 0;">1</td>
            <td style="padding:8px 0;text-align:right;">$49.00</td>
          </tr>
          <tr>
            <td style="padding:8px 0;font-weight:bold;">Total</td>
            <td></td>
            <td style="padding:8px 0;text-align:right;font-weight:bold;">$49.00</td>
          </tr>
        </mj-table>`
    : "";

  const mjmlSource = `<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="${fontFamily}" />
      <mj-text font-size="16px" color="#333333" line-height="1.5" />
      <mj-button background-color="${primaryColor}" color="#ffffff" border-radius="6px" font-size="16px" inner-padding="12px 28px" />
    </mj-attributes>
    <mj-style>
      a { color: ${primaryColor}; }
    </mj-style>
  </mj-head>
  <mj-body background-color="#f4f4f4">
    <!-- Logo header -->
    <mj-section background-color="#ffffff" padding="20px 20px 10px 20px">
      <mj-column>
        <mj-image src="${logoUrl}" width="150px" alt="${brandName} logo" />
      </mj-column>
    </mj-section>
    ${heroSection}
    <!-- Main content -->
    <mj-section background-color="#ffffff" padding="20px 30px">
      <mj-column>
        ${offerBadge}
        <mj-text font-size="26px" font-weight="bold" color="#111827" padding-bottom="8px">
          ${resolve(c.headline)}
        </mj-text>
        <mj-text font-size="16px" color="#555555">
          ${resolve(c.body)}
        </mj-text>
        ${orderSummary}
        ${featureList}
        <mj-button href="${c.cta_href}" align="left">
          ${c.cta_text}
        </mj-button>
      </mj-column>
    </mj-section>
    ${articleCards}
    <!-- Footer -->
    <mj-section background-color="#1f2937" padding="24px 20px">
      <mj-column>
        <mj-text color="#9ca3af" font-size="12px" align="center" line-height="1.6">
          ${address}<br/>
          <a href="${resolve("{{unsubscribe}}")}" style="color:#9ca3af;text-decoration:underline;">Unsubscribe</a>
          &nbsp;|&nbsp;
          <a href="https://example.com/preferences" style="color:#9ca3af;text-decoration:underline;">Email Preferences</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>`;

  const result = mjml2html(mjmlSource, { minify: false });

  return {
    mjml: mjmlSource,
    html: result.html,
    errors: result.errors,
  };
}

module.exports = { buildEmail };
