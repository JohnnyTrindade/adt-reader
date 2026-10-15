# Changelog

## 0.0.2
- All 29 ACE field type codes mapped
- Verified: logical, shortint (new sample AbrGru.ADT from node_adt)
- Decoded per ACE docs (unverified): time, timestamp, modtime, money, int64, rowversion, curdouble, nchar, guid
- Integer NULL (INT32_MIN); deleted records skipped by default
- Synthetic sample generator (`tools/sample_spec.py`) and automatic sample tests

## 0.0.1
- Header, column descriptors and fixed-width records
- character, cicharacter, integer, autoinc, double, date
- CLI: `adt info`, `adt export` (csv, jsonl, parquet)
