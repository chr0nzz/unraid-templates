import glob
import os
import re
import xml.etree.ElementTree as ET

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.environ.get('TRAEFIK_MANAGER_SRC', os.path.join(ROOT, '.traefik-manager'))

RUNTIME_SUPPLIED = {'HOSTNAME', 'PATH', 'TZ', 'PWD', 'HOME', 'PATH_INFO', 'SCRIPT_NAME', 'REMOTE_ADDR'}
NOT_FOR_UNRAID = {'CROWDSEC_STREAM_FRESH_SECONDS'}
READ_INDIRECTLY = {'DOCKER_HOST', 'PLUGINS_DIR', 'ACCESS_LOG_PATH', 'ACME_JSON_PATH'}
"""DOCKER_HOST is read by the docker library, and PLUGINS_DIR, ACCESS_LOG_PATH and ACME_JSON_PATH
through a table of names, so none shows up as a string literal next to environ.get."""

pytestmark = pytest.mark.skipif(
    not os.path.isdir(APP),
    reason='needs a traefik-manager checkout, set TRAEFIK_MANAGER_SRC or clone it to .traefik-manager',
)


def _read(path):
    with open(path, encoding='utf-8') as fh:
        return fh.read()


def _offered(template):
    root = ET.parse(os.path.join(ROOT, 'templates', template)).getroot()
    return {c.get('Target') for c in root.findall('Config') if c.get('Type') == 'Variable'}


def _host_env():
    found = set()
    for path in [os.path.join(APP, 'app.py')] + glob.glob(os.path.join(APP, 'core', '*.py')):
        src = _read(path)
        found |= set(re.findall(r"environ\.get\(\s*['\"]([A-Z][A-Z0-9_]*)['\"]", src))
        found |= set(re.findall(r"environ\[\s*['\"]([A-Z][A-Z0-9_]*)['\"]", src))
        found |= set(re.findall(r"_env_bool\(\s*['\"]([A-Z][A-Z0-9_]*)['\"]", src))
        found |= set(re.findall(r"_cs_int_env\(\s*['\"]([A-Z][A-Z0-9_]*)['\"]", src))
        found |= set(re.findall(r"failure_limit\(\s*['\"]([A-Z][A-Z0-9_]*)['\"]", src))
    return found - RUNTIME_SUPPLIED - NOT_FOR_UNRAID


def _agent_env():
    found = set()
    for path in glob.glob(os.path.join(APP, 'agent', '*.go')):
        if path.endswith('_test.go'):
            continue
        found |= set(re.findall(r'(?:envOr|envInt|envIntRange|envBool|os\.Getenv)\(\s*"([A-Z][A-Z0-9_]*)"', _read(path)))
    return found - RUNTIME_SUPPLIED - NOT_FOR_UNRAID


def test_the_manager_template_offers_every_setting_the_app_reads():
    missing = sorted(_host_env() - _offered('traefik-manager.xml'))
    assert not missing, f'Unraid users cannot set these without editing the container: {missing}'


def test_the_agent_template_offers_every_setting_the_agent_reads():
    missing = sorted(_agent_env() - _offered('traefik-manager-agent.xml'))
    assert not missing, f'Unraid users cannot set these without editing the container: {missing}'


@pytest.mark.parametrize('template,reader', [
    ('traefik-manager.xml', _host_env),
    ('traefik-manager-agent.xml', _agent_env),
])
def test_the_templates_do_not_offer_settings_that_do_nothing(template, reader):
    extra = sorted(_offered(template) - reader() - READ_INDIRECTLY)
    assert not extra, f'{template} offers settings the code never reads: {extra}'
