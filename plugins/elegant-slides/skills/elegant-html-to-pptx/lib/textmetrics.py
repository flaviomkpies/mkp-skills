# -*- coding: utf-8 -*-
"""Medição real de texto pelas métricas da fonte — o antídoto do `n * len(texto)`.

Todo defeito de colisão de caixa que a casa produziu em pptx nasceu de estimar a
largura de um rótulo por contagem de caracteres. Um "W" e um "i" não têm a mesma
largura, e versalete com letter-spacing menos ainda. Aqui se mede.

    from textmetrics import largura, cabe
    largura("PRÊMIO DE MERCADO", "Inter SemiBold", 24, spacing=0.10)  -> px reais

Uso no construtor: posicione o próximo elemento em `x + largura(rotulo, ...) + gap`,
nunca em `x + k * len(rotulo)`. Criado 21/08/2026.
"""
import os, functools
from PIL import ImageFont

# Local ANTES do vault: a pasta fonts/ da skill mora em mount FUSE, e cada tamanho
# distinto relê o TTF pela rede — 9 páginas viravam minutos. (21/08/2026)
DIRS = [os.path.expanduser("~/.local/share/fonts"), os.path.expanduser("~/.fonts"),
        "/usr/share/fonts/truetype",
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "fonts"))]

ARQUIVOS = {
    ("Inter", False, False): "Inter-Regular.ttf",
    ("Inter", True, False): "Inter-Bold.ttf",
    ("Inter SemiBold", False, False): "InterSemiBold-Regular.ttf",
    ("Inter SemiBold", True, False): "InterSemiBold-Regular.ttf",
    ("Fraunces", False, False): "Fraunces-Regular.ttf",
    ("Fraunces", True, False): "Fraunces-Bold.ttf",
    ("Literata", False, False): "Literata-Regular.ttf",
    ("Literata", False, True): "Literata-Italic.ttf",
    ("Literata Light", False, False): "LiterataLight-Regular.ttf",
    ("Literata Light", False, True): "LiterataLight-Italic.ttf",
}


class FonteAusente(Exception):
    """Melhor estourar do que medir com a fonte errada e devolver número plausível."""


@functools.lru_cache(maxsize=64)
def _carrega(familia, tamanho, bold, italic):
    tamanho = int(round(tamanho))   # menos chaves de cache, menos leitura de TTF
    nome = ARQUIVOS.get((familia, bold, italic)) or ARQUIVOS.get((familia, False, False))
    if not nome:
        raise FonteAusente(f"família sem mapeamento: {familia!r}")
    for d in DIRS:
        p = os.path.join(d, nome)
        if os.path.exists(p):
            return ImageFont.truetype(p, int(round(tamanho)))
    raise FonteAusente(f"{nome} não encontrado em {DIRS}")


def largura(texto, familia="Inter", tamanho=24, bold=False, italic=False, spacing=0.0):
    """Largura em px do texto renderizado. `spacing` = letter-spacing em em (0.10 = 10%)."""
    if not texto:
        return 0.0
    f = _carrega(familia, tamanho, bold, italic)
    w = f.getlength(texto)
    return w + spacing * tamanho * max(0, len(texto) - 1)


def altura_linha(familia="Inter", tamanho=24, bold=False, italic=False):
    f = _carrega(familia, tamanho, bold, italic)
    a, d = f.getmetrics()
    return a + d


def cabe(texto, largura_disp, **kw):
    return largura(texto, **kw) <= largura_disp


def quebrar(texto, largura_disp, **kw):
    """Quebra em linhas que cabem em `largura_disp`. Devolve a lista de linhas."""
    linhas, atual = [], ""
    for p in texto.split():
        teste = (atual + " " + p).strip()
        if atual and largura(teste, **kw) > largura_disp:
            linhas.append(atual); atual = p
        else:
            atual = teste
    if atual:
        linhas.append(atual)
    return linhas


def demo():
    # o caso real: o rótulo que colidiu no slide 9 do caso CAPM
    lab = "PRÊMIO DE MERCADO"
    real = largura(lab, "Inter SemiBold", 24, bold=True, spacing=0.10)
    estimado_antigo = 13.6 * len(lab)      # o chute que colidiu
    estimado_novo = 18.5 * len(lab)        # o chute que "consertou"
    assert real > estimado_antigo, (real, estimado_antigo)
    print(f"  '{lab}': real {real:.0f}px · chute antigo {estimado_antigo:.0f}px "
          f"(colide) · chute novo {estimado_novo:.0f}px")

    # largura cresce com o texto e com o corpo
    assert largura("i" * 10, "Inter", 24) < largura("W" * 10, "Inter", 24)
    assert largura("teste", "Inter", 48) > largura("teste", "Inter", 24)
    assert largura("", "Inter", 24) == 0
    # spacing soma nos vãos, não nos caracteres
    a = largura("abc", "Inter", 20, spacing=0)
    b = largura("abc", "Inter", 20, spacing=0.5)
    assert abs((b - a) - 0.5 * 20 * 2) < 1e-6, (a, b)
    # quebra respeita a largura
    ls = quebrar("uma frase razoavelmente longa para quebrar em duas linhas", 200,
                 familia="Inter", tamanho=24)
    assert len(ls) > 1 and all(cabe(l, 200, familia="Inter", tamanho=24) for l in ls)
    # fonte inexistente estoura em vez de mentir
    try:
        largura("x", "NaoExiste", 24); assert False, "devia ter estourado"
    except FonteAusente:
        pass
    print("  autoteste ok")


if __name__ == "__main__":
    demo()
