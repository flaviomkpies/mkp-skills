---
name: desdobrar
description: "After-action review de uma sessão de trabalho: decide se houve aprendizado real, lê o que aconteceu em três camadas (rumo, método, caso concreto) e roteia cada aprendizado para o degrau mais barato que o sustenta. Tem gate de impacto — sessão sem aprendizado novo devolve 'nada a desdobrar'. Use para 'desdobra a sessão', 'after-action', 'o que aprendemos hoje'."
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

# /desdobrar — o que esta sessão ensinou, e onde isso passa a morar

Uma sessão de trabalho produz duas coisas: o resultado, e o que você aprendeu fazendo. O
resultado você já tem. O aprendizado evapora — a menos que alguém decida, na hora, onde ele
passa a morar.

Esta skill faz essa decisão. E faz uma segunda, mais importante: **decide se houve aprendizado**.
Nem toda sessão ensina alguma coisa, e um after-action que sempre encontra algo a registrar está
fabricando, não analisando.

> **Antes da primeira vez:** leia o `ADAPTAR.md` do plugin. Esta skill precisa saber onde ficam
> as coisas no **seu** sistema — sem isso ela pergunta o destino de cada item, toda vez.

## As fases, em ordem

| # | Fase | Sai dela |
|---|---|---|
| 1 | Gate de impacto | "nada a desdobrar", ou a lista de sinais |
| 2 | Leitura em três camadas | uma frase por camada |
| 3 | Via negativa | o que cada coisa nova substitui |
| 4 | Perguntas, uma por camada | no máximo 3 |
| 5 | Registro da sessão | seção datada, acrescentada nunca sobrescrita |
| 6 | Aplicar | edições, commit |
| 7 | Arrumar o ambiente | chama `/kaizen-5s` com o escopo da sessão |

## 1 · Gate de impacto

Pergunte **a si mesmo**, não ao usuário. A sessão teve ao menos um destes sinais?

- **Regra tocada** — algo que era inviolável mudou, nasceu ou caiu.
- **Correção do usuário que muda comportamento futuro** — não o conserto de um bug isolado.
- **Fluxo que se repetiu duas vezes ou mais** — candidato a virar procedimento.
- **Decisão de arquitetura** — caminhos, integrações, contratos entre partes.
- **Falha que revelou um buraco no processo** — não um bug, um buraco.
- **Entregável aprovado** com trabalho vinculado a fechar.

**Zero sinais → pare.** Responda apenas:

> "Sessão executiva, nada a desdobrar."

Sem perguntas, sem arquivos, sem commit. Esta é a resposta certa na maioria das sessões, e a
disciplina de dizê-la é o que faz as outras valerem alguma coisa.

## 2 · As três camadas, de cima para baixo

| Camada | Pergunta-guia | O que é |
|---|---|---|
| **Estratégica** | o que muda no **rumo**? | prioridades, o que começar ou parar, posicionamento |
| **Tática** | o que muda no **como trabalhamos**? | processo, regra, procedimento, arquitetura |
| **Operacional** | o que se faz diferente **amanhã, num caso concreto**? | um detalhe, um caminho, um jeito |

Três regras de leitura:

**Comece de cima.** "Qual foi A maior evolução desta sessão, em uma frase?" se responde primeiro
na estratégica, depois na tática. O operacional é o resto — nunca o começo.

**Camada vazia é normal.** Sessão puramente operacional gera só a seção operacional. Forçar uma
implicação estratégica que não existe é fabricação.

**O anti-padrão tem nome: desdobrar míope.** Vinte micro-aprendizados operacionais
hiperespecíficos e nenhuma leitura de rumo ou de método. O valor está nas camadas de cima; a
operacional existe para servir as outras duas.

### Filtro de ruído operacional

Um micro-aprendizado só se registra se passar em **pelo menos um**:

- **vai voltar** — o caso se repete;
- **compõe padrão** com outro anterior (candidato a virar regra);
- **custou caro** — retrabalho, ou uma correção do usuário.

