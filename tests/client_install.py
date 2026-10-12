"""Install through the official CLI in disposable storage; never call a model."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CLI_VERSION = '2.1.296'


def verify(public=False):
    with tempfile.TemporaryDirectory(prefix='n11-claude-consumer-') as temporary:
        env = {k: v for k, v in os.environ.items()
               if not k.upper().startswith(('ANTHROPIC_', 'CLAUDE_', 'DEADBOLT_'))}
        env.update(CLAUDE_CONFIG_DIR=temporary,
                   CLAUDE_CODE_PLUGIN_PREFER_HTTPS='1')
        workspace = Path(temporary) / 'workspace'
        workspace.mkdir()
        cli = [shutil.which('npx'), '--yes', '@anthropic-ai/claude-code@' + CLI_VERSION]
        assert cli[0], 'Node/npm required for official CLI validation'

        def run(*args):
            result = subprocess.run(cli + list(args), env=env, text=True,
                                    cwd=workspace, capture_output=True, timeout=120)
            assert result.returncode == 0, result.stderr or result.stdout
            return result.stdout

        source = 'seanebones-lang/deadbolt-claude-plugin' if public else str(ROOT)
        receipt = json.loads(run('plugin', 'install', 'deadbolt', '--marketplace',
                                 source, '--json'))
        assert receipt['outcome'] == 'ok'
        items = json.loads(run('plugin', 'list', '--json'))
        assert len(items) == 1
        item = items[0]
        assert item['id'] == 'deadbolt@nexteleven-deadbolt'
        assert item['version'] == '1.0.0' and item['enabled']
        assert list(item['mcpServers']) == ['deadbolt']
        health = run('mcp', 'list')
        assert 'plugin:deadbolt:deadbolt' in health and 'Connected' in health, health
        assert 'Failed' not in health, health
        folder = Path(item.get('readFromFolder') or item['installPath'])
        if public:
            assert folder.resolve().is_relative_to(Path(temporary).resolve())
            expected = json.loads((ROOT / '.claude-plugin/plugin.json').read_text())
            assert json.loads((folder / '.claude-plugin/plugin.json').read_text()) == expected

        # Exercise the actual client-selected plugin artifact, with its exported
        # MCP command and a disposable downstream. No assistant session starts.
        spec = importlib.util.spec_from_file_location('consumer_acceptance',
                                                     ROOT / 'tests/acceptance.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.ROOT = folder
        effects = module.verify()
        assert effects['passed']
        run('plugin', 'uninstall', item['id'])
        assert json.loads(run('plugin', 'list', '--json')) == []
        return {'passed': True, 'official_cli_version': CLI_VERSION,
                'source': source, 'scope': 'isolated CLI install/list/MCP connection/uninstall and exported-command effects; no model-mediated invocation',
                'client_mcp_connected': True,
                'plugin': item['id'], 'effect_cases': len(effects['checks']),
                'temporary_storage_removed_on_exit': True}


if __name__ == '__main__':
    report = verify('--public' in sys.argv)
    (ROOT / 'client-install-report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
