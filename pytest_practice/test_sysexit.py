import pytest

def f():
    raise SystemExit(1) # exits a program

def test_mytest():
    with pytest.raises(SystemExit): # expects function to raise sysexit, which would be a pass
        f()

# running with "pytest -q test_sysexit.py" keeps terminal output brief