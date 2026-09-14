#!/bin/bash
# workspace de origem — elegant-html-slides validate
# Purpose:     Checagem determinística de um deck Elegant/reMarkable (estrutura/tema/a11y) antes de entregar
# Owner:       O autor
# Created:     2026-06-19
# Last-edited: 2026-06-19 (CoS via fast-track)
# Issue:       fast-track
# Lifetime:    durable
# Inputs:      <deck.html>
# Outputs:     relatório stdout + exit 0 (PASS) / 1 (FAIL) / 2 (uso)
# Cron:        manual
set -u
F="${1:-}"
[ -f "$F" ] || { echo "uso: bash scripts/validate.sh <deck.html>"; exit 2; }
fail=0; warn=0
ok(){ printf '  \033[32mOK\033[0m   %s\n' "$1"; }
err(){ printf '  \033[31mFAIL\033[0m %s\n' "$1"; fail=$((fail+1)); }
wrn(){ printf '  \033[33mWARN\033[0m %s\n' "$1"; warn=$((warn+1)); }

echo "validate: $F"

# 1. palco fixo presente
grep -q 'width:[[:space:]]*1920px' "$F" && grep -q 'height:[[:space:]]*1080px' "$F" \
  && ok "palco 1920x1080 (viewport-base)" || err "viewport-base ausente (sem 1920x1080)"

# 2. nunca display:none num slide (regra do motor)
if grep -iE '\.slide[^{]*\{[^}]*display:[[:space:]]*none' "$F" >/dev/null; then
  err "slide usa display:none (use visibility/opacity)"; else ok "sem display:none em .slide"; fi

# 3. fontes web do tema, nunca system/sans genérica
if grep -iE "font-family:[^;}]*(Arial|Helvetica|Roboto)" "$F" >/dev/null; then
  wrn "sans genérica detectada (use Inter no corpo, Fraunces no título)"; else ok "sem sans genérica"; fi
grep -q 'fonts.googleapis.com' "$F" && ok "Google Fonts carregado" || wrn "sem <link> Google Fonts"
grep -qi 'Fraunces' "$F" && { grep -qi 'Inter' "$F" || grep -qi 'Hanken Grotesk' "$F" || grep -qi 'Literata' "$F"; } && ok "Fraunces (título) + corpo (Inter/Hanken/Literata) presentes" || wrn "faltam as fontes do tema (Fraunces título + Inter corpo)"

# 4. paleta do tema (papel/tinta grayscale) + accent único
grep -qiE '#F6F5F1|#FBFAF7|#1A1A1A|var\(--paper\)|var\(--ink\)' "$F" && ok "paleta papel/tinta presente" || wrn "tokens de papel/tinta não detectados"
# anti-slop: gradiente e box-shadow são PROIBIDOS no tema e-ink
grep -qiE 'box-shadow:[^;}]*[1-9]|linear-gradient|radial-gradient' "$F" && wrn "sombra/gradiente detectado — proibido no tema (profundidade = fio + espaço)" || ok "sem sombra/gradiente"

# 5. contagem de slides + rodapé por slide (fonte/atribuição)
slides=$(grep -ocE '<section[^>]*class="[^"]*slide' "$F")
echo "  ..   $slides slides"
foots=$(grep -ocE 'class="foot"' "$F")
[ "$foots" -ge $((slides-1)) ] && ok "rodapé/fonte em quase todo slide ($foots/$slides)" \
  || wrn "poucos rodapés ($foots/$slides) — slide com dado precisa de fonte"

# 6. reduced-motion + nav por teclado (acessibilidade básica)
grep -q 'prefers-reduced-motion' "$F" && ok "prefers-reduced-motion" || wrn "sem prefers-reduced-motion"
grep -qE "ArrowRight|keydown" "$F" && ok "navegação por teclado" || wrn "sem navegação por teclado"

# 7. armadilha do stroke-draw (sumiu no export-pdf) — alerta
if grep -q 'stroke-dashoffset' "$F"; then
  wrn "stroke-dashoffset presente — confirme que aparece no export-pdf (pode sumir no screenshot)"; fi

echo "----"
echo "resultado: $fail FAIL · $warn WARN"
[ "$fail" -eq 0 ] && { echo "PASS (estrutural). Rode o loop de auto-crítica visual antes de entregar."; exit 0; } || { echo "REPROVADO — corrija os FAIL."; exit 1; }
