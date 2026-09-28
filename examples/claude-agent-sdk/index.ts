// A Claude Agent SDK agent that records ticket changes in AvianSuite and
// undoes its own mistake.
//
//   npm install @anthropic-ai/claude-agent-sdk
//   ANTHROPIC_API_KEY=... AVIANSUITE_TOKEN=... npx tsx index.ts
import { query } from "@anthropic-ai/claude-agent-sdk";

const TASK = "Ticket T-1001: the customer confirmed the fix by email, so record its status as resolved. Then notice that T-1001 was the wrong ticket (the email was about T-1002): retract your T-1001 change with a reason, and record T-1002 as resolved instead. Finish by listing the receipt links for your changes.";

for await (const message of query({
  prompt: TASK,
  options: {
    systemPrompt:
      "You update help desk tickets. Record every change with record_fact before you make it, " +
      "and fix your own mistakes with retract_fact or undo_changes; never delete.",
    mcpServers: {
      aviansuite: {
        type: "http",
        url: process.env.AVIANSUITE_MCP_URL ?? "https://mcp.aviansuite.com/mcp",
        headers: { Authorization: `Bearer ${process.env.AVIANSUITE_TOKEN}` },
      },
    },
    allowedTools: ["mcp__aviansuite__*"],
  },
})) {
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
  }
}
