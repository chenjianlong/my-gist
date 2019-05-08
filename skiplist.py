#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Jianlong Chen <jianlong99@gmail.com>
#
# Distributed under terms of the MIT license.

"""
python skiplist
"""

import random

class Node(object):
    def __init__(self, level, key, value):
        self.forward = [None] * level
        self.key = key
        self.value = value


class Skiplist(object):
    def __init__(self, max_level = 32, p = 0.5):
        self.max_level = max_level
        self.header = Node(max_level, 0, 0)
        self.current_level = 0
        self.__probability = p

    def search(self, key):
        x = self.header
        for level in range(self.current_level - 1, -1, -1):
            while x.forward[level] is not None and x.forward[level].key < key:
                x = x.forward[level]

        x = x.forward[0]
        if x is not None and x.key == key:
            return x.value
        else:
            return None

    def insert(self, key, value):
        update = [None] * self.max_level
        x = self.header
        for level in range(self.current_level - 1, -1, -1):
            while x.forward[level] is not None and x.forward[level].key < key:
                x = x.forward[level]

            update[level] = x

        x = x.forward[0]
        if x is not None and x.key == key:
            # found key, just update value
            x.value = value
        else:
            new_level = self.__random_level()
            if new_level > self.current_level:
                for level in range(self.current_level, new_level):
                    update[level] = self.header

                self.current_level = new_level

            x = Node(new_level, key, value)
            for level in range(0, new_level):
                x.forward[level] = update[level].forward[level]
                update[level].forward[level] = x

    def delete(self, key):
        update = [None] * self.max_level
        x = self.header
        for level in range(self.current_level - 1, -1, -1):
            while x.forward[level] is not None and x.forward[level].key < key:
                x = x.forward[level]

            update[level] = x

        x = x.forward[0]
        if x is not None and x.key == key:
            for level in range(0, self.current_level):
                if update[level].forward[level] != x:
                    break

                update[level].forward[level] = x.forward[level]

            del x
            while self.current_level > 0 and\
                    self.header.forward[self.current_level - 1] == None:
                self.current_level -= 1

    def __random_level(self):
        new_level = 1
        while random.random() < self.__probability:
            new_level += 1

        return min(self.max_level, new_level)

def iter(sl):
    x = sl.header
    while x.forward[0] is not None:
        x = x.forward[0]
        yield x.value

    return


def simple_test():
    l = Skiplist()
    print("insert key=3, value='hello'")
    l.insert(3, "hello")
    print("search key=3:", l.search(3))
    print("insert key=6, value='hello2'")
    l.insert(6, "hello2")
    print("insert key=1, value='world'")
    l.insert(1, "world")
    print("search key=1:", l.search(1))
    print("search key=2:", l.search(2))

    print("iter Skiplist:")
    for v in iter(l):
        print(v)

    print("delete key 3")
    l.delete(3)
    print("search key=3:", l.search(3))
    print("delete key 6")
    l.delete(6)
    print("search key=6:", l.search(6))
    print("delete key 1")
    l.delete(1)
    print("search key=1:", l.search(1))
    print("delete key 1")
    l.delete(1)
    print("search key=1:", l.search(1))

    print("iter empty Skiplist:")
    for v in iter(l):
        print(v)


if __name__ == '__main__':
    simple_test()
