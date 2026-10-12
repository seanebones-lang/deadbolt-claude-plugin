# DeadBolt for Claude Code

**Give agents tools. Keep control.** A free Apache-2.0 local MCP plugin from
[NextEleven](https://www.nexteleven.dev/deadbolt).

This plugin includes the exact released **MCP bundle 1.1.0**, containing stable
**engine 1.0.3**. Plugin version **1.0.0** is a separate packaging version.
It needs Node.js 20+ on PATH. Use current Claude Code; directory manifest fields
validate without warnings on Claude Code 2.1.281+ (CI pins 2.1.296). macOS Apple Silicon/Intel, Linux x64 with glibc,
and Windows x64 are included. It requires no Rust build, API key or hosted gate.

## Start with read-only setup

Leave `DEADBOLT_OPERATOR_CONFIG` blank. Claude Code discovers:

- `deadbolt_get_integration_guide`: local setup instructions for stdio, Rust,
  HTTP or Claude Desktop.
- `deadbolt_check_bundle`: hashes this host's packaged engine and reports the
  packaging versions, compatibility and scope.

Try these requests in a Claude Code session with the setup plugin enabled:

1. “Verify the local DeadBolt bundle and tell me whether protection is active.”
2. “Get the DeadBolt stdio integration guide and explain what is outside its boundary.”
3. “Show the DeadBolt guide for embedding the Rust crate in an application.”

These requests use read-only setup tools. They do not configure a server or grant
an action. The acceptance suite calls both tools and all four guide routes.

**Setup mode provides no active protection.** It starts no downstream server,
reads no accounts, creates no policy/state and makes no network requests.
`checksum_matches` checks packaged integrity, not independent certification.

## Install from the NextEleven source marketplace

With Claude Code 2.1.275 or later, run inside Claude Code:

```text
/plugin install deadbolt --marketplace seanebones-lang/deadbolt-claude-plugin
```

This adds our source marketplace and installs the plugin. It does not represent
an Anthropic directory endorsement. Review the install prompt before enabling.
For older clients, register the marketplace first and install its entry:

```sh
claude plugin marketplace add seanebones-lang/deadbolt-claude-plugin
claude plugin install deadbolt@nexteleven-deadbolt
```

Leave the optional `operator_config` blank for read-only setup. Current Claude
Code prompts for this value; older clients without plugin configuration should
use the separately documented ordinary MCP editor helper instead.

## Load a reviewed local copy

```sh
git clone https://github.com/seanebones-lang/deadbolt-claude-plugin.git
claude plugin validate --strict ./deadbolt-claude-plugin/.claude-plugin/plugin.json
claude --plugin-dir ./deadbolt-claude-plugin
```

In that Claude Code session, inspect `/mcp` for the `deadbolt` connection.
This loads local code with your user's privileges; review it before enabling.
Directory publication requires Anthropic review. A public repository does not
establish directory acceptance. The directory does not accept standalone MCPB
listings; this plugin declares a local command and carries the verified bundle
files directly, including its native executables for reviewer inspection.

**Surface support:** this package targets Claude Code on the four hosts above.
Ordinary Claude web/mobile/Desktop chat ignores local MCP commands and gains no
protection from this plugin. Local Cowork can load local commands, but its runtime
must have Node.js 20+ and a packaged OS/architecture. Cowork integration is not
validated here; Linux ARM64 and cloud Cowork are not supported by this bundle.
Do not assume a configuration path on the host is accessible inside a session VM.

## Gate one trusted server

1. Create a private operator-owned directory outside the agent's workspace.
2. Copy `bundle/operator-config.example.json` there. Replace every placeholder
   with absolute paths, a fresh run ID, an explicit tool allow-list, destinations,
   irreversible-tool classification and your spend cap. Never commit that file.
3. In Claude Code's plugin configuration, set `operator_config` to the absolute
   private JSON path. The plugin maps this value to `DEADBOLT_OPERATOR_CONFIG`
   for its local launcher. Restart its MCP connection. When configuration is valid,
   setup tools are replaced by the trusted downstream server's tools. Invalid
   supplied configuration refuses startup; it does not fall back to setup.
4. Verify an allowed dummy effect and a denied dummy effect before using accounts.
   Follow the [editor evaluation](https://seanebones-lang.github.io/deadbolt/editor-tutorial.html).
5. Keep policy, approval, pause, clip, resume and kill in the operator's local CLI,
   outside model tools. The signed native CLI is included in `bundle/native/`.

If your Claude Code version does not provide plugin configuration, use the existing
[editor helper](https://seanebones-lang.github.io/deadbolt/editors.html) to install
and configure the verified release as a normal local MCP connection. Do not
modify plugin source to store a private path or a credential. Do not run both
connections against the same run identity.

The stable engine has a 60-second sliding lease. Silence expires it. Use a fresh
operator-assigned identity for a new run, and never reuse a killed identity or
share one across concurrent sessions. Stable classified irreversible tools use
a broad one-shot grant; the **engine 1.1.0-rc.1** exact-action features are not in
this plugin. Choose that engine separately when those features are required.

## The execution boundary

Only routed `tools/call` requests are gated. Downstream startup, other MCP
methods, arbitrary OS/network access and already-running tool bodies are outside
that boundary. The downstream process stays trusted and runs with your user's
privileges. It can access the environment normally available to that process;
connect only reviewed servers. Client consent and DeadBolt approval are separate.
Unprotected Claude tools and other installed MCP servers are not covered.

This is a permission gate, not an OS sandbox or a compliance certification.
Open policy is the engine default; this launcher's configured mode requires an
explicit nonempty tool allow-list. Reported spend depends on trusted caller
reporting. Local evidence is operator-writable.

## Inspect, reproduce and remove

- `BUNDLE-SOURCE.json` pins the archive URL and SHA-256. `bundle/` contains its
  exact members, provenance, engine source references, licenses and dependency
  notices. `server/entry.cjs` adapts Claude's optional configuration value and
  adds display titles to the two setup tools; it does not change engine policy.
- Run `python3 tests/acceptance.py` (use `python` on Windows). It verifies every
  release member and exercises the exported plugin command with disposable
  effects. No real accounts, model calls or messages are used.
- End a `--plugin-dir` session to unload the development copy; remove an installed
  plugin through Claude Code’s plugin manager. Operator state lives in the private paths you selected and is kept.
  To delete that state, make a separate deliberate backup/removal decision.
- [Source and issues](https://github.com/seanebones-lang/deadbolt) ·
  [Trust guide](https://github.com/seanebones-lang/deadbolt/blob/v1.0.3/docs/TRUST.md) ·
  [Captioned walkthrough](https://www.nexteleven.dev/deadbolt#watch)

## Privacy Policy

The plugin itself adds no telemetry, network calls, account connections or model
provider credentials. Read-only setup reads only bundled metadata, documentation
and this host's packaged executable for checksum verification. It creates no
operator state and starts no downstream server.

Configured mode reads the operator-selected private JSON configuration, launches
that trusted local stdio server and passes requests/responses between it and the
Claude client. Tool names, arguments and responses may contain personal data.
The engine keeps leases, operator approvals and audit events in the private
SQLite/event paths you select. These local records are operator-writable and are
not tamper-proof; their retention is under the operator's control. Removing the
plugin does not remove those records. Back up or delete them separately when you
deliberately choose to do so.

DeadBolt does not send data to NextEleven. Claude's model/service data handling
and the downstream server's network activity and retention follow their own
policies. The trusted downstream process inherits its normal local environment
and user privileges; this plugin does not sanitize that environment or sandbox
its network access. Review it before connecting accounts or personal data.
No services are connected by default. Do not commit private configuration,
credentials or local operator records to the plugin repository.

Support and privacy questions: **nextelevenstudios@gmail.com**.
This developer tool is intended for adult operators. No paid hosting is added;
Claude subscriptions and downstream services are separate.

## Validation coverage

`tests/acceptance.py` checks the exported command with real disposable marker
effects and no model/provider calls. Its report distinguishes protocol coverage
from client UI and model-mediated coverage. A local CLI manifest validation does
not replace the directory's additional checks or reviewer decision.
