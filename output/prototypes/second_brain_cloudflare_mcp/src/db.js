import Database from "better-sqlite3";
import { generateEmbedding, cosineSimilarity } from "./embeddings.js";

const SCHEMA = `
CREATE TABLE IF NOT EXISTS memories (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  content    TEXT    NOT NULL,
  tags       TEXT    DEFAULT '',
  metadata   TEXT    DEFAULT '{}',
  embedding  TEXT    NOT NULL,
  created_at TEXT    DEFAULT (datetime('now')),
  updated_at TEXT    DEFAULT (datetime('now'))
);
`;

export class MemoryStore {
  constructor(dbPath = ":memory:") {
    this.db = new Database(dbPath);
    this.db.exec(SCHEMA);
  }

  remember({ content, tags = [], metadata = {} }) {
    const embedding = generateEmbedding(content);
    const stmt = this.db.prepare(
      `INSERT INTO memories (content, tags, metadata, embedding)
       VALUES (?, ?, ?, ?)`
    );
    const info = stmt.run(
      content,
      JSON.stringify(tags),
      JSON.stringify(metadata),
      JSON.stringify(embedding)
    );
    return { id: info.lastInsertRowid, content, tags, metadata };
  }

  recall(query, topK = 5) {
    const qEmbed = generateEmbedding(query);
    const rows = this.db.prepare("SELECT * FROM memories").all();

    const scored = rows.map((row) => {
      const embedding = JSON.parse(row.embedding);
      const score = cosineSimilarity(qEmbed, embedding);
      return {
        id: row.id,
        content: row.content,
        tags: JSON.parse(row.tags),
        metadata: JSON.parse(row.metadata),
        score: Math.round(score * 1000) / 1000,
        created_at: row.created_at,
      };
    });

    scored.sort((a, b) => b.score - a.score);
    return scored.slice(0, topK);
  }

  forget(id) {
    const info = this.db.prepare("DELETE FROM memories WHERE id = ?").run(id);
    return { deleted: info.changes > 0, id };
  }

  listMemories({ tag, limit = 20 } = {}) {
    let rows;
    if (tag) {
      rows = this.db
        .prepare(
          "SELECT id, content, tags, metadata, created_at FROM memories WHERE tags LIKE ? LIMIT ?"
        )
        .all(`%"${tag}"%`, limit);
    } else {
      rows = this.db
        .prepare(
          "SELECT id, content, tags, metadata, created_at FROM memories LIMIT ?"
        )
        .all(limit);
    }
    return rows.map((r) => ({
      ...r,
      tags: JSON.parse(r.tags),
      metadata: JSON.parse(r.metadata),
    }));
  }

  close() {
    this.db.close();
  }
}
