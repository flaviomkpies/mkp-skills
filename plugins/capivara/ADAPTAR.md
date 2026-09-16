# Adaptar ao seu sistema

> Este é o **segundo** arquivo de configuração. O `ONBOARDING.md` não tem nada a instalar; este
> aqui diz à skill **onde o relatório vai parar** no seu sistema.

O método é portátil: quatro frentes de busca, classificação de risco, fonte em cada afirmação.
O que não é portátil é o **destino**. A versão que eu uso salva numa pasta específica do meu
vault Obsidian, com um template e um frontmatter que são meus — se a skill tentasse isso na sua
máquina, escreveria num caminho que não existe.

Cinco minutos, uma vez.

## Como rodar

Peça ao Claude, dentro do seu projeto:

> "Leia o ADAPTAR.md do plugin capivara e monte meu perfil."

### 1 · Deixe a máquina falar primeiro

```bash
python3 skills/capivara/scripts/detectar_ambiente.py
```

Só leitura. Ele mostra se você tem vault Obsidian, onde ficam seus repositórios e pastas de
notas. Se você já tem um lugar onde guarda pessoas e empresas, ele aparece aqui.

### 2 · Responda três perguntas

1. **Onde mora o registro de uma pessoa ou empresa no seu sistema?** Uma pasta de notas, um CRM,
   uma pasta do projeto, ou nada ainda. "Nada ainda" é resposta válida e comum — nesse caso fica
   o padrão (`./capivara/<nome>-<data>.md`), que é um markdown na pasta em que você está.
2. **Como o arquivo se chama?** O padrão é `<nome>-<data>.md`. Se o seu sistema usa outra
   convenção (só o nome da pessoa, um identificador, uma pasta por entidade), diga qual.
3. **O que vai no cabeçalho?** Se o seu destino usa frontmatter com tags ou propriedades — e se
   há chaves que **outra ferramenta** já gerencia ali e a skill não pode tocar. Essa última é a
   mais importante: skill que sobrescreve campo de sincronização quebra o sistema de quem usa.

### 3 · O perfil é escrito

O Claude preenche `references/perfil-local.md`. Leia antes de aceitar — são poucas linhas.

## Sobre dado pessoal, antes de você usar isto para valer

Esta skill cria um dossiê sobre uma pessoa real, a partir de fontes públicas. Três coisas que não
são detalhe técnico:

- **Motivo de negócio declarado é obrigatório**, e não é burocracia: é o que separa due diligence
  de vigilância. Se você não consegue escrever o motivo numa linha, não rode.
- **Onde você salva importa.** Pasta compartilhada, vault sincronizado com um time, repositório
  público — pense nisso antes de escolher o destino, porque o arquivo contém dado de terceiro.
- **Documento de identidade não circula.** O perfil pode dizer para nem guardar CPF ou CNPJ no
  arquivo; é uma escolha defensável e a skill respeita.

Onde você mora pode ter regra sobre isso (no Brasil, a LGPD; na Europa, o GDPR). Não é conselho
jurídico — é um lembrete de que o arquivo tem dono e tem consequência.

## Quando refazer

Quando mudar onde guarda gente, ou quando notar a skill perguntando o destino que já devia saber.

## Se você tem as outras skills da casa

A `/desdobrar` e a `/kaizen-5s` usam um perfil com as mesmas perguntas, só que mais amplo. Se
você já montou um deles, aproveite a tabela de destinos — ou aponte todas para um arquivo único
fora das pastas dos plugins, que é o que eu faço aqui: assim uma atualização nunca encosta nele.
