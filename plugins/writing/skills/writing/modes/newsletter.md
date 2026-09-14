# Mode: newsletter

> Modo invocado por `/writing newsletter [outline|draft|polish]`.
> Skill mãe: `/writing` (ver `SKILL.md` raiz).

Fluxo para um artigo de newsletter, do material bruto ao texto pronto para publicar. A voz vem
do `DNA.md` (crie o seu com `/writing dna` antes da primeira vez).

## Etapas

**0. Material bruto.** Duas entradas possíveis: você já tem o material (transcrição de áudio,
anotações, rascunho) ou só tem a ideia. No segundo caso, a skill faz perguntas de múltipla
escolha até haver material suficiente — nunca inventa o conteúdo por você.

**1. Outline.** Árvore indentada com o que você disse, nas suas palavras. Gancho de abertura,
ideia principal por bloco, fechamento. Iterar até você aprovar. Mudança depois de aprovado cria
uma versão nova, não edita a aprovada.

**2. Research** (quando o outline tem afirmação que precisa de fonte). Ver `fact-check.md`.
Afirmação sem fonte não entra na prosa.

**3. Prosa.** Transformar o outline aprovado em texto corrido, bloco a bloco, usando as suas
palavras do material bruto. Frase boa que você já escreveu se mantém intacta. Onde faltar
informação, marcar `[COMPLETAR: contexto]` em vez de inventar.

> **Anti-atribuição.** Expressão que a skill inventou entra marcada `[SUGESTÃO]` com
> justificativa, nunca corre na prosa como se fosse sua. Se uma expressão não é rastreável ao
> material bruto, marcar.

**4. Revisão.** Nesta ordem:

1. `python3 ../scripts/tells_pt.py <arquivo>` — gate determinístico. Exit 0 = no máximo 3 tells
   por ~1.000 palavras. Roda **antes** do humanizer: lista de padrões só funciona quando algo
   conta.
2. Passe de DNA — cada frase soa como você falando?
3. Passe de humanizer — `../primitives/humanizer-patterns.md`.

Mostrar os diffs separados, com justificativa. Edits cirúrgicos; se um parágrafo pede reescrita
inteira, voltar à etapa 1.

**5. Publicar.** Você publica, colando o texto final no site do seu canal. A skill não tem
acesso a nenhuma conta.

## Gate de decisão (entre outline e prosa)

Escolha criativa aparece como **decisão a validar**, nunca decidida em silêncio e mostrada
pronta. Para decisão de texto (título, frase, metáfora), traga os candidatos concretos primeiro
e o trade-off depois — nunca a categoria abstrata antes do texto.

## Anti-padrões

- Escrever prosa antes do outline aprovado.
- Citar autor para apadrinhar um conceito que é seu. Citação serve a dado medido, não a
  afirmação conceitual.
- Trocar o número concreto vivido por uma abstração.
- Publicar sem o gate determinístico ter passado.
