def hello():
    return "Hello!"

def number(n, m, *var):
    for i in var:
        print(i)
    return n + m

class Hello:
    text = "hello"

    def hello(self):
        print(self.text)
