# Directory reviewer notes

Candidate plugin 2.0.0-rc.2 carries the exact published MCPB 2.0.0-rc.2 members.
`BUNDLE-SOURCE.json` pins the public archive and SHA-256. Every member is compared
byte-for-byte in `tests/acceptance.py`. Native executable/source references,
build revisions, signatures, licenses and notices are in the bundled provenance.
No engine binary is downloaded during plugin installation or startup.

The directory may require human review of compiled executables and bundled legal
notices. We preserve exact release/legal bytes rather than changing them to suppress
a scan warning. This submission does not assert that its native code passed an
opaque-code scanner. Local tests, directory validation and reviewer acceptance
are separate facts.

The small readable adapter `server/entry.cjs` resolves the optional configuration
placeholder and adds display titles to two read-only setup tools. The bundled
`server/launcher.cjs` verifies the selected binary, validates operator configuration,
checks fixed-bound liveness and launches a trusted downstream through the gate.
Neither adapter nor setup tool calls a remote service. Downstream code may use its
normal inherited environment and privileges; it remains trusted and is disclosed
in the public privacy policy. Operator controls are not model-callable tools.

Manual/CI acceptance downloads the public bundle to verify its pinned bytes. This
is a test operation, not an install hook. Its fixture uses only temporary marker
files and private operator state, with no real accounts or model calls. The
isolated official CLI test removes its temporary install/configuration on exit.
`REVIEWER-TEST.md` gives the reproduction steps and expected results.

This is a prerelease evaluation candidate. Independent artifact-pinned developer
retesting and model-mediated Claude Code acceptance remain distinct from these
protocol tests. The directory listing targets only Claude Code; neither Cowork
nor ordinary Claude web/mobile/Desktop chat is claimed through this plugin.
