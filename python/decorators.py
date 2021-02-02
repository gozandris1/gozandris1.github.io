def runmefirst(f):
    def wrapper():
        print("about to run a function, before running the base function")
        f()
        print("done with the runmefirst function")
    return wrapper


@runmefirst
def hello():
    print("Hello")

hello()