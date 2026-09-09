---
name: to-kindle
description: Junta documentos (markdown ou HTML, inclusive HTML com imagens embutidas) num único e-book EPUB com capa e sumário, um capítulo por arquivo, pronto para o Kindle. Use quando o usuário disser "manda para o Kindle", "vira e-book", "to-epub". Para PDF, converta antes para HTML ou markdown.
---

# /to-kindle

Junta um ou mais arquivos `.md` ou `.html`, na ordem dada, num EPUB com capa, sumário e um capítulo por arquivo.

## Uso

```bash
python3 scripts/docs_to_epub.py <arq1.md> <arq2.html> ... --out <saida.epub> --title "Título" [--subtitle "..."] [--author "..."]
```

- Cada arquivo vira um capítulo; o título do capítulo é o primeiro `h1`, ou o nome do arquivo.
- Imagens em base64 dentro do HTML são extraídas para JPEG.
- Requisitos: Python 3, `pandoc` e `Pillow` (`pip install pillow`). A capa usa a fonte DejaVu; sem ela, troque o caminho no script.
- Limite do Send to Kindle: 49 MB.

## Envio ao Kindle

Envie o `.epub` por e-mail para o seu endereço Send to Kindle (Amazon › Gerenciar conteúdo e dispositivos › Preferências), a partir de um remetente aprovado na sua lista. As flags `--send` e `--drive` do script dependem de scripts da máquina de origem; ignore-as.
