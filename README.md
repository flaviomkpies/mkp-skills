# mkp-skills

Skills para o Claude Code, mantidas por mim. Cada plugin é uma skill (ou um par de skills
irmãs) empacotada para instalar em qualquer máquina.

## Instalar (uma vez)

No Claude Code, com acesso a este repositório privado na sua conta do GitHub:

```
/plugin marketplace add flaviomkpies/mkp-skills
/plugin install <nome>@mkp-skills
```

Plugins disponíveis: `writing`, `to-kindle`, `elegant-slides`, `xlsx-author`, `text-to-bullets`, `show-me`, `capivara`.

## Antes de usar: leia o ONBOARDING

Quatro plugins precisam de alguma instalação ou configuração antes do primeiro uso. Cada um traz
um **`ONBOARDING.md`** na raiz, com o passo a passo:

| Plugin | Precisa de | Onboarding |
|---|---|---|
| **writing** | criar o seu DNA de voz (`/writing dna`) | `plugins/writing/ONBOARDING.md` |
| **to-kindle** | `pandoc`, `pillow`, endereço Send to Kindle | `plugins/to-kindle/ONBOARDING.md` |
| **show-me** | `pymupdf`, `requests`, e um e-mail de contato | `plugins/show-me/ONBOARDING.md` |
| **elegant-slides** | `python-pptx`, Chrome/Chromium | `plugins/elegant-slides/ONBOARDING.md` |

Os outros (`xlsx-author`, `text-to-bullets`, `capivara`) rodam sem configuração —
`xlsx-author` pede `pip install openpyxl`.

## Atualizar

```
/plugin marketplace update mkp-skills
/plugin update <nome>@mkp-skills
```

Em `/plugin`, na aba da marketplace, dá para ligar a atualização automática.

## Recomendações — o que instalar junto

Aqui só moram skills da casa. O que é de outra pessoa não é redistribuído: fica a
indicação e o link para a fonte, que é quem mantém e atualiza.

### Documentos Office — Anthropic

As skills oficiais de Word, PowerPoint, Excel e PDF. São as melhores que existem para
isso e vêm da própria Anthropic:

- **github.com/anthropics/skills** — `docx`, `pptx`, `xlsx`, `pdf`

### Engenharia de software — Matt Pocock

Um conjunto forte para trabalho de código: diagnosticar bug, TDD, modelagem de domínio,
code review, e o `grilling`, que sabata uma decisão sua até achar onde ela não fecha.

```
/plugin install mattpocock-skills@claude-plugins-official
```

- **github.com/mattpocock/skills**

### Apresentações em HTML — frontend-slides

O motor de deck HTML sobre o qual o `elegant-slides` daqui foi construído. Se você quer
escolher o próprio estilo visual em vez de herdar o meu, vá direto na fonte:

- **github.com/zarazhangrui/frontend-slides** (MIT)

### Conversão de arquivo para texto — MarkItDown

PDF, Word, PowerPoint, Excel, imagem e áudio viram markdown para o Claude ler.

```
pip install markitdown
```

- **github.com/microsoft/markitdown** (MIT)

### Vídeo — watch

Baixa o vídeo, extrai frames, pega a transcrição e entrega tudo para o Claude responder
sobre o que está lá dentro.

- **github.com/bradautomates/claude-video** (MIT)

## O que ficou de fora, e por quê

- **Conteúdo pessoal.** A skill `writing` vai com `DNA.md` e `CORRECOES.md` **vazios**: a voz é
  de quem usa, e se constrói com `/writing dna`. Os exemplos de calibração também começam
  vazios.
- **Integrações da máquina de origem.** Envio automático ao Kindle e ao reMarkable, publicação
  em canal, Drive e ferramenta de issues.
- **Skill que não é minha.** Não redistribuo o trabalho de outra pessoa: `docx`, `markitdown`
  e `watch` saíram daqui e viraram indicação na seção acima, apontando para quem mantém.

## Licenças

O código escrito por mim está sob MIT (`LICENSE`). Componentes de terceiros mantêm a licença de
origem, declarada junto do arquivo:

| Componente | Origem | Licença |
|---|---|---|
| motor de slides | zarazhangrui/frontend-slides | MIT (`engine/LICENSE-frontend-slides`) |
| fontes Literata, Inter, Fraunces | Google Fonts / rsms | SIL OFL 1.1 (`fonts/OFL.txt`) |
