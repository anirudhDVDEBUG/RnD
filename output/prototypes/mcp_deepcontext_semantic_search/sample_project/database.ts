// Sample project file for semantic search demo
import { Pool, PoolConfig } from 'pg';

export interface ConnectionPoolOptions {
  maxConnections: number;
  idleTimeoutMs: number;
  connectionTimeoutMs: number;
}

const DEFAULT_POOL_OPTS: ConnectionPoolOptions = {
  maxConnections: 20,
  idleTimeoutMs: 30_000,
  connectionTimeoutMs: 5_000,
};

/** Creates a connection pool with health-check pinging */
export function createConnectionPool(dsn: string, opts?: Partial<ConnectionPoolOptions>) {
  const config: PoolConfig = {
    connectionString: dsn,
    max: opts?.maxConnections ?? DEFAULT_POOL_OPTS.maxConnections,
    idleTimeoutMillis: opts?.idleTimeoutMs ?? DEFAULT_POOL_OPTS.idleTimeoutMs,
    connectionTimeoutMillis: opts?.connectionTimeoutMs ?? DEFAULT_POOL_OPTS.connectionTimeoutMs,
  };
  return new Pool(config);
}

/** Runs a single query with automatic retry on connection errors */
export async function queryWithRetry<T>(
  pool: Pool,
  sql: string,
  params: unknown[] = [],
  retries = 3
): Promise<T[]> {
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const result = await pool.query(sql, params);
      return result.rows as T[];
    } catch (err: any) {
      if (attempt === retries || !isConnectionError(err)) throw err;
      await sleep(100 * attempt);
    }
  }
  return [];
}

function isConnectionError(err: any): boolean {
  return ['ECONNREFUSED', 'ECONNRESET', 'ETIMEDOUT'].includes(err.code);
}

function sleep(ms: number) {
  return new Promise(r => setTimeout(r, ms));
}

/** Transaction wrapper with automatic rollback on error */
export async function withTransaction<T>(pool: Pool, fn: (client: any) => Promise<T>): Promise<T> {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');
    const result = await fn(client);
    await client.query('COMMIT');
    return result;
  } catch (err) {
    await client.query('ROLLBACK');
    throw err;
  } finally {
    client.release();
  }
}
