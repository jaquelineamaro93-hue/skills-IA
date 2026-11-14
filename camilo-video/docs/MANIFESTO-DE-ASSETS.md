# Manifesto de assets — Camilo Ep. 1

Originais preservados (somente leitura) em `assets-originais/`. Nada foi sobrescrito; tudo o que foi derivado está em `public/`.

## Imagens (5 recebidas — o pedido menciona 7)
| Original | Resolução | MD5 | Conteúdo | Cenas | Derivados |
|---|---|---|---|---|---|
| imagens/1.webp | 941×1672 WebP | 8f528abf7bd1cb4c33c8c006a4b80a43 | Patas enrolando ataduras | 01 | public/images/cena1.webp, layers/cena1_fg.png, layers/cena1_bg.jpg |
| imagens/2.webp | 941×1672 WebP | 3bd473d9f9ecb9f13e2eaf61291bc56c | Guarda, sorriso, sol na janela, casas | 02, 07 | cena2.* |
| imagens/3.webp | 941×1672 WebP | 025f28ec5941d8475689814e054196bf | Soco no saco, contra-plongée | 06, thumbnail | cena3.* |
| imagens/4.webp | 941×1672 WebP | 576e3342becb0c6ebab13b0b04e4bfb8 | Close, suor, olhar determinado | 05 | cena4.* |
| imagens/5.webp | 941×1672 WebP | f407f9a034691e7569ad9832533773ed | Treino diante do espelho rachado, "Barrio San Javier, Medellín" | 03, 04 | cena5.* |

Sem duplicatas (hashes distintos). Personagem idêntico nas 5 (pelagem, listras, regata com a bandeira da Colômbia, short azul, ataduras vermelhas, tênis gastos).
Camadas: recorte do personagem com BiRefNet (`scripts/make_layers.py`) + fundo reconstruído por inpainting (usado desfocado, atrás do personagem).
**Faltam:** imagem de Camilo pulando corda (cena 03) e imagem de Camilo na porta da academia (cena 02). Não foram geradas novas imagens.

## Áudios (3 recebidos, ElevenLabs, MP3 44,1 kHz estéreo 128 kbps)
| Original | Duração | MD5 | Voz | Uso |
|---|---|---|---|---|
| audios/narrador_will.mp3 (Will – Deep, Smooth and Affectionate) | 25,34 s | b00002e66f36bf99d37451abc5e85518 | Narrador | N1–N7: todas as 7 frases usadas |
| audios/camilo_take_pt.mp3 (Jonas, take em português) | 15,99 s | e3b8d03dd1730afe44f9d87a8f12610a | Camilo | A1, A2, A4, A5, A6 usadas · "Ah não… De novo!" e "Mas um dia vai ser meu." não usadas |
| audios/camilo_take_es.mp3 (Jonas, take em espanhol) | 11,44 s | 798282bf0754dca0a1dbc607abf4fa20 | Camilo | B1, B2, B3, B5 usadas · "Yo sé que consigo." não usada |

Cortes exatos (entrada/saída em segundos no arquivo original) em `src/timeline.json` → `voiceClips`, definidos por detecção de silêncio + transcrição com marcação de palavras (faster-whisper). Nenhuma mudança de velocidade, tom ou timbre; apenas fade de 10 ms nas bordas e ganho.

## Trilha e efeitos (gerados pelo projeto, 100% originais)
- `public/music/trilha_original.wav` (regerável) — composição própria, sintetizada.
- `public/sfx/*.wav` — ataduras, madeira rangendo, respiração, passo, corda (whoosh e batida), tênis deslizando, soco no ar, impacto no couro, corrente, gongo distante.
- `public/mix/master.wav` — mix final −14 LUFS, pico real −1,5 dBTP.

## Fontes
Anton e Montserrat (SIL Open Font License), via pacotes @fontsource; licenças em `public/fonts/`.
