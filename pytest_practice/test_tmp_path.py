# tmp_path makes temporary directory thats deleted after the test
# useful for testing file paths

def test_needsfiles(tmp_path):
    print(tmp_path)
    assert 0