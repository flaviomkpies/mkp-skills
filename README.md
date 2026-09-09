# mkp-skills

Skills da casa para o Claude Code, mantidas pelo Flavio. Repositório privado.

## Instalar (uma vez)

No Claude Code, com acesso a este repositório na sua conta do GitHub:

```
/plugin marketplace add fmkpMondore/mkp-skills
/plugin install writing@mkp-skills
/plugin install to-kindle@mkp-skills
/plugin install elegant-slides@mkp-skills
/plugin install docx@mkp-skills
/plugin install xlsx-author@mkp-skills
/plugin install markitdown@mkp-skills
/plugin install text-to-bullets@mkp-skills
/plugin install capivara@mkp-skills
/plugin install watch@mkp-skills
```

## Atualizar

Quando o Flavio publicar mudanças:

```
/plugin marketplace update mkp-skills
/plugin update <nome>@mkp-skills
```

Em `/plugin`, na aba da marketplace, dá para ligar a atualização automática.

## Requisitos por plugin

| Plugin | Precisa de |
|---|---|
| writing | nada; na primeira vez, rode `/writing dna` com 3 a 5 textos seus |
| to-kindle | Python 3, `pandoc`, `pip install pillow` |
| elegant-slides | Chrome ou Chromium para conferir o deck; `pip install python-pptx` para o PowerPoint |
| docx | `pip install python-docx` |
| xlsx-author | `pip install openpyxl` |
| markitdown | `pip install markitdown`; imagens com IA só com chave da OpenRouter |
| text-to-bullets | Python 3 |
| capivara | acesso à web pelo Claude |
| watch | `yt-dlp`, `ffmpeg`; transcrição com chave da Groq ou OpenAI |

## O que ficou de fora de propósito

Tudo que depende da máquina do Flavio: envio automático ao Kindle e ao reMarkable, publicação no Substack, Drive, Linear, agentes do Veredas OS.
