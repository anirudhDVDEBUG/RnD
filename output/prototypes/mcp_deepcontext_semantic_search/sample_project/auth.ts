// Sample project file for semantic search demo
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

const JWT_SECRET = process.env.JWT_SECRET || 'dev-secret';

export interface UserPayload {
  userId: string;
  email: string;
  role: 'admin' | 'user' | 'viewer';
}

/** Verifies JWT token and attaches user to request */
export function authenticateRequest(req: Request, res: Response, next: NextFunction) {
  const header = req.headers.authorization;
  if (!header?.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing token' });
  }
  try {
    const payload = jwt.verify(header.slice(7), JWT_SECRET) as UserPayload;
    (req as any).user = payload;
    next();
  } catch {
    res.status(403).json({ error: 'Invalid token' });
  }
}

/** Creates a signed JWT for a user */
export function issueToken(user: UserPayload): string {
  return jwt.sign(user, JWT_SECRET, { expiresIn: '24h' });
}

/** Rate limiter middleware — sliding window per IP */
export function rateLimiter(maxRequests: number, windowMs: number) {
  const hits = new Map<string, number[]>();
  return (req: Request, res: Response, next: NextFunction) => {
    const ip = req.ip || 'unknown';
    const now = Date.now();
    const windowStart = now - windowMs;
    const timestamps = (hits.get(ip) || []).filter(t => t > windowStart);
    if (timestamps.length >= maxRequests) {
      return res.status(429).json({ error: 'Rate limit exceeded' });
    }
    timestamps.push(now);
    hits.set(ip, timestamps);
    next();
  };
}
