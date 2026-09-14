---
name: elegant-html-to-pptx
description: "Converte deck HTML Elegant/reMarkable em PowerPoint nativo e editável, shape a shape, com tema e fontes embutidas + nota de consistência. Use para 'versão pptx do deck', 'PowerPoint editável', 'converter o HTML pra pptx'."
category: documentos-office
tools:
  - Read
  - Write
  - Bash
  - Glob
  - Edit
---
# elegant-html-to-pptx

Ponte **HTML (tema Elegant/reMarkable) → PPTX editável**. O irmão `/elegant-html-slides` é ótimo para prototipar e revisar macro; **mas editar HTML na mão é contraprodutivo**. Quando o autor vai "meter a mão na massa", ele para num PowerPoint. Esta skill faz essa passagem preservando a identidade P&B.

## Caminho preferido quando já existe um deck do tema (método W2, 05/09/2026)

**Clone os slides-arquétipo do pptx mais recente e troque texto e foto**, em vez de reconstruir do HTML.
Foi assim que nasceram o W2 Acme v04 (`03_Scripts/v04/lib.py`, clonando do W1 v42) e o deck do post da
preserva a formatação do 1º run, `set_pic()` troca a foto com crop "cover", e no fim apagam-se os slides
originais. Arquétipos do v04: capa/fecho full-bleed = s67 · 3 colunas com foto = s2 · lista numerada +
foto-metade = s10 · colunas numeradas = s21. Diagramas (bifurcação, linha do tempo, troca entre raias,
chevrons) se desenham com `box/oval/line/curve` do exemplo, sempre sem `<p:style>`.

foto: recorta a foto pelo DOM (full-bleed `object-fit: cover` e coluna com `overflow: hidden`), overlay com alfa,
chevron/pentágono a partir de `clip-path`, oval de `border-radius: 50%`, marcadores ○/□ das listas e fio de rodapé
das linhas de tabela. Medido: 12 slides, 250 caixas nativas, 5 fotos, cobertura textual 100%, visual 98%.
Título grande desce `0.16 × tamanho` para não encostar no kicker (LibreOffice e PowerPoint posicionam a 1ª linha
mais alto que o browser). Sem embed de fonte por padrão: entregar o zip das TTF junto.

Dois utilitários genéricos na `lib/`: **`pptx2html.py`** (pptx → deck HTML de palco fixo, shape a shape,
fotos embutidas; é o caminho para a versão web de um deck nativo) e **`html2pptx.py`** (DOM real via
Playwright → caixas nativas; para HTML feito à mão sem deck anterior).

Regra do autor para qualquer slide (05/09/2026): **nunca um slide chato; o design representa a ideia.**
Lista numerada só quando a ordem é o conteúdo. Detalhe da identidade vigente: `/elegant-html-slides` →
`design.md §Régua W2`.

## Princípio (a decisão que define tudo)

Fidelidade × editabilidade puxam entre si. Três caminhos:
- **Screenshot 1-por-slide** → 100% fiel, 0% editável (uma imagem). NÃO.
- **SVG inteiro do slide → DrawingML** (ppt-master, <issue>) → fiel, mas vira mosaico de vetores que ninguém edita no PowerPoint. NÃO.
- **Reconstrução nativa** → cada texto é uma caixa clicável em Literata, fios são linhas, foto é imagem, e a simbologia SVG entra como PNG decorativo no canto. ~92-96% visual, **100% editável**. SIM.

Esta skill faz o terceiro. O texto é sempre nativo; só a simbologia à mão (rede de nós, glifos, fio serrilhado) entra como imagem.

