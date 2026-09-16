# Onboarding — capivara

## 1. Instalar

Nada. A skill usa a busca web do próprio Claude.

## 2. O segundo arquivo: `ADAPTAR.md`

Este plugin tem **dois** arquivos de configuração, e o segundo é o que faz a skill servir para
você.

O método é portátil — quatro frentes de busca, classificação de risco, fonte em cada afirmação.
O **destino do relatório** não é: a versão que eu uso salva numa pasta do meu vault Obsidian,
com um frontmatter que é meu. Na sua máquina esse caminho não existe.

Antes do primeiro uso, peça ao Claude, dentro do seu projeto:

> "Leia o ADAPTAR.md do plugin capivara e monte meu perfil."

Três perguntas: onde mora o registro de uma pessoa no seu sistema, como o arquivo se chama, e o
que vai no cabeçalho — incluindo **quais chaves outra ferramenta já gerencia** e a skill não pode
tocar.

Cinco minutos. **Sem o perfil ela funciona**: grava um markdown em `./capivara/<nome>-<data>.md`
e avisa que está usando o padrão.

## 3. Antes de usar para valer

Esta skill monta um dossiê sobre uma pessoa real. O `ADAPTAR.md` tem uma seção sobre isso que
vale ler inteira; o essencial são três linhas:

- **Motivo de negócio declarado é obrigatório** — é o que separa due diligence de vigilância.
- **Onde você salva importa** — o arquivo tem dado de terceiro; pense antes de apontar para uma
  pasta compartilhada ou um repositório.
- **CPF e CNPJ nunca circulam** em mensagem, e-mail ou comentário compartilhado.

## 4. Uso

```
/capivara "Nome Completo" --contexto "avaliando aquisição"
```

Sem contexto declarado, ela pergunta antes de rodar.
