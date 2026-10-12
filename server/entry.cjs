'use strict';

// Claude owns user_config expansion. An unset optional variable sometimes remains
// literal; that exact reserved placeholder is still setup mode. Any supplied
// path goes through the unchanged released launcher's strict validation.
const path = require('node:path');
if (process.argv.length !== 2) {
  process.stderr.write('deadbolt-plugin:unexpected_arguments\n');
  process.exitCode = 1;
} else {
  const value = process.env.DEADBOLT_OPERATOR_CONFIG || '';
  const config = value === '${user_config.operator_config}' ? '' : value;
  // Directory-facing display metadata only. Released files and permission
  // enforcement stay unchanged; the setup server uses this same object array.
  const setup = require('../bundle/server/setup.cjs');
  const titles = {
    deadbolt_get_integration_guide: 'DeadBolt integration guide',
    deadbolt_check_bundle: 'Verify the local DeadBolt bundle',
  };
  for (const tool of setup.definitions) {
    tool.title = titles[tool.name];
    tool.annotations = { ...tool.annotations, title: tool.title };
  }
  const entry = path.resolve(__dirname, '../bundle/server/launcher.cjs');
  process.argv = [process.argv[0], entry, config];
  require(entry);
}
