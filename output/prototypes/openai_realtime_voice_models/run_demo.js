/**
 * Orchestrator: starts mock server, runs client demo, then shuts down.
 */
const { startServer } = require("./mock_server");
const { runDemo } = require("./client");

async function main() {
  const wss = startServer();

  // Give server a moment to bind
  await new Promise((r) => setTimeout(r, 300));

  try {
    await runDemo();
  } catch (err) {
    console.error("Demo failed:", err.message);
  } finally {
    wss.close();
    process.exit(0);
  }
}

main();
