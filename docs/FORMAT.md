# ADT table format notes

Working notes on the Advantage Database Server table format (`.adt`). Every item below is tagged:

- **confirmed**: verified against the sample files with a check that would fail if wrong
- **inferred**: consistent with the samples but not independently verified
- **open**: not yet understood

All integers are little-endian.

## File layout

```
+---------------------+  offset 0
| header (400 bytes)  |
+---------------------+  offset 400
| column descriptors  |  column_count x 200 bytes
+---------------------+  offset data_offset
| records             |  record_count x record_length
+---------------------+
```

## Header (400 bytes)

| Offset | Size | Meaning | Status |
|---:|---:|---|---|
| 0 | 16 | `"Advantage Table\0"` signature | confirmed |
| 20 | 4 | always `1` in samples | open |
| 24 | 4 | record count | confirmed |
| 28 | 4 | ? (zero in samples) | open |
| 32 | 4 | data offset (= 400 + 200 × columns) | confirmed |
| 36 | 4 | record length in bytes | confirmed |
| 80 | 4 | `3` in one sample, `0` in the other | open |
| 88 | 4 | `18` in one sample, `0` in the other | open |
| 356 | 2 | always `4` in samples (format version?) | open |
| 358 | 2 | column count | confirmed |

## Column descriptor (200 bytes)

| Offset | Size | Meaning | Status |
|---:|---:|---|---|
| 0 | 129 | column name, NUL-padded (max 128 chars) | confirmed |
| 129 | 2 | type code | confirmed |
| 131 | 4 | byte offset of the field inside the record | confirmed |
| 135 | 2 | field length in bytes | confirmed |
| 137 | 63 | ? (zeros in samples except one column) | open |

Field offsets start at 5, which matches the 5-byte record prefix below.

## Record

| Offset | Size | Meaning | Status |
|---:|---:|---|---|
| 0 | 5 | prefix, `04 00 00 00 00` in every sample | open (status/deleted flag? NULL bitmap?) |
| 5 | … | fields packed back to back, no separators | confirmed |

`record_length == 5 + sum(field lengths)` holds for both samples.

## Type codes

The codes and short descriptions come from the public ACE API documentation ([AdsFieldType enumeration](https://www.xsharp.eu/runtimehelp/html/T_XSharp_ADS_AdsFieldType.htm)). The "Status" column says whether a code has been seen and checked in a real `.adt` file.

| Code | Type | Storage (per ACE docs) | Status in files |
|---:|---|---|---|
| 1 | logical | 1 byte; `T`/`F` seen | confirmed (AbrGru.ADT) |
| 2 | numeric | DBF-style text number | not seen |
| 3 | date | int32 Julian Day Number | confirmed (period 2008-07-01 → 2009-06-30 matches a `NoOfDays = 365` field) |
| 4 | character | fixed-width text, space-padded | confirmed |
| 5 | memo | pointer into `.adm` | not seen |
| 6 | binary | pointer into `.adm` | not seen |
| 7 | image | pointer into `.adm` | not seen |
| 8 | varchar | variable-length text | not seen |
| 9 | compactdate | 3-byte date (DBF) | not seen |
| 10 | double | IEEE 754 float64 | confirmed |
| 11 | integer | int32 | confirmed |
| 12 | shortint | int16 | confirmed (AbrGru.ADT) |
| 13 | time | int32 ms since midnight | not seen |
| 14 | timestamp | int32 JDN + int32 ms since midnight | not seen |
| 15 | autoinc | uint32 | confirmed |
| 16 | raw | untranslated bytes | not seen |
| 17 | curdouble | float64 currency | not seen |
| 18 | money | int64, 4 implied decimals | not seen |
| 19 | int64 | int64 | not seen |
| 20 | cicharacter | fixed-width text, case-insensitive | confirmed |
| 21 | rowversion | int64, incremented on every update | not seen |
| 22 | modtime | 8-byte timestamp, set on update | not seen |
| 23 | varchar_fox | Visual FoxPro varchar | not seen |
| 24 | varbinary_fox | Visual FoxPro varbinary | not seen |
| 25 | system_field | internal | not seen |
| 26 | nchar | UTF-16 text, padded | not seen |
| 27 | nvarchar | unpadded UTF-16 text | not seen |
| 28 | nmemo | variable-length Unicode (memo) | not seen |
| 29 | guid | 16 bytes | not seen (byte order inferred) |

## NULL handling

| Type | NULL representation | Status |
|---|---|---|
| integer | `0x80000000` (INT32_MIN) | confirmed (AbrGru.ADT; also used by node_adt) |
| character / date / logical | all bytes zero | inferred |
| logical | `0x20` (space) seen once; treated as NULL | open |
| timestamp | JDN 0 and ms −1 (per node_adt) | inferred |

Whether a NULL bitmap exists in the record prefix is **open**.

## Deleted records

node_adt treats a record whose first prefix byte is `0x05` as deleted (**inferred**; no deleted record in our samples yet). Live records start with `0x04`.

## Not covered yet

- Memo/BLOB fields, which live in a companion `.adm` file
- Deleted records
- Encrypted tables
- Indexes (`.adi`), which a reader does not need
- Data dictionaries (`.add`)

## Sources

- Sample files and initial notes from [ruby-adt](https://github.com/chasemgray/ruby-adt) (MIT)
- Sample file `AbrGru.ADT` and NULL and deleted-record hints from [node_adt](https://github.com/albertzak/node_adt) (MIT)
- Type codes from the ACE API docs ([X# runtime help](https://www.xsharp.eu/runtimehelp/html/T_XSharp_ADS_AdsFieldType.htm))
- Our own byte-level analysis of those samples

## Known public samples (all already in tests/fixtures)

| File | Source | Records | Types covered |
|---|---|---:|---|
| test.adt | ruby-adt | 1 | integer, character, autoinc, cicharacter |
| A.ADT | ruby-adt | 1 | character, date, integer, double |
| AbrGru.ADT | node_adt | 9 | integer, character, shortint, logical, double |

No public samples were found for memo, money, numeric, timestamp, nchar or other types (searched October 2026).
