<!-- Para grupos brasileiros: Delphi (Telegram, Facebook), fóruns de automação comercial,
     LinkedIn. Ajuste o tom ao grupo. -->

**Alguém aqui ainda tem sistema rodando em Advantage Database Server (ADS)?**

A SAP parou de vender licenças novas do ADS em 31/08/2025, e quem tem dados em tabelas `.adt` vai precisar migrar mais cedo ou mais tarde.

Estou desenvolvendo um leitor open source (MIT) que lê arquivos `.adt` direto do disco, sem o servidor ADS e sem DLLs, e exporta para CSV, JSON ou Parquet:
https://github.com/JohnnyTrindade/adt-reader

Texto, inteiro, data, lógico e double já funcionam e foram testados. Para memo/blob (arquivo `.adm`), money, timestamp e campos Unicode **não existe nenhum arquivo de exemplo público**, e é aí que vocês podem ajudar.

Se você tem o ADS ou o Advantage Data Architect instalado, leva uns 10 minutos: é rodar um script SQL que cria tabelas pequenas com dados fictícios (uma por tipo de campo) e anexar o zip numa issue no GitHub. Passo a passo:
https://github.com/JohnnyTrindade/adt-reader/blob/main/samples/README.md

Também quero ouvir quem passou ou vai passar por migração de ADS: que sistemas usam, que tipos de campo aparecem, onde costuma doer.

Só dados fictícios, nunca dados de clientes. Valeu!
