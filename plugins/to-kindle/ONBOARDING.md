# Onboarding — to-kindle

## 1. Dependências

```
# Linux
sudo apt install pandoc && pip install pillow
# macOS
brew install pandoc && pip install pillow
```

A capa usa a fonte DejaVu Sans. Se não existir na sua máquina, aponte outra `.ttf` no topo de
`skills/to-kindle/scripts/docs_to_epub.py`.

## 2. Configurar o Send to Kindle (uma vez)

1. Amazon › **Gerenciar conteúdo e dispositivos** › **Preferências** › *Documentos pessoais*.
2. Anote o endereço `...@kindle.com` do seu aparelho.
3. Na mesma tela, adicione o **seu e-mail** à lista de remetentes aprovados — a Amazon recusa
   anexo de remetente que não esteja nela.

## 3. Uso

```
python3 skills/to-kindle/scripts/docs_to_epub.py cap1.md cap2.html --out livro.epub --title "Título"
```

Depois envie o `.epub` por e-mail para o endereço do passo 2. Limite da Amazon: 49 MB.

As flags `--send` e `--drive` dependiam de scripts da máquina de origem e não fazem nada aqui.
