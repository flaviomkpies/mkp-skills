# Onboarding — markitdown

## 1. Dependência principal

```
pip install markitdown
```

Isso já cobre PDF, Word, PowerPoint, Excel, HTML, CSV, JSON, XML, ZIP e EPUB.

## 2. Descrição de imagem por IA (opcional)

Só é necessário se você quiser que imagens virem texto descrito. A skill usa a **OpenRouter**,
compatível com a API da OpenAI:

1. Crie a chave em https://openrouter.ai/keys
2. Exporte no seu shell:

```
echo 'export OPENROUTER_API_KEY="sua-chave"' >> ~/.bashrc   # Linux
echo 'export OPENROUTER_API_KEY="sua-chave"' >> ~/.zshrc    # macOS
```

3. Confira: `echo $OPENROUTER_API_KEY`

Detalhe de modelos, custo e exemplos: `skills/markitdown/OPENROUTER_INTEGRATION.md`.

## 3. Transcrição de áudio (opcional)

Precisa de `ffmpeg` instalado (`apt install ffmpeg` ou `brew install ffmpeg`).
