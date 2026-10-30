"""Ghep cac file PNG trong ../sprites thanh ../index.html (mot file chay doc lap).

Dung khi ban da ve sprite rieng: thay file PNG trong thu muc sprites/ (giu ten file),
roi chay:   python3 tools/pack.py

Moi PNG la mot hang ngang cac frame cung kich thuoc, nen trong suot.
Neu ban doi kich thuoc frame, sua bang FRAMES ben duoi (rong, cao).
sunLb.png / sunSb.png (hoa sang len khi nhan vat di ngang) se duoc tu tao tu
sunL.png / sunS.png neu ban khong cung cap file rieng.
"""
import base64, io, json, os
from PIL import Image, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
SPR = os.path.join(HERE, '..', 'sprites')

# ten: (rong 1 frame, cao 1 frame)
FRAMES = {
    'hero':  (13, 22),   # 8 frame: 4 doi mu (dung, buoc trai, buoc phai, chop mat) roi 4 khong mu, cung thu tu
    'cap':   (15, 9),    # 4 frame: mu tot nghiep xoay khi tung len
    'sunL':  (13, 18),   # 3 frame: nghieng trai, thang, nghieng phai
    'sunS':  (11, 12),   # 3 frame, hoa nho hang sau
    'sun':   (13, 13),   # 1 frame (mat troi)
    'cloud': (20, 6),    # 1 frame
}

def brighten(im):
    rgb, a = im.convert('RGB'), im.getchannel('A')
    rgb = ImageEnhance.Brightness(ImageEnhance.Color(rgb).enhance(1.25)).enhance(1.4)
    out = rgb.convert('RGBA'); out.putalpha(a); return out

def load(name):
    p = os.path.join(SPR, name + '.png')
    return Image.open(p).convert('RGBA') if os.path.exists(p) else None

sheets = {}
for name, (fw, fh) in FRAMES.items():
    im = load(name)
    if im is None: raise SystemExit('Thieu file sprites/%s.png' % name)
    if im.height != fh or im.width % fw: raise SystemExit('%s.png phai cao %d va rong chia het cho %d (hien la %dx%d)' % (name, fh, fw, im.width, im.height))
    sheets[name] = (im, fw, fh)
for big, base in (('sunLb', 'sunL'), ('sunSb', 'sunS')):
    im = load(big) or brighten(sheets[base][0])
    sheets[big] = (im, sheets[base][1], sheets[base][2])

out = {}
for name, (im, fw, fh) in sheets.items():
    buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True)
    out[name] = {'src': 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode(), 'w': fw, 'h': fh, 'n': im.width // fw}

tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
open(os.path.join(HERE, '..', 'index.html'), 'w', encoding='utf-8').write(tpl.replace('__SPRITES__', json.dumps(out)))
print('Da tao index.html:', {k: v['n'] for k, v in out.items()})
