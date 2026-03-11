import subprocess
import os 
import pytest 
import pandas as pd 
import gbigcli.generation



@pytest.fixture
def gbigsmiles_cmd()->str:
    return "gbigsmiles"

@pytest.fixture
def check_cmd()->str:
    return "check"

@pytest.fixture
def get_cmd()->str:
    return "get"

def test_check(gbigsmiles_cmd,check_cmd):
    check_output = subprocess.run([gbigsmiles_cmd,check_cmd], capture_output = True )
    assert check_output.stdout.decode().strip() == gbigcli.generation.check_entry(to_return = True)

def test_single_generation(gbigsmiles_cmd,get_cmd,gbigsmiles_sample):
    generated_output = subprocess.run([gbigsmiles_cmd,get_cmd,gbigsmiles_sample], capture_output = True)
    assert len(generated_output.stdout.splitlines()) == 1

def test_multi_generation(gbigsmiles_cmd,get_cmd,gbigsmiles_sample):
    n_samples = 10
    generated_output = subprocess.run([gbigsmiles_cmd,get_cmd,gbigsmiles_sample, str(n_samples)], capture_output = True)
    assert len(generated_output.stdout.decode().splitlines()) == n_samples

def test_multi_generation_csv(gbigsmiles_cmd,get_cmd,gbigsmiles_sample):
    csv_path = "test.csv"
    n_samples = 10
    subprocess.run([gbigsmiles_cmd,get_cmd,gbigsmiles_sample, str(n_samples),str(csv_path)])
    saved_df = pd.read_csv(csv_path,header = 0,index_col=0)
    assert len(saved_df) == n_samples
    os.remove(csv_path)

