# Directory reviewer notes

This plugin intentionally includes the exact published MCPB 1.1.0 members,
including four native executables and their legal/provenance records. Each
executable is under 5 MiB. Executables require human review under the directory
checklist. Their source, build evidence and SHA-256 values are in the bundle's
provenance. No binary is downloaded during plugin startup or installation.

The initial directory lint reported credential findings in the bundled engine
installation/integration documentation. These are illustrative operator CLI
commands, not commands run by this plugin. `DEADBOLT_TOKEN` in that guide is
used for the operator's loopback HTTP sidecar; it is not sent to GitHub. `PWD`
is the shell's current directory, not a credential. Documentation links to
GitHub and the root README's description of downstream HTTP integrations do
not transmit either value. Review the actual `server/entry.cjs` and released
`bundle/server/launcher.cjs`: this plugin's own stdio launcher makes no network
requests. A trusted downstream server can use its inherited environment; this
boundary is disclosed in the README Privacy Policy, and reviewers should
consider any configured downstream independently.

The download-and-run lint in `tests/acceptance.py` refers to a manual/CI test,
not an install or startup hook. That test downloads the public release archive,
verifies its pinned SHA-256 and compares every archive member to the vendored
files. It executes only the local packaged command and disposable marker tools,
uses no real accounts or model calls, and deletes the temporary fixture.

We preserve the release files byte for byte instead of editing the legal,
provenance or documentation snapshots to suppress a lint. These notes do not
assert certification or override a review requirement. Directory validation,
security review and publication remain separate from local acceptance.
