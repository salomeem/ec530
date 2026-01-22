# Can run multiple tests in a class, returns which ones failed and why

class TestClass:
    # test chacks if theres an h in "this"
    def test_one(self):
        x = "this"
        assert "h" in x # make sure these statements are unique to each test, bc they share attributes
    # test sets x to hello and checks for
    # an attribute or method called "check"
    def test_two(self):
        x = "hello"
        assert hasattr(x, "check")