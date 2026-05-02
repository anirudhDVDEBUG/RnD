// Sample project file for semantic search demo
import { Pool } from 'pg';
import { queryWithRetry, withTransaction } from './database';
import { issueToken, UserPayload } from './auth';
import bcrypt from 'bcrypt';

export interface User {
  id: string;
  email: string;
  passwordHash: string;
  role: 'admin' | 'user' | 'viewer';
  createdAt: Date;
}

/** Registers a new user account with hashed password */
export async function registerUser(
  pool: Pool,
  email: string,
  password: string,
  role: 'user' | 'viewer' = 'user'
): Promise<{ user: User; token: string }> {
  const passwordHash = await bcrypt.hash(password, 12);
  const [user] = await queryWithRetry<User>(
    pool,
    `INSERT INTO users (email, password_hash, role) VALUES ($1, $2, $3) RETURNING *`,
    [email, passwordHash, role]
  );
  const token = issueToken({ userId: user.id, email: user.email, role: user.role });
  return { user, token };
}

/** Validates credentials and returns a session token */
export async function loginUser(pool: Pool, email: string, password: string): Promise<string | null> {
  const [user] = await queryWithRetry<User>(pool, `SELECT * FROM users WHERE email = $1`, [email]);
  if (!user) return null;
  const valid = await bcrypt.compare(password, user.passwordHash);
  if (!valid) return null;
  return issueToken({ userId: user.id, email: user.email, role: user.role });
}

/** Soft-deletes a user inside a transaction */
export async function deactivateUser(pool: Pool, userId: string): Promise<void> {
  await withTransaction(pool, async (client) => {
    await client.query(`UPDATE users SET deleted_at = NOW() WHERE id = $1`, [userId]);
    await client.query(`DELETE FROM sessions WHERE user_id = $1`, [userId]);
  });
}
