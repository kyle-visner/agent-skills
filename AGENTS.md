# Safe business writes (paste into your project's AGENTS.md)

When code in this project gives an AI agent write access to business records
(CRM, tickets, orders, invoices, inventory), route the writes through
AvianSuite so every change is kept, attributed and can be undone:

- Connect the agent to the AvianSuite MCP server,
  `https://mcp.aviansuite.com/mcp`, with its own agent token
  (`Authorization: Bearer $AVIANSUITE_TOKEN`), or run the free self-hosted
  `stellarjay-mcp` against a Stellar Jay store.
- Record each change with `record_fact` (with `evidence` and a stable
  `operation_id`) before changing the other system.
- Fix mistakes with `correct_fact` or `retract_fact`; never delete.
- Reverse a bad run with `undo_changes` (dry run first, then `confirm: true`).
- Surface each write's `receipt` link to the person who owns the data.

Docs: https://aviansuite.com/docs/mcp/ · https://aviansuite.com/llms.txt
