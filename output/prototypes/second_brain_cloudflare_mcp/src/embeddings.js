/**
 * Mock embedding generator — produces deterministic 64-dim vectors from text
 * using a simple hash-based approach. In production, this would call OpenAI's
 * text-embedding-ada-002 (1536 dims) via Cloudflare Workers AI or direct API.
 */

const DIMS = 64;

function hashCode(str) {
  let h = 0;
  for (let i = 0; i < str.length; i++) {
    h = ((h << 5) - h + str.charCodeAt(i)) | 0;
  }
  return h;
}

export function generateEmbedding(text) {
  const words = text.toLowerCase().split(/\s+/);
  const vec = new Float64Array(DIMS);

  for (const word of words) {
    const h = hashCode(word);
    for (let d = 0; d < DIMS; d++) {
      // Spread each word's influence across dimensions via simple mixing
      const seed = h ^ (d * 2654435761);
      vec[d] += ((seed & 0xffff) / 32768.0 - 1.0);
    }
  }

  // L2 normalize
  let norm = 0;
  for (let d = 0; d < DIMS; d++) norm += vec[d] * vec[d];
  norm = Math.sqrt(norm) || 1;
  for (let d = 0; d < DIMS; d++) vec[d] /= norm;

  return Array.from(vec);
}

export function cosineSimilarity(a, b) {
  let dot = 0, na = 0, nb = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    na += a[i] * a[i];
    nb += b[i] * b[i];
  }
  return dot / (Math.sqrt(na) * Math.sqrt(nb) || 1);
}
