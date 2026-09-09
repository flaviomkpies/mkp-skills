# EXEMPLO (deck do post da sabatina, 05/09/2026). Copie e troque conteúdo/fotos; a estrutura é o método W2.
# -*- coding: utf-8 -*-
"""Deck "Antes do PowerPoint, peça para a IA te sabatinar" v4 (slide 2 proporcional + slides 3–6 = HTML v6) — método W2 RIPack:
clona slides-modelo do 20260908_Wks2_RIPack_v04.pptx (só leitura), troca texto e foto, apaga o resto.
Arquétipos: capa/fecho full-bleed (s67) · 3 colunas com foto (s2) · lista numerada + foto-metade (s10) · 3 colunas numeradas (s21).
"""
import copy, io, sys
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from PIL import Image

HERE = '/caminho/da/pasta/do/deck'   # exemplo real: vault Efforts/Writing/Newsletter/2026-09-05-sabatina-antes-do-powerpoint/
SRC = f'{HERE}/ref/v04.pptx'   # cópia local (só leitura) do deck-referência: 32_MKP/…/02_W2_Cowork/20260908_Wks2_RIPack_v04.pptx
OUT = f'{HERE}/20260905_sabatina_v4.pptx'
F = f'{HERE}/fotos'
N = 7
E = lambda px: Emu(int(round(px * 6350)))

prs = Presentation(SRC)
S = list(prs.slides)
BLANK = S[0].slide_layout
N_ORIG = len(S)

# ---------- helpers (lib.py do W2, enxuto) ----------
def clone(src):
    new = prs.slides.add_slide(BLANK)
    for sh in list(new.shapes): sh._element.getparent().remove(sh._element)
    for el in src.shapes._spTree:
        if el.tag in (qn('p:nvGrpSpPr'), qn('p:grpSpPr'), qn('p:extLst')): continue
        new.shapes._spTree.append(copy.deepcopy(el))
    for blip in new.shapes._spTree.iter(qn('a:blip')):
        rid = blip.get(qn('r:embed'))
        if rid: blip.set(qn('r:embed'), new.part.relate_to(src.part.rels[rid].target_part, RT.IMAGE))
    for el in list(new.shapes._spTree.iter(qn('a:hlinkClick'))) + list(new.shapes._spTree.iter(qn('a:hlinkHover'))):
        el.getparent().remove(el)
    return new

def named(slide, name):
    r = [sh for sh in slide.shapes if sh.name == name]
    assert r, f'shape {name!r} não achado'
    return r[0]

def by_text(slide, text):
    for sh in slide.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip() == text: return sh
    raise KeyError(text)

def remove(sh): sh._element.getparent().remove(sh._element)

def set_text(sh, text, italic=None):
    """troca o texto preservando o 1º run; \n = novo parágrafo."""
    tf = sh.text_frame; p0 = tf.paragraphs[0]
    runs = p0.runs
    r0 = runs[0] if runs else p0.add_run()
    for r in runs[1:]: r._r.getparent().remove(r._r)
    for p in list(tf.paragraphs)[1:]: p._p.getparent().remove(p._p)
    lines = text.split('\n'); r0.text = lines[0]
    if italic is not None: r0.font.italic = italic
    for ln in lines[1:]:
        newp = copy.deepcopy(p0._p); tf._txBody.append(newp)
        rs = newp.findall(qn('a:r'))
        for r in rs[1:]: newp.remove(r)
        rs[0].find(qn('a:t')).text = ln
    for r in tf._txBody.iter(qn('a:rPr')): r.set('lang', 'pt-BR')
    return sh

