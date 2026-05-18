/**
 * Formatter — converts structured digest into readable bilingual output.
 */

const SECTION_LABELS = {
  policy: { en: 'POLICY & COMPLIANCE', zh: '政策合规', tag: 'POLICY' },
  tools: { en: 'TOOLS & FEATURES', zh: '工具功能', tag: 'TOOL' },
  buzz: { en: 'COMMUNITY BUZZ', zh: '社区热议', tag: 'BUZZ' },
  signals: { en: 'MARKET SIGNALS', zh: '市场信号', tag: 'SIGNAL' },
  actions: { en: 'ACTION ITEMS', zh: '行动建议', tag: 'ACTION' }
};

function formatDigest(digest) {
  const lines = [];

  // English section
  lines.push('--- ENGLISH ---');
  lines.push('');
  for (const [key, label] of Object.entries(SECTION_LABELS)) {
    const items = digest.sections[key] || [];
    if (items.length === 0) continue;
    items.forEach(item => {
      lines.push(`[${label.tag}] ${item.en}`);
    });
  }

  lines.push('');
  lines.push('--- 中文 ---');
  lines.push('');
  for (const [key, label] of Object.entries(SECTION_LABELS)) {
    const items = digest.sections[key] || [];
    if (items.length === 0) continue;
    items.forEach(item => {
      lines.push(`《${label.zh}》${item.zh}`);
    });
  }

  lines.push('');
  lines.push('--- END ---');

  return lines.join('\n');
}

module.exports = { formatDigest };
