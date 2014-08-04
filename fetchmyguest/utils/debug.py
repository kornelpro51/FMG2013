from __future__ import unicode_literals


from collections import deque

def tail(f, n):
    std_out = deque(open(f), n)
    return std_out