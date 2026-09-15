# Onboarding — kaizen-5s

## 1. Instalar

Só **Python 3**. O `scripts/inventario_5s.py` usa a biblioteca padrão.

## 2. O segundo arquivo: `ADAPTAR.md`

Os cinco S são universais. **Onde cada coisa vai parar, não.**

Antes do primeiro uso, peça ao Claude, dentro do seu projeto:

> "Leia o ADAPTAR.md do plugin kaizen-5s e monte meu perfil."

Ele roda `scripts/detectar_ambiente.py` (só leitura) na sua máquina, pergunta o que ela não
revela, e escreve `references/perfil-local.md` — a tabela de destinos, a marca de proveniência
que o seu sistema usa, como se escreve com segurança e, principalmente, **o que é proibido
tocar**.

Sem perfil a skill roda só o que é universal e pergunta cada destino antes de mover. É seguro, e
cansativo.

## 3. Primeiro uso: numa pasta que não dói

```
/kaizen-5s ~/algum/rascunho
```

Leia o relatório **antes** de deixar mover qualquer coisa. Confira em especial o que ela chamou
de descartável: olhe três itens com os próprios olhos. Essa régua erra para mais, sempre — o
número é teto, não estimativa.

Só depois aponte para um espaço que importa. E nunca comece pelo vault.

## 4. O passo 1 é só leitura

```
python3 skills/kaizen-5s/scripts/inventario_5s.py <pasta> [--md]
```

Lista o que está fora do padrão — nota sem frontmatter, versão `_vN` duplicada, cache velho,
pasta sem cabeça de leitura, arquivo com nome que não diz o que é. Não decide nada, não move
nada. Rode sozinho quando quiser só o diagnóstico.
