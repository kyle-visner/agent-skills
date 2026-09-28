// A Vercel AI SDK agent that records ticket changes in AvianSuite and undoes
// its own mistake.
//
//   npm install ai @ai-sdk/anthropic @ai-sdk/mcp
//   ANTHROPIC_API_KEY=... AVIANSUITE_TOKEN=... npx tsx index.ts
import { anthropic } from "@ai-sdk/anthropic";
import { createMCPClient } from "@ai-sdk/mcp";
import { generateText, stepCountIs } from "ai";

const TASK = "Ticket T-1001: the customer confirmed the fix by email, so record its status as resolved. Then notice that T-1001 was the wrong ticket (the email was about T-1002): retract your T-1001 change with a reason, and record T-1002 as resolved instead. Finish by listing the receipt links for your changes.";

const aviansuite = await createMCPClient({
  transport: {
    type: "http",
    url: process.env.AVIANSUITE_MCP_URL ?? "https://mcp.aviansuite.com/mcp",
    headers: { Authorization: `Bearer ${process.env.AVIANSUITE_TOKEN}` },
  },
});

try {
  const { text } = await generateText({
    model: anthropic("claude-opus-5"),
    tools: await aviansuite.tools(),
    stopWhen: stepCountIs(12),
    system:
      "You update help desk tickets. Record every change with record_fact before you make it, " +
      "and fix your own mistakes with retract_fact or undo_changes; never delete.",
    prompt: TASK,
  });
  console.log(text);
} finally {
  await aviansuite.close();
}
