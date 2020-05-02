from deprecated import deprecated

def new_function():
    print("New function")


@deprecated("Use new_function() instead")
def some_deprecated_function():
    print("Some deprecated function")


if __name__ == '__main__':
    some_deprecated_function()

    a = "Test\nHello World\n\n"
    b = "Test\nHello World"
    c = "Test"

    a1 = a.splitlines(False)
    a2 = len(a1)
    b1 = b.splitlines(False)
    b2 = len(b1)
    c1 = c.splitlines(False)
    c2 = len(c1)

    print(repr(a), repr(b), repr(c))
    print(repr(a1), repr(b1), repr(c1))
    print(repr(a2), repr(b2), repr(c2))