## Fontes de referência
- `/elegant-html-slides` — tema de origem (tokens em design.md: paper #FCFCFC, ink #141414, cinzas, hairlines, Literata/Inter).
- ppt-master (<issue>) — pipeline SVG→pptx, aproveitado só pros glifos decorativos.

## Escala (decorar)
Palco 1920x1080 → 16:9 (13.333x7.5"). 6350 EMU por px e 0.5 pt por px nos dois eixos (limpo). Padding do slide do tema: 84px topo/base, 130px laterais → área útil 1660x912.

## Pipeline

### 0. Insumos
- O .html do deck (fonte visual) + os PNGs renderizados dele (referência de layout — use os qc*.png do /elegant-html-slides, ou renderize: export-pdf.sh + pdftoppm).
- O markdown TEXTO-EDITAVEL (fonte do texto, 1:1 com o deck) — é o que garante cobertura textual 100%.

### 1. Extrair identidade
- grep dos tokens de cor (--ink etc.) e font-size (px x0.5 = pt).
- SVGs: re.findall(r'<svg.*?</svg>', html) → 1 arquivo por glifo.

### 2. Fontes (uma vez)
Literata + Inter são Google Fonts (OFL, embutíveis). Instale-as (~/.fonts + fc-cache) para o render fiel via LibreOffice. Já vêm prontas em fonts/.

### 3. Converter os SVG decorativos → PNG transparente
svglib não resolve var(--x) nem tem backend cairo. Receita que funciona:
1. substituir var(--ink)→#141414 etc. no texto do SVG;
2. svg2rlg → renderPDF.drawToFile → pdftoppm -png;
3. PIL: pixels quase-brancos → alpha 0 (glifo P&B sobre paper sem costura).
ATENÇÃO: Fio serrilhado (linha cheia, full-width): NÃO use svglib — ele corta a página em ~75%. Desenhe a polyline direto com PIL a partir dos pontos (garante 100% da largura).

### 4. Construir o deck NATIVO
lib/pptxlib.py dá os helpers (add_text com runs multi-parágrafo, add_line, add_rect, add_img, escala E()/P(), paleta, fontes). Reconstrua slide a slide pelas coordenadas de palco lidas dos PNGs. Chrome comum do tema: nav header, pager (NN/10), hairline de margem, eyebrow tracked, título com barra vertical de accent, rodapé, glifo no canto.

### 5. Aplicar o TEMA + embutir fontes
python3 lib/finalize_pptx.py deck.pptx final.pptx — por cirurgia no zip (robusto):
- theme1.xml: majorFont=Literata Light, minorFont=Inter, clrScheme grayscale, nome do tema;
- layouts renomeados (Capa/Conteúdo/Split-foto/Fechamento/Seção);
- embute as 7 faces TTF (embeddedFontLst logo após notesSz/sldSz, embedTrueTypeFonts=1) — sem isso o PowerPoint do Windows troca Literata por outra fonte.

### 6. NOTA DE CONSISTÊNCIA (obrigatória antes de entregar)
python3 lib/score_conversion.py → 0-100 em 7 dimensões. Meta >= 90. Depois, SEMPRE olhar os PNGs renderizados um a um (a métrica visual é grosseira porque o deck é quase todo branco — o sinal forte é cobertura textual + o olho).

## Checklist de revisão (as 7 dimensões da nota)

| # | Dimensão | Peso | Como mede |
|---|----------|-----:|-----------|
| 1 | Estrutura | 10 | nº de slides bate |
| 2 | Cobertura textual | 25 | % das linhas do TEXTO-EDITAVEL presentes no pptx (objetivo) |
| 3 | Editabilidade | 15 | razão caixas-de-texto nativas / (texto+imagens) |
| 4 | Paleta P&B | 10 | toda cor de fonte em {ink, g1, g2, hair, paper, branco} |
| 5 | Tipografia | 15 | toda run em {Literata Light, Literata, Inter, Inter SemiBold} |
| 6 | Fontes embutidas | 10 | >=6 faces .fntdata no arquivo |
| 7 | Fidelidade visual | 15 | similaridade render-pptx x render-html (proxy) + revisão a olho |

Além disso, revisão visual slide a slide (herdado do /elegant-html-slides): sem sobreposição, nada estoura o palco, contraste ok, glifo/foto aparecem, e a leitura só pelos títulos conta a história.

## Gotchas caros (aprendidos)

### Os dois que estragam TODO fio do tema (medidos no caso IMC, 20/08/2026)

O tema é feito de fios finos. Estes dois bugs atacam exatamente isso, e nenhum aparece no XML
(que fica correto) — só na medição do pixel renderizado.

- **Fio: retângulo de 1px, NUNCA `add_connector`.** `add_line()` grava `<a:ln w="6350">` (0,5pt,
  correto), e mesmo assim o fio sai com **~10px** de espessura fora do PowerPoint. Use
  `add_rect(s, x, y, w, 1, fill=HAIR)`. Vale para fio horizontal e vertical. Helpers:
  ```python
  def hline(s, x, y, w, color=HAIR, px=1): return add_rect(s, x, y, w, px, fill=color)
  def vline(s, x, y, h, color=HAIR, px=1): return add_rect(s, x, y, px, h, fill=color)
  ```
- **Sombra: remover o `<p:style>`, porque `shadow.inherit=False` NÃO basta.** Todo autoshape criado
  pelo python-pptx nasce com `<p:style>` contendo `<a:effectRef idx="2">`, que puxa a **sombra** do
  effectStyle do tema Office. O tema proíbe sombra (`design.md`: profundidade = fio + espaço), e o
  sintoma é um degradê difuso de ~8px embaixo de cada fio e cada barra. `sp.shadow.inherit=False`
  da pptxlib não resolve. Receita:
  ```python
  st = sp._element.find(qn('p:style'))
  if st is not None: sp._element.remove(st)
  spPr = sp._element.spPr
  if spPr.find(qn('a:effectLst')) is None:
      spPr.append(spPr.makeelement(qn('a:effectLst'), {}))
  ```
- **Como medir (não confie no olho em PNG reduzido):** renderize a 150dpi e leia a coluna de pixels
  atravessando o fio. Fio saudável = 1-2px de transição voltando ao papel; sombra = degradê de 8px+
  com mínimo mais claro que o token. Foi essa medição que separou os dois bugs, que se somavam.

### Identidade Régua (Fraunces) vs. variante Elegant (Literata)

A `pptxlib.py` nasceu na variante **Elegant** (papel quente, Literata). Para a **Régua** (branco,
identidade default do `/elegant-html-slides`), sobrescreva no builder:
`SERIF='Fraunces'` · `G2='7C7C7C'` · e no `score_conversion.py`, `FONTS_OK={'Fraunces','Inter','Inter SemiBold'}`
mais os cinzas do deck em `PALETTE`. Fraunces não vem em `fonts/`: baixe o variable do
`google/fonts` e instancie em **`opsz=144, WONK=0`** (opsz alto = o alto contraste que a identidade

### Demais

- MSO_LANGUAGE_ID.PORTUGUESE_BRAZIL não existe → não setar language_id.
- Layouts custom no master via python-pptx são inviáveis; renomear os existentes + master bg paper já constitui "tema" utilizável na galeria do PowerPoint.
- Validar o zip pós-embed abrindo com Presentation() e re-renderizando (LibreOffice ignora fontes embutidas, então o teste real de embedding é abrir no PowerPoint Windows).
- Entregar pptx + PDF lado a lado, nome versionado YYYYMMDD_nome_vN, nunca sobrescrever.

## Saída
- final.pptx (editável) + .pdf na pasta da issue no vault.
- Bloco de nota de consistência (as 7 dimensões + total) no report/Linear.

## Verificação no MOTOR REAL (não confie só no LibreOffice)
LibreOffice rende com as fontes instaladas, mas o motor de layout NÃO é o do PowerPoint — quebra de linha e altura de caixa diferem, e overflow de card passa batido em baixa-res. O motor real do PowerPoint está no Graph: suba o pptx no OneDrive e peça `GET /me/drive/items/{id}/content?format=pdf` (usa graph_client.py, token delegado do autor). Isso rende com o motor real do Office → pdftoppm → avalie slide a slide. Foi assim que apareceu (e foi corrigido) um vazamento de texto no card da coluna 1 das Ofertas que o LibreOffice tinha mascarado.

## Gotchas de fonte embutida (importantes)
- **Ordem no schema:** `embeddedFontLst` vai logo APÓS `notesSz` em presentation.xml. Elementos lxml sem filhos são FALSY — nunca use `find(notesSz) or find(sldSz)` pra achar a âncora (o `or` pula o notesSz e insere fora de ordem → arquivo inválido). Use `is None`.
- **Office online NÃO exporta pptx com fonte embutida** (`export/pdf` devolve `notSupported`/UnsupportedMediaType). Então: verifique LAYOUT com o deck PLAIN (sem embed) via Graph; verifique TIPOGRAFIA com LibreOffice+fonte instalada. O embed não dá pra validar por essas vias — o teste real é abrir no PowerPoint desktop.
- **Garantia de fonte no destino:** como o embed é inverificável aqui, entregue TAMBÉM os TTF pra instalar na máquina do destinatário (serve pra todos os decks futuros do tema). Fonte instalada > embed inverificável.

## Feedbacks do autor incorporados (revisão v3→v4, 22/07)
1. **Idioma da caixa = pt-BR (crítico).** Sem `lang="pt-BR"` na run, o PowerPoint marca todo o texto como erro ortográfico (língua da caixa fica inglês). `pptxlib._apply_run` já seta `rPr.set('lang','pt-BR')`. Verificar no fim: toda run com lang pt-BR.
2. **Ancorar o conteúdo na base do container.** O tema pede conteúdo colado embaixo; posicionar os blocos baixos, não centralizados no meio.
3. **Títulos do mesmo tamanho.** Um único `TITLE` (ex.: 48) para todos os títulos de slide de conteúdo — não variar por slide.
4. **Página de encerramento com contato.** Fechar o deck com um slide "Obrigado!" (glifo + faixa de contato + fio serrilhado), além do contato em Próximos passos.
5. **Agrupamento de elementos (grpSp).** O o autor pediu pra receber os blocos já AGRUPADOS (cada coluna de oferta, cada linha da matriz, cada passo da timeline, o bloco de header) pra alinhar como unidade. python-pptx não cria grupo nativo — precisa embrulhar shapes num `<p:grpSp>` com `chOff/chExt == off/ext` (senão os filhos deslocam). Implementar helper `group(shapes)` e TESTAR (render+Office) antes de confiar, porque grupo malformado quebra o arquivo. Não é overengineering: ele agrupa na mão hoje.
6. **Action-titles + narrativa.** Nas revisões o autor troca rótulos por títulos-conclusão ("Recomendação para iniciar a jornada..." em vez de "Ofertas"). Já escrever assim (herda do /elegant-html-slides §2.5).

## ⚠️ FONTE EMBUTIDA QUEBRA MOBILE/OFFICE-ONLINE (default = NÃO embutir)
Fato confirmado: pptx com `embeddedFontLst` é **rejeitado pelo Office online** (`export/pdf` → notSupported) e **trava no PowerPoint do celular** ("tem um bug / precisa reparar"). Pior ainda depois de N transformações (finalize → save no PowerPoint → edição python-pptx), quando o PowerPoint acumula faces (7→10) e o arquivo fica frágil.
- **DEFAULT: NÃO embutir fontes.** Entregar o pptx LIMPO + o zip das fontes pra instalar (`Acme_fontes_tema.zip`). Fonte instalada > embed inverificável.
- **Verificação que vale:** subir o pptx no OneDrive via Graph e pedir `content?format=pdf`. Se o motor da Microsoft ACEITA (200), o mobile abre. Se dá 406/notSupported, o arquivo tem algo que o mobile também recusa (quase sempre = fonte embutida).
- **strip_fonts.py** remove embeddedFontLst + fntdata + rels de fonte + flags → arquivo universalmente abrível. Usar antes de entregar qualquer deck que passou por embed.
- **finalize idempotente:** se o arquivo JÁ tem fntdata, não re-embute (senão duplica e corrompe — LibreOffice/mobile não abrem).
