"""
    Dummy conftest.py for gbig_cli.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

import pytest
@pytest.fixture
def gbigsmiles_sample()->str:
    return "{[][<]CC([>]), [<]CC([>])COC; CC(C)[>], CC(C)[>], [<][Cl][]}|schulz_zimm(850, 500)|"