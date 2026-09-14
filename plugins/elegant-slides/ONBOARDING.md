# Onboarding — elegant-slides

## 1. Dependências

```
pip install python-pptx pillow
```

E um **Chrome ou Chromium** instalado, usado para renderizar e conferir o deck. Os scripts
procuram sozinhos: variável `CHROME_BIN`, depois o PATH, depois os caminhos comuns de Linux e
macOS. Para forçar um caminho, passe `--chrome /caminho/do/chrome`.

## 2. Auditoria semântica (opcional)

`slop-audit.py` manda o deck para um modelo e devolve flags de texto genérico. Precisa de uma
das duas coisas:

- `ANTHROPIC_API_KEY` no ambiente, **ou**
- o CLI `claude` instalado e autenticado (o script cai nele automaticamente).

Sem nenhuma das duas, pule esta etapa — ela sinaliza, não reprova.

## 3. Fontes

As fontes embutidas (Literata, Inter, Fraunces) vêm em
`skills/elegant-html-to-pptx/fonts/` sob a SIL Open Font License 1.1. O texto da licença está
em `fonts/OFL.txt` e deve acompanhar qualquer redistribuição. Para o render fiel via
LibreOffice, instale-as no sistema (`~/.fonts` + `fc-cache` no Linux, Font Book no macOS).

## 4. Uso

```
python3 skills/elegant-html-slides/scripts/test-deck.py deck.html
python3 skills/elegant-html-to-pptx/lib/html2pptx.py deck.html saida.pptx
```
