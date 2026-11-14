# Camilo | Episódio 1: O Tamanho do Sonho

Produção em **Remotion + React + TypeScript + FFmpeg** (com Python para camadas e áudio). Projeto independente.

## Entregáveis (`output/`)
- `camilo-ep01-o-tamanho-do-sonho-1080x1920.mp4` — episódio vertical final (60,5 s, 30 fps, H.264/AAC)
- `camilo-ep01-legendas-pt-BR.srt` — legendas em português (espanhol traduzido)
- `camilo-ep01-falas-originais.srt` — transcrição literal das falas gravadas (com o espanhol)
- `camilo-ep01-thumbnail-1080x1920.png` — thumbnail vertical
- `docs/` — roteiro técnico com tempos reais, manifesto de assets, relatório de validação e limitações

## Como reproduzir
```bash
npm install
pip install "rembg[cpu]" opencv-python-headless scipy numpy faster-whisper
python3 scripts/make_layers.py        # camadas do personagem (originais intocados)
python3 scripts/build_audio.py        # recortes das vozes, trilha original, SFX e mix master
python3 scripts/make_srt.py           # legendas SRT
npx tsc --noEmit                      # verificação de tipos
npm run render -- --browser-executable=<caminho do Chrome headless>
npm run thumb  -- --browser-executable=<caminho do Chrome headless>
npm run studio                        # edição visual
```
Tudo é guiado por `src/timeline.json`: mude um tempo ali e áudio, imagem e legenda acompanham.

## Estrutura
```
src/scenes/        S1Ataduras … S7Sonho (uma cena por arquivo)
src/components/    LayeredShot (câmera + parallax + deformações locais), Atmosphere (luz, poeira, flare,
                   granulação), Effects (impacto, clarão, corda, suor, brilho nos olhos), Subtitles, EndCard
src/compositions/  Episode (montagem e transições), Thumbnail
src/animation/     keyframes, easing, câmera na mão, tremor
public/            images, layers, voices, music, sfx, mix, fonts
assets-originais/  cópias somente leitura dos arquivos recebidos
```
