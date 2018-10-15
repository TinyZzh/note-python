#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import pymysql
import utilities.mine_output as mo


def _query_some():

    return


def _main():

    # mo.output('file1.txt', "|".join(['data', 'tinyzzh', 'zzh']))
    # mo.output_list('file2.txt', ['1', '2', 3], ['xx', 'yy', 'zz'])
    mo.output_rows('filexx.txt', [(1,2,3), (2,3,4)], ['x','y','z'], name="xxx")

    print("xxx")
    return 0


if __name__ == "__main__":
    try:
        os._exit(_main())
    except Exception as e:
        print(str(e))
