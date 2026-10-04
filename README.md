# AvianSuite agent skills

Safe write access for AI agents. These files teach coding agents (Claude Code,
Cursor, Codex and others) to give the agents they build a safe place to write
business data: [AvianSuite](https://aviansuite.com), where every change is
kept, attributed to the agent that made it, and can be undone.

| What | Where |
|---|---|
| Claude skill | [`skills/safe-business-writes/SKILL.md`](skills/safe-business-writes/SKILL.md) |
| Claude Code plugin (skill + MCP server) | this repo: `.claude-plugin/` and `.mcp.json` |
| Cursor rule | [`cursor/rules/safe-business-writes.mdc`](cursor/rules/safe-business-writes.mdc) |
| AGENTS.md snippet (Codex and others) | [`AGENTS.md`](AGENTS.md) |
| Examples | [`examples/`](examples) |

## Install

Claude Code:

```sh
claude plugin marketplace add kyle-visner/agent-skills
claude plugin install aviansuite@aviansuite
```

Cursor: copy `cursor/rules/safe-business-writes.mdc` into your project's
`.cursor/rules/`. Codex and other agents: paste `AGENTS.md` into yours.

## Examples

Each example is a small ticket agent that records a change, notices it picked
the wrong ticket, and undoes its own mistake ([task](examples/task.txt)):

- [OpenAI Agents SDK](examples/openai-agents/main.py)
- [LangGraph](examples/langgraph/main.py)
- [Vercel AI SDK](examples/vercel-ai-sdk/index.ts)
- [Claude Agent SDK](examples/claude-agent-sdk/index.ts)
- [n8n](examples/n8n/README.md)

Set `AVIANSUITE_TOKEN` to an agent token from
https://app.aviansuite.com/account/agents. No account? Register with
[auth.md](https://aviansuite.com/auth.md): the person types a code and gets a
free sandbox.
Self-hosting is free: see [Stellar Jay](https://github.com/kyle-visner/stellarjay).

## Scope

AvianSuite is for business facts that agents write. It is not a replacement
for every database, analytics warehouse or vector store.
