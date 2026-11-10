"""Brand settings shared by overlay_cards.py and endcard.py.

Looks for brand.json in: $AVATAR_BRAND, ./brand.json, then this skill's examples/brand.json. Any key may be omitted.
{
  "accent": [201, 162, 94],       # highlight color (kickers, URL line, step numbers, gold quote lines)
  "text":   [250, 245, 236],      # light text over video
  "shade":  [20, 14, 10],         # color of the bottom gradient / end-card tint
  "font_serif": ["NotoSerif-SemiBold.ttf", "NotoSerif-Bold.ttf"],   # a file name or a list (first found wins)
  "font_sans": "NotoSans-Regular.ttf",
  "font_sans_bold": ["NotoSans-SemiBold.ttf", "NotoSans-Bold.ttf"],
  "fonts_dir": "/usr/share/fonts/truetype/noto/"
}
Fonts: a file name is looked up in fonts_dir, the skill's fonts/ folder and the usual system folders; if none is
found, DejaVu (ships with most Linux) and then Pillow's built-in font are used, so rendering never crashes.
"""
import json, os, glob
from PIL import ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
_DEF = {'accent': [201, 162, 94], 'text': [250, 245, 236], 'shade': [20, 14, 10],
        'font_serif': ['NotoSerif-SemiBold.ttf', 'NotoSerif-Bold.ttf'], 'font_sans': ['NotoSans-Regular.ttf'],
        'font_sans_bold': ['NotoSans-SemiBold.ttf', 'NotoSans-Bold.ttf'], 'fonts_dir': '/usr/share/fonts/truetype/noto/'}

def _load():
    for p in (os.environ.get('AVATAR_BRAND'), 'brand.json', os.path.join(HERE, '..', 'examples', 'brand.json')):
        if p and os.path.exists(p):
            return {**_DEF, **json.load(open(p))}
    return dict(_DEF)

B = _load()
ACCENT, TEXT, SHADE = tuple(B['accent']), tuple(B['text']), tuple(B['shade'])
_SEARCH = [B['fonts_dir'], os.path.join(HERE, '..', 'fonts'), '/usr/share/fonts', '/usr/local/share/fonts',
           os.path.expanduser('~/.fonts'), '/Library/Fonts', '/System/Library/Fonts', 'C:/Windows/Fonts']
_FALLBACK = {'font_serif': 'DejaVuSerif-Bold.ttf', 'font_sans': 'DejaVuSans.ttf', 'font_sans_bold': 'DejaVuSans-Bold.ttf'}
_cache = {}

def _path(name):
    if isinstance(name, (list, tuple)):       # a list = first file found wins
        return next((p for p in map(_path, name) if p), None)
    if os.path.isabs(name) and os.path.exists(name): return name
    for d in _SEARCH:
        if d and os.path.isdir(d):
            hit = glob.glob(os.path.join(d, '**', name), recursive=True)
            if hit: return hit[0]
    return None

def font(kind, size):
    """kind: 'font_serif' | 'font_sans' | 'font_sans_bold'"""
    key = (kind, size)
    if key not in _cache:
        p = _path(B[kind]) or _path(_FALLBACK[kind])
        _cache[key] = ImageFont.truetype(p, size) if p else ImageFont.load_default(size)
    return _cache[key]
