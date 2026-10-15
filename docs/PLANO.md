# Plano do projeto: adt-reader

## Objetivo

Ser o leitor aberto de referência para tabelas do Advantage Database Server (`.adt`/`.adm`). Deve ler todos os tipos de campo, rodar sem o servidor ADS e exportar para CSV, JSONL e Parquet.

## Por que agora

- A SAP parou de vender licenças novas do ADS em 31/08/2025 e não liberou o código-fonte.
- Os leitores abertos que existem são parciais. A gem Ruby `ruby-adt` é uma versão inicial, e o `node_adt` não lê Memo, Numeric, Money, Time, Binary e outros tipos.
- Não existe leitor em Python nem em Rust.

## Estado atual (v0.0.2)

- Header, descritores de coluna e registros decodificados
- Tabela oficial dos 29 códigos de tipo (documentação da API ACE)
- Verificados em arquivo real: character, cicharacter, integer, shortint, autoinc, double, date, logical
- Decodificados pela documentação, mas ainda sem amostra: time, timestamp, money, int64, nchar, guid…
- NULL de integer (INT32_MIN) e registros deletados (byte 0x05)
- CLI `adt info` / `adt export` (csv, jsonl, parquet)
- 5 testes passando contra as 3 amostras públicas conhecidas (ruby-adt e node_adt)

## Amostras públicas

Em outubro de 2026 só existiam 3 arquivos `.adt` públicos, todos já incluídos em `tests/fixtures`. Nenhum tem memo, money, timestamp ou Unicode. A Fase 1 continua sendo o gargalo.

Alternativas para conseguir amostras:
- Pedir à comunidade (fórum X#, Delphi-PRAXiS, grupos BR) tabelas sintéticas geradas com os tipos que faltam
- Abrir uma issue "sample wanted" no repositório público, com um script ACE pronto para quem tem ADS instalado gerar as tabelas

## Roadmap

### Fase 1: amostras (bloqueante)
- [ ] Conseguir um ambiente que gere `.adt`: Advantage Data Architect / Local Server, se ainda puder ser obtido legalmente, ou um sistema antigo com dados de teste
- [ ] Criar uma tabela por tipo de campo com valores conhecidos (mín., máx., NULL, vazio, acentos)
- [ ] Registrar as amostras em `samples/` com um `.json` do conteúdo esperado

### Fase 2: cobertura de tipos
- [ ] Descobrir os códigos de logical, numeric, money, varchar, raw, guid, rowversion, modtime e unicode
- [ ] Memo/BLOB: ler o arquivo `.adm` (tamanho de bloco, encadeamento)
- [ ] Prefixo de 5 bytes do registro: flag de deletado? bitmap de NULL?
- [ ] Encoding: ANSI vs OEM (cp1252 / cp850), detectar pelo header se possível

### Fase 3: robustez
- [ ] Fuzzing (arquivos truncados ou corrompidos não podem travar o leitor)
- [ ] Streaming para arquivos grandes
- [ ] Modo de recuperação (pular páginas ruins e reportar)

### Fase 4: lançamento
- [ ] Nome final e checagem de disponibilidade no PyPI
- [ ] Repositório no GitHub, CI, publicação no PyPI
- [ ] Divulgação: fórum X# (comunidade ADS), Delphi-PRAXiS, grupos brasileiros de Delphi
- [ ] Opcional: port em Rust e bindings para melhor desempenho

## Validação de demanda (em paralelo)

- [ ] Perguntar em grupos brasileiros de Delphi e automação comercial quem ainda roda ADS
- [ ] Levantar softwares conhecidos que usam ADS

## Regras do projeto

- Trabalhar só a partir de arquivos de dados. Nada de descompilar o ADS.
- Nunca commitar dados reais de clientes. Amostras são sempre sintéticas.
- Cada fato do formato vai para `docs/FORMAT.md` com status (confirmed / inferred / open).
