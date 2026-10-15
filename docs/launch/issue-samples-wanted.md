<!-- Paste as the first issue on GitHub and pin it. Title: -->
<!-- Help wanted: sample .adt files for the remaining field types -->

**adt-reader** reads Advantage Database Server tables (`.adt`) without the ADS engine. SAP stopped selling new ADS licenses on 31 August 2025, so a lot of data will need to move out of these tables over the next few years.

The reader already handles the types we could verify against real files: character, cicharacter, integer, shortint, autoinc, double, date and logical.

Several types are decoded only from the ACE documentation, because **there are no public sample files** for them: time, timestamp, modtime, money, int64, rowversion, curdouble, nchar and guid. Memo, blob and image fields (stored in `.adm` files), numeric and varchar are not supported at all yet.

### How you can help (about 10 minutes)

If you have **ADS or Advantage Data Architect** installed:

1. Run [`samples/generate_samples.sql`](https://github.com/JohnnyTrindade/adt-reader/blob/main/samples/generate_samples.sql) in a free-table ADT connection pointing at an empty folder.
2. Zip the resulting `.adt` + `.adm` files.
3. Open a **Sample submission** issue and attach the zip.

Full instructions: [samples/README.md](https://github.com/JohnnyTrindade/adt-reader/blob/main/samples/README.md).

All values are synthetic, so nothing private is shared. Samples from different ADS versions (8.x through 12.x) and both ANSI and OEM character sets are especially welcome.

### Status per type

| Type | Status |
|---|---|
| character, cicharacter, integer, shortint, autoinc, double, date, logical | ✅ verified |
| time, timestamp, modtime, money, int64, rowversion, curdouble, nchar, guid | 🟡 from docs, needs a sample |
| memo, nmemo, blob, image, nvarchar, varchar, numeric, raw | 🚧 needs a sample to start |
| deleted records | 🟡 inferred, needs a sample |
