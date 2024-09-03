class Foo:
    def fn1(self):
        print('fn1 from foo')

    def fn2(self):
        print('call from fn2')
        self.fn1()


class Bar:
    def __init__(self, foo):
        self.foo = foo 

    def fn1(self):
        print("fn1 from bar")

    def update(self):
        self.foo.fn2()


foo = Foo()


bar = Bar(foo)
bar.update()