#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by vici on 16/03/2017

import time
import asyncio

@asyncio.coroutine
def slow_operation(n):
    yield from asyncio.sleep(1)
    print("Slow operation {} complete".format(n))


@asyncio.coroutine
def main():
    start = time.time()
    yield from asyncio.wait([
        slow_operation(1),
        slow_operation(2),
        slow_operation(3),
    ])
    end = time.time()
    print('Complete in {} second(s)'.format(end-start))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())