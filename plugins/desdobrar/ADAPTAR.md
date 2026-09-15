# Adaptar ao seu sistema

> Este é o **segundo** arquivo de configuração. O `ONBOARDING.md` instala; este aqui ensina a
> skill a trabalhar no **seu** sistema, não no meu.

A `/desdobrar` carrega um método — gate de impacto, três camadas, via negativa, a escada de
destinos. O método é meu e é o que vale a pena copiar. **Os destinos são seus**: onde mora o
registro de uma sessão, onde mora uma regra, onde mora um aprendizado pontual. Sem essa parte, a
skill pergunta o destino de cada coisa, toda vez, e vira fricção em vez de alívio.

Isto se faz **uma vez**, em quinze minutos, com o Claude na sua máquina.

## Como rodar

Peça ao Claude, dentro do seu projeto:

> "Leia o ADAPTAR.md do plugin desdobrar e monte meu perfil."

Ele vai executar os quatro passos abaixo. Você só responde perguntas.

### 1 · Deixe a máquina falar primeiro

```bash
python3 skills/desdobrar/scripts/detectar_ambiente.py
```

Só leitura: nada é movido, nada é escrito. Ele devolve o que achou — repositórios git, vaults
Obsidian, sua configuração do Claude Code (CLAUDE.md, skills, hooks já instalados), ferramentas
no PATH — e termina com as oito perguntas que a máquina **não** tem como responder.

Passe uma pasta se o seu trabalho não mora no HOME: `detectar_ambiente.py ~/work`.

### 2 · Responda o que ele não descobriu

As oito perguntas do fim do relatório. Elas existem porque um diretório não revela intenção: dá
para ver que você tem um vault, não dá para ver se o registro de uma sessão vai nele, numa issue,
ou em lugar nenhum ainda.

Responda em uma linha cada. "Não tenho isso ainda" é resposta válida e das mais úteis — significa
que o degrau está livre, e a skill vai propor o mais barato que sirva.

### 3 · O perfil é escrito

O Claude preenche `references/perfil-local.md` a partir do modelo, com as suas respostas e o que
a detecção achou. Leia antes de aceitar: é um arquivo curto, e cada linha errada ali vira um
arquivo no lugar errado depois.

**O perfil é seu.** Ele fica na sua cópia do plugin e não volta para mim. Uma atualização do
plugin não o sobrescreve — mas guarde uma cópia fora da pasta do plugin se quiser dormir
tranquilo.

### 4 · Teste antes de confiar

Rode `/desdobrar` no fim de uma sessão real, de preferência uma **sem** grande aprendizado. A
resposta certa é *"Sessão executiva, nada a desdobrar"*. Se ela encontrar três coisas para
registrar numa sessão trivial, o gate está frouxo: aperte os sinais no perfil.

Depois rode numa sessão que ensinou algo de verdade e confira dois pontos:

- o que ela classificou como **estratégico** é mesmo sobre rumo, ou é método disfarçado?
- o que ela quer gravar em arquivo sempre-carregado cabe num degrau mais barato?

## Como adaptar o método, e não só os caminhos

O perfil cobre onde as coisas moram. Duas partes do método também podem mudar, e mudá-las é
legítimo:

**Os sinais do gate.** Os seis que vêm no padrão são os que importam no meu trabalho. Se você
programa o dia inteiro, "regressão que os testes não pegaram" provavelmente vale mais que
"correção do usuário". Troque, mas **mantenha o gate apertado**: o valor dele está em dizer não.

**As três camadas.** Rumo, método e caso concreto servem a quase todo trabalho intelectual. Se o
seu tem uma quarta dimensão que não cabe em nenhuma (risco regulatório, custo, segurança),
acrescente uma linha — e aceite que a maioria das sessões vai deixá-la vazia.

O que não se adapta: **começar de baixo**. Listar oito detalhes operacionais e chamar isso de
after-action é o anti-padrão que esta skill existe para evitar, em qualquer sistema.

## Quando refazer

Quando você mudar de sistema (trocou de gerenciador de tarefas, mudou o vault de lugar), ou
quando notar a skill perguntando o destino de algo que já devia saber. Refazer é rodar o passo 1
de novo — leva menos que a primeira vez.

## Se você tem as duas skills

A `/desdobrar` e a `/kaizen-5s` usam o **mesmo perfil**. Responda uma vez e copie o
`perfil-local.md` para a outra — ou aponte as duas para um arquivo único fora das pastas dos
plugins, que é o que eu faço aqui: assim uma atualização nunca encosta nele.
