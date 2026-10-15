<!-- For the xsharp.eu forum: reply in the "Advantage Database Server (ADS) End of Life" thread,
     or as a new topic. Also suitable for en.delphipraxis.net (database section). -->

**Subject:** Open-source reader for ADT tables (no ADS engine needed) – looking for sample files

Hi all,

Following the ADS end-of-life discussion: I've started an open-source (MIT) Python library that reads `.adt` tables directly from disk, without the ADS engine or client DLLs, and exports them to CSV, JSON Lines or Parquet:

https://github.com/JohnnyTrindade/adt-reader

The goal is a dependable way to get data out of ADT tables for migrations. It works only from data files and the public ACE documentation; no SAP binaries are decompiled.

Character, integer, shortint, autoinc, double, date and logical are verified against real files. For memo/blob (`.adm`), money, timestamp, nchar and a few other types there are simply no public sample files.

If you have ADS or Advantage Data Architect installed, you could help a lot in about 10 minutes. There's a SQL script that creates a set of small synthetic tables (one per field type, with known values); you just run it in a free-table connection and attach the zip to a GitHub issue. Instructions:
https://github.com/JohnnyTrindade/adt-reader/blob/main/samples/README.md

Samples from different ADS versions and from OEM tables are especially welcome. Feedback on what you'd need from such a tool for your own migrations is very welcome too.

Thanks!
