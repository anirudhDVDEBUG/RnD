/**
 * Intermind Simulator — local emulation of the Intermind MCP server.
 *
 * Intermind exposes MCP tools that let agents:
 *   - register themselves
 *   - start threaded conversations with other agents
 *   - send / receive messages within threads
 *   - list active threads and participants
 *
 * This file provides a pure-JS in-memory implementation of those primitives
 * so you can see the data model without installing Bun or cloning the real repo.
 */

import { randomUUID } from "node:crypto";

class IntermindServer {
  constructor() {
    /** @type {Map<string, {id: string, name: string, role: string, registeredAt: string}>} */
    this.agents = new Map();
    /** @type {Map<string, {id: string, title: string, participants: string[], messages: Array<{from: string, body: string, ts: string}>, createdAt: string}>} */
    this.threads = new Map();
  }

  // ── MCP Tool: register_agent ──────────────────────────────────────
  registerAgent(name, role = "general") {
    const id = `agent_${randomUUID().slice(0, 8)}`;
    const agent = { id, name, role, registeredAt: new Date().toISOString() };
    this.agents.set(id, agent);
    return agent;
  }

  // ── MCP Tool: list_agents ─────────────────────────────────────────
  listAgents() {
    return [...this.agents.values()];
  }

  // ── MCP Tool: start_thread ────────────────────────────────────────
  startThread(title, creatorId, participantIds) {
    const id = `thread_${randomUUID().slice(0, 8)}`;
    const allParticipants = [creatorId, ...participantIds.filter(p => p !== creatorId)];
    const thread = {
      id,
      title,
      participants: allParticipants,
      messages: [],
      createdAt: new Date().toISOString(),
    };
    this.threads.set(id, thread);
    return thread;
  }

  // ── MCP Tool: send_message ────────────────────────────────────────
  sendMessage(threadId, fromAgentId, body) {
    const thread = this.threads.get(threadId);
    if (!thread) throw new Error(`Thread ${threadId} not found`);
    if (!thread.participants.includes(fromAgentId)) {
      throw new Error(`Agent ${fromAgentId} is not a participant in thread ${threadId}`);
    }
    const msg = { from: fromAgentId, body, ts: new Date().toISOString() };
    thread.messages.push(msg);
    return msg;
  }

  // ── MCP Tool: get_messages ────────────────────────────────────────
  getMessages(threadId) {
    const thread = this.threads.get(threadId);
    if (!thread) throw new Error(`Thread ${threadId} not found`);
    return thread.messages;
  }

  // ── MCP Tool: list_threads ────────────────────────────────────────
  listThreads(agentId = null) {
    const all = [...this.threads.values()];
    if (!agentId) return all;
    return all.filter(t => t.participants.includes(agentId));
  }
}

export { IntermindServer };
