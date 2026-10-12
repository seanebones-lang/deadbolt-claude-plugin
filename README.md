# DeadBolt for Claude Code

**Give agents tools. Keep control.** A free Apache-2.0 local MCP plugin from
[NextEleven](https://www.nexteleven.dev/deadbolt).

Plugin **2.0.0** includes MCP bundle **2.0.0** and the stable engine **2.0.0**.
Every vendored member is pinned to the separately published bundle. Plugin,
bundle and engine remain separate artifacts even when versions match.
This source update does not establish official marketplace acceptance.

Node.js 20+ on PATH is required. Use current Claude Code; CI validates the official
CLI at 2.1.296. Included native targets: macOS Apple Silicon and Intel,
Linux x64 with glibc, and Windows x64. No Rust build, API key or hosted gate is needed.
No engine is downloaded during plugin installation or startup.

## Read-only setup first

Leave the optional `operator_config` blank. Claude discovers exactly two tools:

- `deadbolt_get_integration_guide`: local instructions for stdio, Rust, HTTP or
  Claude Desktop; does not save configuration or grant permission.
- `deadbolt_check_bundle`: reads this host's packaged engine and provenance,
  calculates SHA-256 and reports compatibility and integrity. Does not execute
  the engine, inspect private operator state or test security.

Try: “Verify the DeadBolt bundle and tell me whether protection is active.” Then:
“Get the stdio integration guide and explain its boundaries.”

Setup creates no operator state, starts no downstream server and makes no network
requests. `active_protection` is **false**. Matching a packaged checksum checks
corruption, not independent certification or directory acceptance.

## Install the source marketplace

In Claude Code 2.1.275 or later:

```text
/plugin install deadbolt --marketplace seanebones-lang/deadbolt-claude-plugin
```

Alternatively:

```sh
claude plugin marketplace add seanebones-lang/deadbolt-claude-plugin
claude plugin install deadbolt@nexteleven-deadbolt
```

Review the local-code trust prompt before enabling. This source marketplace is
not an Anthropic endorsement. Existing installs should use the client's plugin
update controls and verify the reported bundle and engine version afterward.
Operator state is stored separately and must be backed up before upgrading.
Do not use a killed or expired identity as a new run, and do not downgrade a
store expecting newer guarantees to an engine that ignores them.

For a reviewed local candidate:

```sh
git clone https://github.com/seanebones-lang/deadbolt-claude-plugin.git
claude plugin validate --strict ./deadbolt-claude-plugin/.claude-plugin/plugin.json
claude --plugin-dir ./deadbolt-claude-plugin
```

Inspect `/mcp` for `deadbolt`. Its local process runs with your user's privileges.
The directory submission targets **Claude Code only**. This plugin does not add
local commands to ordinary Claude web/mobile/Desktop chat. The separate MCPB can
be installed directly in Claude Desktop. Cowork, Linux ARM64 and cloud runtimes
are unverified or unsupported here. A host path may not exist inside a session VM.

## Configure one trusted downstream server

1. Create a private operator-owned state directory outside agent-editable workspaces.
2. Copy `bundle/operator-config.example.json` to a distinct file for each run,
   such as `run-001.json`. Version 2 requires absolute
   paths, a fresh identity, explicit tools, a future integer Unix-seconds
   `hard_deadline_at`, and an explicit `renewal_mode`. The zero deadline is an
   invalid placeholder. Empty `offline_tools` grants no exceptions.
3. Select `supervisor` when an external trusted supervisor controls liveness.
   Immediately provision and start renewal separately, before the default
   60-second idle TTL expires. The plugin never provisions or receives a renewal
   credential. Follow the [supervision guide](https://github.com/seanebones-lang/deadbolt/blob/main/docs/SUPERVISION.md).
   `activity` is an explicit alternative: live admission renews idle TTL, while
   the fixed deadline never moves. The bundled example selects this alternative
   deliberately; it is not supervisor operation.
4. Set the plugin's `operator_config` to the private absolute JSON path and
   restart its MCP connection. Valid configuration replaces setup tools with
   the downstream tools. Invalid or expired configuration stops before downstream
   startup; it never falls back to unprotected setup or silently revives a run.
5. Verify disposable allowed and denied effects before connecting accounts.
   Keep the packaged native CLI's policy, approvals, pause, clip, resume and kill
   with the operator. Client permission and DeadBolt admission are separate.

Fresh standalone engine setup defaults to supervision; this launcher requires
an explicit mode. A supervisor can renew idle TTL while the run is still live,
but never past its fixed deadline. When idle TTL or deadline expires, create a
fresh operator-issued identity for a genuinely new run. Resume and restart cannot
resurrect an expired or killed identity. Do not delete state to hide a denial.

This launcher uses **legacy one-shot tool approvals** for classified irreversible
calls. It removes inherited `DEADBOLT_*` variables, including action grant-file
references, before launching its proxy. It does not deliver exact-action grants.
For reviewed argument-bound approvals use the engine's documented Rust, Python
or explicitly configured raw-proxy integration. Do not claim that a broad tool
grant approves the exact arguments of a later call.

## Understand the boundary

Only routed MCP `tools/call` admissions are gated. Startup has a separate liveness
check; arbitrary OS access, other MCP methods, other tools/servers and already
running work are outside this gate. The downstream remains trusted and inherits
its normal user environment. Use OS isolation and executor-owned cancellation
when those are required.

With destination policy set, every routed tool must declare an allowed destination
unless the operator explicitly excepted that tool as offline. A declared foreign
destination remains denied even for an offline-excepted tool. These are trusted
policy declarations, **not OS egress enforcement**. Spend caps use trusted reported
usage. Local state and evidence are operator-writable; private-path and malformed
state checks do not prevent valid edits by the same user.

Version 2 returns tool denials as `isError: true` with stable reason/retry metadata.
The model can distinguish `paused`, `killed`, `lease_expired`,
`deadline_exceeded`, `purpose_exceeded` and `store_unavailable` without receiving
operator credentials or private policy. A kill prevents new admissions; it does
not automatically cancel an in-flight tool body.

## Reproduce, troubleshoot and remove

Run `python3 tests/acceptance.py` (`python` on Windows). It downloads the pinned
public archive, checks every vendored member, exercises the exported plugin
command and verifies real disposable marker effects. It uses no model or account.
Run `python3 tests/client_install.py` to install/list/connect/uninstall through
the official Claude CLI in temporary storage and repeat the exported-command
checks against the client-selected copy. Manifest validation alone is not enough.

See [REVIEWER-TEST.md](REVIEWER-TEST.md) for a short reviewer runbook and
[REVIEW-NOTES.md](REVIEW-NOTES.md) for inspectable source/provenance references.
CLI/protocol checks do not establish model-mediated Claude Code acceptance.
The [RC2 model receipt](evidence/claude-code-model-rc2-2026-10-12.json) records
separately checked model calls through the session-loaded plugin on macOS ARM64.
It is NextEleven-operated evidence for the `--plugin-dir` route. Marketplace
installation with a model, other hosts and graphical clients are separate checks.

If startup fails, validate the configuration version, absolute paths, tool lists,
future fixed deadline and live identity with the operator CLI. Diagnostics avoid
printing private paths, arguments and credentials. A missing or unsafe store fails
closed. Changing a deadline or mode of an existing run is refused.

When starting a genuinely new run, use a new private configuration filename,
select its absolute path in `operator_config`, and reconnect the MCP server.
During the Claude Code 2.1.296 model test, reusing a configuration pathname after
a failed connection left the plugin unavailable; a new pathname connected to the
fresh identity. The cause of that client behavior has not been established.
Check `/mcp` and the actual exposed tools before treating the new run as ready.
Retain the old run and its evidence; changing configuration never authorizes
reviving a killed or expired identity.

End a `--plugin-dir` session to unload a local copy, or uninstall with Claude's
plugin manager. Operator state is retained at the paths you selected; back it up
or remove it deliberately as a separate action. Do not commit private config,
credentials or state to this repository.

[Engine source and issues](https://github.com/seanebones-lang/deadbolt) ·
[Installation and migration](https://github.com/seanebones-lang/deadbolt/blob/main/docs/INSTALL.md) ·
[Trust boundaries](https://github.com/seanebones-lang/deadbolt/blob/main/docs/TRUST.md) ·
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
