# Boas práticas nas automações

## Estrutura que se repete nos templates
**Gatilho → normalizar → buscar duplicado → criar ou atualizar → avisar/registrar.** Entender esse esqueleto ajuda a
adaptar qualquer template para outra ferramenta.

## Deduplicação
- Telefone: só dígitos, com DDI 55; busque pelos **últimos 8 dígitos** (resolve 9º dígito, DDD e +55 diferentes).
- E-mail: minúsculas e sem espaços antes de buscar.
- Achou contato com negócio aberto → atualize o negócio; sem negócio aberto → crie; não achou → crie contato e negócio.

## Conversões para anúncios (Meta CAPI, Google Ads)
- Normalize antes do hash: minúsculas, sem espaços e acentos no nome; telefone só dígitos com DDI.
- Hash **SHA-256** em e-mail, telefone, nome e sobrenome.
- Envie `fbc` quando houver `fbclid` (clique no anúncio); `fbp` ajuda na correspondência.
- Use `event_time` em segundos e `action_source` coerente (`website`, `system_generated`).
- Teste com o Test Event Code; tire-o em produção.
- Se o telefone não existir, **não** envie um telefone inventado: um valor fixo atrapalha a correspondência.

## Limites e lotes
- Use **Loop Over Items** com lotes pequenos e **Wait** entre eles quando a API tem limite.
- Fluxos destrutivos (apagar contatos): backup, teste com 2 a 3 registros, marcação do que já foi feito.

## Segurança e LGPD
- Chaves sempre em credenciais do n8n, nunca em texto dentro de nós, prints ou planilhas compartilhadas.
- Não grave CPF, endereço e telefone em planilhas abertas para muita gente.
- Ao exportar um fluxo para alguém, rode o sanitizador (`references/sanitizar.md`).

## Organização
- Dê nomes claros aos nós ("Busca contato no Kommo", não "HTTP Request27"); ao renomear, atualize as expressões
  `$('Nome do nó')`.
- Use notas (sticky notes) explicando cada bloco: é o que torna o template vendável e fácil de manter.
- Tenha um workflow de erro para avisar quando algo falha.
