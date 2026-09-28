# n8n: a ticket agent that can undo its own mistakes

1. Add an **AI Agent** node with your chat model.
2. Add an **MCP Client Tool** node as the agent's tool:
   - Endpoint: `https://mcp.aviansuite.com/mcp` (transport: HTTP Streamable)
   - Authentication: Bearer, with an agent token from
     https://app.aviansuite.com/account/agents in an n8n credential.
   - Tools to include: all.
3. In the agent's system message:
   > You update help desk tickets. Record every change with record_fact before
   > you make it, and fix your own mistakes with retract_fact or
   > undo_changes; never delete.
4. Trigger it with this task:
   > Ticket T-1001: the customer confirmed the fix by email, so record its status as resolved. Then notice that T-1001 was the wrong ticket (the email was about T-1002): retract your T-1001 change with a reason, and record T-1002 as resolved instead. Finish by listing the receipt links for your changes.

Every write the workflow makes is attributed to its token. To reverse a bad
run, ask the agent (or any MCP client with a token for the same workspace) to
call `undo_changes` with the workflow's actor and the run's time window.
