# Onboarding — show-me

## 1. Dependências

```
pip install pymupdf requests
pip install pytesseract pillow     # opcional: só para número dentro de figura
```

No Linux, o OCR também pede o binário: `sudo apt install tesseract-ocr`
(no macOS, `brew install tesseract`).

## 2. E-mail de contato (uma vez)

O Unpaywall e o OpenAlex são gratuitos e não usam chave de API — pedem só um e-mail de
contato, que é a etiqueta de polidez das duas. Sem ele as APIs recusam a consulta:

```
echo 'export SHOW_ME_EMAIL="voce@exemplo.com"' >> ~/.bashrc   # Linux
echo 'export SHOW_ME_EMAIL="voce@exemplo.com"' >> ~/.zshrc    # macOS
```

Ou passe `--email` em cada chamada.

## 3. Cache (opcional)

Os PDFs resolvidos ficam em `~/.cache/show-me/sources/`. Reexecução não rebaixa nada. Para
mudar o lugar: `export SHOW_ME_CACHE=/onde/voce/quiser`.

## 4. Teste em 30 segundos

```
python3 skills/show-me/scripts/fetch_pdf.py --doi 10.1038/s41586-021-03819-2
python3 skills/show-me/scripts/highlight.py ~/.cache/show-me/sources/*.pdf         --find "AlphaFold" --out prova.jpg
```

Deve imprimir o número da página e gerar `prova.jpg` com o termo destacado em amarelo.

## 5. O que esperar (e o que não)

- **Busca por título erra.** "Attention is all you need" devolve "Is Attention All You Need?",
  que é outro paper. O script avisa quando o título achado diverge; `--strict` faz ele parar.
  Confira a primeira página antes de usar qualquer PDF como prova.
- **Paywall sem via aberta não resolve.** É o esperado: marque a fonte como não localizável e
  registre o DOI. A skill nunca fabrica print nem URL.
- **Plataforma paga** (Gartner, Scopus, Web of Science) não recebe crawler — use o export
  nativo dela.
