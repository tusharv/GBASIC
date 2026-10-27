"""Static-site checks: links, assets and truthful installation/content boundaries."""
from html.parser import HTMLParser
from pathlib import Path
import struct
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids=set()
        self.links=[]
        self.images=[]
        self.tabs=[]
        self.feed(source)

    def handle_starttag(self, tag, attributes):
        attrs=dict(attributes)
        if attrs.get('id'):
            assert attrs['id'] not in self.ids, f'Duplicate id: {attrs["id"]}'
            self.ids.add(attrs['id'])
        for name in ('href','src'):
            if attrs.get(name):
                self.links.append(attrs[name])
        if tag=='img':
            self.images.append(attrs)
        if attrs.get('role')=='tab':
            self.tabs.append(attrs)


def test_site_local_assets_and_fragment_links():
    page=Page((SITE/'index.html').read_text())
    for link in page.links:
        url=urlsplit(link)
        if url.scheme or url.netloc:
            assert url.scheme in ('https','http','mailto')
            continue
        if url.path:
            assert not url.path.startswith('/'), 'Project Pages needs relative asset paths'
            target=(SITE/unquote(url.path)).resolve()
            assert target.is_relative_to(SITE)
            assert target.exists(), link
        elif url.fragment:
            assert url.fragment in page.ids, link
    assert len(page.images)>=4
    assert all('alt' in img and img.get('width') and img.get('height') for img in page.images)
    for tab in page.tabs:
        assert tab.get('aria-controls') in page.ids
        assert tab.get('id')


def test_readme_and_site_include_real_splash_and_editor_captures():
    readme=(ROOT/'README.md').read_text()
    for name in ('editor','splash','examples','help'):
        image=SITE/'assets'/'screenshots'/f'{name}.png'
        data=image.read_bytes()
        assert data.startswith(b'\x89PNG\r\n\x1a\n')
        width,height=struct.unpack('>II',data[16:24])
        assert width>=1200 and height>=700
        assert f'site/assets/screenshots/{name}.png' in readme
        assert f'assets/screenshots/{name}.png' in (SITE/'index.html').read_text()


def test_site_installation_and_compatibility_are_honest():
    html=(SITE/'index.html').read_text()
    assert 'Python 3.12' in html
    assert 'git clone https://github.com/tusharv/GBASIC.git' in html
    assert 'pip install -e .' in html
    assert '42' in html and '175' in html
    assert 'not yet' in html.lower() and 'QBasic' in html
    assert 'pip install ghost-basic' not in html
    assert 'api_key' not in html.lower()
    assert 'prefers-reduced-motion' in (SITE/'styles.css').read_text()


def test_pages_workflow_publishes_only_static_site():
    text=(ROOT/'.github/workflows/pages.yml').read_text()
    assert 'path: site' in text
    assert 'pages: write' in text and 'id-token: write' in text
    assert 'actions/deploy-pages@' in text
    assert (SITE/'.nojekyll').exists()
