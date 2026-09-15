# Onboarding — desdobrar

## 1. Instalar

Nada além de **Python 3**, que você já tem. A skill é método, não ferramenta.

## 2. O segundo arquivo: `ADAPTAR.md`

Este plugin tem **dois** arquivos de configuração, e o segundo é o que importa.

O `SKILL.md` carrega o método — gate de impacto, três camadas, via negativa, a escada de
destinos. Isso é transferível e vale como está. O que não é transferível são os **destinos**:
onde, no seu sistema, mora o registro de uma sessão, uma regra que vale para sempre, um
aprendizado pontual.

Antes do primeiro uso, peça ao Claude, dentro do seu projeto:

> "Leia o ADAPTAR.md do plugin desdobrar e monte meu perfil."

Ele roda `scripts/detectar_ambiente.py` (só leitura) na **sua** máquina, olha o que você de fato
tem — repositórios, vault, sua configuração do Claude Code, ferramentas no PATH — faz as poucas
perguntas que um diretório não responde, e escreve `references/perfil-local.md`.

Quinze minutos, uma vez. Sem isso a skill funciona, mas pergunta o destino de cada coisa toda vez.

## 3. Primeiro uso

Rode no fim de uma sessão **sem** grande aprendizado. A resposta certa é
*"Sessão executiva, nada a desdobrar"* — o gate existe para dizer não, e essa é a resposta na
maioria das sessões. Se ela achar três coisas para registrar numa sessão trivial, aperte os
sinais do gate no perfil.

## 4. Companheira

A última fase chama a `/kaizen-5s`, que arruma o ambiente. As duas usam o mesmo perfil. Se você
não tiver a outra instalada, a fase vira um lembrete manual — nada quebra.
