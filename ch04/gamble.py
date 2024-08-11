def foo():
    """
    >>> foo() + 4
    7
    """
    return 3



if __name__ == "__main__":
    import doctest

    doctest.testmod()