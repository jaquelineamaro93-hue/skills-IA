# AI Avatar Video — skill para Claude Code e Codex

Transforme roteiros em reels verticais com o **seu avatar de IA falando com a sua própria voz clonada**:
rosto travado, 5 ângulos de câmera, cenário único, voz original sincronizada à boca palavra por palavra,
cards de conversa/passos/frase, card final com o CTA e música baixa. Um MP4 pronto por roteiro.

## O que vem no pacote
| | |
|---|---|
| `SKILL.md` | O fluxo completo, com os pontos de aprovação (identidade, custo, teste) |
| `references/` | Ficha de personagem, prompt de vídeo com bloco de expressões, geradores e custos, voz (ElevenLabs), roteiro e ganchos, pós-produção, checklist de QA, lições de um projeto real, ética |
| `scripts/` | Transcrição local, sincronia de voz, suavização de pele, cards, card final, montagem, QA, diagnóstico |
| `examples/` | Perfil e notas para preencher, plano de montagem, cenas de cards, cores da marca |

### Diferenciais
- **Sincronia de voz medida:** 0,06 s de diferença média entre voz e boca num vídeo real (90% das palavras abaixo de 0,1 s), sem estalos nas emendas.
- **Identidade fiel:** ficha de personagem só a partir de fotos reais, com checklist de aprovação (sobrancelha, óculos, acessórios, assimetrias).
- **Sem "cara de velha":** bloco de expressões jovens no prompt e suavização de pele opcional que não mexe em traços.
- **O CTA nunca some:** montagem que não corta a voz, card final com a voz original e conferência automática do fim.
- **Sem surpresa na conta:** a skill mostra o custo e espera o seu "ok" antes de cada geração paga.
- Transcrição 100% local (Whisper): suas gravações não vão para nenhuma API de transcrição.

## Requisitos
- Claude Code (ou Codex) com acesso a terminal.
- `ffmpeg`, `rubberband` (CLI), Python 3.10+.
- Conta num gerador de vídeo com referência de imagem + áudio (testado com Seedance 2.5 via Artlist ou Manus; Kling/Veo via API também servem). **Os créditos do gerador e da ElevenLabs são pagos à parte.**
- Voz clonada na ElevenLabs (ou outra) — da própria pessoa ou autorizada.

## Instalação
```bash
# Claude Code (pessoal, todos os projetos)
cp -r ai-avatar-video ~/.claude/skills/
# ou só num projeto
cp -r ai-avatar-video <seu-projeto>/.claude/skills/
# Codex
cp -r ai-avatar-video <seu-projeto>/.agents/skills/

# dependências
sudo apt install ffmpeg rubberband-cli fonts-noto-core     # macOS: brew install ffmpeg rubberband
pip install -r ai-avatar-video/requirements.txt
python3 ai-avatar-video/scripts/check_env.py --download-model
```
Gerar pelo Claude com o Artlist: Configurações → Conectores → Adicionar conector personalizado → `https://mcp.artlist.io/mcp`.

## Primeiro uso
Abra o Claude Code na pasta do seu projeto e diga, por exemplo:
> "Quero criar meu avatar de IA. Aqui estão minhas fotos, um vídeo meu falando e o áudio do roteiro 1."

A skill cria o seu `PERFIL.md`, gera a ficha do personagem para você aprovar, monta o prompt, mostra o custo,
gera um vídeo de teste e, aprovado, entrega o MP4 final.

## Suporte e atualizações
Versão no `CHANGELOG.md`. Dúvidas e atualizações: <seu canal de suporte>.

## Licença
Uso conforme `LICENSE.md`. É proibido revender ou redistribuir o pacote.
