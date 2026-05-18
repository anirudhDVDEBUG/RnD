/**
 * Synthesizer — uses Claude to remix raw signals into structured digest.
 * Falls back to rule-based synthesis when no API key is available.
 */

async function synthesize(signals) {
  // If ANTHROPIC_API_KEY is set, use Claude for synthesis
  if (process.env.ANTHROPIC_API_KEY) {
    return await claudeSynthesize(signals);
  }

  // Fallback: rule-based synthesis (demo mode)
  return ruleSynthesize(signals);
}

async function claudeSynthesize(signals) {
  const Anthropic = require('@anthropic-ai/sdk');
  const client = new Anthropic();

  const prompt = `You are an Amazon seller intelligence analyst. Given these raw signals, create a structured daily digest with exactly 5 sections. For each item, provide both English and Chinese versions.

Raw signals:
${JSON.stringify(signals, null, 2)}

Output format (JSON):
{
  "date": "YYYY-MM-DD",
  "sections": {
    "policy": [{"en": "...", "zh": "..."}],
    "tools": [{"en": "...", "zh": "..."}],
    "buzz": [{"en": "...", "zh": "..."}],
    "signals": [{"en": "...", "zh": "..."}],
    "actions": [{"en": "...", "zh": "..."}]
  }
}

Be concise. Each item should be 1-2 sentences max. Actions should be specific and immediately actionable.`;

  const response = await client.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1500,
    messages: [{ role: 'user', content: prompt }]
  });

  try {
    const text = response.content[0].text;
    const jsonMatch = text.match(/\{[\s\S]*\}/);
    return JSON.parse(jsonMatch[0]);
  } catch (e) {
    console.warn('[WARN] Claude response parsing failed, using fallback');
    return ruleSynthesize(signals);
  }
}

function ruleSynthesize(signals) {
  const today = new Date().toISOString().slice(0, 10);

  const policy = signals.filter(s => s.category === 'policy');
  const tools = signals.filter(s => s.category === 'tool');
  const buzz = signals.filter(s => s.category === 'buzz');
  const market = signals.filter(s => s.category === 'signal');

  return {
    date: today,
    sections: {
      policy: policy.map(s => ({
        en: s.summary,
        zh: translateToZh(s)
      })),
      tools: tools.map(s => ({
        en: s.summary,
        zh: translateToZh(s)
      })),
      buzz: buzz.map(s => ({
        en: s.summary,
        zh: translateToZh(s)
      })),
      signals: market.map(s => ({
        en: s.summary,
        zh: translateToZh(s)
      })),
      actions: generateActions(signals)
    }
  };
}

function translateToZh(signal) {
  // Static translations for demo mode
  const translations = {
    'FBA Fee Structure Update': 'FBA费用结构更新 — 6月1日起标准尺寸商品平均每件上涨$0.15，超大尺寸上涨$0.35。',
    'Brand Analytics: Search Funnel Report': '品牌分析新增搜索漏斗报告，展示从搜索词到购买的完整客户路径。',
    'A+ Content Template Expansion': '品牌注册卖家新增5个A+内容模板，包含对比图表、生活场景图和视频模块。',
    'Return Fraud Spike Discussion': '多位卖家反映"未收到商品"索赔激增30%，疑似针对电子品类的协同欺诈。',
    'Prime Day 2026 Prep Thread': '社区建议现在开始备货Prime Day，头部ASIN建议备3倍库存，闪购提交下周开放。',
    'Category Pricing Trends (AM/PM Podcast)': '电子品类均价周环比下降8%；家居厨房月环比上涨12%；杂货自有品牌利润扩大。',
    'Marketplace Pulse: Q2 Seller Growth': 'Q2新卖家注册同比增15%，主要来自东南亚。新卖家平均4.2个月达到$10K营收。',
    'EU Digital Services Act Compliance Deadline': '亚马逊欧洲站要求所有卖家7月15日前完成商业验证更新，否则面临账号暂停。'
  };
  return translations[signal.title] || signal.summary;
}

function generateActions(signals) {
  return [
    {
      en: 'Review and update FBA fee projections in your profit calculator before June 1 changes take effect.',
      zh: '在6月1日费用变更生效前，更新利润计算器中的FBA费用预测。'
    },
    {
      en: 'Start Prime Day inventory planning now — target 3x stock for top ASINs, submit Lightning Deal applications next week.',
      zh: '立即开始Prime Day备货规划 — 头部ASIN备3倍库存，下周提交闪购申请。'
    },
    {
      en: 'EU sellers: complete business verification update before July 15 deadline to avoid suspension.',
      zh: '欧洲站卖家：7月15日前完成商业验证更新，避免账号暂停。'
    },
    {
      en: 'Monitor return claims closely — if seeing INR spike, document and file with Seller Support immediately.',
      zh: '密切监控退货索赔 — 如发现"未收到"激增，立即记录并向卖家支持提交申诉。'
    }
  ];
}

module.exports = { synthesize };
