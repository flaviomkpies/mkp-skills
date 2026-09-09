"""
pptxlib — helper mínimo para reconstruir decks do tema Elegant/reMarkable (P&B)
em PowerPoint NATIVO e editável. Coordenadas em "stage px" (palco 1920x1080),
convertidas para EMU (6350 EMU/px) e pontos (0.5 pt/px).

Reusável: um builder de deck importa daqui; o tema (master paper + fontes
Literata/Inter + layouts nomeados) é montado por build_theme().
"""
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
import copy

# ---- escala palco 1920x1080 -> 16:9 (13.333x7.5in) ----
EMU_PX = 6350          # 12192000/1920 == 6858000/1080
PT_PX  = 0.5           # 960pt / 1920px
def E(px):  return Emu(int(round(px*EMU_PX)))
def P(px):  return Pt(px*PT_PX)

# ---- paleta do tema ----
INK='141414'; G1='4A4A4A'; G2='6E6E6E'; HAIR='DADAD6'; HAIRS='BFBFBA'; PAPER='FCFCFC'
def C(hexs): return RGBColor.from_string(hexs)

# ---- fontes ----
SERIF_LIGHT='Literata Light'   # títulos / números / itálico
SERIF='Literata'               # corpo serif
SANS='Inter'                   # eyebrow / labels / meta / footer
SANS_SB='Inter SemiBold'

STAGE_W=1920; STAGE_H=1080

def new_prs():
    prs=Presentation()
    prs.slide_width=Emu(12192000); prs.slide_height=Emu(6858000)
    return prs

def _set_bg(obj, hexs):
    """define fundo sólido (slide, layout ou master)."""
    # obj tem .background
    bg=obj.background
    bg.fill.solid(); bg.fill.fore_color.rgb=C(hexs)

def blank_layout(prs):
    # layout 6 do template default é "Blank"
    for l in prs.slide_layouts:
        if l.name.lower() in ('blank','em branco'): return l
    return prs.slide_layouts[6]

def add_slide(prs, layout=None):
    s=prs.slides.add_slide(layout or blank_layout(prs))
    _set_bg(s, PAPER)
    # remove placeholders herdados
    for ph in list(s.placeholders):
        ph._element.getparent().remove(ph._element)
    return s

def _apply_run(r, text, font=SANS, size_px=22, color=INK, bold=False, italic=False,
               spacing_em=None, upper=False):
    r.text = text.upper() if upper else text
    r.font.name=font; r.font.size=P(size_px)
    r.font.bold=bold; r.font.italic=italic
    r.font.color.rgb=C(color)
    # força a fonte em latin/ea/cs
    rPr=r._r.get_or_add_rPr()
    # idioma pt-BR na RUN (senão o PowerPoint marca tudo como erro ortográfico em inglês)
    rPr.set('lang','pt-BR')
    for tag in ('latin','ea','cs'):
        e=rPr.find(qn('a:'+tag))
        if e is None:
            e=rPr.makeelement(qn('a:'+tag),{}); rPr.append(e)
        e.set('typeface',font)
    if spacing_em is not None:
        rPr.set('spc', str(int(spacing_em*size_px*PT_PX*100)))  # spc em 1/100 pt

def add_text(slide, x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
             line_px=None, wrap=True, para_gap_px=0):
    """runs: lista de parágrafos; cada parágrafo é lista de dicts de run.
       Um dict de run: {t, font, size, color, bold, italic, spacing, upper}."""
    tb=slide.shapes.add_textbox(E(x),E(y),E(w),E(h)); tf=tb.text_frame
    tf.word_wrap=wrap
    tf.vertical_anchor=anchor
    for m in ('margin_left','margin_right','margin_top','margin_bottom'):
        setattr(tf,m,0)
    first=True
    for para in runs:
        p=tf.paragraphs[0] if first else tf.add_paragraph()
        first=False
        p.alignment=align
        if line_px:
            p.line_spacing=P(line_px)
        if para_gap_px:
            p.space_after=P(para_gap_px)
        for rd in para:
            r=p.add_run()
            _apply_run(r, rd.get('t',''), rd.get('font',SANS), rd.get('size',22),
                       rd.get('color',INK), rd.get('bold',False), rd.get('italic',False),
                       rd.get('spacing'), rd.get('upper',False))
    return tb

def run(t, **kw):
    d={'t':t}; d.update(kw); return d

def add_line(slide, x1, y1, x2, y2, color=HAIR, weight_px=1, dash=None):
    ln=slide.shapes.add_connector(2, E(x1),E(y1),E(x2),E(y2))  # 2 = straight
    ln.line.color.rgb=C(color); ln.line.width=E(weight_px)
    if dash:
        d=ln.line._get_or_add_ln(); pd=d.makeelement(qn('a:prstDash'),{'val':dash}); d.append(pd)
    ln.shadow.inherit=False
    return ln

def add_rect(slide, x, y, w, h, fill=None, line=None, line_px=1):
    sp=slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, E(x),E(y),E(w),E(h))
    sp.shadow.inherit=False
    if fill is None: sp.fill.background()
    else: sp.fill.solid(); sp.fill.fore_color.rgb=C(fill)
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb=C(line); sp.line.width=E(line_px)
    sp.text_frame.paragraphs[0].text=''
    return sp

def add_img(slide, path, x, y, w, h):
    return slide.shapes.add_picture(path, E(x),E(y),E(w),E(h))
