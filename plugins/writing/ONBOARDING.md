# Onboarding — writing

Não precisa de serviço externo. Precisa de **uma configuração única**: o seu DNA de escrita.

## 1. Criar o DNA (obrigatório na primeira vez)

A skill nasce com `DNA.md` e `CORRECOES.md` vazios de propósito — a voz é sua, não vem
embutida. Sem eles a skill escreve em voz neutra, o que quase nunca é o que você quer.

```
/writing dna
```

Tenha à mão **3 a 5 textos seus já publicados** (post, artigo, e-mail longo). Cole ou aponte os
arquivos quando a skill pedir. Ela extrai: padrão de abertura, cadência de frase, vocabulário
recorrente, tipo de fechamento e as suas proibições.

## 2. Guardar seus exemplos

Ponha em `skills/writing/references/examples/` os seus textos publicados (arquivo ou link) e
anote numa linha o que cada um demonstra. A skill lê 2 a 3 antes de escrever prosa. Limite útil:
~12 por canal — mais que isso dilui a voz.

## 3. Gate determinístico (opcional, recomendado)

`scripts/tells_pt.py` conta tells de texto gerado (fragmento, "não é X, é Y", aforismo,
travessão) e sai com erro acima do teto. Só precisa de Python 3:

```
python3 skills/writing/scripts/tells_pt.py seu-texto.md
```

## O que não vem junto

Publicação automática (newsletter, LinkedIn), envio ao leitor e integração com ferramenta de
issues dependiam da máquina de origem e foram removidos. Publique pelo site do seu canal,
colando o texto final.