def set_pic(slide, pic, path):
    """troca a imagem do shape com crop 'cover' (preenche o quadro sem distorcer)."""
    _, rid = slide.part.get_or_add_image_part(path)
    pic._element.blipFill.blip.set(qn('r:embed'), rid)
    iw, ih = Image.open(path).size
    fw, fh = pic.width, pic.height
    ia, fa = iw / ih, fw / fh
    for a in ('crop_left', 'crop_right', 'crop_top', 'crop_bottom'): setattr(pic, a, 0.0)
    if ia > fa:   # imagem mais larga: corta laterais
        c = (1 - fa / ia) / 2; pic.crop_left = pic.crop_right = c
    else:         # imagem mais alta: corta topo/base
        c = (1 - ia / fa) / 2; pic.crop_top = pic.crop_bottom = c

def dup(slide, sh, dx=0, dy=0):
    el = copy.deepcopy(sh._element); sh._element.addnext(el)
    new = slide.shapes[-1] if False else None
    # localizar o shape novo pelo elemento
    for s2 in slide.shapes:
        if s2._element is el: new = s2; break
    new.left = Emu(new.left + E(dx)); new.top = Emu(new.top + E(dy))
    return new

def overlay(slide, after_pic, alpha=0.5, x=0, y=0, w=1920, h=1080, color='141414'):
    sp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, E(x), E(y), E(w), E(h))
    sp.fill.solid(); sp.fill.fore_color.rgb = RGBColor.from_string(color); sp.line.fill.background()
    clr = sp.fill._xPr.find(qn('a:solidFill')).find(qn('a:srgbClr'))
    a = clr.makeelement(qn('a:alpha'), {'val': str(int(alpha * 100000))}); clr.append(a)
    st = sp._element.find(qn('p:style'))
    if st is not None: sp._element.remove(st)
    spPr = sp._element.spPr
    if spPr.find(qn('a:effectLst')) is None: spPr.append(spPr.makeelement(qn('a:effectLst'), {}))
    sp.text_frame.paragraphs[0].text = ''
    after_pic._element.addnext(sp._element)   # logo acima da foto, abaixo dos textos
    return sp

def add_tb(slide, x, y, w, h, text, font='Inter', size=12.5, color='4A4A4A', bold=False, italic=False, align=None):
    tb = slide.shapes.add_textbox(E(x), E(y), E(w), E(h)); tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, ln in enumerate(text.split('\n')):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        if align: p.alignment = align
        r = p.add_run(); r.text = ln; r.font.name = font; r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
        r.font.color.rgb = RGBColor.from_string(color); r._r.get_or_add_rPr().set('lang', 'pt-BR')
    return tb

def pager(slide, n): set_text(named(slide, 'Pager'), f'‹   {n:02d} / {N:02d}   ›')
def credit(slide, text, white=True):
    add_tb(slide, 1420, 1046, 370, 20, text, size=7, color='E8E2DA' if white else '9A9A94').text_frame.paragraphs[0].alignment = 3  # right

FOOT_L, FOOT_R = 'Flavio Pies', 'setembro 2026'

# ---------- 1 · CAPA (s67: foto full-bleed) ----------
s = clone(S[66])
remove(named(s, 'Picture 1')); remove(named(s, 'Agrupar 8'))
pic = named(s, 'Picture 12'); set_pic(s, pic, f'{F}/capa_commons.jpg'); overlay(s, pic, 0.55)
set_text(named(s, 'TextBox 2'), 'Newsletter · IA na prática')
t = named(s, 'TextBox 3'); set_text(t, 'Antes do PowerPoint, peça para a IA te sabatinar'); t.height = E(300); t.width = E(1500)
add_tb(s, 130, 740, 1400, 50, 'este deck saiu de dez perguntas, respondidas antes do primeiro slide', font='Literata', size=18, color='E8E2DA', italic=True)
set_text(named(s, 'TextBox 6'), FOOT_L); set_text(named(s, 'TextBox 7'), FOOT_R); pager(s, 1)
credit(s, 'foto: Jan Kahánek · CC0')

# ---------- helpers de diagrama ----------
from pptx.enum.text import PP_ALIGN as AL
from pptx.enum.shapes import MSO_CONNECTOR
ACC, PAPERC, MUTEC, RULEC = 'D37455', 'F5F1EC', '6E6E6E', 'DADAD6'

