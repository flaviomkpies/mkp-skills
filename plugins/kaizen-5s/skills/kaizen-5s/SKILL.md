---
name: kaizen-5s
description: "Organiza um espaço de trabalho ao fim de uma tarefa pelos cinco S do Kaizen: separa o relevante do descartável, leva cada item ao destino canônico no formato do destino, marca proveniência, deixa uma cabeça de leitura em cada pasta tocada e registra o que ficou pendente. Use para 'arruma', '5S', 'faxina', 'organiza essa pasta / o vault / a pasta temporária', e como última fase de um after-action de sessão."
argument-hint: "[escopo: pasta, vault, pasta temporária da sessão]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

# /kaizen-5s — o trabalho termina quando o ambiente fica arrumado

> Kaizen: pequenas melhorias contínuas, e a primeira delas é o lugar de trabalho. Os cinco S
> (Seiri, Seiton, Seiso, Seiketsu, Shitsuke) são uma ordem, não um checklist solto: primeiro se
> separa, depois se guarda, depois se limpa, depois se padroniza, e só então se sustenta.
> Esta skill é **portátil**: o núcleo vale para qualquer espaço (pasta, vault, área temporária);
> o que é local mora em `references/perfil-local.md`.
>
> **Antes da primeira vez:** leia o `ADAPTAR.md` do plugin. Sem perfil, a skill roda só o que é
> universal e pergunta o destino de cada classe de item antes de mover.

## Quando usar

- Ao fim de qualquer sessão que criou arquivo fora do lugar definitivo (rascunho, script, PDF,
  nota) — a uma rotina de after-action chama esta skill na sua última fase, se você tiver as duas.
- Quando alguém pede "arruma", "faxina", "organiza", "onde está cada coisa" sobre uma pasta, um
  vault Obsidian ou um espaço temporário.
- Antes de compartilhar uma pasta com terceiros, ou antes de arquivar um projeto.

**Não usar** para reorganizar a estrutura de alguém sem pedido (isso é redesenho, não 5S), nem
para "limpar" acervo cuja função você não mediu (ver as regras abaixo).

## Entrada

Um **escopo**: um ou mais espaços a arrumar (pasta local, subárvore de Drive, vault ou pasta de
vault, área temporária da sessão) e o **perfil** do ambiente, que diz onde é o destino canônico de cada
tipo de coisa, qual ontologia vale, como se escreve lá e o que é proibido. Sem perfil, a skill
roda só o que é universal e **pergunta** o destino de cada classe de item antes de mover.

## Regras que valem antes de qualquer fase

1. **Inventário antes de ação.** Primeiro se lista (`scripts/inventario_5s.py <pasta>`, só leitura),
   depois se decide. Nada é movido no mesmo comando que descobre.
2. **O que é de pessoa não se apaga.** Arquivo ou nota criados por humano, ou cuja autoria não se
   sabe, nunca são apagados por esta skill: vão para quarentena **fora** do índice (pasta com ponto,
   ou fora do vault), com o motivo no relatório. Proveniência preenchida por máquina não prova
   autoria — registra o último escritor.
3. **Função antes de forma.** Nota curta pode ser nó do grafo; pasta vazia pode ser índice; link
   mora em propriedade, não só no corpo. Antes de chamar algo de entulho, meça: conteúdo real fora
   de bloco de código e boilerplate, links recebidos (inclusive por propriedade), estrutura que
   depende dela. **O número de "descartável" é teto, não estimativa**: olhe três itens com os
   próprios olhos antes de escrever a recomendação.
4. **Entregável não se sobrescreve.** Versão nova é `_vN+1`; a anterior fica, marcada como
   superada na cabeça da pasta.
5. **Cada destino tem a sua ontologia e a sua ferramenta de escrita.** Respeitar a allow-list de
   tags e propriedades do destino (o perfil diz qual), e escrever pelo caminho que o perfil declara
   confiável, conferindo o resultado pela **fonte** (listagem do remoto), não pelo código de saída.
6. **Mover é árvore ou lista.** Pasta inteira move-se como pasta (uma operação); conjunto de arquivos
   move-se por lista (`--files-from`); **nunca** um processo por arquivo em loop.
7. **Escopo compartilhado pede coordenação.** Se outra sessão, pessoa ou agente pode estar
   trabalhando no mesmo lugar, confira antes; o que tem dono ativo não se move.
8. **Renomear quebra o que aponta.** Antes de renomear pasta ou nota que outras notas citam, procure
   o caminho antigo no conteúdo (inclusive templates e queries) e reescreva só o que existe de fato.

## As cinco fases

### 1 · Seiri — separar

