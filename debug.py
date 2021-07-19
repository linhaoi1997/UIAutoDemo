class Test1:

    def handle(self):
        print("1111")


class Test2(Test1):
    def handle(self): ...


if __name__ == '__main__':
    print(Test2().handle())
