# Fact-check protocol — template canônico

Usado por `modes/fact-check.md` e por outros modos que precisem verificar afirmação antes de publicar.

## Template do prompt do agente Haiku

Quando spawnar um Haiku para fact-check, usar este prompt como base. Substituir `<CLAIM>` pela afirmação a verificar.

```
Pesquisa específica e verificada. Não invente URL.

CLAIM A VERIFICAR: <CLAIM>

INSTRUÇÕES:
1. NÃO confiar em URL fabricada / lembrada. Você precisa BUSCAR e VERIFICAR.
2. Use WebSearch primeiro com termos exatos da claim (entre aspas se for quote).
3. Use WebFetch na URL candidata para CONFIRMAR que a afirmação aparece no conteúdo.
4. Se a afirmação não aparecer no conteúdo da página, reporte isso. NÃO INVENTE URL.

REPORTE em formato canônico:

[STATUS] — Verificado | Parcialmente | Não verificável

URL fonte: <url se aplicável>
Trecho verbatim do conteúdo: "<5-10 linhas de contexto>"
Atribuição correta: <quem realmente disse — pessoa, jornalista, descrição editorial>
Data / evento: <quando, onde>

Notas: <ressalvas, alternativas, fontes adicionais>

Máximo 250 palavras. Direto. Se não encontrar, marque "Não verificável" com razão clara.
```

## Regras críticas

1. **WebFetch real, não inferência.** Se o agente diz "encontrei a URL X com a frase Y" mas não consegue colar o trecho verbatim do WebFetch, é alucinação. Marcar não-verificável.

2. **Quote em artigo ≠ quote da pessoa atribuída.** Se a frase aparece num artigo da Medium / Forbes / etc, é o autor do artigo escrevendo. Atribuir ao autor real, não à pessoa sobre quem o artigo fala. Caso real (ENG-216 / BIZ-172): frase "It is not a model. It is a control layer..." atribuída inicialmente ao Steinberger → na verdade era descrição editorial de artigo Global Times Singapore.

3. **Confirmar página existe E contém o trecho.** WebSearch que retorna URL plausível não basta — sempre WebFetch + grep do trecho.

4. **Limitar tokens.** Spawn Haiku, max 250 palavras de output. Pesquisa ampla → escalar para Sonnet via Birdperson, não Haiku.

5. **Múltiplas fontes ajudam.** Se 2 fontes independentes confirmam o mesmo, confiança alta. 1 fonte só, marcar como "single-source — confirmar antes de publicar".

6. **REFERÊNCIA ≠ CLAIM — validar metadados bibliográficos no documento real.** Verificar que o claim aparece na fonte NÃO valida a citação: autores, ano, título e venue precisam ser conferidos verbatim na primeira página do PDF/artigo real. Caso canônico (artigo Nexo, 2026-07-03): o claim "LLMs erram contagem de letras" estava correto e verificado, mas a referência circulou como "Ricco (2026)" por toda a revisão — o PDF real revelou Conde, Martínez e Reviriego, IEEE Computer, 2025 ("Ricco" era corruptela de "Reviriego"). O erro sobreviveu a regex, LLM-judge e audit de sources porque nenhum passo abria o documento. Regra: toda entrada de bibliografia exige o PDF/página aberto e os metadados copiados de lá, nunca "de como a referência circula".

## Tipos de claim e cuidados

- **Quote literal de uma pessoa** — máximo cuidado. Vai pra publicação como `"frase"` atribuída. Erro = problema de credibilidade.
- **Estatística** — fonte primária. "Estudo X mostrou Y%" precisa do estudo, não de blog que cita o estudo.
- **Data / evento** — confirmar local, data, contexto. "No GTC 2026" pode ser GTC errado.
- **Atribuição de produto/projeto** — quem criou, quando, sob qual licença.
- **URL como referência** — sempre WebFetch antes de incluir no post.

## Output do fact-check para Flavio

3 níveis de aprovação:

- ✅ **Verificado** — pode usar na publicação.
- ⚠️ **Parcialmente** — usar com cuidado: reformular para não atribuir incorretamente, ou marcar como "como reportado por X".
- ❌ **Não verificado** — não publicar essa afirmação. Buscar alternativa ou tirar.

Sempre apontar exatamente o que precisa mudar no texto, não só "verificou ou não".
