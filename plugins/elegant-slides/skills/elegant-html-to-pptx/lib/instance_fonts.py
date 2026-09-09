import sys
from fontTools import ttLib
from fontTools.varLib.instancer import instantiateVariableFont

W="/tmp/claude-1000/-root/f1aac43a-9b96-4478-a0e1-37ec5dbaaed2/scratchpad/ripack/pptx/fonts"

def set_names(font, family, subfamily):
    name=font["name"]
    full=f"{family} {subfamily}".replace(" Regular","").strip() or family
    ps=(family+"-"+subfamily).replace(" ","")
    for nid,val in [(1,family),(2,subfamily),(4,full),(6,ps),(16,family),(17,subfamily)]:
        name.setName(val,nid,3,1,0x409)
        name.setName(val,nid,1,0,0)

def make(src, axes, family, subfamily, out, italic=False, bold=False):
    f=ttLib.TTFont(src)
    instantiateVariableFont(f, axes, inplace=True)
    set_names(f, family, subfamily)
    # fsSelection / macStyle / head
    sel=f["OS/2"].fsSelection
    sel &= ~0b1100001  # clear italic(0), bold(5), regular(6)
    mac=0
    if italic: sel|=0x001; mac|=0x02
    if bold:   sel|=0x020; mac|=0x01
    if not italic and not bold: sel|=0x040
    f["OS/2"].fsSelection=sel
    f["head"].macStyle=mac
    f.save(out); print("saved", out.split('/')[-1], family, subfamily)

# Literata Light (300) roman + italic  → family "Literata Light"
make(f"{W}/Literata-var.ttf", {"wght":300,"opsz":36}, "Literata Light","Regular", f"{W}/LiterataLight-Regular.ttf")
make(f"{W}/Literata-Italic-var.ttf", {"wght":300,"opsz":18}, "Literata Light","Italic", f"{W}/LiterataLight-Italic.ttf", italic=True)
# Literata Regular (400) → family "Literata"
make(f"{W}/Literata-var.ttf", {"wght":400,"opsz":18}, "Literata","Regular", f"{W}/Literata-Regular.ttf")
make(f"{W}/Literata-Italic-var.ttf", {"wght":400,"opsz":18}, "Literata","Italic", f"{W}/Literata-Italic.ttf", italic=True)
# Inter Regular + Bold → family "Inter"
make(f"{W}/Inter-var.ttf", {"wght":400,"opsz":14}, "Inter","Regular", f"{W}/Inter-Regular.ttf")
make(f"{W}/Inter-var.ttf", {"wght":700,"opsz":14}, "Inter","Bold", f"{W}/Inter-Bold.ttf", bold=True)
make(f"{W}/Inter-var.ttf", {"wght":600,"opsz":14}, "Inter SemiBold","Regular", f"{W}/InterSemiBold-Regular.ttf")
