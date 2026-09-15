# Adaptar ao seu sistema

> Este é o **segundo** arquivo de configuração. O `ONBOARDING.md` instala; este aqui ensina a
> skill onde ficam as coisas no **seu** sistema.

Os cinco S são universais: separar, guardar, limpar, padronizar, sustentar. O que não é universal
é **onde cada coisa vai parar**. Sem essa parte a skill continua funcionando — ela só pergunta o
destino de cada classe de item antes de mover, o que é seguro e cansativo.

Isto se faz **uma vez**, em quinze minutos.

## Como rodar

Peça ao Claude, dentro do seu projeto:

> "Leia o ADAPTAR.md do plugin kaizen-5s e monte meu perfil."

### 1 · Deixe a máquina falar primeiro

```bash
python3 skills/kaizen-5s/scripts/detectar_ambiente.py
```

Só leitura. Devolve seus repositórios git, vaults Obsidian, a configuração do Claude Code e as
ferramentas disponíveis — e termina com as oito perguntas que ele não tem como responder sozinho.

### 2 · Responda as oito

Elas viram a tabela de destinos do perfil: onde vai código, onde vai entregável, onde vai fonte,
onde vai nota. "Não tenho isso ainda" é resposta válida — a skill passa a perguntar só naquela
classe, em vez de em todas.

### 3 · O perfil é escrito

O Claude preenche `references/perfil-local.md` a partir do modelo. Leia antes de aceitar: cada
linha errada ali vira um arquivo no lugar errado depois, e arquivo no lugar errado com o nome
certo é o defeito mais caro que esta skill conhece.

### 4 · Teste onde não dói

Rode primeiro numa **pasta temporária de verdade**, nunca no vault, e leia o relatório antes de
deixar mover qualquer coisa:

```
/kaizen-5s ~/algum/rascunho
```

Confira três coisas:

- o que ela chamou de **descartável** é mesmo descartável? Olhe três itens com os próprios olhos.
  O número de descartáveis é **teto, não estimativa** — essa régua erra para mais, sempre.
- o que ela quer **mover** tem destino certo no perfil, ou ela está adivinhando?
- o que ela colocou em **quarentena** faz sentido? Quarentena é onde vai o que você não sabe se
  pode apagar, e o certo é que ela erre para esse lado.

Só depois disso aponte para um espaço que importa.

## O que adaptar além dos caminhos

**A marca de proveniência.** A fase 3 marca o que foi escrito por agente para você distinguir do
que é seu sem abrir histórico. O formato é do seu destino: uma propriedade no frontmatter, um
sufixo no nome, uma pasta separada. Escolha um e escreva no perfil — o importante é existir.

**A cabeça da pasta.** A fase 4 deixa um `_LEIA-ME.md` de até quinze linhas em cada pasta tocada.
Se o seu sistema já usa outro nome para isso (`README.md`, `index.md`, `000 MOC`), diga qual no
perfil e ela usa o seu.

**O que é proibido.** A seção mais importante do perfil. Tudo que a skill nunca deve tocar:
pastas de terceiros, acervo cuja função você não mediu, área sincronizada por um app que reclama
de escrita externa, qualquer coisa versionada por outra pessoa.

O que não se adapta: **nada de humano se apaga**. Arquivo criado por pessoa, ou de autoria
desconhecida, vai para quarentena com o motivo no relatório — nunca para a lixeira. Proveniência
preenchida por máquina não prova autoria: ela registra o último que escreveu.

## Quando refazer

Quando mudar a estrutura do seu sistema, ou quando notar a skill perguntando um destino que ela
já devia saber.

## Se você tem as duas skills

A `/desdobrar` e a `/kaizen-5s` usam o **mesmo perfil**. Responda uma vez e copie o
`perfil-local.md` para a outra — ou aponte as duas para um arquivo único fora das pastas dos
plugins, que é o que eu faço aqui: assim uma atualização nunca encosta nele.
