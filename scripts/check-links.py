"""Check generated URLs, markup metadata and local resources without fetching live sites."""
import pathlib,json,urllib.parse,xml.etree.ElementTree as ET
from html.parser import HTMLParser
R=pathlib.Path(__file__).resolve().parents[1]
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.jsons=[];self.ld=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  for key in ('href','src'):
   if a.get(key):self.links.append(a[key])
  self.ld=tag=='script' and a.get('type')=='application/ld+json'
 def handle_data(self,data):
  if self.ld:self.jsons.append(json.loads(data))
 def handle_endtag(self,tag):
  if tag=='script':self.ld=False
checked=0
for f in [R/'index.html',*sorted((R/'elden').rglob('*.html'))]:
 p=Links();p.feed(f.read_text())
 for href in p.links:
  u=urllib.parse.urlparse(href)
  if u.scheme or u.netloc or not u.path:continue
  target=R/u.path.removeprefix('/GNX/') if u.path.startswith('/GNX/') else f.parent/urllib.parse.unquote(u.path)
  if target.is_dir():target=target/'index.html'
  assert target.exists(),(f,href)
  checked+=1
for el in ET.parse(R/'sitemap.xml').getroot():
 url=el[0].text;assert url.startswith('https://popochan0547-creator.github.io/GNX/');p=urllib.parse.urlparse(url).path.removeprefix('/GNX/');assert (R/p/'index.html').exists()
print('Local links/resources:',checked,'OK; structured JSON-LD OK; sitemap URLs resolve.')