def _nostyle(sp):
    st = sp._element.find(qn('p:style'))
    if st is not None: sp._element.remove(st)
    spPr = sp._element.find(qn('p:spPr'))
    if spPr is not None and spPr.find(qn('a:effectLst')) is None: spPr.append(spPr.makeelement(qn('a:effectLst'), {}))

def box(slide, x, y, w, h, fill, shape=MSO_SHAPE.RECTANGLE):
    sp = slide.shapes.add_shape(shape, E(x), E(y), E(w), E(h))
    sp.fill.solid(); sp.fill.fore_color.rgb = RGBColor.from_string(fill); sp.line.fill.background(); _nostyle(sp)
    sp.text_frame.paragraphs[0].text = ''
    return sp

def oval(slide, cx, cy, r, fill): return box(slide, cx - r, cy - r, 2 * r, 2 * r, fill, MSO_SHAPE.OVAL)

def line(slide, x1, y1, x2, y2, color, w_px=2, dash=None, arrow=False):
    ln = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(x1), E(y1), E(x2), E(y2))
    ln.line.color.rgb = RGBColor.from_string(color); ln.line.width = Pt(w_px * 0.5); _nostyle(ln)
    l = ln.line._get_or_add_ln()
    if dash: l.append(l.makeelement(qn('a:prstDash'), {'val': dash}))
    if arrow: l.append(l.makeelement(qn('a:tailEnd'), {'type': 'triangle', 'w': 'med', 'len': 'med'}))
    return ln

