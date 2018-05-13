#!/usr/bin/env python

def _thousand(n):
    return n * 1000
def _million(n):
    return _thousand(n) * 1000
def _billion(n):
    return _million(n) * 1000

def number(n, include_zero=False):
    tens = [ "zero", "ten", "twenty", "thirty", "forty", "fifty", "sixty", 
             "seventy", "eighty", "ninety" ]
    ones = [ "zero", "one", "two", "three", "four", "five", "six", "seven",
             "eight", "nine", "ten", "eleven", "twelve", "thirteen",
             "fourteen", "fifteen", "sixteen", "seventeen",
             "eighteen", "ninteen" ]
    if n == 0 and include_zero:
        yield "zero"
        return

    if n >= _million(1):
        for i in number(n / _million(1)): yield i
        yield "million"
        if (n % _million(1)) < 100 and (n % _thousand(1)) > 0: yield "and"
        n %= _million(1)
    if n >= _thousand(1):
        for i in number(n / _thousand(1)): yield i
        yield "thousand"
        if (n % _thousand(1)) < 100 and (n % _thousand(1)) > 0: yield "and"
        n %= _thousand(1)

    if n >= 100:
        for i in list(number(n / 100)): yield i
        yield "hundred"
        n %= 100
        if n > 0:
            yield "and"

    if n >= 20:
        yield tens[n / 10]
        n %= 10

    if n > 0:
        yield ones[n]

import random
def numbers(limit, easter_egg=False):
    for n in range(limit):
        r = list(number(n))
        if easter_egg:
            if random.sample(range(1000), 1)[0] == 1: # range picked to keep this as occurring at a fairly low rate
                print "easter egg! ",
                if len(r) > 1:
                    r.insert(random.choice(range(len(r))), "egg")
                else:
                    r.insert(0, "egg")
        yield (n, r)


from testify import *

class TestNumbers(TestCase):
    def test_numbers(self):
        testcase = [
                (0, ["zero"]),
                (1, ["one"]),
                (2, ["two"]),
                (10, ["ten"]),
                (11, ["eleven"]),
                (20, ["twenty"]),
                (21, ["twenty", "one"]),
                (30, ["thirty"]),
                (100, ["one", "hundred"]),
                (101, ["one", "hundred", "and", "one"]),
                (110, ["one", "hundred", "and", "ten"]),
                (113, ["one", "hundred", "and", "thirteen"]),
                (245, ["two", "hundred", "and", "forty", "five"]),
                (879, ["eight", "hundred", "and", "seventy", "nine"]),
                (1337, ["one", "thousand", "three", "hundred", "and", "thirty",
                    "seven"]),
                (10013, ["ten", "thousand", "and", "thirteen"]),
                (80085, ["eighty", "thousand", "and", "eighty", "five"]),
                (9000099, ["nine", "million", "and", "ninety", "nine"]),
            ]
        for (n, result) in testcase:
            assert_equal(result, list(number(n, include_zero=True)))

def main():
    for (n, t) in numbers(5000, easter_egg = True):
        print "{} => {}".format(n, t)
if __name__ == '__main__': main()