Classificar cada item do escopo em três: **relevante** (entregável, fonte, código, nota que alguém
vai reler), **transitório** (saída intermediária, cópia de trabalho, teste) e **suspeito** (não se
sabe a função). Relevante segue para a fase 2; transitório fica onde está se o espaço morre sozinho
(pasta temporária que se apaga sozinha) ou vai para quarentena se o espaço é permanente; suspeito **não se decide agora** —
entra no relatório com o que falta medir.

### 2 · Seiton — cada coisa no seu lugar, no formato do lugar

Para cada item relevante, o perfil responde **onde** e **como**:

| Tipo | Vai para | No formato |
|---|---|---|
| código, script, patch de ferramenta | repositório versionado, com commit | nome sem colisão com o que já existe; docstring com propósito e data |
| entregável, relatório, análise | pasta canônica do assunto | `_vN+1`, nunca sobrescreve; frontmatter do destino |
| fonte (PDF, dataset, transcrição) | biblioteca ou pasta de fontes do assunto | uma pasta por fonte com ficha ao lado; ano da pasta = ano do arquivo |
| nota, síntese, learning | vault, na pasta que o tipo determina | tags da ontologia do destino; um parágrafo por linha, sem hard wrap |
| item cujo assunto está em decisão aberta | pasta do estudo, não a pasta definitiva | com a cabeça dizendo que aguarda decisão |

**Regra:** nada relevante sobrevive só no espaço temporário. Ferramenta remendada durante a sessão
é promovida na mesma sessão, senão a próxima execução roda o código velho.

### 3 · Seiso — limpar e marcar

- Toda nota, ficha e relatório escritos por agente levam a marca de proveniência do destino
  (o perfil diz qual — por exemplo `provenance: ai` no frontmatter da nota), para que
  quem lê distinga o que é dele do que é nosso sem abrir o histórico.
- **Arquivo errado guardado com o nome certo** é o defeito mais caro que existe aqui: renomear com
  prefixo `ERRADO — <o que é de verdade> — ` e deixar no lugar; nunca apagar em silêncio.
- Cache e índice que ficaram velhos (referência nova entrou, pasta mudou) são apagados ou
  regenerados; o relatório diz qual.
- Nome de arquivo com hash, "final2", "novo", "cópia" vira nome que diz o que é.

### 4 · Seiketsu — padronizar a cabeça da pasta

Cada pasta tocada recebe ou atualiza um `_LEIA-ME.md` (ou o índice que o destino usa) de **até 15
linhas**: o que está aqui, qual é a versão vigente, o que está superado e por quê, o que aguarda
decisão de quem, e onde mora o código ou a origem. A pasta se explica sozinha, sem o chat.

### 5 · Shitsuke — sustentar

- O relatório 5S vai para o registro da sessão (com a uma rotina de after-action, a linha **"5S:"** da seção
  datada): o que foi para onde, o que ficou e por quê.
- O que exigiria ferramenta nova, decisão de terceiro ou mais de uma sessão vira **pendência
  declarada**, com dono — não faxina silenciosa nem promessa.
- Regra que se repetiu duas vezes vira guard (hook), não lembrete.

## Saída

1. Relatório curto: inventário (contagens por classe), movimentos (origem → destino, um por linha),
   marcas aplicadas, quarentenas com motivo, pendências com dono.
2. `_LEIA-ME.md` em cada pasta tocada.
3. Com a uma rotina de after-action: a linha "5S:" no registro da sessão.

## Script

`python3 scripts/inventario_5s.py <pasta> [--md]` lista, sem escrever nada: arquivos sem
frontmatter, notas sem proveniência ou sem tag de eixo, famílias `_vN` com versão duplicada,
prefixos `ERRADO`, caches (`idx_cache*.json`, `*.tmp`, `~$*`), pastas sem cabeça (`_LEIA-ME.md`
ou `_<Nome>.md`), notas com hard wrap e stubs sem link recebido. É o passo 1; não decide nada.

## Perfil

`references/perfil-local.md` responde, para o **seu** sistema: qual é o destino canônico de cada
tipo de coisa, qual ontologia vale, como se escreve com segurança, como se move, o que é
proibido e o que já custou caro.

Ele não vem pronto — o `ADAPTAR.md` do plugin monta o seu em quinze minutos, a partir do que o
`scripts/detectar_ambiente.py` acha na sua máquina. **Sem perfil a skill funciona**, só fica mais
lenta: pergunta cada destino antes de mover.

## O que esta skill não faz

Não fecha issue, não decide destino de assunto em aberto, não apaga nada de humano, não reorganiza
taxonomia (isso é decisão do dono do vault), não substitui o lint do vault — ela o chama, quando
o perfil declara um.
