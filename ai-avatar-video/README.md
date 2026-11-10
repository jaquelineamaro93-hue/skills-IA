# AI Avatar Video — skill para Claude Code e Codex

Transforme roteiros em reels verticais e vídeos UGC de produto com o **seu avatar de IA falando com a sua própria voz clonada**:
rosto travado, 5 ângulos de câmera, cenário único, a sua voz original no seu ritmo e na boca do avatar,
cards de conversa/passos/frase, card final com o CTA e música baixa. Um MP4 pronto por roteiro.

## O que vem no pacote
| | |
|---|---|
| `SKILL.md` | O fluxo completo, com os pontos de aprovação (identidade, custo, teste) |
| `references/` | Ficha de personagem, UGC de produto (rótulo legível, cupom, #publi), prompt de vídeo com bloco de expressões, geradores e custos, voz (ElevenLabs), roteiro e ganchos, pós-produção, checklist de QA, lições de um projeto real, ética |
| `scripts/` | Transcrição local, sincronia de voz, suavização de pele, cards, card final, montagem, QA, diagnóstico |
| `examples/` | Perfil e notas para preencher, plano de montagem, cenas de cards, cores da marca |

### Diferenciais
- **Voz natural e na boca, com autocorreção:** a sua voz original, sem acelerar e frear do nada, sem palavra cortada, sem frase sobreposta e sem estalo. O script mede cada frase contra a boca, se corrige sozinho e entrega um relatório (testado num vídeo real: pior trecho a 0,09 s da boca).
- **Identidade fiel:** ficha de personagem só a partir de fotos reais, com checklist de aprovação (sobrancelha, óculos, acessórios, assimetrias).
- **Sem "cara de velha":** bloco de expressões jovens no prompt e suavização de pele opcional que não mexe em traços.
- **O CTA nunca some:** montagem que não corta a voz, card final com a voz original e conferência automática do fim.
- **Sem surpresa na conta:** a skill mostra o custo e espera o seu "ok" antes de cada geração paga.
- Transcrição 100% local (Whisper): suas gravações não vão para nenhuma API de transcrição.

## Testado de ponta a ponta
Num vídeo real de 30 s (avatar gerado no Seedance 2.5 + voz da ElevenLabs): sincronia, cards, card final, música e
conferência final rodando só com os scripts do pacote. Cada defeito encontrado nos testes virou regra e está
documentado em `references/licoes-aprendidas.md`.

## Antes de começar: checklist
Marque tudo antes de rodar a skill. Contas e créditos de terceiros são pagos à parte, direto com cada fornecedor.

### Contas
- [ ] **Claude Code** (app desktop, terminal ou claude.ai/code) — ou **Codex**. Precisa poder rodar comandos no computador.
- [ ] **ElevenLabs** com plano que permita **clonar voz** (clonagem instantânea). A voz é sua ou de quem autorizou por escrito.
- [ ] **Gerador de vídeo com referência de imagem + áudio**, com créditos. Escolha um:
  - [ ] **Artlist** com assinatura que inclua créditos de IA (o teste grátis não libera o Seedance 2.5). Conecte no Claude:
        Configurações → Conectores → Adicionar conector personalizado → `https://mcp.artlist.io/mcp`.
  - [ ] **Manus** (Video Editor), se preferir gerar lá e trazer o MP4.
  - [ ] **OpenRouter** (ou outro provedor) com chave de API para Kling/Veo/Seedance R2V.
- [ ] (Opcional) Imagem: ChatGPT, Gemini ou o próprio Artlist, para a ficha de personagem e a imagem-base.

### Programas no computador
- [ ] **Python 3.10+**
- [ ] **ffmpeg** — `brew install ffmpeg` (Mac) · `sudo apt install ffmpeg` (Linux) · `winget install ffmpeg` (Windows)
- [ ] **Rubber Band** (linha de comando) — `brew install rubberband` · `sudo apt install rubberband-cli`
- [ ] **Fontes Noto** (opcional; sem elas a skill usa uma fonte reserva) — `sudo apt install fonts-noto-core`
- [ ] **Pacotes Python** — `pip install -r ai-avatar-video/requirements.txt`
- [ ] **~2 GB livres** (modelo de transcrição de ~460 MB, baixado uma vez, e os vídeos de trabalho)
- [ ] Rodar `python3 ai-avatar-video/scripts/check_env.py --download-model` e ver **READY**

### Materiais da pessoa
- [ ] **4 a 10 fotos reais** e recentes do rosto: frente, 3/4 dos dois lados, perfil, sorrindo e séria, luz natural, sem filtro
- [ ] **1 vídeo real de 8 a 15 s** falando para a câmera (para gestos e jeito de falar)
- [ ] **Roupa e cenário** escolhidos (foto ou descrição); o cenário de preferência numa foto vertical 9:16
- [ ] **Roteiros** de 30 a 60 s, com gancho no início e CTA no fim
- [ ] **Um áudio da ElevenLabs por roteiro**, com o número no nome (`R01.mp3`, `R02.mp3`…)
- [ ] **Marca:** URL, CTA padrão, cores (opcional) e uma **música** com licença de uso (ex.: catálogo da Artlist)
- [ ] **Autorização por escrito** se o rosto ou a voz não forem seus; autorização para mostrar prints de conversas reais

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
Versão no `CHANGELOG.md`. Dúvidas e atualizações:
[LinkedIn](https://www.linkedin.com/in/jaquelineamaro/) · [Instagram @jaquedocrm1112](https://www.instagram.com/jaquedocrm1112/).

## Quem criou
**Jaqueline Amaro** — especialista em CRM, CX e IA, criadora da [SOMA Mentoria](https://www.somamentoria.com) e da
[Conexão CRM](https://www.conexaocrm.com) (CRM Academy + Mulheres de CRM). Esta skill nasceu da produção dos vídeos
dela com o próprio avatar e a própria voz: cada regra veio de um erro real, corrigido e testado.

## Licença
Uso conforme `LICENSE.md`. É proibido revender ou redistribuir o pacote.
