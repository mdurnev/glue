def hello():
    return "Hello!"

def Sum(n, m):
    return n + m

class Test:
    text = "Hello::hello"

    def __init__(self):
        self.res = 0

    def hello(self):
        return self.text

    def Sum(self, n, m, *var):
        res = 0
        for i in var:
            res += i
        res = n + m + res + self.res
        self.res = res
        return res

class Test1(Test):

    def hello(self):
        return "Test1"

    def __init__(self, val):
        self.res = val
