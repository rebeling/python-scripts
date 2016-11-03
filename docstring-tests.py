"""
Test module's docstrings with doctest.

Doctests searchs for interactive session examples, calls and validates
on return value.
"""


def test_generator(n):
    """Create generator that yields n numbers.

    >>> test_generator(3) #doctest: +ELLIPSIS
    <generator object test_generator at 0x...>
    >>> test_generator(3).next()
    0
    """
    # print val
    for i in xrange(n):
        yield i


if __name__ == '__main__':
    import doctest
    doctest.testmod()
