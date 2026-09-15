---
name: show-me
description: "Caderno de evidências visual: para cada dado ou citação de um documento, acha a fonte primária e captura o print da página com o trecho destacado. Use para 'show me', 'mostra a fonte', 'prova visual', 'de onde veio esse dado'."
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch
---

# Show Me — caderno de evidências visual

## Princípio

Fact-check responde "esse dado bate com a fonte?" (texto). **Show Me responde "me mostra a
fonte"** — entrega a prova material: o print da página original, com o trecho destacado, e o
endereço de onde ela vive. Anti-alucinação por evidência, não por confiança.

- **Consultoria:** o deck que mostra a página real do relatório por trás de um número ganha
  credibilidade na hora.
- **Acadêmico:** prova material de cada citação antes de submeter ou defender.

## Quando não usar

Verificação só textual, sem print, é fact-check comum. Só baixar um paper é trabalho de
gerenciador de referências.

## Antes de executar

O gargalo é **rede, não raciocínio**. Nunca baixe em série o que dá para baixar em paralelo, e
nunca rebaixe o que já está no cache. Paralelizar não custa qualidade: o print é idêntico.

## Pipeline

### Fase 1 — Extrair os alvos

Do documento (`.docx` via python-docx, `.pdf` via pymupdf) extrair a lista de
`(afirmação, autor, ano, dado)`. Sem alvo específico, pegar todas as referências e os dados
quantitativos. **Priorize dado com número** — é onde o print prova alguma coisa. Referência
puramente teórica vai para uma seção-lista com DOI ou ISBN, sem print obrigatório.

### Fase 2 — Resolver as fontes, em cascata e em paralelo

Para cada alvo, resolva o PDF na primeira camada que responder, e dispare todos os alvos em
paralelo (`xargs -P 6` ou jobs em background):

1. **Cache local** — `~/.cache/show-me/sources/<slug>.pdf`, de execuções anteriores.
2. **O que você já tem** — procure no disco por autor e título antes de ir à rede
   (`find ~ -iname "*<autor>*.pdf"`). Quem trabalha com um corpus já baixou metade dele.
3. **Rede, via `scripts/fetch_pdf.py`** — cascata aberta Crossref → Unpaywall → OpenAlex →
   arXiv, gravando no cache:

```bash
python3 scripts/fetch_pdf.py --doi 10.1002/smj.4057 --email voce@exemplo.com
python3 scripts/fetch_pdf.py --title "Dynamic capabilities and strategic management"
```

4. **URL direta**, quando você já sabe onde está (arXiv, NBER, repositório institucional).

**Paywall sem via aberta:** marque *"fonte não localizável visualmente"* e registre o DOI.
Nunca fabrique print nem URL. Plataforma paga (Gartner, Scopus, Web of Science) não recebe
crawler — use o export nativo dela.

**Confira o que baixou.** O fallback de busca por título erra: um PDF de 1.800 páginas pode
chegar no lugar de uma revisão de 20. Case a primeira página com o título antes de usar.

### Fase 3 — Localizar o dado e capturar

`scripts/highlight.py` faz a busca tolerante e o render com destaque:

```bash
python3 scripts/highlight.py fonte.pdf --find "47%" "47 percent" "0.47" --out prova.jpg
```

- **Busca tolerante:** o mesmo dado aparece como `47%`, `47 percent` ou `0.47`; milhar como
  `5,179`, `5179` ou `5.179`. O script cobre as variantes e prefere a página com melhor match
  (abstract ou figura antes de menção solta).
- **Número dentro de figura rasterizada:** não está no texto. Use `--ocr` (pede `pytesseract`)
  ou capture a figura inteira — e diga que é captura, não busca.

### Fase 4 — Conferir e montar o caderno

**Cross-check antes de montar:** confronte o número do print com a afirmação do documento e
**sinalize divergência** — ano de working paper contra o publicado, número diferente,
atribuição trocada. Isso é o recurso da skill, não um acaso.

Monte um bloco por evidência: *afirmação no documento → fonte → localização (path, URL ou DOI)
→ print destacado → nota ou divergência*. A seção final lista as referências teóricas com
localização.

## Três regras que vieram de erro real

1. **Cada trecho citado é conferido por código antes de montar.** Carregue o texto por página
   do PDF, normalize hífen de quebra e ligadura, e **falhe** se a literal não estiver na página
   declarada. Tradução vai ao lado da literal, nunca no lugar dela. Sem isso sai "p. 545" num
   caderno entregue quando era p. 544: PDF de base de dados costuma ter capa, e a paginação do
   arquivo não é a paginação impressa.
2. **Tabela de cobertura no fim: fonte citada → onde está o print.** Extraia por código toda
   referência das colunas de fonte e das notas, compare com os blocos de print, e liste o que
   ficou sem print **com a razão** (PDF não localizado, dado próprio, decisão do autor). Um
   caderno de 30 páginas já foi entregue com onze fontes sem prova, e não havia como notar.
3. **Teto de 4 MB por arquivo HTML entregue.** Print em JPEG, largura 1000 px, qualidade 70,
   nunca PNG. Acima de 4 MB, divida por bloco: arquivo 0 com estrutura, resumo, lacunas e
   cobertura; arquivos 1..N com os prints e links cruzados. A contagem de blocos dentro do
   arquivo não prova entrega — o que o leitor vê na tela prova.

Para ler no papel ou num leitor e-ink: converta com `google-chrome --headless=new
--print-to-pdf` e `@page A4` injetado, e valide o número de páginas com `pdfinfo` antes de
mandar. Navegador em sandbox às vezes renderiza um PDF longo como página única.

## Dependências

```
pip install pymupdf requests
pip install pytesseract pillow     # opcional, só para número dentro de figura
```

Passo a passo no `ONBOARDING.md` do plugin.

## Limites (honestos)

- Número em figura rasterizada: OCR é mais frágil; capturar a figura inteira é mais honesto.
- Paywall sem via aberta: marque como não localizável e registre o DOI. Nunca fabrique a prova.
