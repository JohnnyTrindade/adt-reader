import datetime as dt
from pathlib import Path

import pytest

from adtreader import ADTError, ADTTable

FIX = Path(__file__).parent / "fixtures"


def test_small_table_layout():
    with ADTTable(FIX / "test.adt") as t:
        assert len(t) == 1
        assert t.header.record_length == 213
        assert [c.type_name for c in t.columns] == [
            "integer", "character", "autoinc", "cicharacter", "cicharacter", "cicharacter"]
        # record prefix (5 bytes) + column lengths == record length
        assert 5 + sum(c.length for c in t.columns) == t.header.record_length


def test_small_table_values():
    with ADTTable(FIX / "test.adt") as t:
        row = t.record(0)
        values = list(row.values())
        assert values[0] == 99
        assert values[1] == "9999"
        assert values[2] == 2
        assert values[3:] == [None, None, None]


def test_wide_table_values():
    with ADTTable(FIX / "A.ADT") as t:
        assert t.header.column_count == 32
        row = t.record(0)
        assert row["ProviderNo"] == "43-SAMPLE"
        assert row["State"] == "AL"
        # dates are Julian Day Numbers; the period spans exactly NoOfDays
        assert row["PeriodBeg"] == dt.date(2008, 7, 1)
        assert row["PeriodEnd"] == dt.date(2009, 6, 30)
        assert row["NoOfDays"] == 365
        assert (row["PeriodEnd"] - row["PeriodBeg"]).days + 1 == row["NoOfDays"]
        assert row["PercentOccupancy"] == pytest.approx(93.854226, rel=1e-6)
        assert row["D-6_QuestionYN"] == "Y"


def test_abrgru_logical_and_int_null():
    # AbrGru.ADT comes from node_adt; latin-1 text, German column names
    with ADTTable(FIX / "AbrGru.ADT", encoding="latin-1") as t:
        assert len(t) == 9
        assert t.columns[8].type_name == "logical"
        rows = list(t)
        assert rows[0]["AbrGruId"] == 1
        assert rows[0]["Bez"] == "WGK"
        assert rows[0]["OpKennz"] is False          # stored as b"F"
        assert rows[1]["MtglNrKennz"] is True       # stored as b"T"
        assert rows[0]["MwstGrup"] is None          # int32 NULL = INT_MIN
        assert rows[0]["MwstAusgl"] == 0.0
        assert 5 + sum(c.length for c in t.columns) == t.header.record_length


def test_rejects_non_adt(tmp_path):
    f = tmp_path / "x.adt"
    f.write_bytes(b"\x00" * 500)
    with pytest.raises(ADTError):
        ADTTable(f)
