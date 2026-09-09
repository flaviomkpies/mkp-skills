#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
finalize_pptx: aplica o TEMA (fontes/cores do tema + layouts nomeados) e EMBUTE
as fontes TTF no .pptx — tudo por cirurgia no zip, sem depender de APIs privadas
do python-pptx. Reusável para qualquer deck do tema Elegant P&B.
"""
import sys, os, shutil, zipfile, re
from lxml import etree

FONTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "fonts"))
A  = "http://schemas.openxmlformats.org/drawingml/2006/main"
P  = "http://schemas.openxmlformats.org/presentationml/2006/main"
R  = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
REL= "http://schemas.openxmlformats.org/package/2006/relationships"
def Q(ns,t): return f"{{{ns}}}{t}"

INK='141414'; G1='4A4A4A'; G2='6E6E6E'; HAIR='DADAD6'; PAPER='FCFCFC'
SERIF_LIGHT='Literata Light'; SERIF='Literata'; SANS='Inter'
LAYOUT_NAMES=['Capa','Conteúdo','Split-foto','Fechamento','Seção']
FACES={
    SERIF_LIGHT:{'regular':'LiterataLight-Regular.ttf','italic':'LiterataLight-Italic.ttf'},
    SERIF:      {'regular':'Literata-Regular.ttf','italic':'Literata-Italic.ttf'},
    SANS:       {'regular':'Inter-Regular.ttf','bold':'Inter-Bold.ttf'},
    'Inter SemiBold':{'regular':'InterSemiBold-Regular.ttf'},
}

def _theme(xml):
    root=etree.fromstring(xml)
    tel=root.find(Q(A,'themeElements'))
    clr=tel.find(Q(A,'clrScheme'))
    def setclr(name,hexs):
        el=clr.find(Q(A,name))
        if el is None: return
        for c in list(el): el.remove(c)
        etree.SubElement(el,Q(A,'srgbClr')).set('val',hexs)
    for n,h in [('dk1',INK),('lt1',PAPER),('dk2',G1),('lt2',HAIR),('accent1',INK),
                ('accent2',G1),('accent3',G2),('accent4',HAIR),('accent5',INK),
                ('accent6',G2),('hlink',INK),('folHlink',G2)]: setclr(n,h)
    fs=tel.find(Q(A,'fontScheme'))
    fs.find(Q(A,'majorFont')).find(Q(A,'latin')).set('typeface',SERIF_LIGHT)
    fs.find(Q(A,'minorFont')).find(Q(A,'latin')).set('typeface',SANS)
    root.set('name','RI Pack — Elegant P&B')
    return etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)

def _layout_name(xml, name):
    root=etree.fromstring(xml)
    csld=root.find(Q(P,'cSld'))
    csld.set('name',name)
    return etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)

def finalize(in_path, out_path):
    zin=zipfile.ZipFile(in_path,'r'); names=zin.namelist()
    ct=etree.fromstring(zin.read('[Content_Types].xml'))
    pres=etree.fromstring(zin.read('ppt/presentation.xml'))
    rels=etree.fromstring(zin.read('ppt/_rels/presentation.xml.rels'))
    # content-type fntdata
    if not any(d.get('Extension')=='fntdata' for d in ct.findall(Q(CT,'Default'))):
        d=etree.SubElement(ct,Q(CT,'Default')); d.set('Extension','fntdata'); d.set('ContentType','application/x-fontdata')
    # embed fonts
    used=[int(r.get('Id')[3:]) for r in rels if r.get('Id','').startswith('rId') and r.get('Id')[3:].isdigit()]
    nid=(max(used)+1) if used else 1
    font_bytes={}; efl=etree.Element(Q(P,'embeddedFontLst')); idx=1
    for typ,styles in FACES.items():
        ef=etree.SubElement(efl,Q(P,'embeddedFont'))
        etree.SubElement(ef,Q(P,'font')).set('typeface',typ)
        for style,fn in styles.items():
            font_bytes[f'ppt/fonts/font{idx}.fntdata']=open(os.path.join(FONTS_DIR,fn),'rb').read()
            rId=f'rId{nid}'
            rel=etree.SubElement(rels,Q(REL,'Relationship'))
            rel.set('Id',rId); rel.set('Type','http://schemas.openxmlformats.org/officeDocument/2006/relationships/font')
            rel.set('Target',f'fonts/font{idx}.fntdata')
            etree.SubElement(ef,Q(P,style)).set(Q(R,'id'),rId)
            nid+=1; idx+=1
    pres.set('embedTrueTypeFonts','1'); pres.set('saveSubsetFonts','0')
    # embeddedFontLst DEVE vir logo após notesSz (schema CT_Presentation).
    # OBS: elementos lxml sem filhos são falsy — usar 'is None', nunca 'or'.
    anchor=pres.find(Q(P,'notesSz'))
    if anchor is None: anchor=pres.find(Q(P,'sldSz'))
    anchor.addnext(efl)
    # layout names (por ordem numérica)
    layout_files=sorted([n for n in names if re.match(r'ppt/slideLayouts/slideLayout\d+\.xml$',n)],
                         key=lambda s:int(re.search(r'(\d+)',s.split('/')[-1]).group(1)))
    lay_map={}
    for i,lf in enumerate(layout_files):
        if i<len(LAYOUT_NAMES):
            lay_map[lf]=_layout_name(zin.read(lf), LAYOUT_NAMES[i])
    theme_files=[n for n in names if re.match(r'ppt/theme/theme\d+\.xml$',n)]
    themed={tf:_theme(zin.read(tf)) for tf in theme_files}

    tmp=out_path+'.tmp'; zout=zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED)
    for n in names:
        if n=='[Content_Types].xml': data=etree.tostring(ct,xml_declaration=True,encoding='UTF-8',standalone=True)
        elif n=='ppt/presentation.xml': data=etree.tostring(pres,xml_declaration=True,encoding='UTF-8',standalone=True)
        elif n=='ppt/_rels/presentation.xml.rels': data=etree.tostring(rels,xml_declaration=True,encoding='UTF-8',standalone=True)
        elif n in themed: data=themed[n]
        elif n in lay_map: data=lay_map[n]
        else: data=zin.read(n)
        zout.writestr(n,data)
    for fp,data in font_bytes.items(): zout.writestr(fp,data)
    zin.close(); zout.close(); shutil.move(tmp,out_path)
    print(f"tema aplicado + {len(font_bytes)} faces embutidas -> {os.path.basename(out_path)}")

if __name__=="__main__":
    src=sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(__file__),"RIPack_deck.pptx")
    dst=sys.argv[2] if len(sys.argv)>2 else os.path.join(os.path.dirname(__file__),"RIPack_final.pptx")
    finalize(src,dst)
