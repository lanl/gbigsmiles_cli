import pytest 
import pandas as pd 
import gbigcli.bigsmiles


@pytest.fixture
def stochastic_unit()->str:
    return "{[][$]CHO[$][]}"

@pytest.fixture
def nonstochastic_unit()->str:
    return "CHO"

def test_is_stochastic(stochastic_unit):
    assert gbigcli.bigsmiles.is_stochastic(stochastic_unit)

def test_is_nonstochastic(nonstochastic_unit):
    assert not gbigcli.bigsmiles.is_stochastic(nonstochastic_unit)

@pytest.fixture
def multi_stochastic_units()->str:
    return "{[][$]CHO[$][$]}{[$][$]CC[$][]}"

def test_split_stochastic_units(multi_stochastic_units):
    assert len(gbigcli.bigsmiles.split_bigsmiles(multi_stochastic_units)) == 2 

@pytest.fixture
def bigsmiles_metadata_row():
    return pd.Series({"BigSMILES":"CCC(C){[$][$]CC(C1CCCCC1)[$][$]}{[$][$]CCCC[$],[$]CC(CC)[$][$]}[H]","Mw":100,"Mn":80})

@pytest.fixture
def bigsmiles_metadata_row_with_fractions():
    return pd.Series({"BigSMILES":"CCC(C){[$][$]CC(C1CCCCC1)[$][$]}{[$][$]CCCC[$],[$]CC(CC)[$][$]}[H]","Mw":100,"Mn":80,"f1":.2,"f2":.8})

def test_get_distribution_strings(bigsmiles_metadata_row):
    distribution_strings = gbigcli.bigsmiles.get_distribution_strings(bigsmiles_metadata_row)
    assert len(distribution_strings) == 2

def test_get_gbigsmiles_from_bigsmiles_metadata_row(bigsmiles_metadata_row):
    genbigsmiles = gbigcli.bigsmiles.get_gen_bigsmiles(bigsmiles_metadata_row,full_dist_str="log_normal")
    assert "log_normal" in genbigsmiles

def test_get_gbigsmiles_from_bigsmiles_metadata_row_with_fractions(bigsmiles_metadata_row_with_fractions):
    genbigsmiles = gbigcli.bigsmiles.get_gen_bigsmiles(bigsmiles_metadata_row_with_fractions,full_dist_str="log_normal")
    assert "log_normal" in genbigsmiles