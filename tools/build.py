"""Buduje stronę z src/app.html: tworzy index.html, sw.js i version.json (z nową wersją).

Uruchom po każdej zmianie aplikacji:  python3 tools/build.py
Przed zbudowaniem dopisz linijkę na początku listy CHANGES w src/app.html.
"""
import hashlib, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)

src = open(P('src', 'app.html'), encoding='utf8').read()

# numer wersji i lista zmian z CHANGES w src/app.html
m = re.search(r"const CHANGES=\[(.*?)\n\];", src, re.S)
changes = re.findall(r"\['(\d{4}-\d{2}-\d{2})','((?:[^'\\]|\\.)*)'\]", m.group(1))
assert changes, 'brak wpisów w CHANGES'
ver, date, notes = '1.%d' % (len(changes) - 1), changes[0][0], changes[0][1]

# kod wersji = skrót źródła i pozostałych plików strony
OTHER = ['manifest.webmanifest', 'icon-192.png', 'icon-512.png', 'apple-touch-icon.png']
h = hashlib.sha256(src.encode('utf8'))
for a in OTHER:
    h.update(open(P(a), 'rb').read())
version = h.hexdigest()[:12]
MARK = "const BUILD='__BUILD__';"
assert src.count(MARK) == 1, 'brak znacznika BUILD w src/app.html'
src = src.replace(MARK, "const BUILD='%s';" % version)
i = src.index('<div class="app">')
head, body = src[:i], src[i:]
pre = ('<!doctype html>\n<html lang="pl">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
       '<meta name="theme-color" content="#C4E6FF">\n'
       '<meta name="apple-mobile-web-app-capable" content="yes">\n'
       '<meta name="mobile-web-app-capable" content="yes">\n'
       '<link rel="manifest" href="manifest.webmanifest">\n'
       '<link rel="icon" type="image/png" href="icon-192.png">\n'
       '<link rel="apple-touch-icon" href="apple-touch-icon.png">\n'
       '<meta name="apple-mobile-web-app-title" content="Wczoraj, dziś, jutro">\n'
       '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
       'body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>\n')
open(P('index.html'), 'w', encoding='utf8').write(pre + head + '</head>\n<body>\n' + body + '\n</body>\n</html>\n')

ASSETS = ['index.html'] + OTHER

SW = r"""// Generowane przez tools/build.py – nie edytuj ręcznie.
const VERSION = '__VERSION__';
const CACHE = 'wdj-app-' + VERSION, FONTS = 'wdj-fonts';
const ASSETS = ['./', __ASSETS__];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS.map(u => new Request(u, {cache: 'reload'})))));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE && k !== FONTS).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('message', e => { if (e.data === 'skip') self.skipWaiting(); });
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin === self.location.origin) {
    if (url.pathname.endsWith('/version.json')) return;
    if (req.mode === 'navigate') { e.respondWith(caches.match('index.html').then(r => r || fetch(req))); return; }
    e.respondWith(caches.match(req, {ignoreSearch: true}).then(r => r || fetch(req)));
    return;
  }
  if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    e.respondWith(caches.open(FONTS).then(c => c.match(req).then(hit => {
      const net = fetch(req).then(res => { if (res && (res.ok || res.type === 'opaque')) c.put(req, res.clone()); return res; }).catch(() => hit);
      return hit || net;
    })));
  }
});
"""
sw = SW.replace('__VERSION__', version).replace('__ASSETS__', ', '.join("'%s'" % a for a in ASSETS))
open(P('sw.js'), 'w', encoding='utf8').write(sw)
json.dump({'ver': ver, 'date': date, 'build': version, 'notes': notes}, open(P('version.json'), 'w', encoding='utf8'), ensure_ascii=False)
print('index.html, sw.js i version.json gotowe: wersja %s z %s, kod %s' % (ver, date, version))
