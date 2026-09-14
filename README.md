# mkp-skills

Skills para o Claude Code, mantidas por mim. Cada plugin é uma skill (ou um par de skills
irmãs) empacotada para instalar em qualquer máquina.

## Instalar (uma vez)

No Claude Code, com acesso a este repositório privado na sua conta do GitHub:

```
/plugin marketplace add flaviomkpies/mkp-skills
/plugin install <nome>@mkp-skills
```

Plugins disponíveis: `writing`, `to-kindle`, `elegant-slides`, `xlsx-author`, `markitdown`, `text-to-bullets`, `capivara`, `watch`.

## Antes de usar: leia o ONBOARDING

Cinco plugins precisam de alguma instalação ou configuração antes do primeiro uso. Cada um traz
um **`ONBOARDING.md`** na raiz, com o passo a passo:

| Plugin | Precisa de | Onboarding |
|---|---|---|
| **writing** | criar o seu DNA de voz (`/writing dna`) | `plugins/writing/ONBOARDING.md` |
| **to-kindle** | `pandoc`, `pillow`, endereço Send to Kindle | `plugins/to-kindle/ONBOARDING.md` |
| **elegant-slides** | `python-pptx`, Chrome/Chromium | `plugins/elegant-slides/ONBOARDING.md` |
| **markitdown** | `markitdown`; chave OpenRouter só para imagem | `plugins/markitdown/ONBOARDING.md` |
| **watch** | `yt-dlp`, `ffmpeg`; chave Groq/OpenAI só sem legenda | `plugins/watch/ONBOARDING.md` |

Os outros (`xlsx-author`, `text-to-bullets`, `capivara`) rodam sem configuração —
`xlsx-author` pede `pip install openpyxl`.

## Atualizar

```
/plugin marketplace update mkp-skills
/plugin update <nome>@mkp-skills
```

Em `/plugin`, na aba da marketplace, dá para ligar a atualização automática.

## O que ficou de fora, e por quê

- **Conteúdo pessoal.** A skill `writing` vai com `DNA.md` e `CORRECOES.md` **vazios**: a voz é
  de quem usa, e se constrói com `/writing dna`. Os exemplos de calibração também começam
  vazios.
- **Integrações da máquina de origem.** Envio automático ao Kindle e ao reMarkable, publicação
  em canal, Drive e ferramenta de issues.
- **Word, PowerPoint e Excel oficiais.** As skills `docx`, `pptx` e `xlsx` da Anthropic são
  proprietárias e não podem ser redistribuídas aqui. Instale as oficiais:
  https://github.com/anthropics/skills

## Licenças

O código escrito por mim está sob MIT (`LICENSE`). Componentes de terceiros mantêm a licença de
origem, declarada junto do arquivo:

| Componente | Origem | Licença |
|---|---|---|
| `markitdown` | microsoft/markitdown | MIT (`LICENSE.txt` junto) |
| motor de slides | zarazhangrui/frontend-slides | MIT (`engine/LICENSE-frontend-slides`) |
| `watch` | bradautomates/claude-video | MIT (declarada no frontmatter) |
| fontes Literata, Inter, Fraunces | Google Fonts / rsms | SIL OFL 1.1 (`fonts/OFL.txt`) |
