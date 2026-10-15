# Contributing

Thanks for helping get data out of Advantage Database tables.

## The most useful contribution: sample files

If you have ADS or Advantage Data Architect installed, generate the synthetic sample set described in [samples/README.md](samples/README.md) and open a **Sample submission** issue. It takes about 10 minutes, and each new type it covers moves from "guessed from docs" to "verified".

## Ground rules

- **Data files only.** We work from `.adt`/`.adm` files and public API documentation. Do not contribute anything obtained by decompiling or disassembling SAP/Advantage binaries, and do not paste proprietary documentation.
- **Synthetic data only.** Never commit or attach real customer data, even "anonymized" production tables.
- **Evidence for format claims.** Every statement in `docs/FORMAT.md` carries a status (confirmed / inferred / open). Moving something to *confirmed* needs a sample file and a test that would fail if the claim were wrong.

## Development

```bash
pip install -e ".[dev]"
pytest
python tools/sample_spec.py   # after changing the sample spec
```

Code style: standard library only in the core package; optional dependencies go behind extras.
