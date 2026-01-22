#function takes x and returns x+1
def func(x): 
    return x + 1

# actual test case, always starts with "test_" or ends with "_test"
# runs func(3) then checks if it equals 5
def test_answer(): 
    assert func(3) == 5 # assert statement
