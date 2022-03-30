

class test:

    def __init__(self, n):
        self.n = n

    def __call__(self):
        print("testand")


app = test(1)
print(app())
print()