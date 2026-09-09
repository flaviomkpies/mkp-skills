# CHARTS.md — Data-viz reThink / reMarkable

> Gráficos em **SVG puro** (sem lib). Autorar no palco 1920×1080. **Monocromático: cinza + 1 destaque em tinta (preto sólido)**, **fonte sempre no rodapé**. Valores em **Inter**; título do gráfico em Fraunces se houver.
> Regra: **cascata/waterfall > pizza**. Nunca pizza para parte-do-todo se uma barra comunica melhor.
> Sem cor (a única cor do tema é link). Sem gradiente/sombra/3D no dado; hierarquia = peso de fio + 1 destaque em tinta.

## Princípios
- **Dado → geometria** é responsabilidade do gerador: calcular alturas/posições a partir dos números reais antes de escrever o SVG (não chutar pixels).
- **Eixo só quando agrega.** Preferir rotular o valor direto na barra/ponto a desenhar grade pesada.
- **1 mensagem por gráfico** = o action-title. O gráfico prova o título, não o substitui.
- **Kicker/tracker obrigatório:** todo gráfico de análise leva **1 anotação** (fio fino + rótulo em tinta) marcando a leitura — o "olhe aqui" (ex.: seta + "+26%" no ponto-chave). Sem kicker, o leitor garimpa; com kicker, vê o so-what em 1s.
- **Cor:** quase tudo em **cinza** (`--g2`/`--g1`); **uma** série/barra/ponto-chave em **`--ink`** (preto sólido) para fixar o olho. Δ pode usar glifo ▲/▼ (peso, não cor). Imprime em P&B sem perder nada — nunca dependa de cor.
- **Fonte obrigatória** no rodapé (`.foot`). Dado ilustrativo → marcar "ilustrativo".
- **Fronteira no rodapé:** gráfico que ranqueia/decompõe declara o que **ficou de fora** e por quê ("não inclui D&A/CAPEX — abaixo do EBITDA"). Corte silencioso lê-se como "cobri tudo" quando não cobriu.

## Mapa de escala (helper mental)
`y(v) = base_y - v * (base_y - top_y) / v_max`. Largura de barra ~120–160px; gap ≥ largura/2.

## Receitas

### Waterfall / cascata (parte→todo, value-bridge)
Barras flutuantes: cada incremento começa onde o anterior terminou; conectores tracejados ligam os topos. Base e Total ancorados no eixo; incrementos flutuam. Ver bloco pronto em `snippets.html §7`.
Cores: base/total = `--g1` (âncora); incrementos = `--g2`; passo-chave = `--ink`. Conectores tracejados em `--hair-strong`.

### Barras (comparação)
Vertical para poucas categorias, horizontal para rótulos longos. Valor no topo/fim da barra (**Fraunces**). Destacar 1 barra em `--ink`, resto em `--g2`.

### Tornado / butterfly (sensibilidade)
Barras horizontais **divergentes da linha-base**, uma variável por linha, **ranqueadas por |impacto|** (maior no topo). Cada barra: lado esquerdo = downside (vinho), direito = upside (verde/sage), partindo de uma **baseline vertical** (o valor-base, rotulado). Rótulo de |impacto| (ex.: "±R$2,0M") na ponta. Eixo só com poucos ticks. Capta a **assimetria** (ex.: preço move mais que volume) — é o ponto. Rodapé: choque aplicado + "ceteris paribus" + fonte (modelo/aba). Ver caso `20260619_Sensibilidade_Tornado_EBITDA`.

### Linha (tendência)
`<polyline>` stroke `--ink` 3px + pontos nos vértices. Último ponto rotulado. Área sob a linha com fill `--ink` a ~8% (ou hachura no e-ink) para volume.

### KPI / stat-callout
Numeral grande em **Fraunces** (peso 300, 96–140px) + legenda **JetBrains Mono** caixa-alta + Δ opcional (glifo ▲/▼, por peso não por cor). Arquétipo H do `LAYOUTS.md`.

### Marimekko / 100% empilhado
Só quando precisa de 2 dimensões (share × tamanho). Senão, barras simples.

## Anti-padrões
- ❌ Pizza (use cascata/barra). ❌ Gráfico sem fonte. ❌ Grade/eixo pesado competindo com o dado.
- ❌ 3D, sombra, gradiente no dado (decoração ≠ dado). ❌ Mais de uma mensagem por gráfico.