Hiperespecífico de situação irrepetível: **não registre**. Um registro que ninguém vai reler é
custo, não memória.

## 3 · Via negativa, obrigatória

Antes de acrescentar qualquer regra em arquivo que é lido toda vez:

> **O que isso substitui? O que sai em troca?**

Sem resposta concreta, desça a escada — o aprendizado vira memória ou anotação pontual, não
regra. Com resposta, a edição é cirúrgica e **remove o substituído na mesma operação**.

Sistemas robustos definem-se pelo que removem. Um arquivo de regras que só cresce deixa de ser
lido, e regra que ninguém lê não governa nada.

## 4 · A escada de destinos — do mais barato ao mais caro

Cada aprendizado desce até o degrau **mais barato** que o sustenta. Subir um degrau sem
necessidade é custo permanente, pago em toda sessão futura.

| Degrau | Quando | Custo |
|---|---|---|
| **Memória do agente** | fato sobre você, sobre um projeto, uma preferência | quase zero, entra por relevância |
| **Hook** | precisa ser **garantido**, não lembrado | escreve uma vez, nunca mais depende de ninguém lembrar |
| **Regra com escopo de caminho** | só vale em certos arquivos | zero fora do escopo |
| **Procedimento (skill)** | vários passos, com ordem | carrega só quando chamado |
| **Documento de referência** | detalhe que se consulta | lido sob demanda |
| **Arquivo sempre carregado** | protocolo que vale em toda sessão | **caro: pago em todo turno** |

A pergunta que separa os dois últimos: *isto precisa estar na minha frente sempre, ou eu consigo
ir buscar quando o assunto aparecer?*

## 5 · Perguntas: uma por camada, no máximo três

Só pergunte da camada que tem material de verdade. Cada pergunta **se explica sozinha** — quem
responde pode estar no celular, sem a tabela acima na frente. Abra definindo a camada em uma
linha:

> **Camada tática — muda o como trabalhamos daqui para a frente:** aplicar [evolução] em
> [destino]? Segue o trecho exato que eu escreveria.

Traga o diff concreto de 3 a 5 linhas, não um inventário. Nunca faça uma pergunta por item, nem
uma pergunta estratégica fabricada numa sessão que não teve nenhuma.

## 6 · Registro da sessão

O perfil (`references/perfil-local.md`) diz onde. Duas regras que independem do lugar:

**Acrescentar, nunca sobrescrever.** Uma sessão longa tem vários assuntos; cada desdobramento
**adiciona** a sua seção datada. Sobrescrever apaga o histórico de quem passou antes.

**A síntese é sua, o log é da máquina.** O registro bruto (transcrição, arquivos) alguém ou algo
já guardou. O que esta fase escreve é a leitura: **o que mudou · estado final · como desfazer ·
o que ficou aberto**. Sem ela o histórico tem a conversa crua e nenhuma leitura, e ninguém relê
mil e seiscentos turnos.

## 7 · O ambiente fica arrumado

Última fase, e ela não é opcional: chame **`/kaizen-5s`** com o escopo da sessão. A sessão
termina com o ambiente organizado, não com o trabalho "feito" e o entulho onde caiu. É o mesmo
fundamento: a melhoria contínua começa pelo lugar de trabalho.

Se o `/kaizen-5s` não estiver instalado, faça o mínimo à mão: todo arquivo relevante que só
existe em pasta temporária é promovido ao destino definitivo **nesta sessão** — senão a próxima
execução usa a versão velha.

## Modo automático (sem ninguém para responder)

Rodando por agendamento, sem humano: registre as camadas **estratégica e tática** no registro da
sessão como *proposta*, aplique apenas o operacional que passou no filtro, e **não** mexa em
arquivo de regra nem feche trabalho. Decisão sem gente é rascunho.

## O que esta skill não faz

Não fecha tarefa por conta própria, não decide o rumo por você, não inventa implicação
estratégica onde não houve, e não registra aprendizado que ninguém vai reler.