def curve(slide, p0, p1, p2, p3, color, w_px=2, dash=None, n=32):
    """Bézier cúbica como freeform (polilinha editável)."""
    pts = []
    for i in range(n + 1):
        u = i / n; a, b, c, d = (1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u ** 3
        pts.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    fb = slide.shapes.build_freeform(E(pts[0][0]), E(pts[0][1]), scale=1.0)
    fb.add_line_segments([(E(x), E(y)) for x, y in pts[1:]], close=False)
    sp = fb.convert_to_shape(); sp.fill.background(); sp.line.color.rgb = RGBColor.from_string(color); sp.line.width = Pt(w_px * 0.5); _nostyle(sp)
    if dash:
        l = sp.line._get_or_add_ln(); l.append(l.makeelement(qn('a:prstDash'), {'val': dash}))
    return sp

def eyebrow(slide, x, y, w, text, color=MUTEC, align=None):
    tb = add_tb(slide, x, y, w, 26, text.upper(), size=9, color=color, align=align)
    for r in tb.text_frame.paragraphs[0].runs: r._r.get_or_add_rPr().set('spc', '250')
    return tb

def content_base(n, kicker, title, fecho=None):
    """chrome do s21 (fio, kicker, barra, título, pager, fecho) sem as colunas."""
    s = clone(S[20])
    keep = {'Rule 2778', 'Kicker', 'Rule', 'Title', 'Pager', 'Fecho'}
    for sh in list(s.shapes):
        if sh.name not in keep: remove(sh)
    set_text(named(s, 'Kicker'), kicker); set_text(named(s, 'Title'), title)
    if fecho: set_text(named(s, 'Fecho'), fecho)
    else: remove(named(s, 'Fecho'))
    pager(s, n); return s

# ---------- 2 · TESE (proporção: coluna "eu" larga, coluna "IA" estreita) ----------
def add_pic_cover(slide, path, x, y, w, h):
    pic = slide.shapes.add_picture(path, E(x), E(y), E(w), E(h)); set_pic(slide, pic, path); return pic
s = content_base(2, 'TESE · QUEM DECIDE O QUE ENTRA NO MATERIAL', 'Em deck de cliente, eu respondo por quase 100% do conteúdo', 'Tese')
named(s, 'Rule').height = E(130)
wa, gap = 1230, 40; wb = 1660 - wa - gap
add_pic_cover(s, f'{F}/mao.jpg', 130, 340, wa, 390); add_pic_cover(s, f'{F}/circuito.jpg', 130 + wa + gap, 340, wb, 390)
add_tb(s, 130, 760, wa, 70, 'quase 100%', font='Literata Light', size=32, color=ACC)
add_tb(s, 130, 838, wa, 40, 'eu: o conteúdo', font='Literata', size=16, color='141414')
add_tb(s, 130, 884, 900, 70, 'cada afirmação, cada decisão, a responsabilidade inteira. Nada entra sem eu ter lido e concordado.', size=11.5, color='4A4A4A')
x2 = 130 + wa + gap
add_tb(s, x2, 760, wb, 70, 'o resto', font='Literata Light', size=32, color=MUTEC)
add_tb(s, x2, 838, wb, 40, 'a IA: a forma', font='Literata', size=16, color='141414')
add_tb(s, x2, 884, wb, 70, 'formatar, costurar, pesquisar e propor', size=11.5, color='4A4A4A')
credit(s, 'fotos: Wilfred Iven · Lenharth Systems · CC0', white=False)

# ---------- 3 · PROBLEMA (bifurcação: um sintoma, duas leituras) ----------
s = content_base(3, 'PROBLEMA · POR QUE O DECK SAI ERRADO', 'A IA sabe montar PowerPoint, o que falta é o contexto', 'Problema')
curve(s, (560, 590), (700, 590), (700, 370), (840, 370), 'BFBFBA', 2, dash='dash')
curve(s, (560, 590), (700, 590), (700, 790), (840, 790), ACC, 3)
oval(s, 560, 590, 9, '141414'); oval(s, 840, 370, 7, 'BFBFBA'); oval(s, 840, 790, 9, ACC)
eyebrow(s, 130, 500, 400, 'o sintoma')
add_tb(s, 130, 530, 420, 60, 'O deck sai errado', font='Literata Light', size=22, color='141414')
add_tb(s, 130, 596, 400, 90, 'títulos genéricos, slide que ninguém pediu, número inventado', size=12.5, color='4A4A4A')
eyebrow(s, 880, 285, 900, 'a leitura de sempre', color='9A9A94')
t3 = add_tb(s, 880, 315, 900, 70, 'A IA não sabe fazer PowerPoint', font='Literata Light', size=27, color='8A8A86')
t3.text_frame.paragraphs[0].runs[0]._r.get_or_add_rPr().set('strike', 'sngStrike')
add_tb(s, 880, 392, 900, 40, 'a culpa cai na ferramenta e a conversa acaba aí', size=12.5, color='8A8A86')
eyebrow(s, 880, 700, 900, 'o que acontece', color=ACC)
add_tb(s, 880, 730, 900, 70, 'Ninguém deu o contexto inteiro', font='Literata Light', size=27, color='141414')
add_tb(s, 880, 807, 660, 80, 'sem o pedido hiperdetalhado, a IA assume decisões pequenas em série e fabrica conteúdo que não é seu', size=12.5, color='4A4A4A')

# ---------- 4 · SABATINA (foto full-bleed + 4 chevrons) ----------
s = clone(S[66])
remove(named(s, 'Picture 1')); remove(named(s, 'Agrupar 8'))
pic = named(s, 'Picture 12'); set_pic(s, pic, f'{F}/microfone.jpg'); overlay(s, pic, 0.62)
remove(named(s, 'TextBox 6')); remove(named(s, 'TextBox 7'))
k = named(s, 'TextBox 2'); set_text(k, 'SABATINA · SKILL GRILL-ME, DE MATT POCOCK'); k.top = E(118); k.height = E(26)
for r in k.text_frame.paragraphs[0].runs: r.font.name = 'Inter'; r.font.size = Pt(10); r.font.color.rgb = RGBColor.from_string('E8E2DA'); r._r.get_or_add_rPr().set('spc', '250')
t = named(s, 'TextBox 3'); set_text(t, 'A sabatina vai até não sobrar nada assumido'); t.top = E(145); t.height = E(80); t.width = E(1500)
for r in t.text_frame.paragraphs[0].runs: r.font.size = Pt(33)
box(s, 114, 153, 2, 65, PAPERC)
steps = [('01', 'FRONTEIRA', 'só pergunta o que já dá para perguntar; cada resposta abre a próxima'),
         ('02', 'RECOMENDAÇÃO', 'cada pergunta vem numerada, com a resposta que o agente daria'),
         ('03', 'FATO E DECISÃO', 'fato o agente busca em arquivo ou na web; decisão é sua'),
         ('04', 'SPEC', 'termina escrita, e nada se constrói antes do seu ok')]
cw = (1660 - 16 * 3) / 4
for i, (n_, lab, d) in enumerate(steps):
    x = 130 + i * (cw + 16); last = i == 3
    ch = box(s, x, 560, cw, 112, PAPERC if last else ACC, MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON)
    tf = ch.text_frame; tf.margin_left = E(48 if i == 0 else 60); tf.margin_right = E(10); tf.word_wrap = False; tf.vertical_anchor = 1
    p = tf.paragraphs[0]; p.alignment = AL.LEFT
    r = p.add_run(); r.text = n_ + '  '; r.font.name = 'Literata Light'; r.font.size = Pt(20); r.font.color.rgb = RGBColor.from_string('141414' if last else 'FFFFFF'); r._r.get_or_add_rPr().set('lang', 'pt-BR')
    r = p.add_run(); r.text = lab; r.font.name = 'Inter'; r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = RGBColor.from_string('141414' if last else 'FFFFFF'); r._r.get_or_add_rPr().set('lang', 'pt-BR'); r._r.get_or_add_rPr().set('spc', '80')
    add_tb(s, x + 56, 700, cw - 96, 110, d, size=11.5, color=PAPERC)
add_tb(s, 130, 1001, 1400, 40, 'texto da skill: github.com/mattpocock/skills › skills/productivity/grilling (lido em 05/09/2026)', size=11.5, color='E8E2DA')
pager(s, 4); credit(s, 'foto: freestocks.org via Wikimedia Commons · CC0')

# ---------- 5 · EVIDÊNCIA (linha do tempo, 7 pontos) ----------
s = content_base(5, 'EVIDÊNCIA · O QUE O AGENTE TERIA ASSUMIDO SOZINHO', 'Sem as respostas, o agente teria errado 7 de 7 decisões',
                 'em todas as sete eu escolhi outra coisa; a lista completa está no texto')
add_tb(s, 130, 250, 1400, 40, 'o que ele teria decidido por conta própria, decisão a decisão', font='Literata', size=13, color=MUTEC, italic=True)
box(s, 130, 600, 1660, 1, RULEC)
items = [('01', 'Caso âncora', 'workshop de cliente'), ('02', 'Caminho do leitor', 'prompt colável'), ('03', 'Evidência', 'slide inventado'),
         ('04', 'Meta', 'apêndice inteiro'), ('05', 'Tese', '“zero conteúdo da IA”'), ('06', 'Rascunho de julho', 'post irmão'), ('07', 'Ferramenta do deck', 'gerador genérico')]
step = 1660 / 7
for i, (n_, lab, ass) in enumerate(items):
    cx = 130 + (i + 0.5) * step
    add_tb(s, cx - 110, 500, 220, 60, n_, font='Literata Light', size=28, color=ACC, align=AL.CENTER)
    oval(s, cx, 600, 8, ACC)
    add_tb(s, cx - 110, 640, 220, 70, lab, font='Literata', size=13.5, color='141414', align=AL.CENTER)
    add_tb(s, cx - 110, 722, 220, 60, ass, size=10.5, color=MUTEC, italic=True, align=AL.CENTER)

# ---------- 6 · REGRAS (troca agente → eu) ----------
s = content_base(6, 'REGRAS · O QUE FICOU DEPOIS DE ALGUMAS RODADAS', 'Quatro regras que ficaram',
                 'Dois modos de responder: opções na tela, duas por rodada; ou um áudio pelo Wispr Flow, para expandir o contexto além da pergunta')
eyebrow(s, 130, 300, 470, 'o agente', align=AL.RIGHT); eyebrow(s, 1320, 300, 470, 'eu')
box(s, 640, 330, 1, 590, RULEC); box(s, 1280, 330, 1, 590, RULEC)
rows = [('pergunta só o que muda o material', 'pergunta é dúvida, não confirmação', 'respondo a dúvida, não a confirmação'),
        ('propõe a resposta que ele daria', 'recomendação em cada pergunta', 'corrijo, em vez de criar do zero'),
        ('busca o fato em arquivo ou na web', 'fato é da IA, decisão é minha', 'decido só o que exige julgamento'),
        ('escreve a spec', 'termina em spec escrita', 'leio antes de qualquer slide existir')]
for y, (a, rl, e) in zip((400, 550, 700, 850), rows):
    line(s, 652, y, 1262, y, ACC, 2.5, arrow=True); oval(s, 640, y, 7, '141414')
    add_tb(s, 130, y - 22, 470, 44, a, size=12, color='141414', align=AL.RIGHT)
    add_tb(s, 660, y - 44, 590, 36, rl, font='Literata', size=12, color=ACC, italic=True, align=AL.CENTER)
    add_tb(s, 1320, y - 22, 470, 44, e, size=12, color='141414')

# ---------- 7 · FORMA + FECHO (s67) ----------
s = clone(S[66])
remove(named(s, 'Picture 1')); remove(named(s, 'Agrupar 8'))
pic = named(s, 'Picture 12'); set_pic(s, pic, f'{F}/agulha_commons.jpg'); overlay(s, pic, 0.6)
set_text(named(s, 'TextBox 2'), 'Depois da spec, a skill de forma')
t = named(s, 'TextBox 3'); set_text(t, 'A sabatina decide o que vai no slide. A skill decide como o slide fica'); t.height = E(240); t.width = E(1600)
for r in t.text_frame.paragraphs[0].runs: r.font.size = Pt(44)
add_tb(s, 130, 700, 760, 120, 'Texto: skill writing, com o DNA da minha voz, um vocabulário proibido e sugestão da IA sempre marcada, nunca como minha.', font='Inter', size=14, color='F5F1EC')
add_tb(s, 960, 700, 760, 120, 'Deck: skill de slides com a identidade travada, em HTML e em PowerPoint nativo. Nenhuma das duas inventa.', font='Inter', size=14, color='F5F1EC')
add_tb(s, 130, 850, 1500, 40, 'Saldo desta sabatina: 4 rodadas · 10 perguntas · 1 fato buscado pelo agente · 0 decisões de conteúdo dele', font='Literata', size=16, color='E8E2DA', italic=True)
set_text(named(s, 'TextBox 6'), FOOT_L); set_text(named(s, 'TextBox 7'), FOOT_R); pager(s, 7)
credit(s, 'foto: photos-public-domain.com · CC0')

# ---------- apaga os slides originais ----------
lst = prs.slides._sldIdLst
for sldId in list(lst)[:N_ORIG]:
    prs.part.drop_rel(sldId.rId); lst.remove(sldId)
assert len(prs.slides) == N
# sem <p:style>: conector/forma herdada do v04 puxa sombra do tema Office fora do PowerPoint
for sl in prs.slides:
    for el in list(sl.shapes._spTree.iter(qn('p:sp'))) + list(sl.shapes._spTree.iter(qn('p:cxnSp'))):
        st = el.find(qn('p:style'))
        if st is not None: el.remove(st)
        spPr = el.find(qn('p:spPr'))
        if spPr is not None and spPr.find(qn('a:effectLst')) is None: spPr.append(spPr.makeelement(qn('a:effectLst'), {}))
prs.save(OUT); print('ok ->', OUT)
