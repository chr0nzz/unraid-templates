import glob
import os
import xml.etree.ElementTree as ET

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = sorted(glob.glob(os.path.join(ROOT, 'templates', '*.xml')))

VALID_TYPES   = ('Path', 'Port', 'Variable', 'Label', 'Device')
VALID_DISPLAY = ('always', 'always-hide', 'advanced', 'advanced-hide', 'hidden')
VALID_BOOL    = ('true', 'false')
VALID_PATH_MODE = ('rw', 'ro', 'rw,slave', 'rw,shared', 'ro,slave', 'ro,shared')

CLEARTEXT_OK = ('CROWDSEC_CLIENT_KEY', 'OTP_ENCRYPTION_KEY')


def _read(path):
    with open(path, encoding='utf-8') as fh:
        return fh.read()


def test_there_is_a_template_to_publish():
    assert TEMPLATES, 'an empty repository fails the Community Applications scan'


@pytest.mark.parametrize('path', TEMPLATES, ids=os.path.basename)
def test_the_template_says_what_it_is(path):
    root = ET.parse(path).getroot()
    assert root.tag == 'Container' and root.get('version') == '2'
    for tag in ('Name', 'Repository', 'Overview', 'Icon', 'TemplateURL', 'WebUI', 'Category'):
        el = root.find(tag)
        assert el is not None and (el.text or '').strip(), f'{tag} is required by Community Applications'
    assert root.findtext('Support') or root.findtext('Project'), \
        'a template with neither Support nor Project gets removed from Community Applications'


@pytest.mark.parametrize('path', TEMPLATES, ids=os.path.basename)
def test_every_config_is_on_one_line(path):
    for line in _read(path).splitlines():
        stripped = line.strip()
        if stripped.startswith('<Config'):
            assert stripped.endswith('</Config>'), \
                f'wrapped attributes break the Community Applications parser: {stripped[:60]}'


@pytest.mark.parametrize('path', TEMPLATES, ids=os.path.basename)
def test_every_config_uses_values_unraid_understands(path):
    for cfg in ET.parse(path).getroot().findall('Config'):
        name = cfg.get('Name')
        assert name, 'a Config with no Name renders as a blank field'
        assert cfg.get('Target'), f'{name} has nothing to set'
        assert cfg.get('Type') in VALID_TYPES, f'{name} has Type {cfg.get("Type")!r}'
        assert cfg.get('Display') in VALID_DISPLAY, f'{name} has Display {cfg.get("Display")!r}'
        assert cfg.get('Required') in VALID_BOOL, f'{name} has Required {cfg.get("Required")!r}'
        assert cfg.get('Mask') in VALID_BOOL, f'{name} has Mask {cfg.get("Mask")!r}'
        if cfg.get('Type') == 'Path':
            assert cfg.get('Mode') in VALID_PATH_MODE, f'{name} is a path with Mode {cfg.get("Mode")!r}'
        if cfg.get('Type') == 'Port':
            assert cfg.get('Mode') in ('tcp', 'udp'), f'{name} is a port with Mode {cfg.get("Mode")!r}'


@pytest.mark.parametrize('path', TEMPLATES, ids=os.path.basename)
def test_secrets_are_masked(path):
    for cfg in ET.parse(path).getroot().findall('Config'):
        target = (cfg.get('Target') or '').upper()
        if target.endswith(('_PASSWORD', '_SECRET', '_KEY')) and target not in CLEARTEXT_OK:
            assert cfg.get('Mask') == 'true', f'{target} is typed in the clear'


@pytest.mark.parametrize('path', TEMPLATES, ids=os.path.basename)
def test_the_template_url_points_at_this_file(path):
    url = ET.parse(path).getroot().findtext('TemplateURL') or ''
    assert url.endswith('templates/' + os.path.basename(path)), \
        'Community Applications identifies the template by this URL, it has to match where the file lives'
    assert 'chr0nzz/unraid-templates' in url


def test_the_maintainer_profile_is_present():
    profile = os.path.join(ROOT, 'ca_profile.xml')
    assert os.path.exists(profile), 'submission is blocked without ca_profile.xml in the repository root'
    root = ET.parse(profile).getroot()
    assert root.tag == 'Profile'
    assert (root.findtext('Name') or '').strip(), 'an empty Profile blocks submission'


def test_the_licence_is_where_community_applications_looks():
    assert os.path.exists(os.path.join(ROOT, 'LICENSE')), \
        'an OSI licence at the repository root is a submission requirement'


def test_the_icons_are_committed_not_linked_somewhere_else():
    for path in TEMPLATES + [os.path.join(ROOT, 'ca_profile.xml')]:
        icon = ET.parse(path).getroot().findtext('Icon') or ''
        assert icon.startswith('https://raw.githubusercontent.com/chr0nzz/unraid-templates/main/'), \
            f'{os.path.basename(path)} points its icon outside this repository'
        local = os.path.join(ROOT, icon.rsplit('/main/', 1)[1])
        assert os.path.exists(local), f'{icon} is not in the repository'
