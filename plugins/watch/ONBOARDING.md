# Onboarding — watch

## 1. Dependências

```
# Linux
sudo apt install ffmpeg && pip install yt-dlp
# macOS
brew install ffmpeg yt-dlp
```

## 2. Transcrição (opcional, mas quase sempre vale)

A skill tenta primeiro as **legendas nativas** do vídeo — para a maioria do YouTube isso basta e
não precisa de chave nenhuma. Quando não há legenda, ela cai no Whisper, que precisa de uma
chave:

```
export GROQ_API_KEY="..."      # https://console.groq.com/keys  (rápido e barato)
# ou
export OPENAI_API_KEY="..."    # https://platform.openai.com/api-keys
```

Sem chave e sem legenda, você ainda recebe os frames do vídeo — só não recebe o texto falado.

## 3. Vídeo privado ou com login

`yt-dlp` aceita cookies do seu browser:

```
yt-dlp --cookies-from-browser chrome <url>
```

## 4. Uso

```
/watch <url-ou-caminho> [pergunta]
```
