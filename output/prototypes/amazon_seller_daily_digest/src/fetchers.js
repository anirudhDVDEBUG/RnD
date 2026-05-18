/**
 * Source fetchers — in demo mode returns mock data.
 * In production, each fetcher would scrape/call its respective source.
 */

function getMockSignals() {
  const today = new Date().toISOString().slice(0, 10);
  return [
    {
      source: 'official',
      category: 'policy',
      title: 'FBA Fee Structure Update',
      summary: 'Amazon announces FBA fee increase effective June 1, 2026. Standard-size items will see an average increase of $0.15 per unit. Oversize items increase by $0.35.',
      url: 'https://sellercentral.amazon.com/announcements',
      date: today
    },
    {
      source: 'official',
      category: 'tool',
      title: 'Brand Analytics: Search Funnel Report',
      summary: 'New Search Funnel report now available in Brand Analytics. Shows customer journey from search term to purchase, including click-through and conversion at each stage.',
      url: 'https://sellercentral.amazon.com/brand-analytics',
      date: today
    },
    {
      source: 'official',
      category: 'tool',
      title: 'A+ Content Template Expansion',
      summary: 'Five new A+ Content templates released for Brand Registry sellers. Includes comparison charts, lifestyle imagery modules, and video integration slots.',
      url: 'https://sellercentral.amazon.com/a-plus',
      date: today
    },
    {
      source: 'community',
      category: 'buzz',
      title: 'Return Fraud Spike Discussion',
      summary: 'Multiple sellers on r/FBAsellers and Amazon forums reporting 30% increase in "item not received" claims over past 2 weeks. Suspected coordinated fraud ring targeting electronics category.',
      url: 'https://sellerforums.amazon.com/threads/returns-spike',
      date: today
    },
    {
      source: 'community',
      category: 'buzz',
      title: 'Prime Day 2026 Prep Thread',
      summary: 'Community consensus: start inventory prep now for July Prime Day. Top sellers recommend 3x normal stock levels for top 20% ASINs. Lightning Deal submissions opening next week.',
      url: 'https://sellerforums.amazon.com/threads/prime-day-2026',
      date: today
    },
    {
      source: 'podcast',
      category: 'signal',
      title: 'Category Pricing Trends (AM/PM Podcast)',
      summary: 'Electronics avg. selling price down 8% week-over-week due to competitor flooding. Home & Kitchen up 12% MoM driven by summer seasonal demand. Grocery private label margins expanding.',
      url: 'https://ampmpodcast.com/latest',
      date: today
    },
    {
      source: 'newsletter',
      category: 'signal',
      title: 'Marketplace Pulse: Q2 Seller Growth',
      summary: 'New seller registrations up 15% in Q2 vs Q1, primarily from Southeast Asian sellers. Average new seller reaches $10K revenue in 4.2 months (down from 5.8 months last year).',
      url: 'https://marketplacepulse.com/weekly',
      date: today
    },
    {
      source: 'newsletter',
      category: 'policy',
      title: 'EU Digital Services Act Compliance Deadline',
      summary: 'Amazon EU requires all sellers to update business verification by July 15. Non-compliant accounts face suspension. Affects sellers with EU-facing listings.',
      url: 'https://marketplacepulse.com/eu-dsa',
      date: today
    }
  ];
}

async function fetchAllSources() {
  // In production with proper source access, this would run real fetchers in parallel:
  // const [official, community, podcast, newsletter] = await Promise.all([
  //   fetchOfficial(),
  //   fetchCommunity(),
  //   fetchPodcasts(),
  //   fetchNewsletters()
  // ]);
  // return [...official, ...community, ...podcast, ...newsletter];

  // Demo mode: return mock signals
  return getMockSignals();
}

module.exports = { fetchAllSources };
