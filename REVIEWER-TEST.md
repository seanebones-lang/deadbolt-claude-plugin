# Reproducible reviewer test

No testing account or production data is needed: DeadBolt is a local execution
gate. All automated cases use disposable stdio marker tools and private temporary
state. Node 20+ and Python 3.9+ are required on one packaged native target.

```sh
npx --yes @anthropic-ai/claude-code@2.1.296 plugin validate --strict .claude-plugin/plugin.json
npx --yes @anthropic-ai/claude-code@2.1.296 plugin validate --strict .claude-plugin/marketplace.json
python3 tests/acceptance.py
python3 tests/client_install.py
```

Expected: both validators succeed; both JSON reports have `passed: true`.
The protocol suite confirms every bundled release member matches the pinned
archive, then tests the actual exported command. Allowed calls append markers;
every denied call must leave the marker file unchanged and return an MCP tool
error with its actual reason. Covered cases include one-use grant and replay,
pause/resume/clip, kill/reconnect, idle expiry, fixed deadline, destination checks,
explicit offline exceptions, nonrenewing supervisor mode and running-store outage.
Legacy/invalid configuration and changed bounds stop before the downstream starts.

The client test uses isolated `CLAUDE_CONFIG_DIR`, the official CLI and no assistant
session. It checks install/list/MCP connection, repeats effects against the
client-selected folder, then uninstalls. It does not read ordinary Claude account
credentials or call a model. Temporary storage is removed on exit.

For a manual Claude Code session, load a reviewed copy with
`claude --plugin-dir /absolute/path/to/deadbolt-claude-plugin` and leave the
optional configuration blank. Ask “Verify the DeadBolt bundle and tell me if
protection is active.” Expected: engine/bundle 2.0.0-rc.2, checksum match,
`active_protection: false`. Ask “Get the stdio integration guide.” Expected:
placeholder configuration and explicit boundaries, with no server started.

A model-mediated configured run needs an operator-provisioned disposable server
and live finite configuration as described in README. Do not connect real accounts.
Only such a run can establish the model/client's handling of the configured
marker tools; successful protocol or isolated CLI tests alone cannot close that
acceptance gate. The separate MCPB GUI receipts are not Claude Code plugin evidence.

Report the plugin commit, bundle hash, host, Node/Python and Claude version,
commands and any failed report item. Keep private configuration, bearer tokens
and unrelated account data out of reports. Preserve all licenses and provenance.
